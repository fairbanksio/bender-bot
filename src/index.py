import json
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

# Determine Mode -- RESPOND or LISTEN
mode = os.getenv("BOT_MODE", "RESPOND")
if mode.upper() == "RESPOND":
    slack_mode = "app_mention"
elif mode.upper() == "LISTEN":
    slack_mode = {"type": "message", "subtype": None}
else:
    logger.warning(
        "⚠️ BOT_MODE should be of type RESPOND or LISTEN; defaulting to RESPOND"
    )
    slack_mode = "app_mention"

# Setup Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


# Slack Handlers
# @app.middleware
# def middleware(request, next):
    # logger.debug(f"Request: {str(request)}")
    # logger.debug(f"Headers: {request.headers}")
    # next()


# Handle message changes
@app.event(event={"type": "message", "subtype": "message_changed"})
def handle_change_events(body):
    try:
        context.handle_change(body)
    except Exception as e:
        logger.debug(f"⛔ Change failed: {e}")


# Handle message deletion
@app.event(event={"type": "message", "subtype": "message_deleted"})
def handle_delete_events(body):
    try:
        context.handle_delete(body)
    except Exception as e:
        logger.debug(f"⛔ Delete failed: {e}")


# Handle message events
@app.event(slack_mode)
def handle_app_mentions(ack, body, say, client):
    ack()
    # Add an emoji to the incoming requests
    try:
        channel_id = body["event"]["channel"]
        message_ts = body["event"]["ts"]
        message_type = body["event"]["type"]
        client.reactions_add(channel=channel_id, timestamp=message_ts, name="eyes")
    except Exception as e:
        logger.error(f"⛔ Slackmoji failed: {e}")

    try:
        context.handle_events(body)
    except Exception as e:
        logger.error(f"⛔ Event error: {e} - {body}")

    # Make a call to OpenAI
    start_time = time.time()
    ai_resp = chat_completion(channel_id)
    end_time = time.time()
    elapsed_time = f"{(end_time - start_time):.2f}"

    # Respond to the user
    return say(
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
                        + str(ai_resp["model"].upper())
                        + " || Response Time: "
                        + str(elapsed_time)
                        + "s",
                        "emoji": True,
                    }
                ],
            },
        ],
    )


# Respond to /generate commands
@app.command("/generate")
def generate(ack, say, body):
    ack()
    prompt = body["text"]
    logger.debug(f"📸 Generate image prompt: {prompt}")
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


# Respond to /context commands
@app.command("/context")
def get_context(ack, body, say):
    ack()
    channel_id = body["channel_id"]
    try:
        channel_context = json.dumps(context.CHAT_CONTEXT[channel_id])
    except Exception:
        channel_context = []
    say(f"Channel Context: ```{channel_context}```")
    return


# Respond to /reset commands
@app.command("/reset")
def reset_context(ack, body, say):
    ack()
    channel_id = body["channel_id"]
    context.CHAT_CONTEXT[channel_id].clear()
    say("Hmm, I forgot what we were talking about 🤔")


# Catch all (should be last handler)
@app.event("message")
def handle_message_events(ack, body):
    ack()
    context.handle_events(body)


if __name__ == "__main__":
    try:
        with SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start():
            pass
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception:
        sys.exit(1)
