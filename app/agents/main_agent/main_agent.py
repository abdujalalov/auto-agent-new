from app.agents.main_agent.main_graph import compile_main_graph
import logging
import traceback
from typing import Dict, Any, AsyncGenerator


class MainAgent:
    def __init__(self, send_message=None):
        self.graph  = compile_main_graph()
        self.send_message = send_message

    async def async_stream(
        self, initial_state: Dict[str, Any], recursion_limit: int = 40
    ) -> AsyncGenerator[Dict[str, Any], None]:
        logging.info("Initial state", initial_state)
        limit = {"recursion_limit": recursion_limit}
        try:
            async for event in self.graph.astream(initial_state, limit):
                yield event

        except Exception as e:
            error_message = f"Error in research agent: {str(e)}"
            logging.error(f"Error in run_async: {traceback.format_exc()}")
            yield {"type": "event", "data": error_message}