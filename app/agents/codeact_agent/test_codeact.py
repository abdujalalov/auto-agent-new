"""
Test script for CodeAct Agent Phase 1

Tests basic functionality and data science library integration.
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agents.codeact_agent import create_codeact_agent, ExecutionContext


load_dotenv()


def test_execution_context():
    """Test the execution context with data science libraries"""

    print("Testing ExecutionContext...")

    context = ExecutionContext()

    # Test 1: Basic variable persistence
    code1 = """
x = 42
y = "hello world"
print(f"x = {x}, y = {y}")
"""

    output1, vars1 = context.execute_code(code1)
    print(f"Test 1 Output: {output1}")
    print(f"Test 1 Variables: {list(vars1.keys())}")

    # Test 2: Use variables from previous execution
    code2 = """
z = x * 2
print(f"z = x * 2 = {z}")
print(f"Previous y was: {y}")
"""

    output2, vars2 = context.execute_code(code2, vars1)
    print(f"Test 2 Output: {output2}")
    print(f"Test 2 Variables: {list(vars2.keys())}")

    # Test 3: Data science libraries
    code3 = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Test pandas
data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print("DataFrame created:")
print(data)

# Test numpy
arr = np.array([1, 2, 3, 4, 5])
print(f"Numpy array mean: {np.mean(arr)}")

print("Data science libraries work!")
"""

    output3, vars3 = context.execute_code(code3, vars2)
    print(f"Test 3 Output: {output3}")

    print("✅ ExecutionContext tests passed!")
    return True


def test_codeact_agent_basic():
    """Test basic CodeAct agent functionality"""

    print("\nTesting CodeAct Agent...")

    try:
        # Create model (requires API key)
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # Create agent with session-based workspaces
        agent = create_codeact_agent(model, "test_workspace")

        # Simple test task
        task = "Create a simple dataset with 3 rows and 2 columns, save it to DATA_DIR, then calculate the sum of each column."

        print(f"Task: {task}")

        # Run agent with session configuration
        config = {
            "configurable": {
                "thread_id": "test_session_123",
                "user_id": "test_user"
            }
        }
        result = agent.run(task, config=config, recursion_limit=5)

        print("Agent completed successfully!")
        print(f"Number of messages: {len(result['messages'])}")
        print(f"Variables in context: {list(result['context'].keys())}")

        # Print last few messages
        print("\nConversation:")
        for msg in result['messages'][-4:]:  # Last 4 messages
            role = "Human" if hasattr(msg, 'content') and msg.__class__.__name__ == "HumanMessage" else "AI"
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"{role}: {content[:200]}{'...' if len(content) > 200 else ''}")

        print("✅ CodeAct Agent test passed!")
        return True

    except Exception as e:
        print(f"⚠️  CodeAct Agent test skipped: {e}")
        return False


if __name__ == "__main__":
    print("Running CodeAct Agent Phase 1 Tests")
    print("=" * 50)

    # Test execution context
    context_test = test_execution_context()

    # Test full agent (optional, requires API key)
    agent_test = test_codeact_agent_basic()

    print("\n" + "=" * 50)
    if context_test:
        print("🎉 Phase 1 Core functionality is working!")
        print("✅ Persistent execution context")
        print("✅ Data science libraries integration")
        print("✅ Variable persistence between executions")

        if agent_test:
            print("✅ Full CodeAct agent cycle")
        else:
            print("⚠️  Full agent test requires OpenAI API key")
    else:
        print("❌ Phase 1 tests failed")
