import os
import re

global CHAT_CONTEXT
global CHAT_DEPTH

PATTERN = "<@[a-zA-Z0-9]+>"
CHAT_CONTEXT = []
CONTEXT_DEPTH = 10

def handle_events(body):
    try:
        # Log the incoming message
        input = body["event"]["text"]
        if(os.environ.get("DEBUG")):
            print(input)
        
        # Remove any @BOT mentions from the text
        if(re.search(PATTERN, input)):
            input = re.sub(PATTERN, '', input).lstrip()
        
        # Add the message to CHAT_CONTEXT if it does not already exist 
        latest_msg = {"role": "user", "content": input}
        if latest_msg not in CHAT_CONTEXT:
            CHAT_CONTEXT.append(latest_msg)
        if len(CHAT_CONTEXT) > CONTEXT_DEPTH:
            CHAT_CONTEXT.pop(0)
    except Exception:
        if(os.environ.get("DEBUG")):
            print(body)  # Log incoming events
    return