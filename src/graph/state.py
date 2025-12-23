from pydantic import BaseModel

# ===================
# Define State
# ===================

class AppState(BaseModel):
    github_username: str = ''
    jd_path: str =''
    jd_skills: dict = {}
    gh_analysis: dict = {}
    score: float = 0.0
    report: str = ''