import pytest
from src.tools.file_reader_tool import read_jd_file
import os

def test_read_jd_file(tmp_path):
    jd_content = "Python developer needed."
    jd_path = tmp_path / "jd.txt"
    jd_path.write_text(jd_content, encoding="utf-8")
    result = read_jd_file(str(jd_path))
    assert result == jd_content
