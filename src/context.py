import os
import re

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
        channel_id = body['event']['channel']
        logger.debug(f"Incoming message: [{channel_id}] {message_text}")
        
        # Remove any @BOT mentions from the text
        if(re.search("<@[a-zA-Z0-9]+>", message_text)):
            message_text = re.sub("<@[a-zA-Z0-9]+>", '', message_text).lstrip()

        # Initialize channel chat context if it does not exist
        if channel_id not in CHAT_CONTEXT:
            CHAT_CONTEXT[channel_id] = []

        # Add the message to CHAT_CONTEXT for the given channel_id if it does not already exist
        latest_msg = {"role": "user", "content": f"{message_text}"}
        if latest_msg not in CHAT_CONTEXT[channel_id]:
            CHAT_CONTEXT[channel_id].append(latest_msg)

        if len(CHAT_CONTEXT[channel_id]) > CONTEXT_DEPTH:
            CHAT_CONTEXT[channel_id].pop(0)
    except Exception:
        # Log the incoming event
        logger.debug(f"Incoming event: {body['event']}")
    return