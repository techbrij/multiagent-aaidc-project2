# Performance tests for the workflow

import time
import pytest
from src.graph.workflow import build_app_graph
from src.graph.state import AppState


class TestPerformance:
    """Performance tests for the multi-agent workflow."""

    @pytest.mark.integration
    def test_workflow_step_timings(self):
        """
        Measures the time taken for each step (agent) in the LangGraph workflow.
        Prints timing for each step and asserts each is under a reasonable threshold.
        """
        # Example state setup (adjust as needed)
        github_users = ["techbrij", "psf", "ytdl-org", "httpie", "Textualize", "StephenCleary"]
        github_username = github_users[0]
        print(f"\nGitHub Username: {github_username}\n")
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

    @pytest.mark.integration
    def test_graph_build_time(self):
        """Test that graph building is fast."""
        start = time.perf_counter()
        graph = build_app_graph()
        end = time.perf_counter()
        
        build_time = end - start
        print(f"\nGraph build time: {build_time:.4f} seconds")
        
        # Graph should build in under 1 second
        assert build_time < 1.0, f"Graph building took too long: {build_time:.4f}s"

    @pytest.mark.integration
    def test_multiple_workflow_runs(self):
        """Test running workflow multiple times for consistency."""
        github_username = "octocat"
        jd_path = "data/job-description.txt"
        
        scores = []
        for i in range(2):  # Run twice to check consistency
            graph = build_app_graph()
            state = AppState(
                github_username=github_username,
                jd_path=jd_path,
                jd_text="Python and JavaScript developer needed."
            )
            
            final_state = None
            for event in graph.stream(state, config={"recursion_limit": 100}):
                if isinstance(event, dict):
                    for key in event:
                        if event[key] and isinstance(event[key], dict):
                            if 'score' in event[key]:
                                final_state = event[key]
            
            if final_state:
                scores.append(final_state.get('score', 0))
        
        # Scores should be relatively consistent (within 10%)
        if len(scores) == 2:
            diff = abs(scores[0] - scores[1])
            print(f"\nScore difference between runs: {diff:.4f}")
            assert diff < 0.1, f"Scores differ too much: {scores}"
