# Test configuration and shared fixtures

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import List

from src.graph.state import JDLanguageInfo, MatchRepoInfo, CommitInfo, AppState


# =================
# Sample Data Fixtures
# =================

@pytest.fixture
def sample_jd_text():
    """Sample job description text for testing."""
    return """
    We are looking for a Senior Developer with expertise in Python and JavaScript.
    Experience with Go and TypeScript is a plus. 
    Strong knowledge of REST APIs and SQL databases required.
    """


@pytest.fixture
def sample_jd_text_no_skills():
    """Job description with no recognized technical skills."""
    return "We are looking for a motivated team player with strong communication skills."


@pytest.fixture
def sample_jd_skills():
    """Sample JDLanguageInfo list for testing."""
    return [
        JDLanguageInfo(language='python', weight=0.4, source='explicit'),
        JDLanguageInfo(language='javascript', weight=0.3, source='explicit'),
        JDLanguageInfo(language='go', weight=0.2, source='inferred'),
        JDLanguageInfo(language='typescript', weight=0.1, source='explicit'),
    ]


@pytest.fixture
def sample_github_repos():
    """Sample GitHub API repo response data."""
    return [
        {
            'name': 'python-project',
            'language': 'Python',
            'stargazers_count': 100,
            'open_issues_count': 5,
            'pushed_at': '2025-06-15T10:00:00Z',
        },
        {
            'name': 'js-app',
            'language': 'JavaScript',
            'stargazers_count': 50,
            'open_issues_count': 0,
            'pushed_at': '2025-08-20T14:30:00Z',
        },
        {
            'name': 'old-java-project',
            'language': 'Java',
            'stargazers_count': 10,
            'open_issues_count': 2,
            'pushed_at': '2023-01-01T00:00:00Z',
        },
        {
            'name': 'go-service',
            'language': 'Go',
            'stargazers_count': 0,
            'open_issues_count': 0,
            'pushed_at': '2025-12-01T08:00:00Z',
        },
    ]


@pytest.fixture
def sample_repos_info():
    """Sample MatchRepoInfo list for testing."""
    return [
        MatchRepoInfo(
            name='python-project',
            languages=['python'],
            stars=100,
            has_issues=True,
            last_commit='2025-06-15T10:00:00Z'
        ),
        MatchRepoInfo(
            name='js-app',
            languages=['javascript'],
            stars=50,
            has_issues=False,
            last_commit='2025-08-20T14:30:00Z'
        ),
        MatchRepoInfo(
            name='go-service',
            languages=['go'],
            stars=0,
            has_issues=False,
            last_commit='2025-12-01T08:00:00Z'
        ),
    ]


@pytest.fixture
def sample_commit_info():
    """Sample CommitInfo list for testing."""
    return [
        CommitInfo(name='python-project', commit_count_1y=25),
        CommitInfo(name='js-app', commit_count_1y=10),
    ]


@pytest.fixture
def sample_app_state(sample_jd_skills, sample_repos_info, sample_commit_info):
    """Sample AppState for testing."""
    return AppState(
        github_username='testuser',
        jd_path='data/job-description.txt',
        jd_text='Python and JavaScript developer needed.',
        jd_skills=sample_jd_skills,
        repos_info=sample_repos_info,
        commit_info=sample_commit_info,
        score=0.0,
        report=''
    )


# =================
# Mock Fixtures
# =================

@pytest.fixture
def mock_github_api_success(sample_github_repos):
    """Mock successful GitHub API responses."""
    with patch('src.tools.github_tool.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_github_repos
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_github_api_user_valid():
    """Mock GitHub API for valid user check."""
    with patch('src.tools.github_tool.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_github_api_user_invalid():
    """Mock GitHub API for invalid user check."""
    with patch('src.tools.github_tool.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for JD analysis."""
    with patch('src.agents.jd_analyzer_agent.get_llm') as mock_llm:
        mock_model = MagicMock()
        mock_model.invoke.return_value = MagicMock(
            content='{"languages": [{"language": "python", "weight": 0.5, "source": "explicit"}, {"language": "javascript", "weight": 0.5, "source": "explicit"}], "total_weight": 1.0, "confidence": "high"}'
        )
        mock_llm.return_value = mock_model
        yield mock_llm


@pytest.fixture
def mock_fetch_repos(sample_github_repos):
    """Mock fetch_repos function."""
    with patch('src.agents.repo_match_agent.fetch_repos') as mock_func:
        mock_func.return_value = sample_github_repos
        yield mock_func


@pytest.fixture
def mock_fetch_commit_count():
    """Mock fetch_commit_count function."""
    with patch('src.agents.activity_agent.fetch_commit_count') as mock_func:
        mock_func.return_value = 15
        yield mock_func
