# Integration test for the complete workflow

import time
import pytest
from src.graph.workflow import build_app_graph
from src.graph.state import AppState


class TestWorkflowIntegration:
    """Integration tests for the complete workflow.
    
    Note: These tests require network access and may hit real APIs.
    They should be run sparingly to avoid rate limits.
    """

    @pytest.mark.integration
    def test_workflow_step_timings(self):
        """
        Measures the time taken for each step (agent) in the LangGraph workflow.
        Prints timing for each step and asserts each is under a reasonable threshold.
        """
        # Example state setup
        github_users = ["techbrij", "psf", "ytdl-org", "httpie", "Textualize", "StephenCleary"]
        github_username = github_users[0]
        print(f"\nGitHub Username: {github_username}\n")
        jd_path = "data/job-description.txt"
        
        graph = build_app_graph()
        timings = {}
        state = AppState(github_username=github_username, jd_path=jd_path)
        last_time = time.perf_counter()
        prev_node = None

        def extract_node(event):
            """Extract node name from LangGraph event."""
            if isinstance(event, dict):
                return event.get('name') or event.get('node') or next(iter(event.keys()))
            return getattr(event, 'name', None) or getattr(event, 'node', None)

        for event in graph.stream(state, config={"recursion_limit": 100}):
            node = extract_node(event)
            now = time.perf_counter()
            # Only record timing for actual agent steps
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
    def test_workflow_produces_valid_output(self, tmp_path):
        """Test that workflow produces valid score and report."""
        # Create a test JD file
        jd_content = """
        We are looking for a Software Engineer with experience in:
        - Python
        - JavaScript
        - SQL databases
        Strong problem-solving skills required.
        """
        jd_file = tmp_path / "test_jd.txt"
        jd_file.write_text(jd_content)
        
        graph = build_app_graph()
        state = AppState(
            github_username='octocat',  # Well-known GitHub user
            jd_path=str(jd_file),
            jd_text=jd_content
        )
        
        final_state = None
        for event in graph.stream(state, config={"recursion_limit": 100}):
            # Last event contains final state
            if isinstance(event, dict):
                for key in event:
                    if event[key]:
                        final_state = event[key]
        
        assert final_state is not None
        assert 'score' in final_state
        assert 'report' in final_state
        assert isinstance(final_state['score'], float)
        assert 0.0 <= final_state['score'] <= 1.0
        assert len(final_state['report']) > 0

    @pytest.mark.integration
    def test_workflow_handles_user_with_no_matching_repos(self, tmp_path):
        """Test workflow handles user with no matching repos gracefully."""
        # JD with rare programming language
        jd_content = "We need an expert COBOL developer."
        jd_file = tmp_path / "test_jd.txt"
        jd_file.write_text(jd_content)
        
        graph = build_app_graph()
        state = AppState(
            github_username='octocat',
            jd_path=str(jd_file),
            jd_text=jd_content
        )
        
        final_state = None
        for event in graph.stream(state, config={"recursion_limit": 100}):
            if isinstance(event, dict):
                for key in event:
                    if event[key]:
                        final_state = event[key]
        
        # Should still produce output, even with 0 score
        assert final_state is not None
        assert 'score' in final_state
        assert 'report' in final_state
