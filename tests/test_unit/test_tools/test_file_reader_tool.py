# Tests for file_reader_tool.py

import pytest
import os
from src.tools.file_reader_tool import read_jd_file


class TestReadJdFile:
    """Tests for the read_jd_file function."""

    def test_read_jd_file_success(self, tmp_path):
        """Test reading a valid job description file."""
        jd_content = "Python developer needed with 5 years experience."
        jd_path = tmp_path / "jd.txt"
        jd_path.write_text(jd_content, encoding="utf-8")
        
        result = read_jd_file(str(jd_path))
        
        assert result == jd_content

    def test_read_jd_file_with_whitespace(self, tmp_path):
        """Test that whitespace is stripped from the content."""
        jd_content = "   Python developer needed.   \n\n"
        jd_path = tmp_path / "jd.txt"
        jd_path.write_text(jd_content, encoding="utf-8")
        
        result = read_jd_file(str(jd_path))
        
        assert result == jd_content.strip()

    def test_read_jd_file_unicode(self, tmp_path):
        """Test reading file with unicode characters."""
        jd_content = "Developer needed: Python, 日本語, émojis 🚀"
        jd_path = tmp_path / "jd.txt"
        jd_path.write_text(jd_content, encoding="utf-8")
        
        result = read_jd_file(str(jd_path))
        
        assert result == jd_content

    def test_read_jd_file_multiline(self, tmp_path):
        """Test reading multiline job description."""
        jd_content = """We are looking for a developer.
        
Requirements:
- Python
- JavaScript
- SQL"""
        jd_path = tmp_path / "jd.txt"
        jd_path.write_text(jd_content, encoding="utf-8")
        
        result = read_jd_file(str(jd_path))
        
        assert "Python" in result
        assert "JavaScript" in result

    def test_read_jd_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            read_jd_file("/nonexistent/path/jd.txt")

    def test_read_jd_file_empty_file(self, tmp_path):
        """Test reading an empty file."""
        jd_path = tmp_path / "empty.txt"
        jd_path.write_text("", encoding="utf-8")
        
        result = read_jd_file(str(jd_path))
        
        assert result == ""
