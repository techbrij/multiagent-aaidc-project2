# Tests for repo_match_agent.py

import pytest
from unittest.mock import patch, MagicMock
from src.agents.repo_match_agent import repo_match_agent_node
from src.graph.state import AppState, JDLanguageInfo, MatchRepoInfo


class TestRepoMatchAgentNode:
    """Tests for repo_match_agent_node function."""

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_matches_repos_to_skills(self, mock_fetch_repos):
        """Test that repos matching JD skills are included."""
        mock_fetch_repos.return_value = [
            {
                'name': 'python-project',
                'language': 'Python',
                'stargazers_count': 100,
                'open_issues_count': 5,
                'pushed_at': '2025-06-15T10:00:00Z'
            },
            {
                'name': 'ruby-project',
                'language': 'Ruby',
                'stargazers_count': 50,
                'open_issues_count': 0,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=0.5, source='explicit'),
                JDLanguageInfo(language='javascript', weight=0.5, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        # Only Python repo should match
        assert len(result.repos_info) == 1
        assert result.repos_info[0].name == 'python-project'

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_no_matching_repos(self, mock_fetch_repos):
        """Test handling when no repos match JD skills."""
        mock_fetch_repos.return_value = [
            {
                'name': 'ruby-project',
                'language': 'Ruby',
                'stargazers_count': 50,
                'open_issues_count': 0,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        assert result.repos_info == []

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_multiple_matching_repos(self, mock_fetch_repos):
        """Test matching multiple repos to same skill."""
        mock_fetch_repos.return_value = [
            {
                'name': 'python-app1',
                'language': 'Python',
                'stargazers_count': 100,
                'open_issues_count': 5,
                'pushed_at': '2025-06-15T10:00:00Z'
            },
            {
                'name': 'python-app2',
                'language': 'Python',
                'stargazers_count': 50,
                'open_issues_count': 0,
                'pushed_at': '2025-06-15T10:00:00Z'
            },
            {
                'name': 'js-app',
                'language': 'JavaScript',
                'stargazers_count': 25,
                'open_issues_count': 2,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=0.6, source='explicit'),
                JDLanguageInfo(language='javascript', weight=0.4, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        assert len(result.repos_info) == 3

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_repo_with_no_language(self, mock_fetch_repos):
        """Test handling repos with no language specified."""
        mock_fetch_repos.return_value = [
            {
                'name': 'docs-repo',
                'language': None,
                'stargazers_count': 10,
                'open_issues_count': 0,
                'pushed_at': '2025-06-15T10:00:00Z'
            },
            {
                'name': 'python-project',
                'language': 'Python',
                'stargazers_count': 100,
                'open_issues_count': 5,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        # Only Python repo should match
        assert len(result.repos_info) == 1
        assert result.repos_info[0].name == 'python-project'

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_case_insensitive_matching(self, mock_fetch_repos):
        """Test case insensitive language matching."""
        mock_fetch_repos.return_value = [
            {
                'name': 'project',
                'language': 'PYTHON',
                'stargazers_count': 100,
                'open_issues_count': 5,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        assert len(result.repos_info) == 1

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_repo_info_populated_correctly(self, mock_fetch_repos):
        """Test that MatchRepoInfo is populated with correct data."""
        mock_fetch_repos.return_value = [
            {
                'name': 'test-repo',
                'language': 'Python',
                'stargazers_count': 42,
                'open_issues_count': 7,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        repo = result.repos_info[0]
        assert repo.name == 'test-repo'
        assert repo.languages == ['Python']
        assert repo.stars == 42
        assert repo.has_issues is True
        assert repo.last_commit == '2025-06-15T10:00:00Z'

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_empty_jd_skills(self, mock_fetch_repos):
        """Test handling empty JD skills list."""
        mock_fetch_repos.return_value = [
            {
                'name': 'python-project',
                'language': 'Python',
                'stargazers_count': 100,
                'open_issues_count': 5,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[]
        )
        
        result = repo_match_agent_node(state)
        
        assert result.repos_info == []

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_empty_repos_list(self, mock_fetch_repos):
        """Test handling when user has no repos."""
        mock_fetch_repos.return_value = []
        
        state = AppState(
            github_username='newuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        assert result.repos_info == []

    @patch('src.agents.repo_match_agent.fetch_repos')
    def test_has_issues_false_when_zero_issues(self, mock_fetch_repos):
        """Test has_issues is False when open_issues_count is 0."""
        mock_fetch_repos.return_value = [
            {
                'name': 'test-repo',
                'language': 'Python',
                'stargazers_count': 10,
                'open_issues_count': 0,
                'pushed_at': '2025-06-15T10:00:00Z'
            }
        ]
        
        state = AppState(
            github_username='testuser',
            jd_skills=[
                JDLanguageInfo(language='python', weight=1.0, source='explicit')
            ]
        )
        
        result = repo_match_agent_node(state)
        
        assert result.repos_info[0].has_issues is False
