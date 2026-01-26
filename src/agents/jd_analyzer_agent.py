

import json
from src.tools.file_reader_tool import read_jd_file
from src.tools.static_jd_tool import static_analyze_jd
from langchain_core.messages import SystemMessage, HumanMessage

from src.utils.common import sanitize_text
from src.utils.config import get_llm
from src.utils.logger import logger

SYSTEM_PROMPT_JD_EXTRACTOR = """
You are a technical recruiter assistant specialized in analyzing software engineering job descriptions.

Your task is to extract programming languages required for the role from the provided Job Description.

Rules:
- Only extract programming languages (not frameworks or tools)
- Normalize language names (e.g., Py → Python, JS → JavaScript)
- Infer languages from frameworks when clearly implied (e.g., FastAPI → Python)
- Rank languages by importance
- Assign weights that sum to 1.0
- Use at most 2 decimal places for weights
- Follow the exact JSON schema for the output
- Do not add explanations or commentary

    Output JSON Schema:
    {
    "languages": [
        {
            "language": "string",
            "weight": number,
            "source": "explicit | inferred"
        }
    ],
    "total_weight": number,
    "confidence": "high | medium | low"
    }
"""

def llm_extract_lng_from_JD(jd_text: str) -> dict:

    """
    Uses an LLM to extract programming languages from a job description.

    Args:
        jd_text (str): The job description text.

    Returns:
        dict: A dictionary containing extracted languages, weights, and confidence, following the specified JSON schema.
    """

    user_prompt = f""" Job Description:
                    {jd_text}
                    """
    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT_JD_EXTRACTOR),
            HumanMessage(content=user_prompt)
        ])
        return response.content
    except Exception as e:
        logger.error(f"LLM call failed in llm_extract_lng_from_JD: {str(e)}")
        raise


def jd_agent_node(state):
    """
    Orchestrates the job description analysis process and updates the state with extracted information.

    Args:
        state: The application state object containing the job description path and other context.

    Returns:
        Updates the state object in place with extracted job description information.
    """

    logger.info("Running jd_analyzer agent")
    if not state.jd_text:
        jd_path = state.jd_path
        state.jd_text = read_jd_file(jd_path)  

    # Validate the Job description    
    jd_value_sanitized = sanitize_text(state.jd_text)
    if not jd_value_sanitized or len(jd_value_sanitized) < 10:
        raise Exception("Job description is empty or too short. Please provide a valid job description")

    try:
        result = llm_extract_lng_from_JD(state.jd_text)
        json_result = json.loads(result)
        json_result = json_result.get('languages')
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        json_result = []

    state.jd_skills = json_result
    if not json_result:
        # ************************************************
        #   Fallback Option: In case of empty response or any issue with LLM result
        # ************************************************
        logger.info("Running fallback static analyzer" )
        jd_analyze = static_analyze_jd(state.jd_text)           
        state.jd_skills = jd_analyze.get('tech_stack') or []
    return state
