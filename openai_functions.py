import json
import openai


def auth():
    with open("secrets.json") as f:
        secrets = json.load(f)
    openai.api_key = secrets["openai"]


def write_draft(thread, update, myself, other):
    user_content = f"Below is a chain of messages between myself, {myself}, and {other}. I would like to draft a response to {other} based on this interaction and the following update. Please incorporate this new information and formulate a response to {other} that I can send. Only write the body of the response, do not include a subject. Make sure you use the previous thread as context for your response. \n\nPAST MESSAGES: \n###\n{thread}\n###\n\n NEW INFORMATION TO RELAY:\n###\n{update}\n###"
    model = "gpt-3.5-turbo-16k"  # Use gpt-4 if you have access
    gpt_response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": user_content}]
    )
    response = gpt_response.choices[0].message.content
    return response


if __name__ == "__main__":
    pass
