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

- Run `python3 main.py <EMAIL_ADDRESS>`, replacing with an email address you have corresponded with before and would like to reach out to again

## Testing with Postman

- Follow [this guide](https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/)

## Extensions

- Accept CSV file with many email addresses to batch draft emails
- Use tiktoken to choose a model based on token count
- Support drafting new emails without previous interactions
- Fine-tune the AI model with all past sent emails (in the last year or so) from the user to create a more accurate tone/style
