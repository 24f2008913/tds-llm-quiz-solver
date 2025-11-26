from dotenv import load_dotenv
load_dotenv()

from browser_handler import BrowserHandler

url = "https://tds-llm-analysis.s-anand.net/demo-scrape-data?email=24f2008913@ds.study.iitm.ac.in"
print(f"Fetching: {url}")
print("="*70)

with BrowserHandler() as bh:
    content = bh.fetch_page_content(url)

text = content.get('result') or content.get('text', '')
html = content.get('html', '')

print("\nText content:")
print(text)
print("\n" + "="*70)
print("\nHTML (first 1000 chars):")
print(html[:1000])
