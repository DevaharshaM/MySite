from bs4 import BeautifulSoup
import re

def check_nav(filepath):
    print("Checking navigation in:", filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for previous and next links
    prev_matches = re.findall(r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*nav-prev[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL)
    next_matches = re.findall(r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*nav-next[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL)
    
    # Or search for navigation buttons in general
    nav_links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>.*?Prev.*?</a>|<a[^>]*href="([^"]*)"[^>]*>.*?Next.*?</a>', content, re.IGNORECASE | re.DOTALL)
    print("Previous matches:", prev_matches)
    print("Next matches:", next_matches)
    
    # Search for "the-8051" links in the file
    all_links = re.findall(r'href="([^"]*the-8051[^"]*)"', content)
    print("8051-related links in page:", set(all_links))

check_nav('explorations/the-8051-where-software-touches-hardware/index.html')
print("-" * 50)
check_nav('explorations/the-8051-when-time-becomes-a-signal/index.html')
