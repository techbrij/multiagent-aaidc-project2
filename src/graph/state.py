from typing import List
from pydantic import BaseModel

# ===================
# Define State
# ===================

class AppState(BaseModel):
    github_username: str = ''
    jd_path: str =''
    jd_skills: List[str] = []
    gh_analysis: List = []
    score: float = 0.0
    report: str = ''