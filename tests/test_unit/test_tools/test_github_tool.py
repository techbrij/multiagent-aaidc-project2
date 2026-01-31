# Tests for github_tool.py (mocked)

import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, HTTPError
from src.tools.github_tool import (
    validate_username,
    github_get,
    fetch_repos,
    fetch_profile,
    fetch_commit_count
)


class TestValidateUsername:
    """Tests for validate_username function."""

    @patch('src.tools.github_tool.requests.get')
    def test_valid_username(self, mock_get):
        """Test valid username returns True."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = validate_username('octocat')
        
        assert result is True
        mock_get.assert_called_once()

    @patch('src.tools.github_tool.requests.get')
    def test_nonexistent_username(self, mock_get):
        """Test nonexistent username returns False."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = validate_username('nonexistent-user-12345')
        
        assert result is False

    def test_empty_username(self):
        """Test empty username returns False without API call."""
        result = validate_username('')
        
        assert result is False

    def test_none_username(self):
        """Test None username returns False."""
        result = validate_username(None)
        
        assert result is False

    def test_username_too_long(self):
        """Test username exceeding 39 chars returns False."""
        result = validate_username('a' * 40)
        
        assert result is False

    def test_username_with_consecutive_hyphens(self):
        """Test username with consecutive hyphens returns False."""
        result = validate_username('user--name')
        
        assert result is False

    def test_username_starting_with_hyphen(self):
        """Test username starting with hyphen returns False."""
        result = validate_username('-username')
        
        assert result is False

    def test_username_ending_with_hyphen(self):
        """Test username ending with hyphen returns False."""
        result = validate_username('username-')
        
        assert result is False

    @patch('src.tools.github_tool.requests.get')
    def test_valid_username_with_hyphen(self, mock_get):
        """Test valid username with valid hyphens."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = validate_username('valid-user-name')
        
        assert result is True

    @patch('src.tools.github_tool.requests.get')
    def test_username_whitespace_stripped(self, mock_get):
        """Test username whitespace is stripped."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = validate_username('  octocat  ')
        
        assert result is True


class TestGithubGet:
    """Tests for github_get function."""

    @patch('src.tools.github_tool.requests.get')
    def test_successful_request(self, mock_get):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'login': 'octocat'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = github_get('https://api.github.com/users/octocat')
        
        assert result == {'login': 'octocat'}

    @patch('src.tools.github_tool.requests.get')
    def test_request_with_params(self, mock_get):
        """Test request with query parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = github_get('https://api.github.com/repos', params={'per_page': 10})
        
        mock_get.assert_called_with(
            'https://api.github.com/repos',
            params={'per_page': 10},
            timeout=60
        )

    @patch('src.tools.github_tool.requests.get')
    @patch('src.utils.retry.time.sleep')  # Skip actual sleep - sleep is in retry module
    def test_retry_on_timeout(self, mock_sleep, mock_get):
        """Test retry on timeout error."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'success'}
        mock_response.raise_for_status.return_value = None
        
        # Fail twice, succeed on third
        mock_get.side_effect = [Timeout(), Timeout(), mock_response]
        
        result = github_get('https://api.github.com/test')
        
        assert result == {'data': 'success'}
        assert mock_get.call_count == 3


class TestFetchRepos:
    """Tests for fetch_repos function."""

    @patch('src.tools.github_tool.github_get')
    @patch('src.tools.github_tool.get_max_repos')
    def test_fetch_repos_success(self, mock_max_repos, mock_github_get):
        """Test successful repo fetch."""
        mock_max_repos.return_value = 50
        mock_github_get.return_value = [
            {'name': 'repo1', 'language': 'Python'},
            {'name': 'repo2', 'language': 'JavaScript'},
        ]
        
        result = fetch_repos('testuser')
        
        assert len(result) == 2
        assert result[0]['name'] == 'repo1'

    @patch('src.tools.github_tool.github_get')
    @patch('src.tools.github_tool.get_max_repos')
    def test_fetch_repos_empty(self, mock_max_repos, mock_github_get):
        """Test fetch for user with no repos."""
        mock_max_repos.return_value = 50
        mock_github_get.return_value = []
        
        result = fetch_repos('newuser')
        
        assert result == []

    @patch('src.tools.github_tool.github_get')
    @patch('src.tools.github_tool.get_max_repos')
    def test_fetch_repos_uses_max_repos_config(self, mock_max_repos, mock_github_get):
        """Test that fetch_repos uses max_repos configuration."""
        mock_max_repos.return_value = 100
        mock_github_get.return_value = []
        
        fetch_repos('testuser')
        
        call_args = mock_github_get.call_args[0][0]
        assert 'per_page=100' in call_args


class TestFetchProfile:
    """Tests for fetch_profile function."""

    @patch('src.tools.github_tool.github_get')
    def test_fetch_profile_success(self, mock_github_get):
        """Test successful profile fetch."""
        mock_github_get.return_value = {
            'login': 'octocat',
            'name': 'The Octocat',
            'public_repos': 10
        }
        
        result = fetch_profile('octocat')
        
        assert result['login'] == 'octocat'
        assert result['public_repos'] == 10


class TestFetchCommitCount:
    """Tests for fetch_commit_count function."""

    @patch('src.tools.github_tool.github_get')
    def test_fetch_commit_count_success(self, mock_github_get):
        """Test successful commit count fetch."""
        mock_github_get.return_value = [
            {'sha': 'abc123'},
            {'sha': 'def456'},
            {'sha': 'ghi789'},
        ]
        
        result = fetch_commit_count('testuser', 'testrepo')
        
        assert result == 3

    @patch('src.tools.github_tool.github_get')
    def test_fetch_commit_count_empty(self, mock_github_get):
        """Test commit count for repo with no commits."""
        mock_github_get.return_value = []
        
        result = fetch_commit_count('testuser', 'emptyrepo')
        
        assert result == 0

    @patch('src.tools.github_tool.github_get')
    def test_fetch_commit_count_error_returns_zero(self, mock_github_get):
        """Test that errors return 0."""
        mock_github_get.side_effect = Exception("API Error")
        
        result = fetch_commit_count('testuser', 'badrepo')
        
        assert result == 0

    @patch('src.tools.github_tool.github_get')
    def test_fetch_commit_count_url_includes_since(self, mock_github_get):
        """Test that since parameter is included in URL."""
        mock_github_get.return_value = []
        
        fetch_commit_count('testuser', 'testrepo')
        
        call_url = mock_github_get.call_args[0][0]
        assert 'since=' in call_url
