# Tests for processing_tool.py

import pytest
from unittest.mock import patch
from src.tools.processing_tool import (
    normalize_language,
    is_repo_compatible_with_jd,
    calculate_repo_match_score,
    calculate_commit_score,
    calculate_advanced_score,
    calculate_overall_score
)
from src.graph.state import JDLanguageInfo, MatchRepoInfo, CommitInfo


class TestNormalizeLanguage:
    """Tests for normalize_language function."""

    def test_normalize_basic(self):
        """Test basic language normalization."""
        assert normalize_language('Python') == 'python'
        assert normalize_language('JAVASCRIPT') == 'javascript'
        assert normalize_language('Go') == 'go'

    def test_normalize_with_special_chars(self):
        """Test normalization with special characters."""
        assert normalize_language('C++') == 'c++'
        assert normalize_language('C#') == 'c#'
        assert normalize_language('F#') == 'f#'

    def test_normalize_with_spaces(self):
        """Test normalization with spaces."""
        assert normalize_language(' Python ') == 'python'
        assert normalize_language('  Go  ') == 'go'

    def test_normalize_with_hyphens(self):
        """Test normalization removes hyphens."""
        assert normalize_language('java-script') == 'javascript'
        assert normalize_language('type-script') == 'typescript'

    def test_normalize_with_underscores(self):
        """Test normalization removes underscores."""
        assert normalize_language('java_script') == 'javascript'

    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        assert normalize_language('') == ''

    def test_normalize_none(self):
        """Test normalization of None returns empty string."""
        assert normalize_language(None) == ''


class TestIsRepoCompatibleWithJd:
    """Tests for is_repo_compatible_with_jd function."""

    def test_compatible_repo(self):
        """Test repo is compatible when language matches."""
        repo = {'language': 'Python'}
        jd_skills = ['python', 'javascript', 'go']
        
        assert is_repo_compatible_with_jd(repo, jd_skills) is True

    def test_incompatible_repo(self):
        """Test repo is incompatible when language doesn't match."""
        repo = {'language': 'Ruby'}
        jd_skills = ['python', 'javascript', 'go']
        
        assert is_repo_compatible_with_jd(repo, jd_skills) is False

    def test_repo_no_language(self):
        """Test repo with no language is not compatible."""
        repo = {'language': None}
        jd_skills = ['python', 'javascript']
        
        assert is_repo_compatible_with_jd(repo, jd_skills) is False

    def test_repo_empty_language(self):
        """Test repo with empty language string is not compatible."""
        repo = {'language': ''}
        jd_skills = ['python', 'javascript']
        
        assert is_repo_compatible_with_jd(repo, jd_skills) is False

    def test_case_insensitive_match(self):
        """Test that matching is case insensitive."""
        repo = {'language': 'PYTHON'}
        jd_skills = ['python']
        
        assert is_repo_compatible_with_jd(repo, jd_skills) is True


