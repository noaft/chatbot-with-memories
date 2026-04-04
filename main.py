import chainlit as cl
from core.llms import LLM
from config.settings import Settings
from utils.get_prompt import get_system_prompt

settings = Settings()

LLM_CLIENT = LLM(
    model_name=settings.model_name,
    api_key=settings.api_key,
    llm_url=settings.LLM_url,
    embed_model=settings.embed_model,
    embed_dims=settings.embed_dims,
)
LLM_CLIENT.long_term_memory.reset()

PROMPT = get_system_prompt()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("thread_id", cl.context.session.id)
    user = cl.context.session.user
    user_id = user.identifier if user else "default_user"
    cl.user_session.set("user_id", user_id)

@cl.on_message
async def main(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    user_id = cl.user_session.get("user_id", "default_user")
    response = LLM_CLIENT.generate(PROMPT, message.content, thread_id=thread_id, user_id=user_id)
    await cl.Message(
        content=f"{response}",
    ).send()