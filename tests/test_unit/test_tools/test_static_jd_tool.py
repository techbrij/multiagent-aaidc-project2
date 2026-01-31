# Tests for static_jd_tool.py

import pytest
from src.tools.static_jd_tool import extract_skills, static_analyze_jd


class TestExtractSkills:
    """Tests for extract_skills function."""

    def test_extract_single_skill(self):
        """Test extracting a single skill."""
        jd_text = "We need a Python developer."
        
        result = extract_skills(jd_text)
        
        assert len(result['tech_stack']) == 1
        assert result['tech_stack'][0]['language'] == 'python'
        assert result['tech_stack'][0]['weight'] == 1.0

    def test_extract_multiple_skills(self):
        """Test extracting multiple skills with equal weights."""
        jd_text = "We need expertise in Python, JavaScript, and Go."
        
        result = extract_skills(jd_text)
        
        languages = [item['language'] for item in result['tech_stack']]
        assert 'python' in languages
        assert 'javascript' in languages
        assert 'go' in languages
        assert len(result['tech_stack']) == 3
        # Weights should sum to 1.0
        total_weight = sum(item['weight'] for item in result['tech_stack'])
        assert abs(total_weight - 1.0) < 1e-6

    def test_extract_case_insensitive(self):
        """Test that skill extraction is case insensitive."""
        jd_text = "We need PYTHON and JAVASCRIPT developers."
        
        result = extract_skills(jd_text)
        
        languages = [item['language'] for item in result['tech_stack']]
        assert 'python' in languages
        assert 'javascript' in languages

    def test_extract_with_punctuation(self):
        """Test that skills are extracted from text with punctuation."""
        jd_text = "Requirements: Python, JavaScript. Also Go as well."
        
        result = extract_skills(jd_text)
        
        languages = [item['language'] for item in result['tech_stack']]
        assert 'python' in languages
        assert 'javascript' in languages
        assert 'go' in languages

    def test_extract_no_skills(self):
        """Test with no recognized technical skills."""
        jd_text = "We are looking for a great communicator."
        
        result = extract_skills(jd_text)
        
        assert result['tech_stack'] == []

    def test_extract_cpp(self):
        """Test extracting C++ skill."""
        jd_text = "Looking for C++ developer."
        
        result = extract_skills(jd_text)
        
        languages = [item['language'] for item in result['tech_stack']]
        assert 'c++' in languages

    def test_extract_csharp(self):
        """Test extracting C# skill."""
        jd_text = "Experience with C# required."
        
        result = extract_skills(jd_text)
        
        languages = [item['language'] for item in result['tech_stack']]
        assert 'c#' in languages

    def test_extract_source_is_manual(self):
        """Test that all extracted skills have source='manual'."""
        jd_text = "Python and JavaScript needed."
        
        result = extract_skills(jd_text)
        
        for item in result['tech_stack']:
            assert item['source'] == 'manual'

    def test_extract_many_skills(self):
        """Test extracting many programming languages."""
        jd_text = "Expert in Python, Java, JavaScript, TypeScript, Go, Rust, Ruby, Swift, Kotlin."
        
        result = extract_skills(jd_text)
        
        assert len(result['tech_stack']) >= 7
        # Weights should still sum to 1.0
        total_weight = sum(item['weight'] for item in result['tech_stack'])
        assert abs(total_weight - 1.0) < 1e-6


class TestStaticAnalyzeJd:
    """Tests for static_analyze_jd function."""

    def test_analyze_with_skills(self):
        """Test static analysis with recognized skills."""
        jd_text = "We need a Python and JavaScript developer."
        
        result = static_analyze_jd(jd_text)
        
        assert 'tech_stack' in result
        languages = [item['language'] for item in result['tech_stack']]
        assert 'python' in languages
        assert 'javascript' in languages

    def test_analyze_empty_text(self):
        """Test static analysis with no skills."""
        jd_text = "No technical skills mentioned here."
        
        result = static_analyze_jd(jd_text)
        
        assert result['tech_stack'] == []

    def test_analyze_returns_dict(self):
        """Test that static_analyze_jd returns a dictionary."""
        jd_text = "Python developer needed."
        
        result = static_analyze_jd(jd_text)
        
        assert isinstance(result, dict)

    def test_analyze_preserves_extract_skills_output(self):
        """Test that static_analyze_jd wraps extract_skills correctly."""
        jd_text = "Looking for Go and Rust experts."
        
        extract_result = extract_skills(jd_text)
        analyze_result = static_analyze_jd(jd_text)
        
        assert extract_result == analyze_result
