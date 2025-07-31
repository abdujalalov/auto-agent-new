# Document-Driven CodeAct Agent Implementation Guide

## Project Overview

This guide details the implementation of a document-driven CodeAct agent system that reads methodology framework documents and autonomously executes data analysis tasks through code generation and execution.

## Core Architecture

### AI-Native Agentic Approach
- **No rigid pipelines**: Agent autonomously decides next steps through reasoning
- **Emergent behavior**: Implementation emerges from agent-document interaction
- **Code as unified action space**: Entire Python ecosystem available through code generation
- **Persistent execution context**: Variables and state maintained across code blocks

### Foundation Technologies
- **LangGraph**: State graph framework for agent orchestration
- **LangChain**: Language model integration and prompt management
- **Python exec()**: Controlled code execution with context preservation
- **Markdown processing**: Framework document interpretation

## Technical Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Framework Doc   │───▶│ CodeAct Agent    │───▶│ Comprehensive   │
│ (Prepared MD)   │    │ (LangGraph)      │    │ Report (MD)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Persistent       │
                       │ Python Context   │
                       │ + Tool Access    │
                       └──────────────────┘
```

## Core Components

### 1. CodeActAgent (LangGraph Implementation)

**Purpose**: Main orchestrator implementing Thought-Code-Observation cycle

**Implementation**:
```python
class CodeActState(MessagesState):
    """Extended state for CodeAct agent"""
    script: Optional[str]           # Generated Python code
    context: dict[str, Any]         # Persistent execution context
    current_task: Optional[str]     # Current framework step
    framework_content: Optional[str] # Loaded document content
    report_sections: list[str]      # Generated report sections

def create_codeact_agent(model, tools) -> StateGraph:
    """Create CodeAct agent using LangGraph"""
    # Node 1: Agent reasoning and code generation
    def agent_node(state: CodeActState):
        # Agent reads framework, reasons about next steps
        # Generates Python code for execution
        pass
    
    # Node 2: Code execution with persistent context
    def execution_node(state: CodeActState):
        # Execute code in persistent Python environment
        # Update context with new variables
        # Capture outputs for observation
        pass
    
    # Build graph: agent → execution → agent (loop)
    graph = StateGraph(CodeActState)
    graph.add_node("agent", agent_node)
    graph.add_node("execution", execution_node)
    # Add edges and return compiled graph
```

**Key Features**:
- LangGraph state management for persistence
- Thought-Code-Observation cycle through graph nodes
- Framework document context integration
- Autonomous task decomposition and execution

### 2. Persistent Execution Context

**Purpose**: Maintain Python variables and state across code executions

**Implementation**:
```python
class ExecutionContext:
    """Manages persistent Python execution environment"""
    
    def __init__(self):
        self.globals_dict = {
            # Standard libraries
            'pandas': pandas,
            'numpy': numpy,
            'matplotlib': matplotlib,
            'seaborn': seaborn,
            # Data analysis utilities
            'pd': pandas,
            'np': numpy,
            'plt': matplotlib.pyplot,
        }
        self.execution_history = []
    
    def execute_code(self, code: str) -> tuple[str, dict]:
        """Execute code and return output + updated context"""
        # Capture stdout
        # Execute in controlled environment
        # Update persistent context
        # Return results and new variables
        pass
```

**Key Features**:
- Variable persistence between executions
- Pre-loaded data analysis libraries
- Safe code execution with output capture
- Context state tracking and management

### 3. Document Integration System

**Purpose**: Enable agent to read and interpret framework documents

**Implementation**:
```python
class DocumentReader:
    """Framework document processing and access"""
    
    def load_framework(self, doc_path: str) -> str:
        """Load prepared markdown framework document"""
        pass
    
    def make_available_to_agent(self, content: str, state: CodeActState):
        """Add document content to agent context"""
        # Framework content available in agent reasoning
        # No rigid parsing - agent interprets autonomously
        pass
