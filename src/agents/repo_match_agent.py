"""
Agent: GitHub Profile Analyzer
- Fetches GitHub user and repo data
- Analyzes tech stack, repo quality, activity, seniority signals
"""


from typing import List
from src.graph.state import JDLanguageInfo, MatchRepoInfo
from src.tools.github_tool import fetch_repos
from src.tools.processing_tool import is_repo_compatible_with_jd


def repo_match_agent_node(state):
    """
    Matches GitHub repositories to job description skills and updates the state with compatible repositories.

    Args:
        state: The application state object containing GitHub username and job description skills.

    Returns:
        Updates the state object in place with a list of matched repositories.
    """
    github_username = state.github_username
    jd_skills: List[JDLanguageInfo] = state.jd_skills

    repos = fetch_repos(github_username)

    matched_repos: List[MatchRepoInfo] = []
    skill_lngs = [skill.language.lower() for skill in jd_skills]
    for repo in repos:
        if is_repo_compatible_with_jd(repo, skill_lngs):
            repo = MatchRepoInfo(
                        name =  repo["name"],
                        languages = [repo["language"]] if repo["language"] else [],
                        stars =  repo["stargazers_count"],
                        has_issues =  repo['open_issues_count'] > 0,
                        last_commit = repo["pushed_at"]
                        )

            matched_repos.append(repo)
             
    state.repos_info = matched_repos
    return state