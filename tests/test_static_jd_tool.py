import pytest
from src.tools.static_jd_tool import extract_skills, static_analyze_jd

def test_extract_skills_basic():
    jd_text = "We need a developer skilled in Python, JavaScript, and Go."
    result = extract_skills(jd_text)
    langs = [item['language'] for item in result['tech_stack']]
    assert 'python' in langs
    assert 'javascript' in langs
    assert 'go' in langs
    assert abs(sum(item['weight'] for item in result['tech_stack']) - 1.0) < 1e-6

def test_static_analyze_jd_empty():
    jd_text = "No tech skills mentioned."
    result = static_analyze_jd(jd_text)
    assert result['tech_stack'] == []
