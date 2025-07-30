from typing import Annotated, List

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import (
    BaseModel,
    Field,
)


class GraphState(BaseModel):
    """State definition for the LangGraph Agent/Workflow."""

    messages: Annotated[List[AnyMessage], add_messages] = Field(
        default_factory=list, description="The messages in the conversation"
    )

    # session_id: str = Field(..., description="The unique identifier for the conversation session")
