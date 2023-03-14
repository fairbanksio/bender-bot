import logging
import os
from slack_bolt.async_app import AsyncApp

logging.basicConfig(level=logging.INFO)

# Initializes your app with your bot token and signing secret
app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

@app.middleware  # or app.use(log_request)
async def log_request(logger, body, next):
    logger.info(body)
    return await next()

# Listens to incoming messages that contain "hello"
# To learn available listener method arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
async def message_hello(message, ack, say):
    # say() sends a message to the channel where the event was triggered
    await ack()
    await say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"Hey there <@{message['user']}>!"
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )

@app.event("message")
async def handle_message_events(body, ack, logger):
    await ack()

@app.action("button_click")
async def action_button_click(body, ack, say):
    # Acknowledge the action
    await ack()

if __name__ == "__main__":
    app.start(3000)