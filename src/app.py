"""
GitHub Profile Evaluator
- Uses LangGraph for orchestration
- 3+ agents: JD Analyzer, GitHub Analyzer, Evaluation/Report
- CLI for GitHub username
"""

import os
import sys

from src.graph.workflow import run_workflow
from src.utils.logger import logger

def main():
    print("="*50 + "\nJD-Driven Agentic GitHub Profile Evaluator\n" + "="*50)

    github_username = input("Enter GitHub username: ")
    
    try:
        jd_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job-description.txt')

        logger.info(f"Processing started for user {github_username}")

        final_state = run_workflow(github_username, jd_path, '')
    
        print("\n=== Evaluation Report ===\n")
        print(final_state['report'])
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
