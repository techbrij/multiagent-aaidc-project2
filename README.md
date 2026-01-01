
# JD-Driven Agentic GitHub Profile Evaluator: AAIDC Project2

## Overview

This project evaluates a candidate's public GitHub profile against a provided job description using a multi-agent workflow orchestrated by LangGraph. It analyzes tech stack compatibility, repository activity, and generates a human-readable evaluation report.

## What the system does

Technical hiring often requires manual screening of candidates' open-source contributions to assess their fit for a role. This project automates the process by combining:

- Job description parsing (LLM with static analysis fallback)
- GitHub profile, public repository, activity and advanced analysis
- Multi-agent orchestration (LangGraph)
- Automated scoring and reporting

## Target Audience
AI/ML Practitioners, Engineering team, Hiring Managers and recruiters who want to automate GitHub public profile screening against a job description.

## Features
- Multi-agent orchestration (JD Analyzer, GitHub Repo Analyzer, Activity Analyzer, Evaluation/Report)
- Automated extraction of required skills from job descriptions
- GitHub repo and profile analysis (tech stack, activity)
- Scoring and reporting of candidate-job fit
- Extensible agent and tool architecture

## Architecture & Workflow

![Mutli-agent Architecture](https://github.com/techbrij/multiagent-aaidc-project2/blob/main/images/rt-multiagent-architecture-flow.png?raw=true)

## Technical Stack

- Language: Python 
- Agent Orchestration: LangGraph
- LLM Integration: Configurable via environment variables (Groq)
- GitHub API integration 

### Agents

| Agent Name            | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| JD Analyzer Agent     | Extracts programming languages and skills from job description using LLM with static analysis fallback. |
| Repo Match Agent      | Matches GitHub repositories to required skills.                             |
| Activity Agent        | Analyzes commit activity in relevant repositories in last year.                          |
| Evaluation Agent      | Scores and generates a human-readable report.                               |

### Tools

| Tool Name           | File                  | Description                                              |
|---------------------|-----------------------|----------------------------------------------------------|
| GitHub Tool         | github_tool.py        | Fetches GitHub profile, repositories, and commit counts. |
| File Reader Tool    | file_reader_tool.py   | Reads job description file.                              |
| Static JD Tool      | static_jd_tool.py     | Static extraction of skills from JD.                     |
| Processing Tool     | processing_tool.py    | Skill normalization, repo matching, scoring logic.       |
| Config              | config.py             | Loads LLM and configuration from environment.            |
| Retry Utility       | retry.py              | Robust retry logic for API calls.                        |


## Setup & Installation

### Prerequisites and Requirements

- Python 3.9+
- Internet access for GitHub API
- Groq API key for LLM (if using LLM-based JD analysis)
- pytest for running tests

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/techbrij/multiagent-aaidc-project2
   cd multiagent-aidc-project2
   ```
2. **Create Virtual Environment**
   ```
   python -m venv venv
   ```
3. **Activate the virtual environment**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env` and set your API keys (Groq) and other configuration parameters
   - Example:
     ```
     GROQ_API_KEY=your_groq_api_key
     GROQ_MODEL=llama-3.1-8b-instant

     # Activity criteria
     EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR=20

     # Maximum number of repositories to fetch
     MAX_REPOS_TO_FETCH = 50

     ```
   EXPECTED_MIN_COMMITS_IN_LAST_ONE_YEAR: this parameters is used in activity criteria how many commits are expected for the provided JD.
   MAX_REPOS_TO_FETCH: To control GitHub API call, this is used. 

   These configuration parameters should be tuned based on the JD and GitHub users.


## Usage

You can put your JD file in data folder and modify the path in `src/app.py` OR overwrite `data/job-description.txt` file.

Run the main application:
```
python -m src.app
```
It will ask for GitHub username.  Once you enter, it will process and generate the score.

### Output

The application prints a detailed evaluation report, including:
- Number of relevant repositories
- Tech stack match
- Active repositories in last year
- Overall score and match percentage
- Human-readable summary


Here is the sample output:
```
(venv) PS D:\readytensor\projects\multiagent-aaidc-project2> python -m src.app
==================================================
JD-Driven Agentic GitHub Profile Evaluator
==================================================
Enter GitHub username: techbrij
Running jd_analyzer agent
Using Groq model: llama-3.1-8b-instant
Running repo_match agent
Running activity agent
Running evaluation agent
Criteria: Minimum commits: 20

=== Evaluation Report ===

Total relevant repositories: 28
Active repositories(in last year): 2
Matched skills: ['java', 'javascript', 'python']
Score: 0.83

--- Result ---
Candidate's open-source work matches 82.5% of the required tech stack.
Excellent match.
```

## Scoring Calculations:

The final fit score is calculated in four stages, executed sequentially:

- Repository Language Match Scoring
- Activity Scoring (Relevant Repositories Only)
- Advanced Scoring
- Overall Fit Score Aggregation

**Repository Language Match Score:** LLM gives structured list of JD languages with weights. GitHub APIs gives repository information. The agent will find relevant repositories based on the JD languages. All found languages weights will be added. value: (0-1). If all languages are available, the score will be 1.

**Activity Scoring:** The agent will check how many commits in the relevant repositories in the last one year. In the configuration, minimum commits expectation is defined for the JD. If number of commits is less then the ratio will be score. If number of commits equal or greater than the expectation then it will be 1.

**Advanced Scoring:** It checks how many relevant repositories are starred and using GitHub Issues to ensure actively managed. value: (0 - 1)

**Overall Score = Repo Match Score * 0.5 + Activity Score 0.3 + Advanced Score * 0.2**

**Result:** The final result status is based on the score percentage:

| Score Range | Match Level   |
| ----------- | ------------- |
| > 80%       | Excellent     |
| 50% – 80%   | Good          |
| < 50%       | Partial Match |

**Note:** this is core implementation. Many more criteria and logics can be added to improve the quality.

## Testing

To run all tests:

```
pytest tests/ -s
```

To run the performance test:

```
pytest tests/test_performance.py -s
```

## Configuration

- `.env` file for API keys and model selection
- `data/job-description.txt`: Example job description file
- `src/app.py`: Main entry point

## Example Job Description

See `data/job-description.txt` for a sample JD used in evaluation.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

MIT License (see LICENSE file)

## Contact

Brij Mohan

- GitHub: https://github.com/techbrij

