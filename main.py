import sys
import argparse
import gmail_functions
import logging
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
parser.add_argument("recipient", type=str, help="The email address of the recipient.")
parser.add_argument("--reply", action="store_true", help="Reply to the most recent email thread from the specified recipient.")
parser.add_argument("--verbose", action="store_true", help="Prints logging information to the console.")
args = parser.parse_args()

logging.basicConfig(
        level = logging.INFO if args.verbose else logging.WARNING, 
        format = '%(levelname)s:%(asctime)s:%(message)s')
logger = logging.getLogger(__name__)

def main():
    creds = gmail_functions.auth(logger)
    logger.info("Completed Gmail Authentication flow")

    openai_functions.auth()
    logger.info("Completed OpenAI authentication flow")

    service = build("gmail", "v1", credentials=creds)
    logger.info("Built Gmail endpoint service")

    me = get_own_email(service)
    logger.info("Retrieved user email")

    query = f"from:{args.recipient}"
    last_thread_id = get_most_recent_message(service, query, logger)
    thread = get_thread(service, last_thread_id)
    logger.info("Retrieved last thread with target recipient")

    update = input(f"What would you like to tell {args.recipient}?\n")
    subject = input(f"\nWhat would you like the subject of the email to be?\n")
    content = write_draft(thread, update, me, args.recipient, logger)
    logger.info("Draft has been generated, OpenAI call complete")

    gmail_create_draft(service, subject, content, me, args.recipient)
    print(
        f"\nYour draft has been created!\nRecipient: {args.recipient}\nSubject: {subject}\nContent: {content}\n"
    )

if __name__ == "__main__":
    main()
