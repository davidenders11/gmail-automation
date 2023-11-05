import sys
import argparse
import logging
from gmailwrapper import Gmail
from openaiwrapper import OpenAI
from googleapiclient.discovery import build
import pandas as pd

parser = argparse.ArgumentParser(
    description="Draft emails to specified recipients.")
# stores a bool with the value of True if the flag is present, and False if it is not
parser.add_argument("recipients", type=str, help="The email address of a single recipient or an Excel file with an 'Email' column of recipients.")
parser.add_argument("--reply", action="store_true", help="Reply to the most recent email thread from the specified recipient.")
parser.add_argument("--verbose", action="store_true", help="Prints logging information to the console.")
args = parser.parse_args()

logging.basicConfig(
        level = logging.INFO if args.verbose else logging.WARNING, 
        format = '%(levelname)s:%(asctime)s:%(message)s')
logger = logging.getLogger(__name__)

def main():
    # initialize Gmail and OpenAI classes
    openai = OpenAI(logger)
    gmail = Gmail(logger)

    # parse args.recipients to a list of email addresses
    if "xlsx" in args.recipients:
        workbook = pd.read_excel(args.recipients)
        workbook.head()
        args.recipients = [el for el in workbook['Email'] if isinstance(el, str)]
    else: 
        args.recipients = [args.recipients]

    # get user input
    update = input(f"What new information would you like to tell your recipients?\n")
    if not args.reply: subject = input(f"\nWhat would you like the subject of the email to be?\n") 

    # loop through recipients and create a draft for each
    for address in args.recipients:
        # get the most recent email thread from the specified recipient
        query = f"from:{address}"
        last_thread_id = gmail.get_most_recent_message_ids(query)["threadId"]
        thread = gmail.get_thread(last_thread_id)
        logger.info("Retrieved last thread with target recipients")

        # generate the draft and create it on gmail
        content = openai.write_draft(thread, update, gmail.me, address)
        logger.info("Draft has been generated, OpenAI call complete")
        if args.reply:
            gmail.draft(content, address, thread_id=last_thread_id)
        else:
            gmail.draft(content, address, subject=subject)
        logger.info(
            f"\nYour draft has been created!\nRecipient: {address}"+
            "\nSubject: {subject}\nContent: {content}\n"
        )

    # if batch, for loop through dict
        # if reply, get most recent email thread from recipient, read and generate reply
        # if new, read all past threads from recipient, generate new email
    # if single recipient
        # if reply, get most recent email thread from recipient, read and generate reply
        # if new, generate new email

    # new functions: 
        #  parse args so that args recipient holds a list of recipients (single element if single recipient)
        #  get_all_threads(query) which takes a from:email_address query and returns a string containing all threads
            # might need to implement tiktoken for this so we don't run over openai limit
        # modify openai prompt wording to be neutral for reply/new
        # modify gmail_create_draft to take a reply? boolean

    
        



if __name__ == "__main__":
    main()
