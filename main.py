import sys
import argparse
import logging
from gmail_functions import Gmail
from openai_functions import OpenAI
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
    openai = OpenAI(logger)
    gmail = Gmail(logger)

    query = f"from:{args.recipient}"
    last_thread_id = gmail.get_most_recent_message(query)
    thread = gmail.get_thread(last_thread_id)
    logger.info("Retrieved last thread with target recipient")

    update = input(f"What would you like to tell {args.recipient}?\n")
    subject = input(f"\nWhat would you like the subject of the email to be?\n")
    content = openai.write_draft(thread, update, gmail.me, args.recipient)
    logger.info("Draft has been generated, OpenAI call complete")

    gmail.gmail_create_draft(subject, content, args.recipient)
    print(
        f"\nYour draft has been created!\nRecipient: {args.recipient}\nSubject: {subject}\nContent: {content}\n"
    )

if __name__ == "__main__":
    main()
