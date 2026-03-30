from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("There is some interrupt in api key sorry for inconivence")

def my_model():
    model = ChatOpenAI(model = "gpt-4.1-mini",temperature = 0.3)
    return model
