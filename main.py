import sys
import argparse
import gmail_functions
import openai_functions
from gmail_functions import (
    get_thread,
    get_own_email,
    get_most_recent_message,
    gmail_create_draft,
)
from openai_functions import write_draft
from googleapiclient.discovery import build

parser = argparse.ArgumentParser(
    description="Draft emails to specified recipients.")
# stores a bool with the value of True if the flag is present, and False if it is not
parser.add_argument("--reply", action="store_true", help="Reply to the most recent email thread from the specified recipient.")
parser.add_argument("recipient", type=str, help="The email address of the recipient.")
parser.parse_args()

def main():
    creds = gmail_functions.auth()
    openai_functions.auth()
    service = build("gmail", "v1", credentials=creds)
    me = get_own_email(service)
    other = sys.argv[1]
    query = f"from:{other}"
    last_thread_id = get_most_recent_message(service, query)
    thread = get_thread(service, last_thread_id)
    update = input(f"What would you like to tell {other}?\n")
    subject = input(f"\nWhat would you like the subject of the email to be?\n")
    content = write_draft(thread, update, me, other)
    gmail_create_draft(service, subject, content, me, other)
    print(
        f"\nYour draft has been created!\nRecipient: {other}\nSubject: {subject}\nContent: {content}\n"
    )


if __name__ == "__main__":
    main()
