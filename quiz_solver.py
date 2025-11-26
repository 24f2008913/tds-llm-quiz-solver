"""
Quiz Solver - Main logic for solving quiz tasks
"""
import os
import logging
import time
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from browser_handler import BrowserHandler
from llm_handler import LLMHandler
from data_processor import DataProcessor
import json
import re
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

# Add file handler for debugging
file_handler = logging.FileHandler('quiz_solver_debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


class QuizSolver:
    """Main class for solving quiz tasks"""
    
    def __init__(self):
        self.email = os.getenv('EMAIL')
        self.secret = os.getenv('SECRET')
        self.timeout = int(os.getenv('QUIZ_TIMEOUT', 180))  # 3 minutes
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.llm = LLMHandler()
        self.data_processor = DataProcessor()
        
    def solve_quiz_chain(self, initial_url: str) -> Dict[str, Any]:
        """
        Solve a chain of quiz questions starting from initial_url
        
        Args:
            initial_url: The first quiz URL to solve
        
        Returns:
            Summary of results
        """
        results = []
        current_url = initial_url
        start_time = datetime.now()
        
        while current_url:
            # Check timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= self.timeout:
                logger.warning(f"Quiz timeout reached ({self.timeout}s)")
                break
            
            logger.info(f"Solving quiz at: {current_url}")
            
            try:
                result = self.solve_single_quiz(current_url, start_time)
                results.append(result)
                
                # Check if there's a next URL
                if result.get('correct') and result.get('next_url'):
                    current_url = result['next_url']
                    logger.info(f"Moving to next quiz: {current_url}")
                elif not result.get('correct'):
                    # If wrong and we have a next URL, we can skip or retry
                    if result.get('next_url'):
                        logger.info(f"Answer was wrong, but next URL provided: {result['next_url']}")
                        current_url = result['next_url']
                    else:
                        logger.info("Answer was wrong and no next URL. Ending chain.")
                        break
                else:
                    # Quiz complete
                    logger.info("Quiz chain completed successfully!")
                    break
                    
            except Exception as e:
                logger.error(f"Error solving quiz: {str(e)}", exc_info=True)
                results.append({
                    'url': current_url,
                    'error': str(e),
                    'correct': False
                })
                break
        
        return {
            'total_quizzes': len(results),
            'results': results,
            'elapsed_time': (datetime.now() - start_time).total_seconds()
        }
    
    def solve_single_quiz(self, quiz_url: str, start_time: datetime) -> Dict[str, Any]:
        """
        Solve a single quiz question
        
        Args:
            quiz_url: URL of the quiz
            start_time: When the quiz chain started (for timeout tracking)
        
        Returns:
            Result dict with answer and response
        """
        # Step 1: Fetch the quiz page
        with BrowserHandler() as browser:
            page_content = browser.fetch_page_content(quiz_url)
            
            # Step 2: Extract and parse the question
            question_data = self.parse_quiz_page(page_content, browser, quiz_url)
        
        # Step 3: Analyze the question using LLM
        analysis = self.llm.analyze_quiz_question(
            question_text=question_data['question'],
            context=question_data
        )
        
        logger.info(f"Question analysis: {json.dumps(analysis, indent=2)}")
        
        # Step 4: Solve the question
        answer = self.solve_question(question_data, analysis)
        
        logger.info(f"Raw answer from solve_question: {answer}")
        
        # Clean up answer if it's wrapped in markdown code blocks
        # BUT ONLY if it looks like an LLM response, not a scraped value
        if isinstance(answer, str) and len(answer) > 50:  # Only clean if it's a long response
            # Remove markdown code blocks
            answer = re.sub(r'^```(?:json)?\s*', '', answer.strip())
            answer = re.sub(r'\s*```$', '', answer.strip())
            # Try to parse as JSON if it looks like JSON
            if answer.strip().startswith('{'):
                try:
                    parsed = json.loads(answer)
                    # DON'T extract the 'answer' field - this is likely a template
                    # Just keep the whole thing and let the LLM figure it out
                    logger.warning(f"Answer looks like JSON template, keeping as-is")
                except json.JSONDecodeError:
                    pass
        
        # Step 5: Submit the answer
        submit_result = self.submit_answer(
            submit_url=question_data['submit_url'],
            quiz_url=quiz_url,
            answer=answer
        )
        
        return {
            'url': quiz_url,
            'question': question_data['question'],
            'answer': answer,
            'correct': submit_result.get('correct', False),
            'next_url': submit_result.get('url'),
            'reason': submit_result.get('reason'),
            'response': submit_result
        }
    
    def parse_quiz_page(self, page_content: Dict[str, Any], browser: BrowserHandler, base_url: str = None) -> Dict[str, Any]:
        """
        Parse the quiz page to extract question, submit URL, and any data sources
        
        Args:
            page_content: Content fetched from browser
            browser: Browser handler instance
            base_url: Base URL for resolving relative URLs
        
        Returns:
            Parsed question data
        """
        text = page_content.get('result') or page_content.get('text', '')
        html = page_content.get('html', '')
        
        # Extract links
        links = browser.extract_links(html)
        
        # Try to find submit URL - NO FALLBACK, must be extracted from page
        submit_url = None
        for pattern in [r'POST.*?(https?://[^\s<>"]+/submit[^\s<>"]*)',
                       r'Post.*?to\s+(https?://[^\s<>"]+)',
                       r'submit.*?(https?://[^\s<>"]+)',
                       r'https?://[^\s<>"]+/submit[^\s<>"]*']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                submit_url = match.group(1)
                logger.info(f"Extracted submit URL: {submit_url}")
                break
        
        if not submit_url:
            logger.error("CRITICAL: Submit URL not found in quiz page!")
            logger.error(f"Page text: {text[:500]}...")
            raise ValueError("Submit URL not found in quiz page. Cannot proceed without explicit submit endpoint.")
        
        # Extract scraping URLs (relative or absolute) - NO HARDCODED PATTERNS
        scrape_urls = []
        # Generic patterns that work for any URL structure
        scrape_pattern = r'Scrape\s+([/\w\-?=&%.]+)'
        matches = re.findall(scrape_pattern, text, re.IGNORECASE)
        for match in matches:
            if match:
                scrape_urls.append(match)
                logger.info(f"Extracted scrape URL: {match}")
        
        # Extract data file links
        data_files = []
        for link in links:
            url = link['url']
            if url and any(ext in url.lower() for ext in ['.pdf', '.csv', '.xlsx', '.json', '.txt']):
                data_files.append(url)
        
        return {
            'question': text,
            'submit_url': submit_url,
            'data_files': data_files,
            'scrape_urls': scrape_urls,
            'links': links,
            'html': html,
            'base_url': base_url
        }
    
    def solve_question(self, question_data: Dict[str, Any], analysis: Dict[str, Any]) -> Any:
        """
        Solve the question based on analysis
        
        Args:
            question_data: Parsed question data
            analysis: LLM analysis of the question
        
        Returns:
            The answer
        """
        task_type = analysis.get('task_type', 'unknown')
        data_sources = analysis.get('data_sources', [])
        base_url = question_data.get('base_url', '')
        
        logger.info(f"solve_question called. scrape_urls: {question_data.get('scrape_urls')}")
        logger.info(f"question_data keys: {list(question_data.keys())}")
        
        # Handle web scraping tasks - PRIORITY #1
        scrape_urls = question_data.get('scrape_urls', [])
        logger.info(f"Scrape URLs type: {type(scrape_urls)}, value: {scrape_urls}")
        
        if scrape_urls and len(scrape_urls) > 0:
            logger.info(f"==> SCRAPING PATH: Found {len(scrape_urls)} URLs to scrape")
            for scrape_path in scrape_urls:
                try:
                    logger.info(f"Processing scrape path: {scrape_path}")
                    # Make URL absolute
                    if not scrape_path.startswith('http'):
                        scrape_url = urljoin(base_url, scrape_path)
                    else:
                        scrape_url = scrape_path
                    
                    logger.info(f"Scraping URL: {scrape_url}")
                    with BrowserHandler() as browser:
                        scrape_content = browser.fetch_page_content(scrape_url)
                    
                    # Extract secret code or data
                    text = scrape_content.get('result') or scrape_content.get('text', '')
                    html = scrape_content.get('html', '')
                    
                    logger.info(f"Scraped text (first 500 chars): {text[:500]}")
                    
                    # Look for secret codes with multiple patterns
                    secret_patterns = [
                        r'secret\s*code\s+is\s+(\d+)',  # "Secret code is 64726"
                        r'secret\s*code[:\s]+(\d+)',  # "Secret code: 64726" or "Secret code 64726"
                        r'code[:\s]+is[:\s]+(\d+)',  # "code is 64726"
                        r'answer[:\s]+is[:\s]+(\d+)',  # "answer is 64726"
                        r'<strong>(\w+)</strong>',  # HTML bold tags
                        r'\b(\d{5,})\b',  # 5+ digit numbers
                        r'\b([A-Z0-9]{6,})\b',  # 6+ uppercase alphanumeric
                    ]
                    
                    for pattern in secret_patterns:
                        secret_match = re.search(pattern, text, re.IGNORECASE)
                        if secret_match:
                            secret_code = secret_match.group(1)
                            logger.info(f"Found secret code: {secret_code}")
                            return secret_code
                    
                    # If no pattern match, use LLM to extract
                    logger.info("No regex match, using LLM to extract secret code")
                    
                    # First try to extract any standalone alphanumeric code
                    words = text.split()
                    for word in words:
                        # Look for words that are likely secret codes (6+ alphanumeric)
                        if len(word) >= 6 and word.isalnum():
                            logger.info(f"Found likely secret code by word scan: {word}")
                            return word
                    
                    # Last resort: use LLM
                    answer = self.llm.generate_completion(
                        prompt=f"This text contains a secret code or answer value. Extract ONLY that value (no template, no JSON, no explanations):\\n\\n{text[:1000]}",
                        system_prompt="You extract secret codes. Return ONLY the code itself as plain text. Never return templates or examples.",
                        temperature=0,
                        max_tokens=50  # Limit to prevent long responses
                    )
                    cleaned = answer.strip().strip('`"\'{}()<>')  # Remove common wrapping chars
                    logger.info(f"LLM extracted: {cleaned}")
                    return cleaned
                    
                except Exception as e:
                    logger.error(f"Error scraping {scrape_path}: {str(e)}", exc_info=True)
                    # Don't fall through - raise or return error
                    raise
        else:
            logger.info("==> LLM PATH: No scrape URLs found, using LLM to solve")
        
        # Download and process data files if needed
        processed_data = None
        
        if data_sources or question_data['data_files']:
            files_to_process = data_sources or question_data['data_files']
            
            for file_url in files_to_process:
                try:
                    # Make URL absolute if needed
                    if not file_url.startswith('http'):
                        file_url = urljoin(base_url, file_url)
                    
                    logger.info(f"Downloading data file: {file_url}")
                    local_file = self.data_processor.download_file(file_url)
                    
                    # Process based on file type
                    if file_url.endswith('.pdf'):
                        processed_data = self.data_processor.process_pdf(local_file)
                    elif file_url.endswith('.csv'):
                        processed_data = self.data_processor.process_csv(local_file)
                    elif file_url.endswith('.xlsx') or file_url.endswith('.xls'):
                        processed_data = self.data_processor.process_excel(local_file)
                    elif file_url.endswith('.json'):
                        processed_data = self.data_processor.process_json(local_file)
                    
                except Exception as e:
                    logger.error(f"Error processing data file: {str(e)}")
        
        # If we need visualization
        if 'visualization' in task_type or 'chart' in question_data['question'].lower():
            # This would require creating a chart and returning base64
            pass
        
        # Safety check: if we have scrape_urls but got here, something went wrong
        if scrape_urls and len(scrape_urls) > 0:
            logger.error("BUG: Had scrape URLs but reached LLM generation. This shouldn't happen!")
            # Try to return a meaningful error instead of a template
            return "ERROR: Scraping failed"
        
        # Generate answer using LLM (only for non-scraping questions)
        answer = self.llm.generate_answer(
            question=question_data['question'],
            data=processed_data,
            analysis=analysis
        )
        
        return answer
    
    def submit_answer(self, submit_url: str, quiz_url: str, answer: Any) -> Dict[str, Any]:
        """
        Submit the answer to the quiz endpoint
        
        Args:
            submit_url: URL to submit to
            quiz_url: Original quiz URL
            answer: The answer to submit
        
        Returns:
            Response from submission
        """
        payload = {
            'email': self.email,
            'secret': self.secret,
            'url': quiz_url,
            'answer': answer
        }
        
        logger.info(f"Submitting answer to: {submit_url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                submit_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'correct': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
                
        except Exception as e:
            logger.error(f"Error submitting answer: {str(e)}")
            return {
                'correct': False,
                'error': str(e)
            }
