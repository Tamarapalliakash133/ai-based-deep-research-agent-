from langchain_openai import ChatOpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


def my_model():
    model = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.3,
        api_key=OPENAI_API_KEY
    )
    return model
