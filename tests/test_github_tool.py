import pytest
from src.tools.github_tool import fetch_repos, fetch_commit_count

# These tests are integration-style and may hit the real GitHub API.
# For real CI, use mocking (e.g., requests-mock) to avoid rate limits.

def test_fetch_repos_public():
    repos = fetch_repos('octocat')
    assert isinstance(repos, list)
    assert any('name' in repo for repo in repos)

def test_fetch_commit_count_public():
    # This will return 0 if repo is empty or API is rate-limited
    count = fetch_commit_count('octocat', 'Hello-World')
    assert isinstance(count, int)
    assert count >= 0
