
from datetime import datetime, timedelta
import requests
from typing import Dict, List
from dateutil.relativedelta import relativedelta

from src.utils.retry import with_retry

GITHUB_API = "https://api.github.com"


def github_get(url: str, params: dict = None):
    def _request():
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json()

    return with_retry(_request)


# Helper to fetch user repos
def fetch_repos(username: str) -> List[Dict]:
    """
    Fetches repositories for a given GitHub username.

    Args:
        username (str): GitHub username.

    Returns:
        List[Dict]: List of repository information dictionaries.
    """
    try:
        url = f"{GITHUB_API}/users/{username}/repos?per_page=50&type=owner&sort=updated"   
        return github_get(url)
    except requests.exceptions.HTTPError  as e:
            status = e.response.status_code
            if status == 404:
                print('User or Repo not found.')
            raise

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
    return github_get(url)

def fetch_commit_count(username: str, repo: str) -> int:
    """
    Fetches the number of commits in a repository for a user in the past year.

    Args:
        username (str): GitHub username.
        repo (str): Repository name.

    Returns:
        int: Number of commits in the last year.
    """
    try:
        since = (datetime.utcnow() - relativedelta(years=1)).isoformat()
        url = f"{GITHUB_API}/repos/{username}/{repo}/commits?since={since}"
        json_result = github_get(url)
        return len(json_result) 
    except:
        return 0





