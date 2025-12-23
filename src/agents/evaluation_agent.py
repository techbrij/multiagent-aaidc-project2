"""
Agent: Evaluation & Report
- Compares JD and GitHub analysis
- Scores match and generates a report
"""
from typing import Dict

def compute_score(jd_skills: Dict, gh_analysis: Dict) -> float:
    jd_stack = set(jd_skills.get('tech_stack', []))
    gh_stack = set(gh_analysis.get('languages', []))
    # Simple overlap score
    if not jd_stack:
        return 0.0
    overlap = jd_stack & gh_stack
    score = len(overlap) / len(jd_stack)
    # Add bonus for seniority signals
    seniority = gh_analysis.get('seniority_signals', {})
    bonus = 0.1 * sum([seniority.get('has_tests', 0), seniority.get('has_docs', 0), seniority.get('has_issues', 0)])
    return min(score + bonus, 1.0)

def generate_report(jd_skills: Dict, gh_analysis: Dict, score: float) -> str:
    lines = [
        f"Tech stack match: {jd_skills.get('tech_stack', [])} vs {gh_analysis.get('languages', [])}",
        f"Seniority signals: {gh_analysis.get('seniority_signals', {})}",
        f"Score: {score:.2f}",
        "\n--- Human-Readable Evaluation ---",
        f"Candidate's open-source work matches {score*100:.1f}% of the required tech stack.",
    ]
    if score > 0.8:
        lines.append("Excellent match. Strong signals of seniority and activity.")
    elif score > 0.5:
        lines.append("Good match. Some seniority/activity signals present.")
    else:
        lines.append("Partial match. Consider more relevant contributions or signals.")
    return '\n'.join(lines)


def evaluation_agent_node(state):
    jd_skills = state.jd_skills
    gh_analysis = state.gh_analysis
    score = compute_score(jd_skills, gh_analysis)
    report = generate_report(jd_skills, gh_analysis, score)
    state.score = score
    state.report = report
    return state