from typing import Dict, List

from src.graph.state import CommitInfo, JDLanguageInfo, MatchRepoInfo
from src.utils.config import get_min_commits

def is_repo_compatible_with_jd(repo: Dict, jd_skills: List[str]) -> bool:
    """
    Checks if a repository is compatible with the job description skills.

    Args:
        repo (Dict): Repository information dictionary.
        jd_skills (List[str]): List of required skills from the job description.

    Returns:
        bool: True if the repository matches any of the required skills, False otherwise.
    """
    name = repo["name"].lower()
    description = (repo["description"] or "").lower()
    language = (repo["language"] or "").lower()

    text = f"{name} {description} {language}"
    return any(skill in text for skill in jd_skills)



def calculate_repo_match_score(jd_skills: List[JDLanguageInfo], repos_info: List[MatchRepoInfo]):
        """
        Calculates the skill match score between job description skills and repository languages.

        Args:
            jd_skills (List[JDLanguageInfo]): List of job description language info objects.
            repos_info (List[MatchRepoInfo]): List of repository info objects.

        Returns:
            Tuple[float, List[str]]: Skill match score and list of matched skills.
        """
                
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
    """
    Calculates the commit score based on the number of commits in the last year.

    Args:
        commit_info (List[CommitInfo]): List of commit info objects for repositories.

    Returns:
        float: Commit score (0.0 to 1.0).
    """
    total_commits = 0
    for repo in commit_info:
        total_commits += repo.commit_count_1y

    min_commits = get_min_commits()
    commit_score =  min(total_commits/min_commits, 1.0)
    return commit_score


def calculate_advanced_score(repos_info: List[MatchRepoInfo])-> float:
    """
    Calculates an advanced score based on open issues and starred repositories.

    Args:
        repos_info (List[MatchRepoInfo]): List of repository info objects.

    Returns:
        float: Advanced score (0.0 to 1.0).
    """
    
    total_open_issues_repo = 0
    total_starred_repo = 0
    total_relevant_repos = len(repos_info)
    for repo in repos_info:
        total_open_issues_repo += repo.has_issues
        total_starred_repo += repo.stars > 0

    advanced_score = (total_open_issues_repo + total_starred_repo)/(2* total_relevant_repos)
    return advanced_score

def calculate_overall_score(skill_score, commit_score, advanced_score ) -> float:
    """
    Calculates the overall score as a weighted sum of skill, commit, and advanced scores.

    Args:
        skill_score (float): Skill match score.
        commit_score (float): Commit activity score.
        advanced_score (float): Advanced repository score.

    Returns:
        float: Overall score (0.0 to 1.0).
    """
    overall_score = skill_score * 0.5 + commit_score * 0.3 + advanced_score * 0.2
    return overall_score

