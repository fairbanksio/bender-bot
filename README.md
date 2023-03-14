# bender-bot

A Python based Slack bot

## Requirements
- [A Slack token](https://api.slack.com/apps)
	- Create a new Slack app from scratch
	- Add `chat:write` & `channel.history` permissions for the Bot user
	- Install the app to your workplace
- ngrok installed for testing: `sudo snap install ngrok`

(Note: `slack` and `slackclient` are no longer supported. Please use `slack_bolt`.)

## Setup
- Setup pipenv: `pip install pipenv && pipenv shell`
- Install dependencies: `pipenv install`


## Usage
- Launch the service with your Slack token: `SLACK_BOT_TOKEN='xoxb-xxxxxxxx' SLACK_SIGNING_SECRET='xxxxxxxx' python3 index.py` 
- In a new window, front the service with ngrok: `ngrok http 8080`
- On [Slack](https://api.slack.com/apps), provide the ngrok url as the endpoint under Event Subscriptions
- Invite the bot to a channel and send a sample message

## To Do
- [x] Slack Event Support
- [ ] Docker Support
- [ ] Integrate with OpenAI APIs

## Resources:
- Slack Bolt for Python: https://github.com/slackapi/bolt-python
- Slack API docs: https://pypi.org/project/slack-sdk