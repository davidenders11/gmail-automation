## G-Mail Automation App

The motivation for this app is as follows: G-Mail has features for automating and simplifying certain repetitive tasks, such as the template feature and automatic responses. However, these are not easily configurable, and still require manual composition and sending of messages. I hope to address this by creating a series of Python scripts which will significantly reduce the manual intervention necessary to complete such mundane tasks.

Another motivation for this app is to practice and refine the incorporation of AI-powered APIs by using API calls to draft custom messages based on previous interactions with users. The user should be able to drop a list of email addresses to the tool, and the tool will automatically generate a series of drafts to each of these users based on previous messages.

# Adding test users

This project is still in testing phase. If you'd like to tie this project to your own Google Developer account, (this guide)[https://developers.google.com/gmail/api/quickstart/python] will walk you through the process. To add test users, head to the OAuth Consent Screen under the "APIs & Services" section in the Google Cloud Console, and add a test user.

# Getting OpenAI Access

Navigate to [openai.com], create an account, create an API key, save it, and place it in a file named `secrets.json` for local testing. Remember to never push or share this.

# Testing with Postman

- Follow (this guide)[https://blog.postman.com/how-to-access-google-apis-using-oauth-in-postman/]

# Extensions

- Accept CSV of email addresses to batch draft
