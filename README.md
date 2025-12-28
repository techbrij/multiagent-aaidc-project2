
# JD-Driven Agentic GitHub Profile Evaluator: AAIDC Project2

## Overview

This project evaluates a candidate's public GitHub profile against a provided job description using a multi-agent workflow orchestrated by LangGraph. It analyzes tech stack compatibility, repository activity, and generates a human-readable evaluation report.

**Key Features:**
- Multi-agent orchestration (JD Analyzer, GitHub Repo Analyzer, Activity Analyzer, Evaluation/Report)
- Automated extraction of required skills from job descriptions
- GitHub repo and profile analysis (tech stack, activity)
- Scoring and reporting of candidate-job fit
- Extensible agent and tool architecture

## Architecture & Workflow

The workflow consists of the following agents:

1. **JD Analyzer Agent**: Extracts required programming languages and skills from the job description (LLM with static analysis fallback).
2. **Repo Match Agent**: Matches candidate's GitHub repositories to required skills.
3. **Activity Agent**: Analyzes repository activity (commits in the last year).
4. **Evaluation Agent**: Scores the match and generates a report.

The workflow is orchestrated using LangGraph:
```
JD Analyzer → Repo Match → Activity → Evaluation → Report
```

## Setup & Installation

1. **Clone the repository**
   ```
   git clone <repo-url>
   cd multiagent-aaidc-project2
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
   - Copy `.env.example` to `.env` and set your API keys (Groq)
   - Example:
     ```
     GROQ_API_KEY=your_groq_api_key
     GROQ_MODEL=llama-3.1-8b-instant
     ```

## Usage

Run the main application:
```
python -m src.app
```
You can modify job description path in `src/app.py`.

## Agents & Tools

### Agents

| Agent Name            | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| JD Analyzer Agent     | Extracts programming languages and skills from job description using LLM with static analysis fallback. |
| Repo Match Agent      | Matches GitHub repositories to required skills.                             |
| Activity Agent        | Analyzes commit activity in relevant repositories.                          |
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

## Configuration

- `.env` file for API keys and model selection
- `data/job-description.txt`: Example job description file
- `src/app.py`: Main entry point

## Example Job Description

See `data/job-description.txt` for a sample JD used in evaluation.

## Output

The application prints a detailed evaluation report, including:
- Number of relevant repositories
- Tech stack match
- Active repositories in last year
- Overall score and match percentage
- Human-readable summary

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

MIT License (see LICENSE file)

## Contact

For questions or support, contact the project maintainer.

## TODO / Future Improvements

- Add more criteria for better scoring
- Add support for more advanced JD parsing (NLP, entity extraction)
- Add web UI for interactive usage
- Improve error handling and logging

