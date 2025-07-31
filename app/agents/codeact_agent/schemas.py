from typing import Annotated, List, Optional, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, field_validator
from pathlib import Path


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
    
    index_document_path: Optional[str] = Field(
        default=None, description="Path to the index/table of contents document that references other framework documents"
    )
    
    current_task: Optional[str] = Field(
        default=None, description="Description of the current task being executed"
    )
    
    report_sections: List[str] = Field(
        default_factory=list, description="Generated report sections and outputs"
    )
    
    @field_validator('index_document_path')
    @classmethod
    def validate_index_path(cls, v: Optional[str]) -> Optional[str]:
        """Validate that index document path exists and is accessible"""
        if v is None:
            return v
        
        try:
            # Strip whitespace (including newlines) from path
            v = v.strip()
            
            # Use Path without resolve() to avoid os.getcwd() blocking call
            path = Path(v)
            
            # Basic path validation without file system calls
            if not path.suffix.lower() in ['.md', '.txt']:
                raise ValueError(f"Index document must be a markdown or text file: {v}")
            
            # Return the cleaned path string - file existence will be checked at runtime
            return v
        except Exception as e:
            raise ValueError(f"Invalid index document path '{v}': {e}")


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