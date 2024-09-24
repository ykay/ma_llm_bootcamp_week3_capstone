import chainlit as cl
from langfuse.openai import AsyncOpenAI
from dotenv import load_dotenv
import config

# from langsmith.wrappers import wrap_openai
# from langsmith import traceable

load_dotenv()

# Retrieve context
with open('data/llm_bootcamp_week1_transcript.txt', 'r') as file:
    full_text = file.read()

# print(full_text)

# Initialize OpenAI client
endpoint_url = "https://api.openai.com/v1"
client = AsyncOpenAI()
# https://platform.openai.com/docs/models/gpt-4o
model_name = "gpt-4o-mini"
model_kwargs = {
    "model": model_name, 
    "temperature": 0.2, 
    "max_tokens": 500,
}

# System prompt w/ context
system_msg = (
    f"{config.SYSTEM_PROMPT}: \n\n\n {full_text}"
)

@cl.on_message
async def on_message(message: cl.Message):
    # Maintain an array of messages in the user session
    message_history = cl.user_session.get("message_history", [])

    # Provide the system prompt
    message_history.append({"role": "system", "content": system_msg})

    # Record the user's message in the history
    message_history.append({"role": "user", "content": message.content})

    response_message = cl.Message(content="")
    await response_message.send()

    # Pass in the full message history for each request
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **model_kwargs
    )
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    # Record the AI's response in the history
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)