import os
import re

from src.tools.file_reader_tool import read_jd_file
from src.tools.github_tool import validate_username
from src.utils import config
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
    jd_value = st.text_area("", value=jd_text, height=500, label_visibility="collapsed")

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
    username = st.text_input("GitHub User Name: (Suppose the profile url is https://github.com/techbrij then user name is techbrij)", value=github_username, help="Suppose the profile url is https://github.com/techbrij then user name is techbrij")
    
    if st.button("🔍 Analyze Profile"):
        if not username:
            st.error("Please enter a GitHub user name")
        elif not validate_username(username):
            st.error("Please enter a valid GitHub user name.") 
        else:
            with st.spinner("Running multi-agent analysis..."):
                logger.info(f"Processing started for user {username} from UI")
                try:
                    result = run_workflow(
                        github_username=github_username,
                        jd_path='',
                        jd_text=jd_text                        
                    ) 

                    # Convert output to Markdown for better formatting and visualization
                    markdowns = []
                    markdowns.append('**Evaluation Report:**')     
                    output = result['report'].split("\n")
                    for line in output:
                        if ('- Result -' in line):
                            markdowns.append('#### Result')
                        elif ': ' in line:
                            markdowns.append('- **' + line.replace(': ', ':** '))
                        elif "Candidate's open-source" in line:
                            result = re.sub(r'(\d+(?:\.\d+)?%)', r'<span style="font-size:1.5em; font-weight:bold;">\1</span>', line)
                            markdowns.append(result)
                        else:
                            markdowns.append(line)

                    st.markdown('\n'.join(markdowns), unsafe_allow_html=True)
                    logger.info("Processing completed on UI")

                except Exception as e:
                    logger.error(f"UI error: {e}")
                    st.error(
                        "An error occurred while analyzing the repository. "
                        "Please check your configuration and try again."
                    )

# Footer
st.markdown("---")
st.caption("Made by [TechBrij](https://github.com/techbrij) as part of the Agentic AI Developer Certification (AAIDC- Module 3). ", text_alignment="center")