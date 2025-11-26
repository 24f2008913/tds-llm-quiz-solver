"""Test the exact API flow"""
from dotenv import load_dotenv
load_dotenv()

from quiz_solver import QuizSolver
import json

solver = QuizSolver()
initial_url = "https://tds-llm-analysis.s-anand.net/demo"

print("Testing complete chain from API perspective...")
print("="*70)

try:
    result = solver.solve_quiz_chain(initial_url)
    print("\nChain Result:")
    print(json.dumps(result, indent=2, default=str))
    
    print("\n" + "="*70)
    print("DETAILED RESULTS:")
    for i, quiz_result in enumerate(result['results'], 1):
        print(f"\nQuiz {i}:")
        print(f"  URL: {quiz_result.get('url', 'N/A')[:80]}")
        print(f"  Answer: {quiz_result.get('answer', 'N/A')}")
        print(f"  Correct: {quiz_result.get('correct', 'N/A')}")
        if not quiz_result.get('correct'):
            print(f"  Response: {quiz_result.get('response', {})}")
            
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
