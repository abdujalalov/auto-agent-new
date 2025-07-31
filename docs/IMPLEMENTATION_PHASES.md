# Implementation Phases - Document-Driven CodeAct Agent

## Overview

This document breaks down the implementation into logical phases that can be completed in single sessions with clear start/end points and testable outcomes.

## Phase 1: Core CodeAct Engine Foundation
**Session Goal**: Working CodeAct agent with persistent execution context
**Estimated Duration**: 1-2 hours

### Tasks

#### Task 1.1: Basic LangGraph CodeAct Structure
- Create `app/agents/codeact_agent/` directory structure
- Implement basic `CodeActState` extending `MessagesState`
- Create simple 2-node graph: `agent_node` → `execution_node`
- Basic state transitions and message handling

**Deliverables**:
```python
# codeact_agent.py with basic structure
class CodeActState(MessagesState):
    script: Optional[str]
    context: dict[str, Any]

def create_codeact_agent() -> StateGraph:
    # Basic graph implementation
```

#### Task 1.2: Persistent Execution Context
- Implement `ExecutionContext` class
- Python `exec()` with controlled environment
- Variable persistence between code executions
- Output capture and context updates

**Deliverables**:
```python
# execution_context.py
class ExecutionContext:
    def execute_code(self, code: str) -> tuple[str, dict]:
        # Safe execution with persistence
```

#### Task 1.3: Basic Agent Prompting
- Simple system prompt for code generation
- Thought-Code-Observation pattern instructions
- Basic tool availability description
- Integration with LangGraph nodes

**Deliverables**:
```markdown
# prompts/codeact_system.md
Basic prompt template for CodeAct reasoning
```

#### Task 1.4: Data Science Libraries Integration
- Pre-load pandas, numpy, matplotlib in execution context
- Make libraries available as variables
- Test library access and persistence
- Basic visualization capabilities

**Test Criteria**:
- [ ] Agent can generate and execute Python code
- [ ] Variables persist between code executions
- [ ] Pandas, numpy, matplotlib accessible
- [ ] Output captured and returned to agent
- [ ] Multi-step analysis with variable reuse works

**Example Test**:
```python
# Agent should be able to execute this sequence:
# Step 1: Create data
data = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})

# Step 2: Analyze (in next execution, data still available)
result = data.describe()
print(result)

# Step 3: Visualize (data and result still available)
plt.plot(data['x'], data['y'])
plt.show()
```

---

## Phase 2: Document Integration & Framework Reading
**Session Goal**: Agent can read and reason about framework documents
**Estimated Duration**: 1-2 hours

### Tasks

#### Task 2.1: Document Reader Implementation
- Create `DocumentReader` class
- Simple markdown file loading
- Integration with agent state
- Framework content accessibility

**Deliverables**:
```python
# document_reader.py
class DocumentReader:
    def load_framework(self, path: str) -> str:
        # Load prepared markdown documents
    
    def integrate_with_state(self, content: str, state: CodeActState):
        # Make content available to agent
```

#### Task 2.2: Enhanced Agent Prompting for Frameworks
- Update system prompts to include framework guidance
- Instructions for reading and following methodology
- Framework compliance expectations
- Autonomous interpretation instructions

**Deliverables**:
```markdown
# Updated prompts/codeact_system.md
Enhanced prompt with framework reading capabilities
```

#### Task 2.3: Framework Context Integration
- Add framework content to agent reasoning context
- Document content available in agent prompts
- No rigid parsing - agent interprets naturally
- Framework-aware code generation

#### Task 2.4: Sample Framework Testing
- Use existing `.data/sample_task_documents/` frameworks
- Test with Data Quality Framework
- Agent reads, understands, and plans approach
- Methodology step identification through reasoning

**Test Criteria**:
- [ ] Agent can load framework documents
- [ ] Framework content appears in agent context
- [ ] Agent demonstrates understanding of methodology
- [ ] Agent plans analysis approach based on framework
- [ ] Framework compliance visible in agent reasoning

**Example Test**:
```python
# Agent should be able to:
# 1. Read Data Quality Framework
# 2. Identify key methodology steps
# 3. Plan data analysis approach
# 4. Explain how it will follow framework
```

---

## Phase 3: Advanced Data Analysis Capabilities
**Session Goal**: Sophisticated data analysis with framework compliance
**Estimated Duration**: 1-2 hours

### Tasks

