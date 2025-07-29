"""For Langgraph Studio Compatibility"""
from app.agents.main_agent.main_graph import compile_main_graph

graph = compile_main_graph()

__all__ = ["graph"]
