"""
Agent: GitHub Profile Analyzer
- Fetches GitHub user and repo data
- Analyzes tech stack, repo quality, activity, seniority signals
"""


from src.tools.github_tool import analyze_github


def github_agent_node(state):
    github_username = state.github_username
    jd_skills = state.jd_skills
    gh_analysis = analyze_github(github_username, jd_skills)
    state.gh_analysis = gh_analysis
    return state