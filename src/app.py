"""
GitHub Profile Evaluator
- Uses LangGraph for orchestration
- 3+ agents: JD Analyzer, GitHub Analyzer, Evaluation/Report
- CLI for GitHub username
"""

import os
import sys

from src.graph.workflow import run_workflow
from src.tools.github_tool import validate_username
from src.utils.logger import logger

def main():
    print("="*50 + "\nJD-Driven Agentic GitHub Profile Evaluator\n" + "="*50)


    while True:
        github_username = input("Enter GitHub username: ").strip()
        if not validate_username(github_username):
            print("Invalid GitHub username. Usernames must be 1-39 characters, alphanumeric or hyphens, no leading/trailing/consecutive hyphens.")
            continue
        break

    try:
        jd_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job-description.txt')

        logger.info(f"Processing started for user {github_username}")

        final_state = run_workflow(github_username, jd_path, '')

        # Output validation
        report = final_state.get('report', '')
        score = final_state.get('score', None)
        if not isinstance(report, str) or not report.strip():
            logger.error("Output validation failed: report is missing or not a string.")
            print("Internal error: Evaluation report is missing or invalid.")
            sys.exit(1)
        if not isinstance(score, float) or not (0.0 <= score <= 1.0):
            logger.error(f"Output validation failed: score is invalid ({score}).")
            print("Internal error: Score is missing or out of range.")
            sys.exit(1)

        print("\n=== Evaluation Report ===\n")
        print(report)
        logger.info("Processing completed")

    except KeyboardInterrupt:
        print("\n\n  Processing cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print("Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
