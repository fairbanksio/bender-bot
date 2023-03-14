# bender-bot

A Python based Slack bot

## Requirements
- [A Slack token](https://api.slack.com/apps)
	- Create a new app from scratch
	- Add `chat:write` permissions
	- Install the app to your workplace

(Note: `slack` and `slackclient` are no longer supported. Please use `slack-sdk`.)

## Setup
- Setup pipenv: `pip install pipenv && pipenv shell`
- Install dependencies: `pipenv install`
- Launch with your Slack token: `SLACK_TOKEN='xoxb-xxxxxxxx' python3 index.py` 

## Usage
- WIP

## To Do
- [ ] Docker Support
- [ ] Integration with OpenAI APIs

## Resources:
- Slack API docs: https://pypi.org/project/slack-sdk/