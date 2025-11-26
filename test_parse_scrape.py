"""Direct test of scraping quiz parsing"""
from quiz_solver import QuizSolver
from browser_handler import BrowserHandler
import json

quiz_url = "https://tds-llm-analysis.s-anand.net/demo-scrape?email=24f2008913@ds.study.iitm.ac.in&id=10362"

print(f"Testing quiz at: {quiz_url}")
print("="*70)

solver = QuizSolver()

print("\n1. Fetching page...")
with BrowserHandler() as browser:
    page_content = browser.fetch_page_content(quiz_url)
    
    print("\n2. Parsing quiz page...")
    question_data = solver.parse_quiz_page(page_content, browser, quiz_url)

print("\n3. Parsed question data:")
print(json.dumps(question_data, indent=2, default=str))

print("\n4. Scrape URLs found:")
print(question_data.get('scrape_urls'))
