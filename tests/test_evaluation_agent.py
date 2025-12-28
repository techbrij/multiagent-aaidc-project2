import pytest
from src.graph.state import JDLanguageInfo, MatchRepoInfo, CommitInfo, AppState
from src.agents.evaluation_agent import generate_report

def test_generate_report_scores():
    report = generate_report(0.9, "Python, Go", 3, 2)
    assert "Excellent match" in report
    report = generate_report(0.6, "Python", 2, 1)
    assert "Good match" in report
    report = generate_report(0.3, "Go", 1, 0)
    assert "Partial match" in report
