"""Test scrape URL extraction"""
import re

test_text = """Scrape /demo-scrape-data?email=24f2008913@ds.study.iitm.ac.in (relative to this page). Get the secret code from this page. POST the secret code back to /submit
{
  "email": "24f2008913@ds.study.iitm.ac.in",
  "secret": "your secret",
  "url": "this page's URL",
  "answer": "the secret code you scraped"
}
"""

print("Testing scrape URL extraction regex...")
print("="*60)

scrape_pattern = r'Scrape\s+([/\w-]+(?:\?[^\s]+)?)|/demo-scrape[^\s<>"]*'
matches = re.findall(scrape_pattern, test_text, re.IGNORECASE)
print(f"Pattern: {scrape_pattern}")
print(f"Matches: {matches}")

# Better pattern
scrape_pattern2 = r'Scrape\s+(/[^\s\)]+)'
matches2 = re.findall(scrape_pattern2, test_text, re.IGNORECASE)
print(f"\nBetter pattern: {scrape_pattern2}")
print(f"Matches: {matches2}")
