"""CodeAct Agent Graph Compilation"""

from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import RetryPolicy

from .codeact_agent import CodeActAgent


def compile_codeact_graph() -> CompiledStateGraph:
    """Compile the CodeAct graph for LangGraph Studio"""
    
    # Create model (will use environment variables for API key)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Create agent with session-based workspaces
    agent = CodeActAgent(model, "studio_workspace")
    
    # Return the compiled graph (session contexts created dynamically)
    return agent.graph