# Tests for retry.py

import pytest
import time
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from src.utils.retry import with_retry


class TestWithRetry:
    """Tests for with_retry function."""

    def test_success_on_first_try(self):
        """Test function succeeds on first try."""
        mock_func = MagicMock(return_value='success')
        
        result = with_retry(mock_func)
        
        assert result == 'success'
        assert mock_func.call_count == 1

    @patch('src.utils.retry.time.sleep')
    def test_retry_on_timeout(self, mock_sleep):
        """Test retries on Timeout error."""
        mock_func = MagicMock()
        mock_func.side_effect = [Timeout(), Timeout(), 'success']
        
        result = with_retry(mock_func)
        
        assert result == 'success'
        assert mock_func.call_count == 3
        assert mock_sleep.call_count == 2

    @patch('src.utils.retry.time.sleep')
    def test_retry_on_connection_error(self, mock_sleep):
        """Test retries on ConnectionError."""
        mock_func = MagicMock()
        mock_func.side_effect = [ConnectionError(), 'success']
        
        result = with_retry(mock_func)
        
        assert result == 'success'
        assert mock_func.call_count == 2

    @patch('src.utils.retry.time.sleep')
    def test_retry_on_rate_limit_429(self, mock_sleep):
        """Test retries on 429 rate limit error."""
        mock_func = MagicMock()
        error_response = MagicMock()
        error_response.status_code = 429
        http_error = HTTPError()
        http_error.response = error_response
        mock_func.side_effect = [http_error, 'success']
        
        result = with_retry(mock_func)
        
        assert result == 'success'
        assert mock_func.call_count == 2

    @patch('src.utils.retry.time.sleep')
    def test_retry_on_rate_limit_403(self, mock_sleep):
        """Test retries on 403 abuse protection error."""
        mock_func = MagicMock()
        error_response = MagicMock()
        error_response.status_code = 403
        http_error = HTTPError()
        http_error.response = error_response
        mock_func.side_effect = [http_error, 'success']
        
        result = with_retry(mock_func)
        
        assert result == 'success'

    def test_no_retry_on_other_http_error(self):
        """Test no retry on non-rate-limit HTTP errors."""
        mock_func = MagicMock()
        error_response = MagicMock()
        error_response.status_code = 404
        http_error = HTTPError()
        http_error.response = error_response
        mock_func.side_effect = http_error
        
        with pytest.raises(HTTPError):
            with_retry(mock_func)
        
        assert mock_func.call_count == 1

    def test_no_retry_on_request_exception(self):
        """Test no retry on generic RequestException."""
        mock_func = MagicMock()
        mock_func.side_effect = RequestException()
        
        with pytest.raises(RequestException):
            with_retry(mock_func)
        
        assert mock_func.call_count == 1

    @patch('src.utils.retry.time.sleep')
    def test_max_retries_exceeded_timeout(self, mock_sleep):
        """Test RuntimeError after max retries on Timeout."""
        mock_func = MagicMock()
        mock_func.side_effect = Timeout()
        
        with pytest.raises(RuntimeError, match="Timeout after 3 retries"):
            with_retry(mock_func, max_retries=3)
        
        assert mock_func.call_count == 3

    @patch('src.utils.retry.time.sleep')
    def test_max_retries_exceeded_connection_error(self, mock_sleep):
        """Test RuntimeError after max retries on ConnectionError."""
        mock_func = MagicMock()
        mock_func.side_effect = ConnectionError()
        
        with pytest.raises(RuntimeError, match="ConnectionError after 3 retries"):
            with_retry(mock_func, max_retries=3)

    @patch('src.utils.retry.time.sleep')
    def test_exponential_backoff(self, mock_sleep):
        """Test exponential backoff between retries."""
        mock_func = MagicMock()
        mock_func.side_effect = [Timeout(), Timeout(), 'success']
        
        with_retry(mock_func, base_delay=1.0, backoff_factor=2.0)
        
        # First retry: sleep(1.0), Second retry: sleep(2.0)
        assert mock_sleep.call_count == 2
        calls = [call[0][0] for call in mock_sleep.call_args_list]
        assert calls[0] == 1.0
        assert calls[1] == 2.0

    @patch('src.utils.retry.time.sleep')
    def test_custom_max_retries(self, mock_sleep):
        """Test custom max_retries parameter."""
        mock_func = MagicMock()
        mock_func.side_effect = Timeout()
        
        with pytest.raises(RuntimeError):
            with_retry(mock_func, max_retries=5)
        
        assert mock_func.call_count == 5

    @patch('src.utils.retry.time.sleep')
    def test_custom_base_delay(self, mock_sleep):
        """Test custom base_delay parameter."""
        mock_func = MagicMock()
        mock_func.side_effect = [Timeout(), 'success']
        
        with_retry(mock_func, base_delay=0.5)
        
        mock_sleep.assert_called_with(0.5)

    def test_returns_function_result(self):
        """Test that function result is returned correctly."""
        mock_func = MagicMock(return_value={'data': 'test', 'count': 42})
        
        result = with_retry(mock_func)
        
        assert result == {'data': 'test', 'count': 42}
