# bender-bot

A Python based Slack bot with OpenAI integration

## Requirements
- Python 3.9+
- [A Slack token](https://api.slack.com/apps)
	- Create a new Slack app from scratch
	- Add `chat:write`, `channel.history` and `app_mention` scopes for the Bot user
	- Install the app to your workplace
- An [OpenAI API key](https://platform.openai.com/account/api-keys)
- ngrok installed for development: `sudo snap install ngrok`

(Note: `slack` and `slackclient` are no longer supported. Please use `slack_bolt`.)

## Setup
- Setup pipenv: `pip install pipenv && pipenv shell`
- Install dependencies: `pipenv install`

## Usage
- Launch the service with your Slack token: `SLACK_BOT_TOKEN='xoxb-xxxxxxxx' SLACK_SIGNING_SECRET='xxxxxxxx' OPENAI_API_KEY='xxxxxxxx' python3 index.py` 
- For development purposes, front the service with ngrok in a new window: `ngrok http 3000`. Note the returned ngrok endpoint. (This url may change over time!)
- On [Slack](https://api.slack.com/apps), provide the ngrok url as the endpoint under Event Subscriptions.
- Invite the bot to a channel and send a sample message

## To Do
- [x] Slack Event Support
- [x] Docker Support
- [x] Integrate with OpenAI APIs
- [ ] Maintain conversation context
- [ ] Support for emoji events
- [ ] Better error handling

## Resources:
- Slack Bolt for Python: https://github.com/slackapi/bolt-python
- Slack API docs: https://pypi.org/project/slack-sdk
- Slack Block Kit Builder: https://app.slack.com/block-kit-builder
- OpenAI Chat Completion API: https://platform.openai.com/docs/api-reference/chat/create?lang=python
- OpenAI Pricing: https://openai.com/pricing