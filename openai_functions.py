import json
import openai


def auth():
    with open("secrets.json") as f:
        secrets = json.load(f)
    openai.api_key = secrets["openai"]


def write_draft(thread, update, myself, other):
    user_content = f"Below is a chain of messages between myself, {myself}, and {other}. I would like to draft a response to {other} based on this interaction and the following update. Please incorporate this new information and formulate a response to {other} that I can send (a subject line is not necessary). Make sure you use the thread as context for your response. \n\nPAST MESSAGES: \n###\n{thread}\n###\n\n NEW INFORMATION:\n###\n{update}\n###"
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=[{"role": "user", "content": user_content}]
    )
    response = gpt_response.choices[0].message.content
    return response


if __name__ == "__main__":
    pass
