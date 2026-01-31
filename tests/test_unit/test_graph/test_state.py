# Tests for state.py

import pytest
from src.graph.state import JDLanguageInfo, MatchRepoInfo, CommitInfo, AppState


class TestJDLanguageInfo:
    """Tests for JDLanguageInfo dataclass."""

    def test_create_jd_language_info(self):
        """Test creating JDLanguageInfo instance."""
        info = JDLanguageInfo(language='python', weight=0.5, source='explicit')
        
        assert info.language == 'python'
        assert info.weight == 0.5
        assert info.source == 'explicit'

    def test_jd_language_info_attributes(self):
        """Test all attributes are accessible."""
        info = JDLanguageInfo(language='javascript', weight=0.3, source='inferred')
        
        assert hasattr(info, 'language')
        assert hasattr(info, 'weight')
        assert hasattr(info, 'source')


class TestMatchRepoInfo:
    """Tests for MatchRepoInfo dataclass."""

    def test_create_match_repo_info(self):
        """Test creating MatchRepoInfo instance."""
        info = MatchRepoInfo(
            name='test-repo',
            languages=['python', 'javascript'],
            stars=100,
            has_issues=True,
            last_commit='2025-01-01T00:00:00Z'
        )
        
        assert info.name == 'test-repo'
        assert info.languages == ['python', 'javascript']
        assert info.stars == 100
        assert info.has_issues is True
        assert info.last_commit == '2025-01-01T00:00:00Z'

    def test_match_repo_info_empty_languages(self):
        """Test MatchRepoInfo with empty languages list."""
        info = MatchRepoInfo(
            name='no-lang-repo',
            languages=[],
            stars=0,
            has_issues=False,
            last_commit='2025-01-01T00:00:00Z'
        )
        
        assert info.languages == []


class TestCommitInfo:
    """Tests for CommitInfo dataclass."""

    def test_create_commit_info(self):
        """Test creating CommitInfo instance."""
        info = CommitInfo(name='test-repo', commit_count_1y=25)
        
        assert info.name == 'test-repo'
        assert info.commit_count_1y == 25

    def test_commit_info_zero_commits(self):
        """Test CommitInfo with zero commits."""
        info = CommitInfo(name='empty-repo', commit_count_1y=0)
        
        assert info.commit_count_1y == 0


class TestAppState:
    """Tests for AppState Pydantic model."""

    def test_create_app_state_defaults(self):
        """Test creating AppState with defaults."""
        state = AppState()
        
        assert state.github_username == ''
        assert state.jd_path == ''
        assert state.jd_text == ''
        assert state.jd_skills == []
        assert state.repos_info == []
        assert state.commit_info == []
        assert state.score == 0.0
        assert state.report == ''

    def test_create_app_state_with_values(self):
        """Test creating AppState with custom values."""
        state = AppState(
            github_username='testuser',
            jd_path='/path/to/jd.txt',
            jd_text='Python developer needed',
            score=0.85,
            report='Test report'
        )
        
        assert state.github_username == 'testuser'
        assert state.jd_path == '/path/to/jd.txt'
        assert state.jd_text == 'Python developer needed'
        assert state.score == 0.85
        assert state.report == 'Test report'

    def test_app_state_with_skills(self):
        """Test AppState with JD skills."""
        skills = [
            JDLanguageInfo(language='python', weight=0.5, source='explicit'),
            JDLanguageInfo(language='javascript', weight=0.5, source='explicit')
        ]
        state = AppState(jd_skills=skills)
        
        assert len(state.jd_skills) == 2

    def test_app_state_with_repos(self):
        """Test AppState with repo info."""
        repos = [
            MatchRepoInfo(name='repo1', languages=['python'], stars=10, has_issues=True, last_commit='2025-01-01T00:00:00Z')
        ]
        state = AppState(repos_info=repos)
        
        assert len(state.repos_info) == 1

    def test_app_state_with_commits(self):
        """Test AppState with commit info."""
        commits = [
            CommitInfo(name='repo1', commit_count_1y=25)
        ]
        state = AppState(commit_info=commits)
        
        assert len(state.commit_info) == 1

    def test_app_state_assignment(self):
        """Test assigning values to AppState."""
        state = AppState()
        state.github_username = 'newuser'
        state.score = 0.75
        
        assert state.github_username == 'newuser'
        assert state.score == 0.75

    def test_app_state_dict_conversion(self):
        """Test converting AppState to dict."""
        state = AppState(
            github_username='testuser',
            jd_path='/path/to/jd.txt',
            score=0.5
        )
        
        state_dict = state.model_dump()
        
        assert state_dict['github_username'] == 'testuser'
        assert state_dict['jd_path'] == '/path/to/jd.txt'
        assert state_dict['score'] == 0.5
