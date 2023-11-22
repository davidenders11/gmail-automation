from __future__ import print_function

import os.path
import json
import sys
import base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from email.message import EmailMessage


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


class Gmail:
    def __init__(self, logger):
        self.logger = logger
        self.auth()
        self.me = self.service.users().getProfile(userId="me").execute()["emailAddress"]

    def auth(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists("token.json"):
            token = json.load(open("token.json"))
            expiry = datetime.fromisoformat(token["expiry"])
            if expiry < datetime.now(expiry.tzinfo):
                self.logger.info(
                    "Token expired, removing token.json and re-authenticating"
                )
                print("AHHHHH IT WORKED")
                os.remove("token.json")
                creds = None
            else:
                self.logger.info("Reading credentials from existing token.json")
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Credentials expired, sending refresh request")
                creds.refresh(Request())
            else:
                self.logger.info(
                    "Credentials not found, sending auth request to local server"
                )
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                self.logger.info("Saving credentials to token.json")
                token.write(creds.to_json())
        self.service = build("gmail", "v1", credentials=creds)
        self.logger.info("Completed Gmail authentication flow")

    def get_message_headers(self, message_id):
        """Get a message and return its References, In-Reply-To, and Subject headers"""
        payload = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id)
            .execute()["payload"]
        )
        references_value = None
        in_reply_to_value = None
        subject = None

        for header in payload["headers"]:
            if header["name"] == "References":
                refs = header["value"]
            elif header["name"] == "Message-ID":
                in_reply_to_value = header["value"]
            elif header["name"] == "Subject":
                subject = header["value"]
        references_value = refs + " " + in_reply_to_value
        return references_value, in_reply_to_value, subject

    def get_most_recent_message_ids(self, query):
        """
        Get the most recent message matching the query
        """
        self.logger.info(f"Querying Gmail for most recent message with query: {query}")
        result = self.service.users().messages().list(userId="me", q=query).execute()
        messages = []
        if "messages" in result:
            messages.extend(result["messages"])
        while "nextPageToken" in result:
            page_token = result["nextPageToken"]
            result = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, pageToken=page_token)
                .execute()
            )
            if "messages" in result:
                messages.extend(result["messages"])

        return messages[0]

    def get_thread(self, thread_id):
        """
        Get a thread and print each message including its sender and body
        """
        response = (
            self.service.users().threads().get(userId="me", id=thread_id).execute()
        )
        messages = response["messages"]
        thread = ""
        for message in messages:
            # specify sender in final string
            for header in message["payload"]["headers"]:
                if header["name"] == "From":
                    thread += f"From: {header['value']}"

            # get messages content and add to string
            for part in message["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    content = urlsafe_b64decode(part["body"]["data"]).decode()
                    # remove any lines that start with ">" as these are redundant
                    content = "\n".join(
                        [
                            line
                            for line in content.split("\n")
                            if not line.startswith(">")
                        ]
                    )
                    thread += f"Body:\n{content}"
                elif part["mimeType"] == "multipart/alternative":
                    for subpart in part["parts"]:
                        if subpart["mimeType"] == "text/plain":
                            content = urlsafe_b64decode(
                                subpart["body"]["data"]
                            ).decode()
                            # remove any lines that start with ">"
                            content = "\n".join(
                                [
                                    line
                                    for line in content.split("\n")
                                    if not line.startswith(">")
                                ]
                            )
                            thread += f"Body:\n{content}"
                            break

        return thread

    # If I want draft replies to work, the subject needs to be the same as the original thread, and the thread id needs to be the same as the original thread
    # And I need to also fill in the "In-Reply-To" header and the "References" header to be "Message-ID" of the most recent message in the thread and the "References"
    # header to be the "References" header of the most recent plus the "Message-ID" of the most recent message in the thread
    # I think these are set using the same message["To"] syntax as below, so like message["In-Reply-To"] = message["Message-ID"] of the most recent message in the thread
    # headers and stuff docs here: https://datatracker.ietf.org/doc/html/rfc2822#section-2.2
    def new_draft(self, content, other, subject):
        """Create and insert a draft email.
        Print the returned draft's message and id.
        Returns: Draft object, including draft id and message meta data.
        """
        try:
            message = EmailMessage()

            message.set_content(content)

            message["To"] = other
            message["From"] = self.me
            if subject:
                message["Subject"] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {"message": {"raw": encoded_message}}
            draft = (
                self.service.users().drafts().create(userId="me", body=body).execute()
            )

        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None

        return draft

    def reply_draft(
        self, content, other, subject, thread_id, references_value, in_reply_to_value
    ):
        """Create and insert a draft email.
        Print the returned draft's message and id.
        Returns: Draft object, including draft id and message meta data.
        """
        try:
            message = EmailMessage()

            message.set_content(content)

            message["To"] = other
            message["From"] = self.me
            message["Subject"] = subject
            message["References"] = references_value
            message["In-Reply-To"] = in_reply_to_value

            print(f"\n\n\nBefore encoding {message}\n\n\n")

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {
                "message": {
                    "threadId": thread_id,  # The thread id of the main message to reply to
                    "raw": encoded_message,
                }
            }

            draft = (
                self.service.users().drafts().create(userId="me", body=body).execute()
            )

        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None

        return draft


def main():
    pass


if __name__ == "__main__":
    pass
