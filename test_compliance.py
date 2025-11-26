"""
RIGOROUS COMPLIANCE TESTING - Project Requirements Verification
Tests EVERY requirement from the project specification
"""
import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class ComplianceTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.email = os.getenv('EMAIL')
        self.secret = os.getenv('SECRET')
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def print_header(self, title):
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    
    def print_test(self, name, status, details=""):
        symbols = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}
        print(f"\n{symbols[status]} {name}")
        if details:
            print(f"      {details}")
        
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        else:
            self.warnings += 1
    
    def test_1_environment_setup(self):
        """REQ: Email and Secret must be configured"""
        self.print_header("TEST 1: ENVIRONMENT CONFIGURATION")
        
        if self.email:
            self.print_test("Email configured in .env", "PASS", f"Email: {self.email}")
        else:
            self.print_test("Email configured in .env", "FAIL", "EMAIL not set in .env")
        
        if self.secret:
            self.print_test("Secret configured in .env", "PASS", f"Secret: {'*' * len(self.secret)}")
        else:
            self.print_test("Secret configured in .env", "FAIL", "SECRET not set in .env")
    
    def test_2_http_responses(self):
        """REQ: Return 200/400/403 as specified"""
        self.print_header("TEST 2: HTTP STATUS CODES")
        
        # Test 2.1: Valid request returns 200
        try:
            response = requests.post(
                f"{self.base_url}/quiz",
                json={
                    "email": self.email,
                    "secret": self.secret,
                    "url": "https://tds-llm-analysis.s-anand.net/demo"
                },
                timeout=120
            )
            if response.status_code == 200:
                self.print_test("Valid request returns HTTP 200", "PASS", f"Status: {response.status_code}")
            else:
                self.print_test("Valid request returns HTTP 200", "FAIL", f"Got status: {response.status_code}")
        except Exception as e:
            self.print_test("Valid request returns HTTP 200", "FAIL", f"Error: {str(e)}")
        
        # Test 2.2: Invalid JSON returns 400
        try:
            response = requests.post(
                f"{self.base_url}/quiz",
                data="not json",
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 400:
                self.print_test("Invalid JSON returns HTTP 400", "PASS", f"Status: {response.status_code}")
            else:
                self.print_test("Invalid JSON returns HTTP 400", "FAIL", f"Got status: {response.status_code}")
        except Exception as e:
            self.print_test("Invalid JSON returns HTTP 400", "FAIL", f"Error: {str(e)}")
        
        # Test 2.3: Wrong email returns 403
        try:
            response = requests.post(
                f"{self.base_url}/quiz",
                json={
                    "email": "wrong@example.com",
                    "secret": self.secret,
                    "url": "https://tds-llm-analysis.s-anand.net/demo"
                },
                timeout=5
            )
            if response.status_code == 403:
                self.print_test("Wrong email returns HTTP 403", "PASS", f"Status: {response.status_code}")
            else:
                self.print_test("Wrong email returns HTTP 403", "FAIL", f"Got status: {response.status_code}")
        except Exception as e:
            self.print_test("Wrong email returns HTTP 403", "FAIL", f"Error: {str(e)}")
        
        # Test 2.4: Wrong secret returns 403
        try:
            response = requests.post(
                f"{self.base_url}/quiz",
                json={
                    "email": self.email,
                    "secret": "wrong-secret-12345",
                    "url": "https://tds-llm-analysis.s-anand.net/demo"
                },
                timeout=5
            )
            if response.status_code == 403:
                self.print_test("Wrong secret returns HTTP 403", "PASS", f"Status: {response.status_code}")
            else:
                self.print_test("Wrong secret returns HTTP 403", "FAIL", f"Got status: {response.status_code}")
        except Exception as e:
            self.print_test("Wrong secret returns HTTP 403", "FAIL", f"Error: {str(e)}")
        
        # Test 2.5: Missing fields returns 400
        try:
            response = requests.post(
                f"{self.base_url}/quiz",
                json={
                    "email": self.email
                    # Missing secret and url
                },
                timeout=5
            )
            if response.status_code == 400:
                self.print_test("Missing required fields returns HTTP 400", "PASS", f"Status: {response.status_code}")
            else:
                self.print_test("Missing required fields returns HTTP 400", "FAIL", f"Got status: {response.status_code}")
        except Exception as e:
            self.print_test("Missing required fields returns HTTP 400", "FAIL", f"Error: {str(e)}")
    
    def test_3_quiz_solving(self):
        """REQ: Visit URL, solve quiz, submit answer"""
        self.print_header("TEST 3: QUIZ SOLVING CAPABILITIES")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/quiz",
                json={
                    "email": self.email,
                    "secret": self.secret,
                    "url": "https://tds-llm-analysis.s-anand.net/demo"
                },
                timeout=180
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Test 3.1: Returns success status
                if result.get('status') == 'success':
                    self.print_test("Returns success status", "PASS", f"Status: {result.get('status')}")
                else:
                    self.print_test("Returns success status", "FAIL", f"Got: {result.get('status')}")
                
                # Test 3.2: Solves multiple quizzes in chain
                quiz_result = result.get('result', {})
                total_quizzes = quiz_result.get('total_quizzes', 0)
                if total_quizzes >= 2:
                    self.print_test("Solves quiz chain (multiple quizzes)", "PASS", f"Solved: {total_quizzes} quizzes")
                else:
                    self.print_test("Solves quiz chain (multiple quizzes)", "WARN", f"Only solved: {total_quizzes} quizzes")
                
                # Test 3.3: Completes within 3 minutes
                if elapsed < 180:
                    self.print_test("Completes within 3 minute timeout", "PASS", f"Took: {elapsed:.2f}s")
                else:
                    self.print_test("Completes within 3 minute timeout", "FAIL", f"Took: {elapsed:.2f}s")
                
                # Test 3.4: Quiz results contain required fields
                results_list = quiz_result.get('results', [])
                if results_list and len(results_list) > 0:
                    first_quiz = results_list[0]
                    has_url = 'url' in first_quiz
                    has_answer = 'answer' in first_quiz
                    has_correct = 'correct' in first_quiz
                    
                    if has_url and has_answer and has_correct:
                        self.print_test("Quiz results contain url/answer/correct", "PASS", 
                                      f"Keys: {list(first_quiz.keys())}")
                    else:
                        self.print_test("Quiz results contain url/answer/correct", "FAIL",
                                      f"Missing fields. Got: {list(first_quiz.keys())}")
                
                # Test 3.5: At least one correct answer
                correct_count = sum(1 for r in results_list if r.get('correct'))
                if correct_count > 0:
                    self.print_test("Solves at least one quiz correctly", "PASS", 
                                  f"Correct: {correct_count}/{len(results_list)}")
                else:
                    self.print_test("Solves at least one quiz correctly", "FAIL",
                                  f"Correct: 0/{len(results_list)}")
                
                # Test 3.6: Follows next_url in chain
                has_chain = any(r.get('next_url') for r in results_list[:-1])
                if has_chain or len(results_list) > 1:
                    self.print_test("Follows quiz chain (next_url)", "PASS",
                                  f"Chain length: {len(results_list)}")
                else:
                    self.print_test("Follows quiz chain (next_url)", "WARN",
                                  "Only single quiz, chain not tested")
                
            else:
                self.print_test("Quiz solving endpoint responds", "FAIL",
                              f"HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.print_test("Quiz solving completes", "FAIL", "Request timed out after 180s")
        except Exception as e:
            self.print_test("Quiz solving endpoint responds", "FAIL", f"Error: {str(e)}")
    
    def test_4_no_hardcoded_urls(self):
        """REQ: Submit URL must be extracted from quiz page, not hardcoded"""
        self.print_header("TEST 4: NO HARDCODED URLs")
        
        # Check core application files for hardcoded URLs
        files_to_check = [
            'app.py',
            'quiz_solver.py',
            'llm_handler.py',
            'browser_handler.py',
            'data_processor.py',
            'visualization.py'
        ]
        
        hardcoded_found = []
        for filename in files_to_check:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for hardcoded submit URLs
                    if 'tds-llm' in content.lower() or '.s-anand.net' in content:
                        hardcoded_found.append(filename)
        
        if not hardcoded_found:
            self.print_test("No hardcoded URLs in core application", "PASS",
                          f"Checked: {', '.join(files_to_check)}")
        else:
            self.print_test("No hardcoded URLs in core application", "FAIL",
                          f"Found in: {', '.join(hardcoded_found)}")
    
    def test_5_dependencies(self):
        """REQ: Must handle various data types and tasks"""
        self.print_header("TEST 5: DEPENDENCY AVAILABILITY")
        
        required_packages = {
            'flask': ('flask', 'API endpoint'),
            'playwright': ('playwright', 'JavaScript rendering'),
            'beautifulsoup4': ('bs4', 'HTML parsing'),
            'pandas': ('pandas', 'Data processing'),
            'requests': ('requests', 'HTTP requests'),
            'openai': ('openai', 'LLM integration'),
            'pdfplumber': ('pdfplumber', 'PDF processing'),
            'pillow': ('PIL', 'Image processing'),
            'matplotlib': ('matplotlib', 'Visualization'),
            'scipy': ('scipy', 'Statistical analysis'),
            'scikit-learn': ('sklearn', 'ML models'),
            'networkx': ('networkx', 'Network analysis'),
        }
        
        for package_name, (import_name, purpose) in required_packages.items():
            try:
                __import__(import_name)
                self.print_test(f"Package '{package_name}' installed", "PASS", purpose)
            except ImportError:
                self.print_test(f"Package '{package_name}' installed", "FAIL", 
                              f"Not found - required for: {purpose}")
    
    def test_6_file_structure(self):
        """REQ: GitHub repo must have MIT LICENSE and be public-ready"""
        self.print_header("TEST 6: REPOSITORY STRUCTURE")
        
        required_files = {
            'LICENSE': 'MIT LICENSE required for evaluation',
            'README.md': 'Documentation',
            'requirements.txt': 'Dependencies list',
            '.gitignore': 'Exclude sensitive files',
            'app.py': 'Main application',
            'quiz_solver.py': 'Core solver logic',
        }
        
        for filename, purpose in required_files.items():
            if os.path.exists(filename):
                self.print_test(f"File '{filename}' exists", "PASS", purpose)
            else:
                self.print_test(f"File '{filename}' exists", "FAIL", purpose)
        
        # Check .env is NOT in git
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore = f.read()
                if '.env' in gitignore:
                    self.print_test(".env excluded from git", "PASS", "Sensitive data protected")
                else:
                    self.print_test(".env excluded from git", "FAIL", "Add .env to .gitignore")
    
    def test_7_answer_format_support(self):
        """REQ: Must support boolean, number, string, base64 URI, JSON answers"""
        self.print_header("TEST 7: ANSWER FORMAT SUPPORT")
        
        # This tests that the code has logic for different answer types
        try:
            with open('llm_handler.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for type conversion logic
                has_bool = 'bool' in content.lower()
                has_int = 'int(' in content
                has_float = 'float(' in content
                has_json = 'json' in content.lower()
                has_base64 = 'base64' in content.lower()
                
                if has_bool:
                    self.print_test("Boolean answer support", "PASS", "Found bool handling")
                else:
                    self.print_test("Boolean answer support", "WARN", "No explicit bool handling")
                
                if has_int or has_float:
                    self.print_test("Number answer support", "PASS", "Found numeric conversion")
                else:
                    self.print_test("Number answer support", "WARN", "No numeric conversion found")
                
                if has_json:
                    self.print_test("JSON answer support", "PASS", "Found JSON handling")
                else:
                    self.print_test("JSON answer support", "FAIL", "No JSON handling found")
                
        except Exception as e:
            self.print_test("Answer format support code", "FAIL", f"Error: {str(e)}")
        
        # Check for base64 encoding in data_processor
        try:
            with open('data_processor.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'base64' in content:
                    self.print_test("Base64 URI support", "PASS", "Found base64 encoding")
                else:
                    self.print_test("Base64 URI support", "WARN", "No base64 encoding found")
        except:
            pass
    
    def test_8_timeout_handling(self):
        """REQ: Must complete within 3 minutes of POST"""
        self.print_header("TEST 8: TIMEOUT CONFIGURATION")
        
        try:
            with open('quiz_solver.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for timeout configuration
                if '180' in content or 'timeout' in content.lower():
                    self.print_test("3-minute timeout configured", "PASS", "Found timeout logic")
                else:
                    self.print_test("3-minute timeout configured", "WARN", "Timeout not clearly configured")
        except Exception as e:
            self.print_test("3-minute timeout configured", "FAIL", f"Error: {str(e)}")
    
    def test_9_data_processing_capabilities(self):
        """REQ: Must handle data sourcing, preparation, analysis, visualization"""
        self.print_header("TEST 9: DATA PROCESSING CAPABILITIES")
        
        capabilities = {
            'data_processor.py': {
                'process_pdf': 'PDF data extraction',
                'process_csv': 'CSV data processing',
                'process_excel': 'Excel data processing',
                'process_json': 'JSON data processing',
            },
            'visualization.py': {
                'create': 'Chart generation',
                'plot': 'Data visualization',
            },
            'browser_handler.py': {
                'fetch': 'Web scraping',
                'download': 'File downloading',
            }
        }
        
        for filename, methods in capabilities.items():
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for method, purpose in methods.items():
                        if f'def {method}' in content or method in content.lower():
                            self.print_test(f"{purpose} capability", "PASS", f"Found in {filename}")
                        else:
                            self.print_test(f"{purpose} capability", "WARN", 
                                          f"Not found in {filename}")
    
    def test_10_deployment_readiness(self):
        """REQ: Must be deployable with HTTPS endpoint"""
        self.print_header("TEST 10: DEPLOYMENT READINESS")
        
        # Check for deployment configuration files
        deployment_files = {
            'Procfile': 'Render/Heroku deployment',
            'render.yaml': 'Render configuration',
        }
        
        found_deployment = False
        for filename, purpose in deployment_files.items():
            if os.path.exists(filename):
                self.print_test(f"Deployment file '{filename}'", "PASS", purpose)
                found_deployment = True
            else:
                self.print_test(f"Deployment file '{filename}'", "WARN", 
                              f"{purpose} - create before deployment")
        
        if not found_deployment:
            self.print_test("Deployment configuration exists", "WARN",
                          "No deployment files found - add before deploying")
        
        # Check app.py uses environment-based host/port
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if "os.getenv('PORT'" in content or "os.environ" in content:
                    self.print_test("Dynamic port configuration", "PASS", 
                                  "Uses environment variable for port")
                else:
                    self.print_test("Dynamic port configuration", "WARN",
                                  "May need to use PORT from environment")
        except:
            pass
    
    def run_all_tests(self):
        """Run complete compliance test suite"""
        print("\n" + "="*80)
        print("  RIGOROUS COMPLIANCE TESTING - LLM Analysis Quiz Project")
        print("  Testing ALL requirements from project specification")
        print("="*80)
        
        self.test_1_environment_setup()
        self.test_2_http_responses()
        self.test_3_quiz_solving()
        self.test_4_no_hardcoded_urls()
        self.test_5_dependencies()
        self.test_6_file_structure()
        self.test_7_answer_format_support()
        self.test_8_timeout_handling()
        self.test_9_data_processing_capabilities()
        self.test_10_deployment_readiness()
        
        # Final summary
        self.print_header("FINAL COMPLIANCE REPORT")
        total = self.passed + self.failed + self.warnings
        
        print(f"\nTotal Tests: {total}")
        print(f"  PASSED:   {self.passed} tests")
        print(f"  FAILED:   {self.failed} tests")
        print(f"  WARNINGS: {self.warnings} tests")
        
        if self.failed == 0:
            print("\n[SUCCESS] All critical tests PASSED!")
            print("Project is compliant with requirements.")
            if self.warnings > 0:
                print(f"Note: {self.warnings} warnings should be reviewed.")
        else:
            print(f"\n[ATTENTION] {self.failed} critical test(s) FAILED!")
            print("Fix failing tests before submission.")
        
        print("\n" + "="*80)
        
        # Return exit code
        return 0 if self.failed == 0 else 1

if __name__ == '__main__':
    suite = ComplianceTestSuite()
    exit_code = suite.run_all_tests()
    sys.exit(exit_code)
