"""Quick test script for AI Pipe integration"""
import os
from dotenv import load_dotenv
from llm_handler import LLMHandler

load_dotenv()

def test_aipipe():
    print("=" * 60)
    print("Testing AI Pipe Integration")
    print("=" * 60)
    
    # Initialize handler
    print("\n1. Initializing LLM Handler...")
    handler = LLMHandler()
    print(f"   ✓ Model: {handler.model}")
    print(f"   ✓ Base URL: {handler.openai_base_url}")
    
    # Test simple completion
    print("\n2. Testing simple completion...")
    try:
        response = handler.generate_completion(
            prompt="What is 2 + 2? Answer with just the number.",
            temperature=0
        )
        print(f"   ✓ Response: {response}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False
    
    # Test JSON mode
    print("\n3. Testing JSON mode...")
    try:
        response = handler.generate_completion(
            prompt="Return a JSON object with fields: name='Test', value=42",
            json_mode=True
        )
        print(f"   ✓ Response: {response}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All AI Pipe tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_aipipe()
    exit(0 if success else 1)
