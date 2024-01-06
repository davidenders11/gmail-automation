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
  - the `recipient` argument is the email address of your intended recipient OR an excel file containing email addresses
    - The tool will look for an `Email` column, so make sure that the addresses are all organized in one column with the header `Email`

## Extensions

- Use tiktoken to choose a model based on token count
- Fine-tune the AI model with all past sent emails (in the last year or so) from the user to create a more accurate tone/style
- Error check for token.json missing and remove the file and try again if so
- Make sure still works if there are no previous interactions

## Documentation

- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [Gmail API](https://developers.google.com/gmail/api/reference/rest)
- [Gmail Python Library](https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#create)
- [Email standards](https://datatracker.ietf.org/doc/html/rfc2822#section-2.2)

## Program Flow

- Use argparse to parse options: either read emails from sheet or take single email, and choose reply or new draft
- OpenAI and Gmail object created
- CLI prompt asks user for desired content/new information to include in the email (and a subject if it's a new email)
- `gmail.get_most_recent_message_ids()` gets the threadId and messageId for the most recent interaction with the specified recipient(s)
- `gmail.get_thread()` compiles all the messages from the most recent thread into a single string and does some cleanup
- `openai.write_draft()` writes a draft based on the new information, incorporating context from past messages
- Then the `Gmail` class has two functions for replies: one for new messages and one for replies to threads:
  - If it's a reply, we first retrieve the necessary headers with `gmail.get_message_headers()` (according to RFC 2822 specifications), then set these headers and create the draft in `gmail.reply_draft()`
  - Else, pass in content, recipient, and subject to `gmail.new_draft()`
