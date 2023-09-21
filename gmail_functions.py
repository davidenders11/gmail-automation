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

from email.message import EmailMessage


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def auth():
    """
    Authenticates user and saves token.json
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_most_recent_message(service, query):
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token)
            .execute()
        )
        if "messages" in result:
            messages.extend(result["messages"])
    return messages[0]["threadId"]


# def search_threads(service, query):
#     result = service.users().threads().list(userId="me", q=query).execute()
#     threads = []
#     if "threads" in result:
#         threads.extend(result["threads"])
#     while "nextPageToken" in result:
#         page_token = result["nextPageToken"]
#         result = (
#             service.users()
#             .threads()
#             .list(userId="me", q=query, pageToken=page_token)
#             .execute()
#         )
#         if "threads" in result:
#             threads.extend(result["threads"])
#     return threads


def get_thread(service, thread_id):
    """
    Get a thread and print each message including its sender and body
    """
    response = service.users().threads().get(userId="me", id=thread_id).execute()
    messages = response["messages"]
    thread = ""
    for message in messages:
        for header in message["payload"]["headers"]:
            if header["name"] == "From":
                thread += f"From: {header['value']}"
        # print(f"\n\nMESSAGE:\n\n{message}")
        for part in message["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                content = urlsafe_b64decode(part["body"]["data"]).decode()
                # remove any lines that start with ">"
                content = "\n".join(
                    [line for line in content.split("\n") if not line.startswith(">")]
                )
                thread += f"Body:\n{content}"
            elif part["mimeType"] == "multipart/alternative":
                for subpart in part["parts"]:
                    if subpart["mimeType"] == "text/plain":
                        content = urlsafe_b64decode(subpart["body"]["data"]).decode()
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


def get_own_email(service):
    """
    Get own email address
    """
    response = service.users().getProfile(userId="me").execute()
    return response["emailAddress"]


def gmail_create_draft(service, subject, content, me, other):
    """Create and insert a draft email.
    Print the returned draft's message and id.
    Returns: Draft object, including draft id and message meta data.
    """
    try:
        message = EmailMessage()

        message.set_content(content)

        message["To"] = other
        message["From"] = me
        message["Subject"] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}
        # pylint: disable=E1101
        draft = (
            service.users().drafts().create(userId="me", body=create_message).execute()
        )

        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None

    return draft


def main():
    """
    Use for testing Gmail API calls
    """
    me = get_own_email(service)
    other = sys.argv[1]
    creds = auth()
    service = build("gmail", "v1", credentials=creds)
    query = f"from:{other}"
    # threads = search_threads(service, query)
    last_thread_id = get_most_recent_message(service, query)
    # print(get_thread(service, last_thread_id))
    print(get_own_email(service))


if __name__ == "__main__":
    pass