## Setup

#### Requirements

- Python 3.9+
- [A Slack app token](https://api.slack.com/apps)
	- Create a Slack app from scratch
		- NEW: Create a new app using a Slack [app manifest](../manifest.yml)
	- Install the app into your Slack workspace
- An [OpenAI API key](https://platform.openai.com/account/api-keys) for Chat capabilities
- A [Replica API key](https://replicate.com/account) for Image related features

(Note: Python packages `slack` and `slackclient` are no longer supported. Please use `slack_bolt`.)

#### Local

- Setup pipenv: `pip install pipenv && pipenv shell`
- Install dependencies: `pipenv install`
- Launch the service with your Slack token: `SLACK_APP_TOKEN='xapp-xxxxx' SLACK_BOT_TOKEN='xoxb-xxxxx' SLACK_SIGNING_SECRET='xxxxx' OPENAI_API_KEY='xxxxx' REPLICATE_API_TOKEN='xxxxx' python3 index.py`
- Invite the bot to a channel and send a sample message

#### Docker

bender-bot is also available for deployment via Docker:
```
docker run -d --env-file .env jonfairbanks/bender-bot
```

#### Docker-Compose

bender-bot can also be stood up using Docker Compose:
```
docker compose up
```

Remember to rename _.env.sample_ to _.env_ and change values