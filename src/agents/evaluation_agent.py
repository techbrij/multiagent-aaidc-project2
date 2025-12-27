"""
Agent: Evaluation & Report
- Compares JD and GitHub analysis
- Scores match and generates a report
"""

from src.graph.state import AppState
from src.tools.processing_tool import calculate_advanced_score, calculate_commit_score, calculate_overall_score, calculate_repo_match_score



def generate_report(overall_score: float, matched_skills: str, total_relevant_repos: int, total_active_repos: int) -> str: 
    """
    Generates a human-readable evaluation report based on the overall score and repository analysis.

    Args:
        overall_score (float): The overall match score between candidate and job description.
        matched_skills (str): Description of matched skills.
        total_relevant_repos (int): Number of relevant repositories found.
        total_active_repos (int): Number of active repositories in the last year.

    Returns:
        str: A formatted evaluation report string.
    """   

    lines = [
         f"Found {total_relevant_repos} relevant repositories. ",
        f"Tech stack match: {matched_skills}",
        f"Active repositories {total_active_repos} in last year. ",
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
    return '\n'.join(lines)


def evaluation_agent_node(state: AppState):
    """
    Evaluates the candidate's GitHub public profile against the job description and updates the state with evaluation results.

    Args:
        state (AppState): The application state containing all relevant analysis data.

    Returns:
        Updates the state object in place with evaluation results and report.
    """
    
    skill_score, matched_skills = calculate_repo_match_score(state.jd_skills, state.repos_info)
    commit_score = calculate_commit_score(state.commit_info)
    advanced_score = calculate_advanced_score(state.repos_info)

    overall_score = calculate_overall_score(skill_score, commit_score, advanced_score)

    total_relevant_repos = len(state.repos_info)
    total_active_repos = len(state.commit_info)

    report = generate_report(overall_score, matched_skills, total_relevant_repos, total_active_repos)

    state.score = overall_score
    state.report = report
    return state
