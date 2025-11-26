"""
Test quiz solver with dynamic parameters (no hardcoded values)
This simulates how the actual evaluation will work
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_dynamic_endpoint():
    """Test with parameters loaded from environment - simulates real evaluation"""
    import requests
    
    # Get credentials from environment (like the evaluator will)
    email = os.getenv('EMAIL')
    secret = os.getenv('SECRET')
    
    if not email or not secret:
        print("ERROR: EMAIL and SECRET must be set in .env file")
        sys.exit(1)
    
    # Test different quiz URLs dynamically
    test_cases = [
        {
            "name": "Demo Quiz Chain",
            "url": "https://tds-llm-analysis.s-anand.net/demo"
        },
        # Add more test URLs here as needed
    ]
    
    base_url = "http://127.0.0.1:5000"
    
    print("=" * 70)
    print("DYNAMIC PARAMETER TEST - Simulating Real Evaluation")
    print("=" * 70)
    print(f"\nCredentials loaded from .env:")
    print(f"  Email: {email}")
    print(f"  Secret: {'*' * len(secret)}")
    print(f"\nTesting endpoint: {base_url}/quiz")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[TEST {i}] {test_case['name']}")
        print(f"Quiz URL: {test_case['url']}")
        print("-" * 70)
        
        # Build payload dynamically
        payload = {
            "email": email,
            "secret": secret,
            "url": test_case['url']
        }
        
        try:
            print("Sending POST request...")
            response = requests.post(
                f"{base_url}/quiz",
                json=payload,
                timeout=300  # 5 minutes max
            )
            
            print(f"\nResponse Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"SUCCESS")
                print(f"\nStatus: {result.get('status')}")
                
                if 'result' in result:
                    quiz_result = result['result']
                    print(f"Total Quizzes: {quiz_result.get('total_quizzes', 0)}")
                    print(f"Elapsed Time: {quiz_result.get('elapsed_time', 0):.2f}s")
                    
                    if 'results' in quiz_result:
                        print(f"\nQuiz Chain Results:")
                        for idx, quiz in enumerate(quiz_result['results'], 1):
                            print(f"\n  Quiz {idx}:")
                            print(f"    URL: {quiz.get('url', 'N/A')}")
                            print(f"    Answer: {quiz.get('answer', 'N/A')}")
                            print(f"    Correct: {quiz.get('correct', False)}")
                            if quiz.get('next_url'):
                                print(f"    Next URL: {quiz['next_url']}")
                            if quiz.get('error'):
                                print(f"    Error: {quiz['error']}")
                
            elif response.status_code == 403:
                print(f"AUTHENTICATION FAILED")
                print(f"Response: {response.json()}")
                print("\nPossible issues:")
                print("  - Email doesn't match server configuration")
                print("  - Secret doesn't match server configuration")
                
            elif response.status_code == 400:
                print(f"BAD REQUEST")
                print(f"Response: {response.json()}")
                
            else:
                print(f"UNEXPECTED STATUS CODE")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"CONNECTION FAILED")
            print("Make sure the Flask server is running:")
            print("  python app.py")
            
        except requests.exceptions.Timeout:
            print(f"REQUEST TIMEOUT")
            print("Quiz took longer than 5 minutes")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    print("\n" + "=" * 70)


def test_invalid_credentials():
    """Test that invalid credentials are properly rejected"""
    import requests
    
    print("\n" + "=" * 70)
    print("TESTING CREDENTIAL VALIDATION")
    print("=" * 70)
    
    base_url = "http://127.0.0.1:5000"
    test_url = "https://tds-llm-analysis.s-anand.net/demo"
    
    test_cases = [
        {
            "name": "Wrong Email",
            "email": "wrong@example.com",
            "secret": os.getenv('SECRET'),
            "expected": 403
        },
        {
            "name": "Wrong Secret",
            "email": os.getenv('EMAIL'),
            "secret": "wrong-secret",
            "expected": 403
        },
        {
            "name": "Missing Email",
            "email": None,
            "secret": os.getenv('SECRET'),
            "expected": 400
        },
        {
            "name": "Valid Credentials",
            "email": os.getenv('EMAIL'),
            "secret": os.getenv('SECRET'),
            "expected": 200
        }
    ]
    
    for test in test_cases:
        print(f"\n[TEST] {test['name']}")
        
        payload = {
            "url": test_url
        }
        if test['email']:
            payload['email'] = test['email']
        if test['secret']:
            payload['secret'] = test['secret']
        
        try:
            response = requests.post(
                f"{base_url}/quiz",
                json=payload,
                timeout=5
            )
            
            if response.status_code == test['expected']:
                print(f"  PASS - Got expected status {test['expected']}")
            else:
                print(f"  FAIL - Expected {test['expected']}, got {response.status_code}")
                print(f"  Response: {response.text}")
                
        except requests.exceptions.Timeout:
            if test['expected'] == 200:
                print(f"  TIMEOUT (but request was accepted)")
            else:
                print(f"  FAIL - Timeout")
        except Exception as e:
            print(f"  ERROR: {str(e)}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    print("\nDYNAMIC PARAMETER TESTING")
    print("This test uses environment variables instead of hardcoded values")
    print("This simulates how the actual evaluation will work\n")
    
    # Test valid requests with dynamic parameters
    test_dynamic_endpoint()
    
    # Test invalid credential handling
    test_invalid_credentials()
    
    print("\nDYNAMIC PARAMETER TEST COMPLETE\n")
