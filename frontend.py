import os
import re

from src.tools.file_reader_tool import read_jd_file
from src.tools.github_tool import validate_username
from src.utils import config
from src.utils.common import sanitize_text
from src.utils.logger import logger
import streamlit as st
from dotenv import load_dotenv

from src.graph.workflow import run_workflow


# Load environment variables 
load_dotenv()

jd_path = os.path.join(os.path.dirname(__file__), 'data', 'job-description.txt')
jd_text = read_jd_file(jd_path)

st.set_page_config(
    page_title="JD-Driven Agentic GitHub Profile Evaluator",
    layout="wide",
)

st.markdown("""
<style>
    /* Remove top padding */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("JD-Driven Agentic GitHub Profile Evaluator ")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Job Description")
    jd_value = st.text_area("job description", value=jd_text, height=500, label_visibility="collapsed")

with col2:

    config_info = f"""
                #### Configuration
                - **LLM Model:** llama-3.1-8b-instant
                - **Expected minimum commits in last year:** {config.get_min_commits()}
                - **Max repos to fetch:** {config.get_max_repos()}
                """
    
    st.markdown(config_info)
    st.info("If you want to change configuration, please update .env file and rerun the application")

    github_username = "techbrij"
    username = st.text_input(
        "GitHub User Name: (Suppose the profile url is https://github.com/techbrij then user name is techbrij)",
        value=github_username,
        help="Suppose the profile url is https://github.com/techbrij then user name is techbrij"
    )

    if st.button("🔍 Analyze Profile"):
        username = username.strip()
        jd_value_sanitized = sanitize_text(jd_value)
        error_message = None
        # Security: enforce max length limits
        MAX_USERNAME_LEN = 39
        MAX_JD_LEN = 5000
        try:
            if not username:
                error_message = "Please enter a GitHub user name"
            elif len(username) > MAX_USERNAME_LEN:
                logger.warning(f"Blocked username over max length: {username}")
                error_message = f"GitHub username too long (max {MAX_USERNAME_LEN} characters)."
            elif not validate_username(username):
                error_message = "Please enter a valid GitHub user name. Usernames must be 1-39 characters, alphanumeric or hyphens, no leading/trailing/consecutive hyphens."
            elif not jd_value_sanitized or len(jd_value_sanitized) < 10:
                error_message = "Job description is empty or too short. Please provide a valid job description."
            elif len(jd_value_sanitized) > MAX_JD_LEN:
                logger.warning("Blocked JD over max length.")
                error_message = f"Job description too long (max {MAX_JD_LEN} characters)."
            if error_message:
                st.error(error_message)
            else:
                with st.spinner("Running multi-agent analysis..."):
                    logger.info(f"Processing started for user {username} from UI")
                    try:
                        result = run_workflow(
                            github_username=username,
                            jd_path='',
                            jd_text=jd_value_sanitized
                        )
                    except Exception as e:
                        logger.error(f"Workflow execution error: {e}")
                        raise
                        
                    if result:
                        # Output validation
                        report = result.get('report', '')
                        score = result.get('score', None)
                        if not isinstance(report, str) or not report.strip():
                            logger.error("Output validation failed: report is missing or not a string.")
                            st.error("Internal error: Evaluation report is missing or invalid.")
                            
                        if not isinstance(score, float) or not (0.0 <= score <= 1.0):
                            logger.error(f"Output validation failed: score is invalid ({score}).")
                            st.error("Internal error: Score is missing or out of range.")
                            
                    

                        markdowns = []
                        markdowns.append('**Evaluation Report:**')
                        output_lines = report.split("\n")
                        for line in output_lines:
                            if ('- Result -' in line):
                                markdowns.append('#### Result')
                            elif ': ' in line:
                                markdowns.append('- **' + line.replace(': ', ':** '))
                            elif "Candidate's open-source" in line:
                                result_line = re.sub(r'(\d+(?:\.\d+)?%)', r'<span style="font-size:1.5em; font-weight:bold;">\1</span>', line)
                                markdowns.append(result_line)
                            else:
                                markdowns.append(line)

                        st.markdown('\n'.join(markdowns), unsafe_allow_html=True)
                    logger.info("Processing completed on UI")
        except Exception as e:
            logger.error(f"UI error: {e}")
            if "Toxicity" in str(e):
                st.error(f"{str(e)} Please check the provided Job description.")
            else:
                st.error("An unexpected error occurred. Please try again or contact support.")

# Footer
st.markdown("---")
st.caption("Made by [TechBrij](https://github.com/techbrij) as part of the Agentic AI Developer Certification (AAIDC- Module 3). ", text_alignment="center")