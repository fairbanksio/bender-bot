# bender-bot

A Python based Slack bot with AI based features

- Chat Completion via ChatGPT
- Image Generation via Stable Diffusion

## Requirements
- Python 3.9+
- [A Slack token](https://api.slack.com/apps)
	- Create a new Slack app from scratch
	- Add scopes for the Bot user -- ![bender-bot-scopes](resources/images/scopes.png)
	- Install the app into your Slack workspace
- An [OpenAI API key](https://platform.openai.com/account/api-keys) for Chat capabilities
- A [Replica API key](https://replicate.com/account) for Image related features
- ngrok installed for development: `sudo snap install ngrok`

(Note: Python packages `slack` and `slackclient` are no longer supported. Please use `slack_bolt`.)

## Setup

#### Local

- Setup pipenv: `pip install pipenv && pipenv shell`
- Install dependencies: `pipenv install`
- Launch the service with your Slack token: `SLACK_BOT_TOKEN='xoxb-xxxxx' SLACK_SIGNING_SECRET='xxxxx' OPENAI_API_KEY='xxxxx' REPLICATE_API_TOKEN='xxxxx' python3 index.py` 
- For development purposes, front the service with ngrok in a new window: `ngrok http 3000`. Note the returned ngrok endpoint. (**This url may change over time!**)
- On [Slack](https://api.slack.com/apps), provide https://<YOUR-NGROK-URL>.ngrok.io/slack/events as the endpoint under Event Subscriptions.
- Setup Slack slash commands -- ![bender-bot-slash](resources/images/slash.png)
- Invite the bot to a channel and send a sample message

#### Docker

bender-bot is also available for deployment via Docker:
```
docker run -d -p 3000:3000 jonfairbanks/bender-bot
```

#### Options

Options can be overridden or enable using the following env variables:

- **DEBUG**: Enables additional logging of events, requests, responses and chat context

## Usage

#### General Chat
```
@Bender what is the deepest body of water in North America? 
```
![bender-bot-chat](resources/images/usage-chat.png)

#### Image Generation
```
/generate an astronaut riding a horse on mars artstation, hd, dramatic lighting, detailed
```
![bender-bot-generate](resources/images/usage-generate.png)

## To Do
- [x] Slack Event Support
- [x] Docker Support
- [ ] Helm Support
- [ ] Docker Build via Github Actions
- [x] Integrate with OpenAI APIs
- [x] Maintain conversation context
- [ ] Support Private Channels & Messages
- [ ] Support File Uploads
- [ ] Support for emoji events 🔥
- [x] Prompt based image generation (Stable Diffusion)
- [x] Improve Context via Chat History
- [x] Better error handling
- [ ] Code Refactoring
- [ ] Helm Support

## Resources:

#### Slack
- Slack Bolt for Python: https://github.com/slackapi/bolt-python
- Slack API docs: https://pypi.org/project/slack-sdk
- Slack Block Kit Builder: https://app.slack.com/block-kit-builder

#### OpenAI
- OpenAI Chat Completion API: https://platform.openai.com/docs/api-reference/chat/create?lang=python
- OpenAI Pricing: https://openai.com/pricing

#### Replicate
- Replicate Python SDK: https://replicate.com/docs/get-started/python
- Replicate Pricing: https://replicate.com/pricing