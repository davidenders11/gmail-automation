import argparse

parser = argparse.ArgumentParser(
    description="Draft emails to specified recipients.")
parser.add_argument("--reply", action="store_true", help="Reply to the most recent email thread from the specified recipient.")
parser.add_argument("recipient", type=str, help="The email address of the recipient.")


args = parser.parse_args()
print(args.reply, args.recipient)