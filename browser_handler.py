"""
Browser Handler - Manages headless browser operations using Playwright
"""
import logging
from playwright.sync_api import sync_playwright, Browser, Page
import base64

logger = logging.getLogger(__name__)


class BrowserHandler:
    """Handles headless browser operations for rendering JavaScript pages"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    def __enter__(self):
        """Context manager entry"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        logger.info("Browser launched")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser closed")
    
    def fetch_page_content(self, url: str, wait_time: int = 3000) -> dict:
        """
        Fetch and render a JavaScript page
        
        Args:
            url: URL to fetch
            wait_time: Time to wait for page to render (milliseconds)
        
        Returns:
            dict with 'html', 'text', and 'title' keys
        """
        try:
            page = self.browser.new_page()
            logger.info(f"Navigating to: {url}")
            
            # Navigate to the page
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for dynamic content to render
            page.wait_for_timeout(wait_time)
            
            # Extract content
            html_content = page.content()
            text_content = page.inner_text('body')
            title = page.title()
            
            # Check for specific elements that might contain the quiz
            result_div = page.query_selector('#result')
            if result_div:
                result_text = result_div.inner_text()
                logger.info("Found #result element")
            else:
                result_text = None
            
            page.close()
            
            return {
                'html': html_content,
                'text': text_content,
                'title': title,
                'result': result_text
            }
            
        except Exception as e:
            logger.error(f"Error fetching page: {str(e)}")
            raise
    
    def decode_base64_content(self, encoded_str: str) -> str:
        """
        Decode base64 encoded content
        
        Args:
            encoded_str: Base64 encoded string
        
        Returns:
            Decoded string
        """
        try:
            decoded_bytes = base64.b64decode(encoded_str)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception as e:
            logger.error(f"Error decoding base64: {str(e)}")
            raise
    
    def download_file(self, page: Page, url: str, save_path: str) -> str:
        """
        Download a file from a URL
        
        Args:
            page: Playwright page object
            url: URL to download from
            save_path: Path to save the file
        
        Returns:
            Path to downloaded file
        """
        try:
            with page.expect_download() as download_info:
                page.goto(url)
            
            download = download_info.value
            download.save_as(save_path)
            logger.info(f"File downloaded to: {save_path}")
            
            return save_path
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise
    
    def extract_links(self, html: str) -> list:
        """
        Extract all links from HTML content
        
        Args:
            html: HTML content
        
        Returns:
            List of URLs
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            links.append({
                'url': a_tag['href'],
                'text': a_tag.get_text(strip=True)
            })
        
        return links
    
    def screenshot(self, url: str, save_path: str) -> str:
        """
        Take a screenshot of a page
        
        Args:
            url: URL to screenshot
            save_path: Path to save screenshot
        
        Returns:
            Path to screenshot
        """
        try:
            page = self.browser.new_page()
            page.goto(url, wait_until='networkidle')
            page.screenshot(path=save_path, full_page=True)
            page.close()
            
            logger.info(f"Screenshot saved to: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            raise
