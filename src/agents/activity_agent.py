
from datetime import datetime, timedelta
from typing import List

from src.graph.state import CommitInfo, MatchRepoInfo
from src.tools.github_tool import fetch_commit_count

# Analyze repos for activity
def analyze_activity(state) -> List[CommitInfo]:  
    username = state.github_username
    repos: List[MatchRepoInfo] = state.repos_info
    cutoff = datetime.utcnow() - timedelta(days=365)  
    commit_details = []
    for repo in repos:              
        if datetime.strptime(repo.last_commit, '%Y-%m-%dT%H:%M:%SZ') > cutoff:
            commits = fetch_commit_count(username, repo.name)
            commit_details.append(CommitInfo(name=repo.name, commit_count_1y=commits))
            
    state.commit_info = commit_details
    return state