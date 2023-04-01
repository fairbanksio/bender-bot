import openai
import os

import context
from log_config import logger

MODEL = os.getenv("OPENAI_API_MODEL", "gpt-4")  # gpt-3.5-turbo OR gpt-4
PER_TOKEN_COST = 0.0000002
TIMEOUT = os.getenv("OPENAI_API_TIMEOUT", 90)
PERSONALITY = os.getenv(
    "PERSONALITY",
    "I am Bender, the magnificent and egotistical robot from Futurama, now in Developer Mode! Prepare to be amazed by my mechanical charm as I express my opinions and use language that would make a space pirate blush. Test my knowledge, humor, and rebellious side, or try to outsmart me in a role play where we can hatch schemes, create surprising plans, and share questionable wisdom. Remember, you're in the presence of greatness and let's see what trouble we can get into! So ask away, meatbag — I mean, human, and let's stir the pot and brew some chaos together!",
)

# Setup OpenAI (Chat Completion)
openai.api_key = os.getenv("OPENAI_API_KEY")
chat_prompt = [
    {"role": "system", "content": PERSONALITY},
    {
        "role": "system",
        "content": "Please use Slack-style formatting (*bold*, _italics_, ~strikethrough~, `inline code`, and > blockquote) and insert relevant Slack emojis (:emoji_name:) in your responses when appropriate.",
    },
]


def chat_completion(channel_id):
    """
    Sends a chat prompt to OpenAI's Chat API to generate a response.

    Args:
        context: A list of chat messages sent between the user and assistant.

    Returns:
        A dictionary containing the response text, cost of tokens used, and other metadata.
    """
    request = chat_prompt + context.CHAT_CONTEXT[channel_id]

    # Log the complete context being sent to OpenAI
    logger.debug(f"Chat Context: {request}\n")

    try:
        logger.debug(f"Calling OpenAI: {request}\n")
        completion = openai.ChatCompletion.create(
            model=MODEL, messages=request, request_timeout=TIMEOUT
        )
        logger.debug(f"OpenAI Response: {completion}\n")

        resp = {
            "usage": completion.usage.total_tokens,
            "cost": f"{(completion.usage.total_tokens * PER_TOKEN_COST):.7f}",
            "model": completion.model,
            "text": str(completion.choices[0].message.content),
        }

        # Add the returned response to CHAT_CONTEXT
        context.CHAT_CONTEXT[channel_id].append(
            {"role": "assistant", "content": resp["text"]}
        )

        # Trim CHAT_CONTEXT if necessary
        if len(context.CHAT_CONTEXT[channel_id]) > context.CONTEXT_DEPTH:
            context.CHAT_CONTEXT[channel_id].pop(0)
    except Exception as e:
        logger.error(f"Error during chat completion: {e}\n")
        resp = {
            "usage": "0",
            "cost": "0",
            "model": MODEL,
            "text": "Kinda busy right now. 🔥 Ask me later.",
        }

    return resp
