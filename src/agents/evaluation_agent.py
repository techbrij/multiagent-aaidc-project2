"""
Agent: Evaluation & Report
- Compares JD and GitHub analysis
- Scores match and generates a report
"""
from typing import Dict

EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR = 15

def generate_score_and_report(jd_skills: Dict, gh_analysis: Dict) -> tuple[float, str]:

    jd_stack = set(jd_skills)
    gh_stack = set(lang.lower() for repo in gh_analysis for lang in repo.get('languages', []))
    # Simple overlap score
    if not jd_stack:
        return 0.0
    overlap = jd_stack & gh_stack

    skill_score = len(overlap) / len(jd_stack)    

    total_commits = sum(r["commit_count_1y"] for r in gh_analysis)
    commit_score =  min(total_commits/EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR, 1.0)

    overall_score = (skill_score + commit_score) / 2

    lines = [
         f"Found {len(gh_analysis)} relevant repositories. "
        f"Tech stack match: {jd_stack} vs {gh_stack}",
        f"Active development with {total_commits} commits in last year. "
        f"Score: {overall_score:.2f}",
        "\n--- Human-Readable Evaluation ---",
        f"Candidate's open-source work matches {overall_score*100:.1f}% of the required tech stack.",
    ]
    if overall_score > 0.8:
        lines.append("Excellent match. Strong signals of seniority and activity.")
    elif overall_score > 0.5:
        lines.append("Good match. Some seniority/activity signals present.")
    else:
        lines.append("Partial match. Consider more relevant contributions or signals.")
    return (overall_score, '\n'.join(lines))


def evaluation_agent_node(state):
    jd_skills = state.jd_skills
    gh_analysis = state.gh_analysis
    score, report = generate_score_and_report(jd_skills, gh_analysis)
    state.score = score
    state.report = report
    return state