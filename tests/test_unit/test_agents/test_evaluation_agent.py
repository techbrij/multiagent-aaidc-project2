# Tests for evaluation_agent.py

import pytest
from unittest.mock import patch, MagicMock
from src.agents.evaluation_agent import generate_report, evaluation_agent_node
from src.graph.state import AppState, JDLanguageInfo, MatchRepoInfo, CommitInfo


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_excellent_match(self):
        """Test report for excellent match (>80%)."""
        report = generate_report(0.9, "python, javascript", 5, 3)
        
        assert "Excellent match" in report
        assert "90.0%" in report
        assert "Total relevant repositories: 5" in report
        assert "Active repositories(in last year): 3" in report

    def test_good_match(self):
        """Test report for good match (50-80%)."""
        report = generate_report(0.65, "python", 3, 2)
        
        assert "Good match" in report
        assert "65.0%" in report

    def test_partial_match(self):
        """Test report for partial match (<50%)."""
        report = generate_report(0.3, "go", 1, 0)
        
        assert "Partial match" in report
        assert "30.0%" in report

    def test_boundary_excellent(self):
        """Test exact 0.8 boundary (should be Good, not Excellent)."""
        report = generate_report(0.8, "python", 2, 1)
        
        assert "Good match" in report

    def test_boundary_good(self):
        """Test exact 0.5 boundary (should be Partial, not Good)."""
        report = generate_report(0.5, "python", 2, 1)
        
        assert "Partial match" in report

    def test_above_boundary_excellent(self):
        """Test just above 0.8 boundary is Excellent."""
        report = generate_report(0.81, "python", 2, 1)
        
        assert "Excellent match" in report

    def test_above_boundary_good(self):
        """Test just above 0.5 boundary is Good."""
        report = generate_report(0.51, "python", 2, 1)
        
        assert "Good match" in report

    def test_zero_score(self):
        """Test report with zero score."""
        report = generate_report(0.0, "", 0, 0)
        
        assert "Partial match" in report
        assert "0.0%" in report

    def test_perfect_score(self):
        """Test report with perfect score."""
        report = generate_report(1.0, "python, javascript, go", 10, 8)
        
        assert "Excellent match" in report
        assert "100.0%" in report

    def test_matched_skills_in_report(self):
        """Test that matched skills appear in report."""
        report = generate_report(0.75, "python, javascript, typescript", 5, 3)
        
        assert "python" in report
        assert "javascript" in report
        assert "typescript" in report

    def test_score_formatting(self):
        """Test score is formatted to 2 decimal places."""
        report = generate_report(0.8333, "python", 3, 2)
        
        assert "Score: 0.83" in report


class TestEvaluationAgentNode:
    """Tests for evaluation_agent_node function."""

    @patch('src.agents.evaluation_agent.calculate_repo_match_score')
    @patch('src.agents.evaluation_agent.calculate_commit_score')
    @patch('src.agents.evaluation_agent.calculate_advanced_score')
    @patch('src.agents.evaluation_agent.calculate_overall_score')
    def test_evaluation_updates_state(
        self, mock_overall, mock_advanced, mock_commit, mock_repo_match
    ):
        """Test that evaluation updates state with score and report."""
        mock_repo_match.return_value = (0.8, ['python', 'javascript'])
        mock_commit.return_value = 0.7
        mock_advanced.return_value = 0.6
        mock_overall.return_value = 0.75
        
        state = AppState(
            github_username='testuser',
            jd_path='test.txt',
            jd_text='Python developer',
            jd_skills=[
                JDLanguageInfo(language='python', weight=0.5, source='explicit'),
            ],
            repos_info=[
                MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
            ],
            commit_info=[
                CommitInfo(name='repo1', commit_count_1y=25),
            ]
        )
        
        result = evaluation_agent_node(state)
        
        assert result.score == 0.75
        assert result.report != ''
        assert "python" in result.report.lower()

    @patch('src.agents.evaluation_agent.calculate_repo_match_score')
    @patch('src.agents.evaluation_agent.calculate_commit_score')
    @patch('src.agents.evaluation_agent.calculate_advanced_score')
    @patch('src.agents.evaluation_agent.calculate_overall_score')
    def test_evaluation_calls_all_score_functions(
        self, mock_overall, mock_advanced, mock_commit, mock_repo_match
    ):
        """Test that all scoring functions are called."""
        mock_repo_match.return_value = (0.5, ['python'])
        mock_commit.return_value = 0.5
        mock_advanced.return_value = 0.5
        mock_overall.return_value = 0.5
        
        state = AppState(
            github_username='testuser',
            jd_skills=[JDLanguageInfo(language='python', weight=1.0, source='explicit')],
            repos_info=[],
            commit_info=[]
        )
        
        evaluation_agent_node(state)
        
        mock_repo_match.assert_called_once()
        mock_commit.assert_called_once()
        mock_advanced.assert_called_once()
        mock_overall.assert_called_once()

    @patch('src.agents.evaluation_agent.calculate_repo_match_score')
    @patch('src.agents.evaluation_agent.calculate_commit_score')
    @patch('src.agents.evaluation_agent.calculate_advanced_score')
    @patch('src.agents.evaluation_agent.calculate_overall_score')
    def test_evaluation_empty_repos(
        self, mock_overall, mock_advanced, mock_commit, mock_repo_match
    ):
        """Test evaluation with no matched repositories."""
        mock_repo_match.return_value = (0.0, [])
        mock_commit.return_value = 0.0
        mock_advanced.return_value = 0.0
        mock_overall.return_value = 0.0
        
        state = AppState(
            github_username='testuser',
            jd_skills=[],
            repos_info=[],
            commit_info=[]
        )
        
        result = evaluation_agent_node(state)
        
        assert result.score == 0.0
        assert "Total relevant repositories: 0" in result.report
