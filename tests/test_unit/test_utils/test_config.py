# Tests for config.py

import pytest
import os
from unittest.mock import patch, MagicMock


class TestGetLlm:
    """Tests for get_llm function."""

    @patch.dict(os.environ, {'GROQ_API_KEY': 'test-key', 'GROQ_MODEL': 'test-model'})
    @patch('src.utils.config.ChatGroq')
    def test_get_llm_with_key(self, mock_chat_groq):
        """Test get_llm returns ChatGroq when API key is set."""
        from src.utils.config import get_llm
        
        mock_chat_groq.return_value = MagicMock()
        
        result = get_llm()
        
        mock_chat_groq.assert_called_once_with(
            api_key='test-key',
            model='test-model',
            temperature=0.3
        )

    @patch.dict(os.environ, {'GROQ_API_KEY': 'test-key'}, clear=True)
    @patch('src.utils.config.ChatGroq')
    def test_get_llm_default_model(self, mock_chat_groq):
        """Test get_llm uses default model when not specified."""
        from src.utils.config import get_llm
        
        mock_chat_groq.return_value = MagicMock()
        
        # Clear GROQ_MODEL to test default
        if 'GROQ_MODEL' in os.environ:
            del os.environ['GROQ_MODEL']
        
        result = get_llm()
        
        call_kwargs = mock_chat_groq.call_args[1]
        assert call_kwargs['model'] == 'llama-3.1-8b-instant'

    @patch.dict(os.environ, {}, clear=True)
    def test_get_llm_missing_key_raises(self):
        """Test get_llm raises ValueError when API key is missing."""
        # Need to reimport to pick up cleared env
        import importlib
        import src.utils.config as config_module
        
        # Clear the key
        if 'GROQ_API_KEY' in os.environ:
            del os.environ['GROQ_API_KEY']
        
        with pytest.raises(ValueError, match="Missing Groq Key"):
            config_module.get_llm()


class TestGetMinCommits:
    """Tests for get_min_commits function."""

    @patch.dict(os.environ, {'EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR': '25'})
    def test_get_min_commits_from_env(self):
        """Test get_min_commits returns env value."""
        from src.utils.config import get_min_commits
        
        result = get_min_commits()
        
        assert result == 25

    @patch.dict(os.environ, {}, clear=True)
    def test_get_min_commits_default(self):
        """Test get_min_commits returns default when env not set."""
        from src.utils.config import get_min_commits
        
        if 'EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR' in os.environ:
            del os.environ['EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR']

        result = get_min_commits()
        
        assert result == 15  # default value

    @patch.dict(os.environ, {'EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR': '100'})
    def test_get_min_commits_returns_int(self):
        """Test get_min_commits returns an integer."""
        from src.utils.config import get_min_commits
        
        result = get_min_commits()
        
        assert isinstance(result, int)


class TestGetMaxRepos:
    """Tests for get_max_repos function."""

    @patch.dict(os.environ, {'MAX_REPOS_TO_FETCH': '100'})
    def test_get_max_repos_from_env(self):
        """Test get_max_repos returns env value."""
        from src.utils.config import get_max_repos
        
        result = get_max_repos()
        
        assert result == 100

    @patch.dict(os.environ, {}, clear=True)
    def test_get_max_repos_default(self):
        """Test get_max_repos returns default when env not set."""
        from src.utils.config import get_max_repos
        
        if 'MAX_REPOS_TO_FETCH' in os.environ:
            del os.environ['MAX_REPOS_TO_FETCH']

        result = get_max_repos()
        
        assert result == 50  # default value

    @patch.dict(os.environ, {'MAX_REPOS_TO_FETCH': '200'})
    def test_get_max_repos_returns_int(self):
        """Test get_max_repos returns an integer."""
        from src.utils.config import get_max_repos
        
        result = get_max_repos()
        
        assert isinstance(result, int)
