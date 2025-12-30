import os

from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv


load_dotenv()

def get_llm() -> BaseChatModel:
    """
    Returns a language model instance configured from environment variables.

    Returns:
        BaseChatModel: An instance of the language model for chat-based tasks.
    Raises:
        ValueError: If the API key is missing.
    """
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
    """
    Returns the expected minimum number of commits in the last year from environment or default.

    Returns:
        int: Minimum number of expected commits in the last year.
    """
    min_commits = os.getenv("EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR", 15)
    return int(min_commits)