"""
GitHub Profile Evaluator
- Uses LangGraph for orchestration
- 3+ agents: JD Analyzer, GitHub Analyzer, Evaluation/Report
- CLI for GitHub username
"""

import os

from src.graph.workflow import run_workflow

def main():
    print("="*50 + "\nJD-Driven Agentic GitHub Profile Evaluator\n" + "="*50)

    github_username = input("Enter GitHub username: ")
    
    jd_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job-description.txt')
    
    final_state = run_workflow(github_username, jd_path)
   
    print("\n=== Evaluation Report ===\n")
    print(final_state['report'])

if __name__ == "__main__":
    main()
