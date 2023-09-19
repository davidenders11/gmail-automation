import json
import openai

with open("secrets.json") as f:
    secrets = json.load(f)

openai.api_key = secrets["openai"]

gpt_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "user", "content": "Do a flip!"}],
)
response = gpt_response.choices[0].message.content
print(response)
