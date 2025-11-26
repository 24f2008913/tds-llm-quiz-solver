"""Quick test - what does the API actually call?"""
import requests
import json

url = "http://127.0.0.1:5000/quiz"
payload = {
    "email": "24f2008913@ds.study.iitm.ac.in",
    "secret": "24f2008913iitmbstdsp2",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
}

print("Sending request to API...")
print("="*70)

response = requests.post(url, json=payload, timeout=180)

print(f"\nStatus: {response.status_code}")
print("\nResponse:")
result = response.json()
print(json.dumps(result, indent=2))

print("\n" + "="*70)
print("SECOND QUIZ ANALYSIS:")
if 'result' in result and 'results' in result['result'] and len(result['result']['results']) > 1:
    quiz2 = result['result']['results'][1]
    print(f"Answer type: {type(quiz2['answer'])}")
    print(f"Answer length: {len(quiz2['answer']) if isinstance(quiz2['answer'], str) else 'N/A'}")
    print(f"Answer: {quiz2['answer'][:200]}")
    print(f"Correct: {quiz2['correct']}")
