from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from src.agents.evaluation_agent import evaluation_agent_node
from src.agents.github_analyzer import github_agent_node
from src.agents.jd_analyzer import jd_agent_node
from src.graph.state import AppState

# ===================
# Build Graph
# ===================

def build_app_graph() -> CompiledStateGraph:
     # Build LangGraph workflow
    workflow = StateGraph(AppState)
    workflow.add_node('jd_agent', jd_agent_node)
    workflow.add_node('github_agent', github_agent_node)
    workflow.add_node('evaluation_agent', evaluation_agent_node)

    # Define edges (jd_agent -> github_agent -> evaluation_agent -> END)
    workflow.add_edge('jd_agent', 'github_agent')
    workflow.add_edge('github_agent', 'evaluation_agent')
    workflow.add_edge('evaluation_agent', END)

    # Set entry point
    workflow.set_entry_point('jd_agent')

    return workflow.compile()

def run_workflow(github_username: str, jd_path: str):
    
    graph = build_app_graph()

    # Run the workflow
    final_state = graph.invoke(AppState(github_username=github_username, jd_path=jd_path), config={"recursion_limit": 100})
    return final_state