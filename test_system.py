"""
Test script to verify the quiz solver locally
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test that environment is properly configured"""
    print("=== Testing Environment Configuration ===\n")
    
    required_vars = ['EMAIL', 'SECRET']
    optional_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * len(value[:10])}")
        else:
            print(f"✗ {var}: NOT SET (required)")
            all_good = False
    
    print()
    
    has_llm_key = False
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * len(value[:10])}")
            has_llm_key = True
        else:
            print(f"○ {var}: not set (optional)")
    
    if not has_llm_key:
        print("\n⚠ Warning: No LLM API key configured. At least one is needed.")
        all_good = False
    
    print()
    return all_good


def test_imports():
    """Test that all required packages are installed"""
    print("=== Testing Package Imports ===\n")
    
    packages = [
        ('flask', 'Flask'),
        ('playwright.sync_api', 'Playwright'),
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('requests', 'Requests'),
        ('bs4', 'BeautifulSoup4'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('pdfplumber', 'PDFPlumber'),
        ('matplotlib', 'Matplotlib'),
    ]
    
    all_good = True
    
    for module, name in packages:
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_good = False
    
    print()
    return all_good


def test_browser():
    """Test that Playwright browser is installed"""
    print("=== Testing Playwright Browser ===\n")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://www.google.com')
            title = page.title()
            browser.close()
        
        print(f"✓ Chromium browser working (tested with Google)")
        print(f"  Page title: {title}\n")
        return True
        
    except Exception as e:
        print(f"✗ Browser test failed: {str(e)}")
        print("  Run: playwright install chromium\n")
        return False


def test_llm_connection():
    """Test LLM API connection"""
    print("=== Testing LLM Connection ===\n")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    all_good = False
    
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'test successful'"}],
                max_tokens=10
            )
            
            result = response.choices[0].message.content
            print(f"✓ OpenAI API working")
            print(f"  Response: {result}\n")
            all_good = True
            
        except Exception as e:
            print(f"✗ OpenAI API error: {str(e)}\n")
    
    if anthropic_key:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Say 'test successful'"}]
            )
            
            result = response.content[0].text
            print(f"✓ Anthropic API working")
            print(f"  Response: {result}\n")
            all_good = True
            
        except Exception as e:
            print(f"✗ Anthropic API error: {str(e)}\n")
    
    return all_good


def test_flask_app():
    """Test that Flask app starts"""
    print("=== Testing Flask Application ===\n")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print(f"✓ Health endpoint working")
                print(f"  Response: {response.json}\n")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}\n")
                return False
            
            # Test invalid request
            response = client.post('/quiz', json={})
            if response.status_code == 400:
                print(f"✓ Validation working (rejected empty request)")
            else:
                print(f"⚠ Validation may not be working properly\n")
            
            # Test invalid credentials
            response = client.post('/quiz', json={
                'email': 'wrong',
                'secret': 'wrong',
                'url': 'test'
            })
            if response.status_code == 403:
                print(f"✓ Authentication working (rejected invalid credentials)\n")
            else:
                print(f"⚠ Authentication may not be working properly\n")
        
        return True
        
    except Exception as e:
        print(f"✗ Flask app error: {str(e)}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("LLM Quiz Solver - System Test")
    print("=" * 50)
    print()
    
    results = {
        'Environment': test_environment(),
        'Packages': test_imports(),
        'Browser': test_browser(),
        'LLM API': test_llm_connection(),
        'Flask App': test_flask_app(),
    }
    
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    print()
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test:.<30} {status}")
    
    print()
    
    if all(results.values()):
        print("🎉 All tests passed! Your system is ready.")
        print("\nNext steps:")
        print("1. Review your .env file configuration")
        print("2. Test with the demo quiz")
        print("3. Deploy to your chosen platform")
        print("4. Submit the Google Form")
        return 0
    else:
        print("⚠ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
