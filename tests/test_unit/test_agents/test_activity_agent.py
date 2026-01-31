# Tests for activity_agent.py

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.agents.activity_agent import analyze_activity
from src.graph.state import AppState, JDLanguageInfo, MatchRepoInfo, CommitInfo


class TestAnalyzeActivity:
    """Tests for analyze_activity function."""

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_analyzes_recent_repos(self, mock_fetch_commit):
        """Test that recent repos are analyzed for commits."""
        mock_fetch_commit.return_value = 25
        
        # Recent repo (within last year)
        recent_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(
                    name='recent-repo',
                    languages=['python'],
                    stars=10,
                    has_issues=True,
                    last_commit=recent_date
                )
            ]
        )
        
        result = analyze_activity(state)
        
        assert len(result.commit_info) == 1
        assert result.commit_info[0].name == 'recent-repo'
        assert result.commit_info[0].commit_count_1y == 25

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_skips_old_repos(self, mock_fetch_commit):
        """Test that old repos (>1 year) are skipped."""
        mock_fetch_commit.return_value = 25
        
        # Old repo (more than 1 year ago)
        old_date = (datetime.utcnow() - timedelta(days=400)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(
                    name='old-repo',
                    languages=['python'],
                    stars=10,
                    has_issues=True,
                    last_commit=old_date
                )
            ]
        )
        
        result = analyze_activity(state)
        
        assert result.commit_info == []
        mock_fetch_commit.assert_not_called()

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_mixed_old_and_new_repos(self, mock_fetch_commit):
        """Test filtering of mixed old and new repos."""
        mock_fetch_commit.return_value = 15
        
        recent_date = (datetime.utcnow() - timedelta(days=60)).strftime('%Y-%m-%dT%H:%M:%SZ')
        old_date = (datetime.utcnow() - timedelta(days=400)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(name='recent1', languages=['python'], stars=10, has_issues=True, last_commit=recent_date),
                MatchRepoInfo(name='old1', languages=['python'], stars=5, has_issues=False, last_commit=old_date),
                MatchRepoInfo(name='recent2', languages=['javascript'], stars=20, has_issues=True, last_commit=recent_date),
            ]
        )
        
        result = analyze_activity(state)
        
        # Only 2 recent repos should be analyzed
        assert len(result.commit_info) == 2
        repo_names = [c.name for c in result.commit_info]
        assert 'recent1' in repo_names
        assert 'recent2' in repo_names
        assert 'old1' not in repo_names

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_empty_repos_list(self, mock_fetch_commit):
        """Test handling empty repos list."""
        state = AppState(
            github_username='testuser',
            repos_info=[]
        )
        
        result = analyze_activity(state)
        
        assert result.commit_info == []
        mock_fetch_commit.assert_not_called()

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_correct_commit_count_recorded(self, mock_fetch_commit):
        """Test that actual commit count from API is recorded."""
        mock_fetch_commit.side_effect = [10, 25, 50]
        
        recent_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit=recent_date),
                MatchRepoInfo(name='repo2', languages=['python'], stars=5, has_issues=False, last_commit=recent_date),
                MatchRepoInfo(name='repo3', languages=['javascript'], stars=20, has_issues=True, last_commit=recent_date),
            ]
        )
        
        result = analyze_activity(state)
        
        assert result.commit_info[0].commit_count_1y == 10
        assert result.commit_info[1].commit_count_1y == 25
        assert result.commit_info[2].commit_count_1y == 50

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_calls_fetch_with_correct_params(self, mock_fetch_commit):
        """Test fetch_commit_count is called with correct username and repo."""
        mock_fetch_commit.return_value = 5
        
        recent_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='myuser',
            repos_info=[
                MatchRepoInfo(name='myrepo', languages=['python'], stars=10, has_issues=True, last_commit=recent_date)
            ]
        )
        
        analyze_activity(state)
        
        mock_fetch_commit.assert_called_once_with('myuser', 'myrepo')

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_boundary_date_exactly_365_days(self, mock_fetch_commit):
        """Test repo at exactly 365 days boundary."""
        mock_fetch_commit.return_value = 10
        
        # Exactly at the cutoff - should NOT be included (cutoff is 365 days ago)
        boundary_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(name='boundary-repo', languages=['python'], stars=10, has_issues=True, last_commit=boundary_date)
            ]
        )
        
        result = analyze_activity(state)
        
        # The comparison is > cutoff, so exactly at cutoff should NOT be included
        assert len(result.commit_info) == 0

    @patch('src.agents.activity_agent.fetch_commit_count')
    def test_boundary_date_just_inside(self, mock_fetch_commit):
        """Test repo just inside 365 days boundary."""
        mock_fetch_commit.return_value = 10
        
        # Just inside the cutoff
        just_inside = (datetime.utcnow() - timedelta(days=364)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        state = AppState(
            github_username='testuser',
            repos_info=[
                MatchRepoInfo(name='inside-repo', languages=['python'], stars=10, has_issues=True, last_commit=just_inside)
            ]
        )
        
        result = analyze_activity(state)
        
        assert len(result.commit_info) == 1
