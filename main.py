import chainlit as cl
from core.llms import LLM
from config.settings import Settings
from utils.get_prompt import get_system_prompt

settings = Settings()

LLM_CLIENT = LLM(
    model_name=settings.model_name,
    api_key=settings.api_key,
    llm_url=settings.LLM_url
)

PROMPT = get_system_prompt()

@cl.on_message
async def main(message: cl.Message):
    response = LLM_CLIENT.generate(PROMPT, message.content)
    await cl.Message(
        content=f"{response}",
    ).send()