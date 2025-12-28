import pytest
from src.tools.processing_tool import normalize_language, is_repo_compatible_with_jd

def test_normalize_language_variants():
    assert normalize_language('Python') == 'python'
    assert normalize_language('C++') == 'c++'
    assert normalize_language('java-script') == 'javascript'
    assert normalize_language(' Go ') == 'go'

def test_is_repo_compatible_with_jd():
    repo = {'language': 'Python'}
    jd_skills = ['python', 'go']
    assert is_repo_compatible_with_jd(repo, jd_skills)
    repo = {'language': 'Ruby'}
    assert not is_repo_compatible_with_jd(repo, jd_skills)
