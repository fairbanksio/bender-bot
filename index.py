import logging
import openai
import os
from slack_bolt.async_app import AsyncApp

logging.basicConfig(level=logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")
app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

async def chat_completion(user_msg):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_msg}
        ]
    )
    return await completion.choices[0].message
    
@app.middleware
async def log_request(logger, body, next):
    #logger.info(body["event"]["text"]) # Log incoming message(s)
    return await next()

# Listens to incoming messages that contain "bender"
# Available listener methods: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("bender") # Should swap to app.command?
async def message_bender(logger, message, ack, say):
    await ack()
    user_msg = message["event"]["text"]
    logger.info(user_msg)
    ai_resp = await chat_completion(user_msg)
    await say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"<@{message['user'] + ': ' + ai_resp}>"
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"<@{message['user'] + ': ' + ai_resp}>",
    )


# Catch all handler
@app.event("message")
async def handle_message_events(ack):
    await ack()

@app.action("button_click")
async def action_button_click(logger, body, ack):
    logger.info(body)
    await ack()

if __name__ == "__main__":
    app.start(3000)