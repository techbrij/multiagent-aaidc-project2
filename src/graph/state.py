from typing import List
from pydantic import BaseModel
from dataclasses import dataclass


# ===================
# Define State
# ===================

@dataclass
class JDLanguageInfo():
    language: str
    weight: float
    source: str

@dataclass
class MatchRepoInfo():
    name: str
    languages: List[str]
    stars: int 
    has_issues: bool
    last_commit: str
    


@dataclass
class CommitInfo():
    name: str
    commit_count_1y: float

class AppState(BaseModel):
    github_username: str = ''
    jd_path: str =''
    jd_skills: List[JDLanguageInfo] = []
    repos_info: List[MatchRepoInfo] = []
    commit_info: List[CommitInfo] = []
    score: float = 0.0
    report: str = ''

