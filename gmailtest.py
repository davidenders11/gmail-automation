import sys
import argparse
import logging
from gmailwrapper import Gmail
from openaiwrapper import OpenAI
from googleapiclient.discovery import build
import pandas as pd
import json

logging.basicConfig(
        level = logging.ERROR, 
        format = '%(levelname)s:%(asctime)s:%(message)s')
logger = logging.getLogger(__name__)

gmail = Gmail(logger)

query = f"from:andrew@xostrucks.com"

# last_thread_id = gmail.get_most_recent_message_ids(query)["threadId"]
id = gmail.get_most_recent_message_ids(query)["id"]
payload = gmail.get_message(id)

# Find the "References" and "In-Reply-To" headers and extract their "value" fields
references_value = None
in_reply_to_value = None
subject = None

for header in payload["headers"]:
    if header["name"] == "References":
        references_value = header["value"]
    elif header["name"] == "In-Reply-To":
        in_reply_to_value = header["value"]
    elif header["name"] == "Subject":
        subject = header["value"]

print("References Value:", references_value)
print("In-Reply-To Value:", in_reply_to_value)
print("Subject:", subject)

# print(json.dumps(message, indent=2))
# print(last_thread_id)
# thread = gmail.get_thread(last_thread_id)
# # logger.info("Retrieved last thread with target recipients")

# # generate the draft and create it on gmail, this should draft a reply
# gmail.draft("content", "andrew@xostrucks.com", thread_id=last_thread_id)
