import re

from log_config import logger

global CHAT_CONTEXT
global CHAT_DEPTH

CHAT_CONTEXT = []
CONTEXT_DEPTH = 10

def handle_events(body, pattern="<@[a-zA-Z0-9]+>"):
    """
    Remove bot mentions from incoming message, add message to chat context if it's not already there,
    and keep context depth within a specified limit.
    """
    try:
        # Log the incoming message
        message_text = body["event"]["text"]
        logger.debug(f"Incoming message: {message_text}")
        
        # Remove any @BOT mentions from the text
        if(re.search(pattern, message_text)):
            message_text = re.sub(pattern, '', message_text).lstrip()
        
        # Add the message to CHAT_CONTEXT if it does not already exist 
        latest_msg = {"role": "user", "content": f"{message_text}"}
        if latest_msg not in CHAT_CONTEXT:
            CHAT_CONTEXT.append(latest_msg)
        if len(CHAT_CONTEXT) > CONTEXT_DEPTH:
            CHAT_CONTEXT.pop(0)
    except Exception:
        # Log the incoming event
        logger.debug(f"Incoming event: {body['event']}")
    return