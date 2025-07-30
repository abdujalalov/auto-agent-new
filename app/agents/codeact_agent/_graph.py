"""For LangGraph Studio Compatibility"""
from app.agents.codeact_agent.codeact_graph import compile_codeact_graph

graph = compile_codeact_graph()

__all__ = ["graph"]