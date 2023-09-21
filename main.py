import sys
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
    # "I really enjoyed my time at Samba, and learned lots of different web development techniques and also did some development operations. I also got to work with a lot of different technologies, including React, Node, and Docker. I didn't have much guidance from other engineers, which I thought somewhat defeated the purpose of an internship"
    subject = input(f"What would you like the subject of the email to be?\n")
    content = write_draft(thread, update, me, other)
    gmail_create_draft(service, subject, content, me, other)
    print(
        f"\nYour draft has been created!\nRecipient: {other}\nSubject: {subject}\nContent: {content}\n"
    )


if __name__ == "__main__":
    main()
