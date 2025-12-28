"""
Agent: JD Analyzer
- Reads job description from file
- Extracts required tech stack, skills, and role expectations
"""


from typing import Dict, List

def extract_skills(jd_text: str) -> Dict[str, List[str]]:
    """
    Extracts technical skills from the job description text using keyword matching.

    Args:
        jd_text (str): The job description text.

    Returns:
        Dict[str, List[str]]: Dictionary containing the extracted tech stack.
    """

    # Simple regex-based extraction for demo; can be replaced with NLP
    tech_keywords = [
        'python', 'javascript', 'typescript', 'java', 'c', 'c++', 'c#', 'go', 'rust', 'php',
        'ruby', 'swift', 'kotlin', 'r', 'matlab', 'scala', 'dart', 'objective-c', 'shell', 'powershell',
        'groovy', 'perl', 'lua', 'haskell', 'elixir', 'julia', 'fortran', 'assembly', 'cobol', 'scratch',
        'solidity', 'vba', 'abap', 'bash', 'nim', 'crystal', 'ocaml', 'f#', 'smalltalk', 'apex',
        'hack', 'pony', 'zig', 'vala', 'red', 'd', 'awk', 'idl', 'postscript'
    ]

    tech_stack = []
    translator = str.maketrans({p: " " for p in ",."})
    jd_norm = f" {jd_text.lower().translate(translator)} "

    found = [kw for kw in tech_keywords if f" {kw.lower()} " in jd_norm]

    if found:
        total_found = len(found)
        per_weight = 1/total_found
        tech_stack =  [{
                "language": lng,
                "weight": per_weight,
                "source": "manual"
            } for lng in found]
    return {'tech_stack': tech_stack}

def static_analyze_jd(jd_text: str) -> Dict:   
    """
    Performs a static analysis of the job description to extract skills and tech stack.

    Args:
        jd_text (str): The job description text.

    Returns:
        Dict: Dictionary containing extracted skills and tech stack.
    """
    skills = extract_skills(jd_text)
    return {**skills}