class TestCalculateRepoMatchScore:
    """Tests for calculate_repo_match_score function."""

    def test_full_match(self):
        """Test score when all JD skills are matched."""
        jd_skills = [
            JDLanguageInfo(language='python', weight=0.5, source='explicit'),
            JDLanguageInfo(language='javascript', weight=0.5, source='explicit'),
        ]
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
            MatchRepoInfo(name='repo2', languages=['javascript'], stars=5, has_issues=False, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score, matched = calculate_repo_match_score(jd_skills, repos_info)
        
        assert score == 1.0
        assert set(matched) == {'python', 'javascript'}

    def test_partial_match(self):
        """Test score with partial skill match."""
        jd_skills = [
            JDLanguageInfo(language='python', weight=0.5, source='explicit'),
            JDLanguageInfo(language='javascript', weight=0.3, source='explicit'),
            JDLanguageInfo(language='go', weight=0.2, source='inferred'),
        ]
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score, matched = calculate_repo_match_score(jd_skills, repos_info)
        
        assert score == 0.5
        assert matched == ['python']

    def test_no_match(self):
        """Test score when no skills match."""
        jd_skills = [
            JDLanguageInfo(language='python', weight=0.5, source='explicit'),
            JDLanguageInfo(language='javascript', weight=0.5, source='explicit'),
        ]
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['ruby'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score, matched = calculate_repo_match_score(jd_skills, repos_info)
        
        assert score == 0.0
        assert matched == []

    def test_empty_jd_skills(self):
        """Test score with empty JD skills."""
        jd_skills = []
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score = calculate_repo_match_score(jd_skills, repos_info)
        
        assert score == 0.0

    def test_empty_repos(self):
        """Test score with empty repos."""
        jd_skills = [
            JDLanguageInfo(language='python', weight=0.5, source='explicit'),
        ]
        repos_info = []
        
        score, matched = calculate_repo_match_score(jd_skills, repos_info)
        
        assert score == 0.0
        assert matched == []


class TestCalculateCommitScore:
    """Tests for calculate_commit_score function."""

    @patch('src.tools.processing_tool.get_min_commits')
    def test_exceeds_minimum(self, mock_get_min_commits):
        """Test score caps at 1.0 when exceeding minimum commits."""
        mock_get_min_commits.return_value = 20
        commit_info = [
            CommitInfo(name='repo1', commit_count_1y=30),
            CommitInfo(name='repo2', commit_count_1y=25),
        ]
        
        score = calculate_commit_score(commit_info)
        
        assert score == 1.0

    @patch('src.tools.processing_tool.get_min_commits')
    def test_partial_commits(self, mock_get_min_commits):
        """Test score is proportional for partial commits."""
        mock_get_min_commits.return_value = 100
        commit_info = [
            CommitInfo(name='repo1', commit_count_1y=25),
            CommitInfo(name='repo2', commit_count_1y=25),
        ]
        
        score = calculate_commit_score(commit_info)
        
        assert score == 0.5

    @patch('src.tools.processing_tool.get_min_commits')
    def test_zero_commits(self, mock_get_min_commits):
        """Test score is 0 with no commits."""
        mock_get_min_commits.return_value = 20
        commit_info = []
        
        score = calculate_commit_score(commit_info)
        
        assert score == 0.0

    @patch('src.tools.processing_tool.get_min_commits')
    def test_exact_minimum(self, mock_get_min_commits):
        """Test score is 1.0 at exact minimum commits."""
        mock_get_min_commits.return_value = 50
        commit_info = [
            CommitInfo(name='repo1', commit_count_1y=50),
        ]
        
        score = calculate_commit_score(commit_info)
        
        assert score == 1.0


class TestCalculateAdvancedScore:
    """Tests for calculate_advanced_score function."""

    def test_all_starred_with_issues(self):
        """Test max score when all repos have stars and issues."""
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
            MatchRepoInfo(name='repo2', languages=['javascript'], stars=5, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score = calculate_advanced_score(repos_info)
        
        assert score == 1.0

    def test_no_stars_no_issues(self):
        """Test zero score with no stars or issues."""
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=0, has_issues=False, last_commit='2025-01-01T00:00:00Z'),
            MatchRepoInfo(name='repo2', languages=['js'], stars=0, has_issues=False, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score = calculate_advanced_score(repos_info)
        
        assert score == 0.0

    def test_mixed_repos(self):
        """Test score with mixed repo states."""
        repos_info = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z'),
            MatchRepoInfo(name='repo2', languages=['js'], stars=0, has_issues=False, last_commit='2025-01-01T00:00:00Z'),
        ]
        
        score = calculate_advanced_score(repos_info)
        
        # 1 starred + 1 with issues out of 4 total (2 repos * 2 criteria)
        assert score == 0.5

    def test_empty_repos(self):
        """Test score is 0 with empty repos."""
        repos_info = []
        
        score = calculate_advanced_score(repos_info)
        
        assert score == 0.0


class TestCalculateOverallScore:
    """Tests for calculate_overall_score function."""

    def test_perfect_scores(self):
        """Test overall score with perfect component scores."""
        score = calculate_overall_score(1.0, 1.0, 1.0)
        
        # 1.0*0.5 + 1.0*0.3 + 1.0*0.2 = 1.0
        assert score == 1.0

    def test_zero_scores(self):
        """Test overall score with zero component scores."""
        score = calculate_overall_score(0.0, 0.0, 0.0)
        
        assert score == 0.0

    def test_weighted_scores(self):
        """Test overall score respects weights."""
        # skill=0.5, commit=0.3, advanced=0.2
        score = calculate_overall_score(0.8, 0.6, 0.4)
        
        # 0.8*0.5 + 0.6*0.3 + 0.4*0.2 = 0.4 + 0.18 + 0.08 = 0.66
        assert abs(score - 0.66) < 0.01

    def test_skill_weighted_heavily(self):
        """Test that skill score has the most weight."""
        score1 = calculate_overall_score(1.0, 0.0, 0.0)  # Only skill
        score2 = calculate_overall_score(0.0, 1.0, 0.0)  # Only commit
        score3 = calculate_overall_score(0.0, 0.0, 1.0)  # Only advanced
        
        assert score1 == 0.5
        assert score2 == 0.3
        assert score3 == 0.2
