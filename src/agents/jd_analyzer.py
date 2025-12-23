

from src.tools.jd_tool import analyze_jd


def jd_agent_node(state):
    jd_path = state.jd_path
    jd_analyze = analyze_jd(jd_path)
    state.jd_skills = jd_analyze.get('tech_stack') or []
    return state
