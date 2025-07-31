"""
Persistent Execution Context for CodeAct Agent

Manages Python execution environment with persistent variables and state.
"""

import sys
import io
import os
import traceback
from pathlib import Path
from typing import Any, Dict, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ExecutionContext:
    """Manages persistent Python execution environment"""
    
    def __init__(self, workspace_dir: str = None, framework_document_path: str = None):
        """Initialize execution context with data science libraries and workspace"""
        
        # Set up workspace directory
        if workspace_dir is None:
            workspace_dir = "agent_workspace"
        
        self.workspace_path = Path(workspace_dir).resolve()
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for organization
        (self.workspace_path / "data").mkdir(parents=True, exist_ok=True)
        (self.workspace_path / "outputs").mkdir(parents=True, exist_ok=True)
        (self.workspace_path / "visualizations").mkdir(parents=True, exist_ok=True)
        (self.workspace_path / "reports").mkdir(parents=True, exist_ok=True)
        
        # Change working directory to workspace
        self.original_cwd = os.getcwd()
        os.chdir(self.workspace_path)
        
        self.globals_dict = {
            # Standard libraries
            'pd': pd,
            'pandas': pd,
            'np': np,
            'numpy': np,
            'plt': plt,
            'matplotlib': plt,
            'sns': sns,
            'seaborn': sns,
            
            # Built-in functions
            'print': print,
            'len': len,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'sum': sum,
            'max': max,
            'min': min,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            
            # Common imports
            '__builtins__': __builtins__,
            
            # Workspace utilities
            'WORKSPACE_PATH': str(self.workspace_path),
            'DATA_DIR': str(self.workspace_path / "data"),
            'OUTPUT_DIR': str(self.workspace_path / "outputs"), 
            'VIZ_DIR': str(self.workspace_path / "visualizations"),
            'REPORTS_DIR': str(self.workspace_path / "reports"),
        }
        
        # Add framework document path if provided
        if framework_document_path:
            # Convert to absolute path since we're changing working directory
            abs_framework_path = Path(framework_document_path).resolve()
            self.globals_dict['FRAMEWORK_DOCUMENT_PATH'] = str(abs_framework_path)
        
        # Execution history for debugging
        self.execution_history = []
        
        # Configure matplotlib for non-interactive use
        self._configure_matplotlib()
    
    def _configure_matplotlib(self):
        """Configure matplotlib for headless execution with workspace"""
        try:
            plt.switch_backend('Agg')  # Non-interactive backend
            plt.ioff()  # Turn off interactive mode
            
            # Set default save location for plots
            plt.rcParams['savefig.directory'] = str(self.workspace_path / "visualizations")
        except Exception as e:
            print(f"Warning: Could not configure matplotlib: {e}")
    
    def execute_code(self, code: str, existing_context: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Execute Python code with persistent context
        
        Args:
            code: Python code to execute
            existing_context: Previous execution context to merge
            
        Returns:
            Tuple of (output_string, updated_context)
        """
        
        # Merge existing context
        if existing_context:
            self.globals_dict.update(existing_context)
        
        # Capture stdout
        old_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Prepare execution context (like LangGraph CodeAct reference)
        _locals = self.globals_dict.copy()
        if existing_context:
            _locals.update(existing_context)
        
        # Store original keys before execution (like LangGraph CodeAct reference)
        original_keys = set(_locals.keys())
        
        try:
            # Execute the code (following LangGraph CodeAct README pattern)
            exec(code, __builtins__, _locals)
            
            # Get the output
            output = captured_output.getvalue()
            
            # Store execution in history
            self.execution_history.append({
                'code': code,
                'output': output,
                'success': True
            })
            
            # Only return NEW variables created during execution (like LangGraph CodeAct reference)
            # Clean up non-serializable objects that shouldn't persist (like file handles)
            new_keys = set(_locals.keys()) - original_keys
            user_variables = {}
            for key in new_keys:
                value = _locals[key]
                # Skip file-like objects and other non-persistent types by their type
                if isinstance(value, (io.IOBase, io.TextIOWrapper, io.BufferedWriter, io.BufferedReader)):
                    continue  # File objects don't need to persist
                user_variables[key] = value
            
            return output if output else "Code executed successfully.", user_variables
            
        except Exception as e:
            # Capture error
            error_output = f"Error: {str(e)}\n{traceback.format_exc()}"
            
            # Store failed execution in history
            self.execution_history.append({
                'code': code,
                'output': error_output,
                'success': False
            })
            
            # Return empty new variables on error
            return error_output, {}
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
    
    def get_context(self) -> Dict[str, Any]:
        """Get current execution context variables (empty for fresh context)"""
        # In the new pattern, we only track variables created during execution
        # Initial context is empty - variables are built up incrementally
        return {}
    
    def reset_context(self):
        """Reset execution context to initial state"""
        self.__init__()
    
    def get_available_variables(self) -> str:
        """Get string representation of available variables"""
        variables = []
        for key, value in self.globals_dict.items():
            if not key.startswith('_') and not callable(value):
                try:
                    var_type = type(value).__name__
                    if hasattr(value, 'shape'):  # pandas/numpy objects
                        var_info = f"{key}: {var_type} {value.shape}"
                    else:
                        var_info = f"{key}: {var_type}"
                    variables.append(var_info)
                except:
                    variables.append(f"{key}: {type(value).__name__}")
        
        return "Available variables:\n" + "\n".join(variables) if variables else "No variables defined yet."
    
    def add_library(self, name: str, library: Any):
        """Add a library to the execution context"""
        self.globals_dict[name] = library
    
    def get_execution_history(self) -> list:
        """Get execution history for debugging"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
    
    def get_workspace_info(self) -> str:
        """Get information about the workspace"""
        info = [
            f"Workspace: {self.workspace_path}",
            f"Data directory: {self.workspace_path / 'data'}",
            f"Outputs directory: {self.workspace_path / 'outputs'}",
            f"Visualizations directory: {self.workspace_path / 'visualizations'}",
            f"Reports directory: {self.workspace_path / 'reports'}",
        ]
        return "\n".join(info)
    
    def cleanup(self):
        """Cleanup workspace and restore original working directory"""
        try:
            os.chdir(self.original_cwd)
        except Exception as e:
            print(f"Warning: Could not restore original working directory: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup()