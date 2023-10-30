# G-Mail Automation App

The motivation for this app is as follows: G-Mail has features for automating and simplifying certain repetitive tasks, such as the template feature and automatic responses. However, these are not easily configurable, and still require manual composition and sending of messages. I hope to address this by creating a series of Python scripts which will significantly reduce the manual intervention necessary to complete such mundane tasks.

Another motivation for this app is to practice and refine the incorporation of AI-powered APIs by using API calls to draft custom messages based on previous interactions with users. The user should be able to input email addresses and the tool will automatically generate drafts to these users based on previous messages.

## Setup

- Create a Google Cloud project in order to generate credentials: follow [this guide](https://developers.google.com/gmail/api/quickstart/python) (no need to run the `quickstart.py` sample)
- As the guide mentions, you must add each email address you'd like to use for testing as a "test user".
- Create an account on [openai.com] and create a new secret API key
- Create file `secrets.json` in the root directory and populate with the following content:

```
{
  "openai": "YOUR_OPENAI_API_KEY"
}
```

- **Remember that API keys should never be pushed to your repository or shared.** There are many better ways to store API keys than this, and this method should only be used temporarily for testing.

## Usage

- Run `main.py [-h] [--reply] [--verbose] recipient`
  - the `--reply` flag indicates that you would like to reply to a thread instead of writing a new email
  - the `--verbose` flag indicates that logging should be displayed
  - the `recipient` argument is the email address of your intended recipient

## Extensions

- Accept CSV file with many email addresses to batch draft emails
- Use tiktoken to choose a model based on token count
- Support drafting new emails without previous interactions
- Fine-tune the AI model with all past sent emails (in the last year or so) from the user to create a more accurate tone/style
- Error check for token.json missing and remove the file and try again if so
- Answer [this question](https://stackoverflow.com/questions/66895957/google-api-with-python-error-when-trying-to-refresh-token) if you fixed the problem

## Documentation

- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Gmail API](https://developers.google.com/gmail/api/reference/rest)
- [Gmail Python Library](https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.drafts.html#create)
- [Email standards](https://datatracker.ietf.org/doc/html/rfc2822#section-2.2)
