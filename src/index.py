import os
import sys
import time

import context

from images import generate_image
from chat import chat_completion
from log_config import logger

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Setup Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


# Slack Handlers
@app.middleware
def middleware(ack, body, next):
    ack()
    try:
        context.handle_events(body)
    except Exception as e:
        logger.error(e)
    return next()


# Respond to @BOT mentions
@app.event("app_mention")
def message_bender(body, say):
    # Make a call to OpenAI
    channel_id = body["event"]["channel"]
    start_time = time.time()
    ai_resp = chat_completion(channel_id)
    end_time = time.time()
    elapsed_time = f"{(end_time - start_time):.2f}"

    # Respond to the user
    say(
        text=ai_resp["text"],
        blocks=[
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
                        + str(len(context.CHAT_CONTEXT[channel_id]))
                        + " || Model: "
                        + str(ai_resp["model"])
                        + " || Response Time: "
                        + str(elapsed_time) + "s",
                        "emoji": True,
                    }
                ],
            },
        ],
    )


# Respond to /generate commands
@app.command("/generate")
def generate(say, body):
    prompt = body["text"]
    logger.debug(f"Generate Image prompt: {prompt}")
    image = generate_image(prompt)
    say(
        text=prompt,
        blocks=[
            {
                "type": "image",
                "title": {"type": "plain_text", "text": prompt, "emoji": True},
                "image_url": image,
                "alt_text": prompt,
            }
        ],
    )


# Respond to /reset commands
@app.command("/reset")
def reset_context(body, say):
    channel_id = body["event"]["channel"]
    context.CHAT_CONTEXT[channel_id].clear()
    say("Done :white_check_mark:")  # Should probably be a private message


# Catch all (should be last handler)
@app.event("message")
def handle_message_events():
    pass


if __name__ == "__main__":
    try:
        with SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start():
            pass
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception:
        sys.exit(1)
