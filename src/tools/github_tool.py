
from datetime import datetime, timedelta
import requests
from typing import Dict, List
from dateutil.relativedelta import relativedelta

GITHUB_API = "https://api.github.com"

# Helper to fetch user repos
def fetch_repos(username: str) -> List[Dict]:
    """
    Fetches repositories for a given GitHub username.

    Args:
        username (str): GitHub username.

    Returns:
        List[Dict]: List of repository information dictionaries.
    """
    url = f"{GITHUB_API}/users/{username}/repos?per_page=50&type=owner&sort=updated"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

# Helper to fetch user profile
def fetch_profile(username: str) -> Dict:
    """
    Fetches the GitHub profile for a given username.

    Args:
        username (str): GitHub username.

    Returns:
        Dict: Dictionary containing profile information.
    """
    url = f"{GITHUB_API}/users/{username}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def fetch_commit_count(username: str, repo: str) -> int:
    """
    Fetches the number of commits in a repository for a user in the past year.

    Args:
        username (str): GitHub username.
        repo (str): Repository name.

    Returns:
        int: Number of commits in the last year.
    """
    since = (datetime.utcnow() - relativedelta(years=1)).isoformat()
    url = f"{GITHUB_API}/repos/{username}/{repo}/commits?since={since}"
    r = requests.get(url)
    return len(r.json()) if r.status_code == 200 else 0





