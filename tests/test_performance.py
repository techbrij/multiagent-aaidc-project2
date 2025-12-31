import time
import pytest
from src.graph.workflow import build_app_graph
from src.graph.state import AppState

def test_workflow_step_timings():
    """
    Measures the time taken for each step (agent) in the LangGraph workflow.
    Prints timing for each step and asserts each is under a reasonable threshold.
    """
    # Example state setup (adjust as needed)
    github_users = ["techbrij", "psf", "ytdl-org", "httpie", "Textualize", "StephenCleary"]
    github_username = github_users[0]
    print (f"\nGitHub Username: {github_username}\n")
    jd_path = "data/job-description.txt"    
    
    graph = build_app_graph()
    timings = {}
    state = AppState(github_username=github_username, jd_path=jd_path)
    last_time = time.perf_counter()
    prev_node = None

    # Use graph.stream to iterate over each step/event
    def extract_node(event):
        # LangGraph events may be dicts or objects; try both
        if isinstance(event, dict):
            return event.get('name') or event.get('node') or next(iter(event.keys()))
        # Some LangGraph versions use .name, some .node
        return getattr(event, 'name', None) or getattr(event, 'node', None)

    for event in graph.stream(state, config={"recursion_limit": 100}):
        node = extract_node(event)
        now = time.perf_counter()
        # Only record timing for actual agent steps (not system/END events)
        if node and node not in ("__start__", "__end__", "END", None):
            if prev_node is not None:
                timings[prev_node] = now - last_time
            last_time = now
            prev_node = node
    # Capture timing for the last node
    if prev_node is not None:
        timings[prev_node] = time.perf_counter() - last_time

    final_state = event.get(node)
    if final_state:
        print(final_state.get('report'))        

    for node, t in timings.items():
        print(f"{node}: {t:.4f} seconds")
        assert t < 30, f"Step {node} took too long!"
