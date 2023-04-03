import mimetypes
import os
import re

import files

from images import interrogate_image
from log_config import logger

global CHAT_CONTEXT
global CHAT_DEPTH

CHAT_CONTEXT = {}
CONTEXT_DEPTH = os.environ.get("CONTEXT_DEPTH", 25)


def handle_events(body):
    """
    Remove bot mentions from incoming message, add message to chat context if it's not already there,
    and keep context depth within a specified limit.
    """

    try:
        # Log the incoming message
        message_text = body["event"]["text"]
        channel_id = body["event"]["channel"]
        logger.debug(f"📨 Incoming message: [{channel_id}] {message_text}\n")

        # Remove any @BOT mentions from the text
        if re.search("<@[a-zA-Z0-9]+>", message_text):
            message_text = re.sub("<@[a-zA-Z0-9]+>", "", message_text).lstrip()

        # Initialize channel chat context if it does not exist
        if channel_id not in CHAT_CONTEXT:
            CHAT_CONTEXT[channel_id] = []

        # Add the message to CHAT_CONTEXT for the given channel_id if it does not already exist
        latest_msg = {"role": "user", "content": f"{message_text}"}
        if latest_msg not in CHAT_CONTEXT[channel_id]:
            CHAT_CONTEXT[channel_id].append(latest_msg)

        if len(CHAT_CONTEXT[channel_id]) > CONTEXT_DEPTH:
            CHAT_CONTEXT[channel_id].pop(0)

        # Handle files
        if "files" in body["event"].keys():
            try:
                # Extract file info
                attached_file = body["event"]["files"][0]
                remote_file_url = attached_file["url_private_download"]
                remote_file_name = attached_file["name"]

                # Save temp copy and get local file path
                local_file_path = files.save_file(remote_file_url, remote_file_name)

                # TO DO: check mimetype of file
                mimetype = mimetypes.guess_type(local_file_path)
                if mimetype:
                    logger.debug(f"The MIME type of '{local_file_path}' is: {mimetype}")
                else:
                    logger.debug(f"🤷 Unknown MIME type for '{local_file_path}'")

                if mimetype == "image":
                    # Filetype: Image
                    prompt = interrogate_image(local_file_path)
                    logger.debug(f"🔍 Extracted prompt: {prompt}")
                    # TO DO: Inject the prompt (if image) into CONTEXT
                elif mimetype == "text":
                    # TO DO: Inject into CONTEXT
                    pass
                else:
                    # TO DO: Handle other cases
                    pass

                # Delete temp file
                files.delete_file(local_file_path)

            except Exception as e:
                logger.error(f"⛔ Failed to process file: {e}")

    except Exception:
        # Log the incoming event
        logger.debug(f"🖱️ Incoming event: {body['event']}\n")
    return


def handle_change(body):
    # Log the changed message
    message_text = body["event"]["previous_message"]["text"]
    new_message_text = body["event"]["message"]["text"]
    channel_id = body["event"]["channel"]
    try:
        for i, s in enumerate(CHAT_CONTEXT[channel_id]):
            if message_text in s["content"]:
                CHAT_CONTEXT[channel_id][i]["content"] = new_message_text
                logger.debug(
                    f"📝 Context changed: [{channel_id}] {message_text} ➞ {new_message_text}\n"
                )
                break
    except Exception as e:
        logger.error(f"⛔ Change failed: [{channel_id}] {e}\n")


def handle_delete(body):
    # Log the deleted message
    message_text = body["event"]["previous_message"]["text"]
    channel_id = body["event"]["channel"]
    try:
        for i, s in enumerate(CHAT_CONTEXT[channel_id]):
            if message_text in s["content"]:
                CHAT_CONTEXT[channel_id].remove(CHAT_CONTEXT[channel_id][i])
                logger.debug(f"🗑️ Context deleted: [{channel_id}] {message_text}\n")
                break
    except Exception as e:
        logger.error(f"⛔ Delete failed: [{channel_id}] {e}\n")