```

**Key Features**:
- Simple markdown document loading
- Content integration into agent context
- Agent-driven interpretation (no rigid parsing)
- Framework methodology accessible for reasoning

### 4. Agent Prompt Engineering

**Purpose**: Enable autonomous reasoning and framework compliance

**Implementation** (inspired by smolagents patterns):
```python
CODEACT_SYSTEM_PROMPT = """
You are an expert data analysis agent who solves tasks by generating and executing Python code.

You have access to a framework document that describes methodology steps. Read and follow the framework to complete data analysis tasks.

Work in a cycle of Thought, Code, and Observation:

1. **Thought**: Analyze the framework and current situation. Plan your next step.
2. **Code**: Generate Python code to execute your plan. Use print() to capture important results.
3. **Observation**: Review code execution results and plan next steps.

Framework document is available in your context. Read it carefully and follow the methodology.

Available libraries: pandas, numpy, matplotlib, seaborn, and full Python ecosystem.
Variables persist between code executions - reuse them as needed.

Generate comprehensive analysis and prepare detailed reports with your findings.
"""
```

**Key Features**:
- Thought-Code-Observation guidance
- Framework compliance instruction
- Autonomous reasoning encouragement
- Report generation direction

### 5. Report Generation System

**Purpose**: Autonomous creation of comprehensive markdown reports

**Agent-Driven Approach**:
- Agent autonomously structures reports based on analysis
- Results embedded directly from code execution outputs
- Framework compliance demonstrated through methodology following
- Comprehensive documentation similar to Claude artifacts

**Implementation**:
```python
# Agent generates reports through code execution
report_code = """
# Agent autonomously creates report sections
report_content = f'''
# Data Quality Analysis Report

## Executive Summary
{analysis_summary}

## Methodology
Following the Data Quality Framework:
{methodology_steps}

## Analysis Results
{detailed_results}

## Visualizations
{chart_descriptions}

## Conclusions
{conclusions}
'''

print("REPORT_SECTION:", report_content)
"""
```

## Implementation Flow

### Phase 1: Core CodeAct Engine
1. **LangGraph Setup**: Create basic state graph with agent/execution nodes
2. **Context Management**: Implement persistent Python execution environment
3. **Basic Prompting**: Simple system prompts for code generation
4. **Tool Integration**: Make pandas, matplotlib available in execution context

**Test**: Agent executes multi-step data analysis with persistent variables

### Phase 2: Document Integration
1. **Document Loading**: Simple markdown file reading capability
2. **Context Integration**: Make framework content available to agent
3. **Agent Reasoning**: Prompts for framework interpretation and following
4. **Methodology Compliance**: Agent reasons about framework steps

**Test**: Agent reads Data Quality Framework and plans analysis approach

### Phase 3: Data Analysis Capabilities
1. **Library Integration**: Full data science stack in execution context
2. **Visualization Generation**: Chart creation and result capture
3. **Statistical Analysis**: Comprehensive data analysis patterns
4. **Result Management**: Output capture and organization

**Test**: Agent completes sophisticated data quality assessment

### Phase 4: Report Generation
1. **Autonomous Structuring**: Agent creates comprehensive report layouts
2. **Result Embedding**: Integration of analysis outputs into markdown
3. **Framework Documentation**: Methodology compliance demonstration
4. **Artifact Creation**: Publication-ready comprehensive reports

**Test**: Agent produces complete, artifact-style analysis documentation

## Technical Decisions

### LangGraph vs Custom Implementation
- **Choose LangGraph**: Mature state management, good patterns, extensible
- **Benefits**: Clean architecture, message handling, state persistence
- **Integration**: Works with existing LangChain models and tools

### Execution Environment
- **Local Python exec()**: Simple, direct access to full Python ecosystem
- **Controlled Context**: Safe execution with persistent variable management
- **Future**: Can extend to Docker/E2B for enhanced security

### Document Processing
- **Index-Based Navigation**: Agent reads index document and resolves references to methodology documents
- **Relative Path Resolution**: Documents organized in standardized `agent_tasks/task_name/` structure  
- **Agent-Driven**: Framework interpretation through reasoning, not rigid rules
- **Multi-Document Support**: Agent autonomously decides which documents to read based on task

### Prompt Engineering
- **Smolagents Inspiration**: Detailed examples and reasoning patterns
- **Framework Focus**: Emphasis on methodology compliance and documentation
- **Autonomous Operation**: Encourages independent reasoning and adaptation

## Integration with Existing Codebase

### Current Structure Compatibility
- **app/agents/**: Add new CodeAct agent alongside existing main_agent
- **app/core/**: Utilize existing configuration and logging systems
- **LangGraph Integration**: Compatible with existing langgraph.json configuration

### File Organization
```
app/agents/
├── codeact_agent/
│   ├── __init__.py
│   ├── codeact_agent.py      # Main agent implementation
│   ├── execution_context.py   # Persistent context management
│   ├── schemas.py           # State and config schemas
│   └── prompts/
│       └── codeact_system.md  # Agent prompts

