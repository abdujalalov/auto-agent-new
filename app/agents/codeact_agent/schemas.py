from typing import Annotated, List, Optional, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class CodeActState(BaseModel):
    """State definition for the CodeAct Agent/Workflow."""

    messages: Annotated[List[AnyMessage], add_messages] = Field(
        default_factory=list, description="The messages in the conversation"
    )
    
    script: Optional[str] = Field(
        default=None, description="The Python code script to be executed"
    )
    
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Persistent execution context with variables and tools"
    )
    
    framework_content: Optional[str] = Field(
        default=None, description="Content of the loaded framework document"
    )
    
    current_task: Optional[str] = Field(
        default=None, description="Description of the current task being executed"
    )
    
    report_sections: List[str] = Field(
        default_factory=list, description="Generated report sections and outputs"
    )


class CodeActConfig(BaseModel):
    """Configuration schema for CodeAct Agent"""
    
    thread_id: Optional[str] = Field(
        default=None, description="Session/thread identifier for workspace isolation"
    )
    
    user_id: Optional[str] = Field(
        default=None, description="User identifier for multi-user support"
    )
    
    workspace_name: Optional[str] = Field(
        default=None, description="Custom workspace name override"
    )