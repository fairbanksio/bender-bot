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

# Determine Mode
mode = os.getenv("BOT_MODE", "RESPOND")  # RESPOND or LISTEN
if mode.upper() == "RESPOND":
    slack_mode = "app_mention"
elif mode.upper() == "LISTEN":
    slack_mode = {"type": "message", "subtype": None}
else:
    logger.warning(
        "BOT_MODE should be of type RESPOND or LISTEN; defaulting to RESPOND"
    )
    slack_mode = "app_mention"

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


# Handle message edits
@app.event(event={"type": "message", "subtype": "message_changed"})
def handle_change_events(body):
    try:
        context.handle_change(body)
    except Exception as e:
        logger.debug(f"Change Message Failed: {e}")


# Handle message deletion
@app.event(event={"type": "message", "subtype": "message_deleted"})
def handle_delete_events(body):
    try:
        context.handle_delete(body)
    except Exception as e:
        logger.debug(f"Delete Message Failed: {e}")


# Respond to message events
@app.event(slack_mode)
def handle_message_events(body, say, client):
    # Add an emoji to the incoming requests
    try:
        channel_id = body["event"]["channel"]
        message_ts = body["event"]["ts"]
        client.reactions_add(channel=channel_id, timestamp=message_ts, name="eyes")
    except Exception as e:
        logger.error(f"Slackmoji Failed: {e}")

    # Artificial Wait to Prevent Spam in LISTEN mode
    if os.getenv("BOT_MODE") == "LISTEN":
        time.sleep(60)

    # Make a call to OpenAI
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


# Respond to /context commands
@app.command("/context")
def get_context(body, say):
    channel_id = body["channel_id"]
    say("```" + {context.CHAT_CONTEXT[channel_id]} + "```")


# Respond to /reset commands
@app.command("/reset")
def reset_context(body, say):
    channel_id = body["channel_id"]
    context.CHAT_CONTEXT[channel_id].clear()
    say("Hmm, I forgot what we were talking about 🤔")


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
