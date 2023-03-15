import json
import logging
import openai
import os
from slack_bolt import App

logging.basicConfig(level=logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

def chat_completion(user_msg):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_msg}
        ]
    )
    return str(completion.choices[0].message.content)
    
@app.middleware
def log_request(logger, body, next):
    logger.info(body["event"]["text"]) # Log incoming message(s)
    return next()

@app.message("bender-bot-debug")
def event_test(body, ack, say, logger):
    ack()
    logger.info(body)
    say('```' + json.dumps(body) + '```')

@app.event("app_mention")
def message_bender(event, ack, say, logger):
    ack()
    logger.info(event)
    user_msg = event["text"]
    logger.info(user_msg)
    ai_resp = chat_completion(user_msg)
    say(ai_resp) # Convert to support Blocks?

# Catch all handler
@app.event("message")
def handle_message_events(ack):
    ack()

if __name__ == "__main__":
    app.start(3000)