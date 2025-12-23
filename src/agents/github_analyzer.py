"""
Agent: GitHub Profile Analyzer
- Fetches GitHub user and repo data
- Analyzes tech stack, repo quality, activity, seniority signals
"""

import datetime
import requests
from typing import Dict, List
from dateutil.relativedelta import relativedelta

GITHUB_API = "https://api.github.com"

# Helper to fetch user repos
def fetch_repos(username: str) -> List[Dict]:
    url = f"{GITHUB_API}/users/{username}/repos?per_page=100&type=owner&sort=updated"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

# Helper to fetch user profile
def fetch_profile(username: str) -> Dict:
    url = f"{GITHUB_API}/users/{username}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def fetch_commit_count(username: str, repo: str) -> int:
    since = (datetime.utcnow() - relativedelta(years=1)).isoformat()
    url = f"{GITHUB_API}/repos/{username}/{repo}/commits?since={since}"
    r = requests.get(url)
    return len(r.json()) if r.status_code == 200 else 0

# Analyze repos for tech stack, activity, quality, seniority
def analyze_github(username: str) -> Dict:
   
    repos = fetch_repos(username)
    # Tech stack: collect languages
    languages = set()
    for repo in repos:
        if repo.get('language'):
            languages.add(repo['language'].lower())
    # Activity: count commits, PRs, issues (last 12 months)
    # For demo, just count updated_at in last 12 months
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=365)
    active_repos = [r for r in repos if datetime.strptime(r['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > cutoff]
    # Seniority: look for tests, docs, issues, PRs
    seniority_signals = {
        'has_tests': any('test' in (r['name'].lower() + (r.get('description') or '').lower()) for r in repos),
        'has_docs': any('doc' in (r['name'].lower() + (r.get('description') or '').lower()) for r in repos),
        'has_issues': any(r['open_issues_count'] > 0 for r in repos),
        'repo_count': len(repos),
        'active_repo_count': len(active_repos)
    }
    return {
        'languages': list(languages),
        'seniority_signals': seniority_signals,
        'repos': repos
    }

def github_agent_node(state):
    github_username = state.github_username
    gh_analysis = analyze_github(github_username)
    state.gh_analysis = gh_analysis
    return state