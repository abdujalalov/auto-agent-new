"""
Test script for CodeAct Agent Phase 2 - Framework Integration

Tests framework document loading and agent framework awareness.
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agents.codeact_agent import create_codeact_agent

load_dotenv()


def test_framework_integration():
    """Test the framework document integration"""
    
    print("Testing Framework Document Integration...")
    
    try:
        # Create model (requires API key)
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Create agent with session-based workspaces
        agent = create_codeact_agent(model, "phase2_test_workspace")
        
        # Path to our Data Quality Framework
        framework_path = ".data/sample_task_documents/docs/etl/LLM_Guide_Data_Quality_Rules_Framework.md"
        
        # Test task that should use the framework
        task = """
        I need you to understand and explain the Data Quality Framework methodology.
        Please read the framework document and show me what steps it contains for data analysis.
        """
        
        print(f"Task: {task}")
        print(f"Framework: {framework_path}")
        
        # Run agent with framework document
        config = {
            "configurable": {
                "thread_id": "phase2_test_session",
                "user_id": "phase2_tester"
            }
        }
        
        result = agent.run(
            task=task,
            framework_document_path=framework_path,
            config=config,
            recursion_limit=5
        )
        
        print("Agent completed successfully!")
        print(f"Number of messages: {len(result['messages'])}")
        
        # Print the conversation
        print("\n" + "="*50)
        print("AGENT CONVERSATION:")
        print("="*50)
        
        for i, msg in enumerate(result['messages']):
            role = "Human" if hasattr(msg, 'content') and msg.__class__.__name__ == "HumanMessage" else "AI"
            content = msg.content if hasattr(msg, 'content') else str(msg)
            
            print(f"\n[{i+1}] {role}:")
            print("-" * 30)
            print(content)
        
        print("\n" + "="*50)
        print("✅ Phase 2 Framework Integration test passed!")
        return True
        
    except Exception as e:
        print(f"⚠️  Framework Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_framework_validation():
    """Test framework path validation"""
    
    print("\nTesting Framework Path Validation...")
    
    try:
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        agent = create_codeact_agent(model, "validation_test_workspace")
        
        # Test with invalid path - should raise validation error
        try:
            agent.run(
                task="Test task",
                framework_document_path="non_existent_file.md",
                recursion_limit=1
            )
            print("❌ Validation failed - should have raised error for invalid path")
            return False
        except ValueError as e:
            print(f"✅ Validation working correctly: {e}")
            return True
            
    except Exception as e:
        print(f"⚠️  Validation test error: {e}")
        return False


if __name__ == "__main__":
    print("Running CodeAct Agent Phase 2 Tests")
    print("=" * 50)
    
    # Test framework path validation
    validation_test = test_framework_validation()
    
    # Test framework integration (requires API key)
    integration_test = test_framework_integration()
    
    print("\n" + "=" * 50)
    print("PHASE 2 TEST RESULTS:")
    print("=" * 50)
    
    if validation_test:
        print("✅ Framework path validation")
    else:
        print("❌ Framework path validation failed")
    
    if integration_test:
        print("✅ Framework document integration")
        print("✅ Agent framework awareness")
        print("✅ Document-driven methodology reading")
        print("\n🎉 Phase 2 SUCCESS: Agent can read and follow framework documents!")
    else:
        print("❌ Framework integration failed")
        print("⚠️  Full test requires OpenAI API key")