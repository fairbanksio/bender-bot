import os
import sys
import time

import context
import files

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
    
    # Catch files
    if "files" in body["event"].keys():
        try:
            # extract file info
            attached_file = body["event"]["files"][0]
            remote_file_url = attached_file["url_private_download"]
            remote_file_name = attached_file["name"]

            # save temp copy and get local file path
            downloaded_image_path = files.save_file(remote_file_url, remote_file_name)

            # Do something with the file
            # check mimetype of file, and if supported image, send to CLIPInterrogator
            logger.debug(f"Image downloaded: {downloaded_image_path}")

            # delete temp file
            files.delete_file(downloaded_image_path)

        except Exception as e:
            logger.error(f"Failed to process file: {e}")   
    else:
        logger.debug("Event did not contain any files to process")

     
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
