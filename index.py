import logging
import os
import sys

import context

from images import generate_image
from chat import chat_completion

from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Setup Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

# Slack Handlers
@app.middleware
def middleware(ack, body, next):
    ack()
    context.handle_events(body)
    return next()

# Respond to @BOT mentions
@app.event("app_mention")
def message_bender(say):
    # Make a call to OpenAI
    ai_resp = chat_completion()

    # Respond to the user
    say(
        text = ai_resp["text"],
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": ai_resp["text"]}},
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Complexity: "
                        + str(ai_resp["usage"])
                        + " || Est. Cost: "
                        + str(ai_resp["cost"])
                        + "¢ || Context Depth: "
                        + str(len(context.CHAT_CONTEXT))
                        + " || Model: "
                        + str(ai_resp["model"]),
                        "emoji": True,
                    }
                ],
            },
        ],
    )

# [BROKEN] Respond to emoji events
@app.event("reaction_added")
def say_something_to_reaction(say):
    say("OK!")

# Respond to /generate commands
@app.command("/generate")
def generate(say, body):
    prompt = body["text"]
    image = generate_image(prompt)
    say(
        text = prompt,
        blocks = [
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": prompt,
                    "emoji": True
                },
                "image_url": image,
                "alt_text": prompt
            }
	    ]
    )

# Respond to /prompt commands
@app.command("/prompt")
def generate_prompt_text(body, logger):
    logger.info(body)

# Respond to /reset commands
@app.command("/reset")
def reset_context(say):
    context.CHAT_CONTEXT.clear()
    say("Done :white_check_mark:") # Should probably be a private message

# Catch all (should be last handler)
@app.event("message")
def handle_message_events():
    pass

if __name__ == "__main__":
    try:
        app.start(3000)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)