agent_tasks/                 # Agent task definitions
├── data_warehouse_agent/
│   ├── index.md            # Task index with document references
│   └── docs/
│       ├── data_quality_framework.md
│       └── sql_server_guide.md
└── other_task_type/
    ├── index.md
    └── docs/
```

### Agent Task Structure
Each agent task follows a standardized pattern:
- **index.md**: Main entry point with project overview and document references
- **docs/**: Methodology documents referenced by index with relative paths
- **Relative paths**: All document references use `./docs/filename.md` format
- **Path resolution**: Agent uses `INDEX_DOCUMENT_DIR` + relative path to access documents

## Security Considerations

### Current Implementation Status
**⚠️ Development Mode**: Current implementation uses raw `exec()` following LangGraph CodeAct README pattern. Suitable for development and testing but requires hardening for production.

### Security Architecture Evolution

#### Phase 1: Current State (Development Safe)
- **Pattern**: LangGraph CodeAct reference implementation
- **Execution**: Raw `exec()` with variable isolation
- **Workspace**: Session-based isolation with dedicated directories
- **Suitable for**: Development, testing, trusted environments

#### Phase 5: Security Hardening (Planned)
Based on SmolaAgents security model:

**Import Restrictions**:
```python
DANGEROUS_MODULES = [
    "builtins", "io", "multiprocessing", "os", "pathlib",
    "pty", "shutil", "socket", "subprocess", "sys"
]
```

**Function Filtering**:
```python
DANGEROUS_FUNCTIONS = [
    "builtins.eval", "builtins.exec", "builtins.__import__",
    "os.system", "subprocess.run", "posix.system"
]
```

**File System Controls**:
- Restrict file access to workspace directories only
- Path validation for all file operations
- Safe file operation wrappers

#### Phase 6: Production Security (Future)
**Sandbox Options**:
1. **LangChain Sandbox** (Pyodide/WebAssembly)
   - Complete isolation from host system
   - WebAssembly security model
   - Python interpreter in browser-like environment

2. **E2B Remote Execution**
   - Cloud-based secure execution
   - Complete network isolation
   - Enterprise-grade security

3. **Docker Containerization**
   - OS-level isolation
   - Resource limits and monitoring
   - Network restrictions

### Risk Assessment

#### Current Risks (Development Phase)
- **File system access**: Agent can read/write any accessible files
- **Network access**: Agent can make HTTP requests, download content
- **System commands**: Potential access to shell commands via imports
- **Resource consumption**: No limits on CPU/memory usage

#### Mitigated Risks
- ✅ **Variable isolation**: Only new variables stored in state (prevents pollution)
- ✅ **Workspace isolation**: Session-based directories prevent user conflicts
- ✅ **Serialization safety**: Fixed pickle issues with proper variable filtering

#### Production Requirements
- [ ] Import restrictions implemented
- [ ] Dangerous function filtering active
- [ ] File system access limited to workspace
- [ ] Resource limits and monitoring
- [ ] Complete execution environment isolation

### Security Timeline
- **Phase 2-4**: Continue development with current security model
- **Phase 5**: Implement security hardening (import/function restrictions)
- **Phase 6**: Deploy production-grade sandbox before live deployment

**Note**: Current implementation follows industry-standard patterns (LangGraph CodeAct, SmolaAgents) and is appropriate for development phases. Security hardening will be implemented following proven patterns from reference implementations.

## Success Criteria

### Minimum Viable Product
- [x] Agent reads index document and resolves references to methodology documents
- [x] Executes multi-step data analysis with persistent context
- [x] Generates comprehensive markdown report
- [x] Demonstrates autonomous reasoning and framework following
- [x] Multi-document navigation with relative path resolution

### Enhanced Capabilities
- [ ] Complex data analysis workflows
- [ ] Advanced visualizations and charts
- [x] Multiple framework document support
- [ ] Interactive report elements

## Key Design Principles

1. **AI-Native**: Agent reasoning drives behavior, not rigid programming
2. **Emergent Behavior**: Capabilities emerge from agent-document interaction
3. **Code-Centric**: Unified action space through Python code generation
4. **Document-Driven**: Framework documents control agent methodology
5. **Autonomous Operation**: Minimal human intervention in execution cycles
6. **Comprehensive Output**: Artifact-style reports with embedded analysis

This implementation guide provides the complete technical blueprint for building our document-driven CodeAct agent system using LangGraph and modern agentic AI principles.