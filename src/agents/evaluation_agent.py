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

    total_relevant_repos = len(gh_analysis)
    total_commits = 0
    total_open_issues_repo = 0
    total_starred_repo = 0

    for repo in gh_analysis:
        total_commits += repo["commit_count_1y"]
        total_open_issues_repo += repo["has_issues"]
        total_starred_repo += repo["stars"] > 0

    commit_score =  min(total_commits/EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR, 1.0)

    advanced_score = (total_open_issues_repo + total_starred_repo)/(2* total_relevant_repos)

    overall_score = skill_score * 0.5 + commit_score * 0.3 + advanced_score * 0.2

    lines = [
         f"Found {total_relevant_repos} relevant repositories. "
        f"Tech stack match: {jd_stack} vs {gh_stack}",
        f"Active development with {total_commits} commits in last year. "
        f"Score: {overall_score:.2f}",
        "\n--- Human-Readable Evaluation ---",
        f"Candidate's open-source work matches {overall_score*100:.1f}% of the required tech stack.",
    ]
    if overall_score > 0.8:
        lines.append("Excellent match.")
    elif overall_score > 0.5:
        lines.append("Good match.")
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