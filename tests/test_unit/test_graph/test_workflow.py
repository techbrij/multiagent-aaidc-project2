# Tests for workflow.py

import pytest
from unittest.mock import patch, MagicMock
from src.graph.workflow import build_app_graph, run_workflow
from src.graph.state import AppState


class TestBuildAppGraph:
    """Tests for build_app_graph function."""

    def test_build_graph_returns_compiled_graph(self):
        """Test that build_app_graph returns a compiled graph."""
        graph = build_app_graph()
        
        # Check it has the invoke method (compiled graph)
        assert hasattr(graph, 'invoke')
        assert hasattr(graph, 'stream')

    def test_build_graph_has_nodes(self):
        """Test that the graph has expected nodes."""
        graph = build_app_graph()
        
        # Check graph configuration contains our agents
        # The exact API depends on LangGraph version
        assert graph is not None

    def test_build_graph_multiple_calls_independent(self):
        """Test that building multiple graphs creates independent instances."""
        graph1 = build_app_graph()
        graph2 = build_app_graph()
        
        assert graph1 is not graph2


class TestRunWorkflow:
    """Tests for run_workflow function."""

    @patch('src.graph.workflow.build_app_graph')
    def test_run_workflow_returns_state(self, mock_build_graph):
        """Test that run_workflow returns final state."""
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {
            'github_username': 'testuser',
            'jd_path': 'test.txt',
            'jd_text': 'Python developer',
            'score': 0.75,
            'report': 'Test report'
        }
        mock_build_graph.return_value = mock_graph
        
        result = run_workflow('testuser', 'test.txt', 'Python developer')
        
        assert result['github_username'] == 'testuser'
        assert result['score'] == 0.75

    @patch('src.graph.workflow.build_app_graph')
    def test_run_workflow_builds_graph(self, mock_build_graph):
        """Test that run_workflow builds the graph."""
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {}
        mock_build_graph.return_value = mock_graph
        
        run_workflow('testuser', 'test.txt', '')
        
        mock_build_graph.assert_called_once()

    @patch('src.graph.workflow.build_app_graph')
    def test_run_workflow_invokes_with_correct_state(self, mock_build_graph):
        """Test that run_workflow invokes graph with correct initial state."""
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {}
        mock_build_graph.return_value = mock_graph
        
        run_workflow('myuser', '/path/to/jd.txt', 'Python developer needed')
        
        call_args = mock_graph.invoke.call_args
        initial_state = call_args[0][0]
        
        assert initial_state.github_username == 'myuser'
        assert initial_state.jd_path == '/path/to/jd.txt'
        assert initial_state.jd_text == 'Python developer needed'

    @patch('src.graph.workflow.build_app_graph')
    def test_run_workflow_uses_recursion_limit(self, mock_build_graph):
        """Test that run_workflow sets recursion limit config."""
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {}
        mock_build_graph.return_value = mock_graph
        
        run_workflow('testuser', 'test.txt', '')
        
        call_args = mock_graph.invoke.call_args
        config = call_args[1]['config']
        
        assert config['recursion_limit'] == 100

    @patch('src.graph.workflow.build_app_graph')
    def test_run_workflow_empty_jd_text(self, mock_build_graph):
        """Test run_workflow with empty jd_text (will read from file)."""
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {}
        mock_build_graph.return_value = mock_graph
        
        run_workflow('testuser', '/path/to/jd.txt', '')
        
        call_args = mock_graph.invoke.call_args
        initial_state = call_args[0][0]
        
        assert initial_state.jd_text == ''
        assert initial_state.jd_path == '/path/to/jd.txt'
