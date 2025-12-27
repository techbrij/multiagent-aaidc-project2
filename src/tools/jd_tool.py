"""
Agent: JD Analyzer
- Reads job description from file
- Extracts required tech stack, skills, and role expectations
"""


from typing import Dict, List

def read_jd_file(jd_path: str) -> str:
    with open(jd_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_skills(jd_text: str) -> Dict[str, List[str]]:

    jd_text = jd_text.lower()

    # Simple regex-based extraction for demo; can be replaced with NLP
    tech_keywords = [
        'python', 'java', 'c\+\+', 'javascript', 'typescript', 'react', 'node', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'sql', 'nosql', 'ml', 'ai', 'nlp', 'data', 'api', 'rest', 'graphql', 'linux',
        'git', 'ci/cd', 'testing', 'unit test', 'integration test', 'agile', 'scrum', 'devops', 'microservices'
    ]
    found = []
    for kw in tech_keywords:
        if f' {kw} ' in jd_text:
            found.append(kw)

    total_found = len(found)
    per_weight = 1/total_found
    tech_stack =  [{
            "language": lng,
            "weight": per_weight,
            "source": "manual"
         } for lng in found]
    return {'tech_stack': tech_stack}

def analyze_jd(jd_path: str) -> Dict:
    jd_text = read_jd_file(jd_path)
    skills = extract_skills(jd_text)
    return {'jd_text': jd_text, **skills}