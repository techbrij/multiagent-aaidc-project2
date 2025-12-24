
from datetime import datetime, timedelta
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


def repo_matches_jd(repo: Dict, jd_skills: List[str]) -> bool:
    name = repo["name"].lower()
    description = (repo["description"] or "").lower()
    language = (repo["language"] or "").lower()

    text = f"{name} {description} {language}"
    return any(skill in text for skill in jd_skills)


# Analyze repos for tech stack, activity, quality, seniority
def analyze_github(username: str, jd_skills: List[str]) -> Dict:
   
    repos = fetch_repos(username)
    matched_repos = []
    cutoff = datetime.utcnow() - timedelta(days=365)  

    for repo in repos:
        if repo_matches_jd(repo, jd_skills):
            
            if datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > cutoff:
                commits = fetch_commit_count(username, repo["name"])
            else:
                commits = 0
            
            matched_repos.append({
                "name": repo["name"],
                "languages": [repo["language"]] if repo["language"] else [],
                "stars": repo["stargazers_count"],
                'has_issues': repo['open_issues_count'] > 0,
                "last_commit": repo["pushed_at"],
                "commit_count_1y": commits
            })

    return matched_repos