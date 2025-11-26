"""Direct test of solving the scraping quiz"""
from dotenv import load_dotenv
load_dotenv()

from quiz_solver import QuizSolver
from datetime import datetime
import json

quiz_url = "https://tds-llm-analysis.s-anand.net/demo-scrape?email=24f2008913@ds.study.iitm.ac.in&id=10378"

print(f"Testing direct quiz solving for: {quiz_url}")
print("="*70)

solver = QuizSolver()
start_time = datetime.now()

try:
    result = solver.solve_single_quiz(quiz_url, start_time)
    print("\nResult:")
    print(json.dumps(result, indent=2, default=str))
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
