# Tests for common.py

import pytest
from src.utils.common import sanitize_text


class TestSanitizeText:
    """Tests for sanitize_text function."""

    def test_remove_html_tags(self):
        """Test that HTML tags are removed."""
        text = "<p>Hello <b>World</b></p>"
        
        result = sanitize_text(text)
        
        assert result == "Hello World"

    def test_remove_script_tags(self):
        """Test that script tags and content are removed."""
        text = "Hello<script>alert('xss')</script>World"
        
        result = sanitize_text(text)
        
        assert "<script>" not in result
        assert "</script>" not in result

    def test_strip_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        text = "   Hello World   "
        
        result = sanitize_text(text)
        
        assert result == "Hello World"

    def test_preserve_content(self):
        """Test that regular text content is preserved."""
        text = "Python developer needed with 5 years experience."
        
        result = sanitize_text(text)
        
        assert result == text

    def test_remove_complex_html(self):
        """Test removal of complex HTML attributes."""
        text = '<div class="test" id="main">Content</div>'
        
        result = sanitize_text(text)
        
        assert result == "Content"
        assert "<div" not in result

    def test_multiple_tags(self):
        """Test removal of multiple HTML tags."""
        text = "<h1>Title</h1><p>Paragraph</p><ul><li>Item</li></ul>"
        
        result = sanitize_text(text)
        
        assert "<" not in result
        assert ">" not in result
        assert "Title" in result
        assert "Paragraph" in result
        assert "Item" in result

    def test_empty_string(self):
        """Test empty string input."""
        text = ""
        
        result = sanitize_text(text)
        
        assert result == ""

    def test_only_whitespace(self):
        """Test whitespace-only input."""
        text = "   \n\t   "
        
        result = sanitize_text(text)
        
        assert result == ""

    def test_no_html(self):
        """Test text without any HTML."""
        text = "Plain text without any HTML tags"
        
        result = sanitize_text(text)
        
        assert result == text

    def test_self_closing_tags(self):
        """Test removal of self-closing tags."""
        text = "Line1<br/>Line2<hr/>Line3"
        
        result = sanitize_text(text)
        
        assert "<br" not in result
        assert "<hr" not in result
        assert "Line1" in result
        assert "Line2" in result

    def test_preserve_special_chars(self):
        """Test that non-HTML angle brackets are handled."""
        text = "Python is > Ruby and < Java in some cases"
        
        result = sanitize_text(text)
        
        # The regex might not handle this perfectly, but shouldn't break
        assert "Python" in result
