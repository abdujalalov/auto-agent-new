"""
CodeAct Agent Implementation using LangGraph

Implements Thought-Code-Observation cycle with persistent execution context.
"""

import re
from typing import Any, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, RetryPolicy
from langfuse.langchain import CallbackHandler

from .execution_context import ExecutionContext
from .schemas import CodeActState, CodeActConfig
from .prompts import CODEACT_SYSTEM


class CodeActAgent:
    """CodeAct Agent using LangGraph for autonomous code execution"""
    
    def __init__(self, model, base_workspace_dir: str = "agent_workspace"):
        self.model = model
        self.base_workspace_dir = base_workspace_dir
        # Use the proper system prompt that includes framework document instructions
        system_prompt = CODEACT_SYSTEM

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{messages}")
        ])
        self.graph = self._create_graph()
    
    def _create_graph(self) -> CompiledStateGraph:
        """Create the LangGraph StateGraph for CodeAct cycle"""
        
        def agent_node(state: CodeActState, config: RunnableConfig) -> Command:
            """Agent reasoning and code generation node"""
            
            # Prepare messages with framework context if provided
            messages = state.messages.copy()
            
            # Add index document context if provided
            if state.index_document_path:
                # Convert to absolute path for the agent since execution context changes working directory
                from pathlib import Path
                abs_framework_path = Path(state.index_document_path).resolve()
                
                framework_context = f"\n\n**Framework Document Available**: {abs_framework_path}\n" \
                                  f"Read this document to understand the methodology you should follow."
                
                # Add framework context to the conversation
                if messages and hasattr(messages[-1], 'content'):
                    # Append to the last human message if it exists
                    last_msg = messages[-1]
                    if hasattr(last_msg, 'content'):
                        from langchain_core.messages import HumanMessage
                        enhanced_content = last_msg.content + framework_context
                        messages[-1] = HumanMessage(content=enhanced_content)
            
            # Use prompt template to format messages
            formatted_prompt = self.prompt_template.format_messages(
                messages=messages
            )
            
            # Get model response
            response = self.model.invoke(formatted_prompt)
            
            # Extract code blocks from response
            code = self._extract_code_blocks(response.content)
            
            if code:
                # If code found, go to execution
                return Command(
                    goto="execution",
                    update={
                        "messages": [AIMessage(content=response.content)],
                        "script": code
                    }
                )
            else:
                # No code, end the cycle
                return Command(
                    goto=END,
                    update={
                        "messages": [AIMessage(content=response.content)],
                        "script": None
                    }
                )
        
        def execution_node(state: CodeActState, config: RunnableConfig) -> Dict[str, Any]:
            """Code execution node with persistent context"""
            
            if not state.script:
                return {"messages": []}
            
            # Get session-based workspace
            execution_context = self._get_session_context(config, state.index_document_path)
            
            # Execute code in persistent context
            output, new_context = execution_context.execute_code(
                state.script,
                state.context
            )
            
            # Update state with execution results
            observation_msg = HumanMessage(
                content=f"Observation: {output}"
            )
            
            return {
                "messages": [observation_msg],
                "context": new_context
            }
        
        # Build the graph with config schema
        graph = StateGraph(state_schema=CodeActState, config_schema=CodeActConfig)
        retry_policy = RetryPolicy(max_attempts=3)
        
        graph.add_node("agent", agent_node, retry=retry_policy)
        graph.add_node("execution", execution_node, retry=retry_policy)
        
        # Add edges - the agent node uses Command routing
        # so we don't need to define outgoing edges for it
        graph.set_entry_point("agent")
        graph.add_edge("execution", "agent")
        
        # Compile the graph (callbacks disabled for testing)
        # langfuse_handler = CallbackHandler()
        compiled_graph = graph.compile()
        # compiled_graph = graph.compile().with_config({"callbacks": [langfuse_handler]})

        return compiled_graph
    
    def _get_session_context(self, config: RunnableConfig, index_document_path: str = None) -> ExecutionContext:
        """Get or create session-based execution context"""
        configurable = config.get("configurable", {})
        
        # Get session identifier (thread_id from LangGraph Studio or custom session_id)
        session_id = (
            configurable.get("thread_id") or 
            configurable.get("session_id") or 
            "default"
        )
        
        # Get user identifier for multi-user support
        user_id = configurable.get("user_id", "anonymous")
        
        # Get custom workspace name
        workspace_name = configurable.get("workspace_name")
        
        # Create session-specific workspace directory
        if workspace_name:
            workspace_dir = f"{self.base_workspace_dir}/{workspace_name}"
        else:
            workspace_dir = f"{self.base_workspace_dir}/{user_id}_{session_id}"
        
        # Return execution context for this session
        return ExecutionContext(workspace_dir, index_document_path)
    
    def _extract_code_blocks(self, content: str) -> Optional[str]:
        """Extract and combine Python code blocks from agent response"""
        
        # Pattern to match ```python code blocks
        pattern = r'```python\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            # Combine all code blocks
            combined_code = '\n\n'.join(matches)
            return combined_code
        
        # Also try generic ``` blocks
        pattern = r'```\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            # Check if it looks like Python code
            combined_code = '\n\n'.join(matches)
            if any(keyword in combined_code for keyword in ['import', 'def', 'print', '=']):
                return combined_code
        
        return None
    
    def run(self, task: str, framework_document_path: str = None, config: Dict[str, Any] = None, recursion_limit: int = 5) -> Dict[str, Any]:
        """Run the CodeAct agent on a task"""
        
        # Merge recursion limit with provided config
        run_config = {"recursion_limit": recursion_limit}
        if config:
            run_config.update(config)
        
        # Get session context for initial state
        session_context = self._get_session_context({"configurable": run_config.get("configurable", {})}, framework_document_path)
        
        initial_state = CodeActState(
            messages=[HumanMessage(content=task)],
            script=None,
            context=session_context.get_context(),
            framework_document_path=framework_document_path,
            current_task=task,
            report_sections=[]
        )
        
        # Run the graph with session-aware configuration
        final_state = self.graph.invoke(initial_state, config=run_config)
        
        return {
            "messages": final_state["messages"],
            "context": final_state["context"],
            "final_state": final_state
        }


def create_codeact_agent(model, base_workspace_dir: str = "agent_workspace") -> CodeActAgent:
    """Factory function to create a CodeAct agent"""
    return CodeActAgent(model, base_workspace_dir)