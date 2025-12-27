import os

from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv


load_dotenv()

def get_llm() -> BaseChatModel:
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    model_key = os.getenv("GROQ_API_KEY")
    
    if model_key:
        print(f"Using Groq model: {model_name}")
        return ChatGroq(
            api_key=model_key, model=model_name, temperature=0.3
        )
    else:
        raise ValueError("Missing Groq Key")
    

def get_min_commits() -> int:
    return os.getenv("EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR", 15)