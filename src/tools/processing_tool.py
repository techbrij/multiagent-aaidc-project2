from typing import Dict, List

from src.graph.state import CommitInfo, JDLanguageInfo, MatchRepoInfo
from src.utils.config import get_min_commits

def is_repo_compatible_with_jd(repo: Dict, jd_skills: List[str]) -> bool:
    name = repo["name"].lower()
    description = (repo["description"] or "").lower()
    language = (repo["language"] or "").lower()

    text = f"{name} {description} {language}"
    return any(skill in text for skill in jd_skills)



def calculate_repo_match_score(jd_skills: List[JDLanguageInfo], repos_info: List[MatchRepoInfo]):
                
        jd_stack = {skill.language.lower(): skill.weight for skill in jd_skills}
        gh_stack = set(lang.lower() for repo in repos_info for lang in repo.languages)

        # Simple overlap score
        if not jd_stack:
            return 0.0
        
        skill_score = 0.0
        matched_skills = []
        for gh in gh_stack:
            weight = jd_stack.get(gh, 0) 
            if weight > 0:
                skill_score += weight
                matched_skills.append(gh)

        return skill_score, matched_skills



def calculate_commit_score(commit_info: List[CommitInfo]) -> float:
    total_commits = 0
    for repo in commit_info:
        total_commits += repo.commit_count_1y

    min_commits = get_min_commits()
    commit_score =  min(total_commits/min_commits, 1.0)
    return commit_score


def calculate_advanced_score(repos_info: List[MatchRepoInfo])-> float:
    
    total_open_issues_repo = 0
    total_starred_repo = 0
    total_relevant_repos = len(repos_info)
    for repo in repos_info:
        total_open_issues_repo += repo.has_issues
        total_starred_repo += repo.stars > 0

    advanced_score = (total_open_issues_repo + total_starred_repo)/(2* total_relevant_repos)
    return advanced_score

def calculate_overall_score(skill_score, commit_score, advanced_score ) -> float:
    overall_score = skill_score * 0.5 + commit_score * 0.3 + advanced_score * 0.2
    return overall_score