#### Task 3.1: Enhanced Data Analysis Tools
- Expand execution context with advanced libraries
- Statistical analysis capabilities (scipy, statsmodels)
- Advanced visualization (plotly, seaborn)
- Data quality assessment utilities

**Deliverables**:
```python
# Enhanced execution_context.py
# Additional libraries: scipy, statsmodels, plotly, seaborn
# Custom utility functions for data quality
```

#### Task 3.2: Framework-Driven Analysis Patterns
- Agent reasoning for methodology compliance
- Step-by-step framework following
- Data quality assessment workflows
- Statistical analysis patterns

#### Task 3.3: Result Capture and Organization
- Structured output management
- Analysis result organization
- Chart and visualization handling
- Framework step completion tracking

#### Task 3.4: Complex Workflow Testing
- Multi-step data analysis workflows
- Framework methodology following
- Advanced statistical analysis
- Comprehensive data quality assessment

**Test Criteria**:
- [ ] Agent performs complex data analysis
- [ ] Framework methodology steps followed
- [ ] Advanced visualizations generated
- [ ] Statistical analysis completed
- [ ] Results organized and structured
- [ ] Framework compliance demonstrated

**Example Test**:
```python
# Agent should complete full data quality assessment:
# 1. Load and explore dataset
# 2. Follow Data Quality Framework steps
# 3. Perform completeness, validity, accuracy analysis
# 4. Generate statistical summaries
# 5. Create visualizations
# 6. Document findings
```

---

## Phase 4: Comprehensive Report Generation
**Session Goal**: Autonomous creation of artifact-style reports
**Estimated Duration**: 1-2 hours

### Tasks

#### Task 4.1: Autonomous Report Structure Generation
- Agent-driven report planning
- Comprehensive documentation structure
- Framework compliance documentation
- Analysis result integration

#### Task 4.2: Report Content Generation
- Markdown report creation through code execution
- Result embedding and formatting
- Chart integration and descriptions
- Comprehensive analysis documentation

**Deliverables**:
```python
# Agent generates comprehensive reports like:
"""
# Data Quality Analysis Report

## Executive Summary
[Agent-generated summary]

## Methodology
[Framework compliance documentation]

## Analysis Results
[Detailed findings with embedded results]

## Visualizations
[Charts and analysis]

## Conclusions
[Agent-generated conclusions]
"""
```

#### Task 4.3: Artifact-Style Output Creation
- Publication-ready report generation
- Professional formatting and structure
- Comprehensive documentation style
- Shareable analysis artifacts

#### Task 4.4: End-to-End Workflow Testing
- Complete document-to-report workflow
- Framework reading → Analysis → Report generation
- Comprehensive system testing
- Real-world scenario validation

**Test Criteria**:
- [ ] Agent generates comprehensive reports autonomously
- [ ] Reports include all analysis components
- [ ] Framework compliance documented
- [ ] Professional, artifact-style formatting
- [ ] End-to-end workflow completed successfully
- [ ] Reports are publication-ready

**Example Test**:
```python
# Complete workflow:
# 1. Agent reads Data Quality Framework
# 2. Loads sample dataset
# 3. Performs comprehensive analysis
# 4. Generates publication-ready report
# 5. Report includes methodology, results, visualizations
# 6. Framework compliance demonstrated throughout
```

---

## Success Metrics

### Phase 1 Success
- ✅ Working CodeAct execution cycle
- ✅ Persistent Python context
- ✅ Basic data analysis capabilities
- ✅ Multi-step code execution

### Phase 2 Success
- ✅ Framework document integration
- ✅ Agent framework comprehension
- ✅ Methodology-aware planning
- ✅ Framework-driven reasoning

### Phase 3 Success
- ✅ Complex data analysis workflows
- ✅ Framework compliance in analysis
- ✅ Advanced statistical capabilities
- ✅ Comprehensive data quality assessment

### Phase 4 Success
- ✅ Autonomous report generation
- ✅ Artifact-style documentation
- ✅ End-to-end workflow completion
- ✅ Publication-ready outputs

## Technical Testing Strategy

### Unit Testing (Per Phase)
- Individual component functionality
- State management and persistence
- Code execution and context handling
- Framework integration and interpretation

### Integration Testing (End of Each Phase)
- Component interaction validation
- State flow between graph nodes
- Document-to-analysis-to-report pipeline
- Framework compliance verification

### System Testing (Phase 4)
- Complete workflow validation
- Real-world scenario testing
- Performance and reliability assessment
- Output quality evaluation

## Risk Mitigation

