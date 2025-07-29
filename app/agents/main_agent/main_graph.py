from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import RetryPolicy

from app.agents.main_agent.nodes.chat import chat as chat_node
from app.agents.main_agent.schemas import GraphState


def create_main_graph() -> StateGraph:
    graph = StateGraph(state_schema=GraphState)
    retry_policy = RetryPolicy(max_attempts=3)

    # --- add nodes ---
    graph.add_node('chat', chat_node, retry=retry_policy)

    # --- add edges ---
    graph.set_entry_point('chat')
    graph.set_finish_point('chat')

    return graph


langfuse_handler = CallbackHandler()


def compile_main_graph() -> CompiledStateGraph:
    graph = create_main_graph()
    graph.name = "MainAgentGraph"
    # compiled_graph = graph.compile()
    compiled_graph = graph.compile().with_config({"callbacks": [langfuse_handler]})

    return compiled_graph
