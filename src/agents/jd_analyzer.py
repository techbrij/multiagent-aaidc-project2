

import json
from typing import List
from src.tools.jd_tool import analyze_jd
from langchain_core.messages import SystemMessage, HumanMessage

from src.utils.llm import get_llm

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
        print(f"LLM call failed in llm_extract_lng_from_JD: {str(e)}")
        raise





def jd_agent_node(state):
    jd_path = state.jd_path
    jd_analyze = analyze_jd(jd_path)    
    jd_text = jd_analyze.get('jd_text')
    result = llm_extract_lng_from_JD(jd_text)
    try:
        json_result = json.loads(result)
        json_result = json_result.get('languages')
    except Exception as e:
        print(f'Error: {str(e)}')
        json_result = []

    state.jd_skills = json_result
    if not json_result:        
        state.jd_skills = jd_analyze.get('tech_stack') or []
    return state