### Technical Risks
- **Context Management**: Ensure reliable variable persistence
- **Code Execution Safety**: Controlled execution environment
- **Framework Interpretation**: Agent understanding validation
- **Report Quality**: Comprehensive output verification

### Mitigation Strategies
- Extensive testing at each phase boundary
- Clear success criteria and validation
- Incremental complexity introduction
- Regular checkpoint validation

## Development Environment Setup

### Prerequisites
- Python 3.11+
- LangGraph and LangChain installed
- Data science libraries (pandas, numpy, matplotlib, seaborn)
- Access to sample framework documents

### Session Preparation
- Activate virtual environment
- Navigate to project root
- Load existing configuration
- Access to sample datasets for testing

---

## Phase 5: Security Hardening
**Session Goal**: Secure code execution environment with safety restrictions
**Estimated Duration**: 1-2 hours

### Background
Currently using raw `exec()` following LangGraph CodeAct README pattern. While functional, this poses security risks in production environments.

### Tasks

#### Task 5.1: Import Restrictions
- Implement SmolaAgents-style dangerous module filtering
- Create allowlist of safe imports (data science libraries)
- Block dangerous modules: `os`, `subprocess`, `socket`, `sys`, etc.
- Add import validation before code execution

**Deliverables**:
```python
# Security module for import filtering
DANGEROUS_MODULES = ["builtins", "io", "os", "subprocess", "sys", ...]
ALLOWED_IMPORTS = ["pandas", "numpy", "matplotlib", "seaborn", ...]

def validate_imports(code: str) -> bool:
    # Parse and validate imports in code
```

#### Task 5.2: Dangerous Function Filtering  
- Block dangerous built-in functions
- Disable `eval`, `exec`, `__import__`, `open` access
- Implement custom safer alternatives where needed
- Add function call validation

**Deliverables**:
```python
DANGEROUS_FUNCTIONS = [
    "builtins.eval", "builtins.exec", "builtins.__import__",
    "os.system", "subprocess.run", ...
]

def create_safe_globals() -> dict:
    # Return filtered globals dict with dangerous functions removed
```

#### Task 5.3: File System Restrictions
- Limit file access to workspace directories only
- Implement path validation for file operations
- Add safe file operation wrappers
- Block access to system files

#### Task 5.4: Resource Limits
- Add execution timeout limits
- Memory usage constraints
- CPU usage monitoring
- Prevent infinite loops and resource exhaustion

**Test Criteria**:
- [ ] Dangerous imports are blocked
- [ ] Dangerous functions are inaccessible
- [ ] File access limited to workspace
- [ ] Resource limits prevent abuse
- [ ] All current functionality still works

---

## Phase 6: Production Security Environment
**Session Goal**: Enterprise-grade secure execution environment
**Estimated Duration**: 2-3 hours

### Tasks

#### Task 6.1: Evaluate Sandbox Options
- Research LangChain Sandbox (Pyodide/WebAssembly)
- Evaluate E2B remote execution
- Compare Docker containerization
- Performance and security analysis

#### Task 6.2: Implement Chosen Sandbox
- Integrate selected sandbox solution
- Migrate from raw `exec()` to sandboxed execution
- Maintain all current agent functionality
- Add sandbox-specific optimizations

#### Task 6.3: Security Testing
- Penetration testing of execution environment
- Validate all security restrictions
- Performance benchmarking
- Security audit documentation

**Deliverables**:
```python
# Production-ready secure executor
class SecureExecutor:
    def execute_code(self, code: str) -> tuple[str, dict]:
        # Sandboxed execution with full security
```

**Test Criteria**:
- [ ] Complete isolation from host system
- [ ] No access to dangerous operations
- [ ] Production-ready security posture
- [ ] Performance acceptable for agent use
- [ ] All agent features functional

---

## Implementation Priority

### Current Status (Phase 2 Complete)
- ✅ Core CodeAct engine working
- ✅ Framework document integration  
- ✅ Session-based workspaces
- ✅ Serialization issues resolved

### Next Priority: Phase 3
**Advanced data analysis capabilities** - This provides immediate value for complex analytical tasks.

### Security Implementation Timeline
- **Phase 5**: After Phase 3/4 completion (when core functionality is mature)
- **Phase 6**: Before production deployment

### Notes
- Security hardening can be developed in parallel with feature development
- Current implementation is suitable for development and testing
- Production deployment requires Phase 6 completion

This phased approach ensures manageable development sessions with clear milestones and testable outcomes at each stage.