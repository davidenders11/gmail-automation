import json
import openai
import logging


class OpenAI:
    def __init__(self, logger):
        self.logger = logger
        self.auth()

    def auth(self):
        with open("secrets.json") as f:
            secrets = json.load(f)
        openai.api_key = secrets["openai"]
        self.logger.info("Completed OpenAI authentication flow")

    def write_draft(self, thread, update, myself, other, reply):
        if reply:
            user_content = f"Below is a chain of messages between myself, {myself}, and {other}. I would like to draft a response to {other} based on this interaction and the following update. Please incorporate this new information and formulate a response to {other} that I can send. Only write the body of the response, do not include a subject. Make sure you use the previous thread as context for your response. \n\nPAST MESSAGES:\n###\n{thread}\n###\n\nNEW INFORMATION TO RELAY:\n###\n{update}\n###"
        else:
            user_content = f"Below is the most recent thread of messages between myself, {myself}, and {other}. I would like to draft a new message to {other} based on the following update. Please use the past messages as context to our relationship, but don't refer back to these messages. Please formulate response to {other} that I can send. Only write the body of the response, do not include a subject. Please be formal but also friendly. \n\nPAST MESSAGES:\n###\n{thread}\n###\n\nNEW INFORMATION TO RELAY:\n###\n{update}\n###"
        self.logger.info(f'Chat Completion prompt is: "{user_content}"')
        model = "gpt-3.5-turbo"
        # model = "gpt-4-1106-preview"  # Use gpt-4 if you have access
        self.logger.info(f"Chat Completion model is: {model}")
        gpt_response = openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": user_content}]
        )
        response = gpt_response.choices[0].message.content
        return response


if __name__ == "__main__":
    pass
