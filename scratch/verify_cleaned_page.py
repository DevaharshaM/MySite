import re
from bs4 import BeautifulSoup

html_path = 'explorations/the-8051-when-time-becomes-a-signal/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("1. Heading count and titles:")
headings = [h.text.strip() for h in soup.find_all(['h2', 'h3']) if not any(x in h.text.lower() for x in ['cookie', 'legal', 'nav', 'menu', 'about', 'filter', 'contact'])]
for h in headings:
    print("  ", h)

print("\n2. Checking for removed EdgeCase:")
print("   EdgeCase present?", "EdgeCase" in html or "edgecase" in html.lower() and "edgecase-container" in html)
print("   Simulator root present?", "edgecase-workbench-root" in html or "tsim-" in html)

print("\n3. Checking for removed Waveform section:")
print("   Waveform heading present?", "When Counting Becomes a Waveform" in html)
print("   intel_8051_timer_to_waveform.svg present?", "intel_8051_timer_to_waveform.svg" in html)

print("\n4. Architecture of Time Link check:")
arch_links = soup.find_all('a', href=re.compile(r'the-architecture-of-time'))
for l in arch_links:
    print("   Link:", l)
    print("   Has target='_blank'?", l.get('target') == '_blank')

print("\n5. Raw Math audit in generated HTML:")
math_patterns = [r'\\frac', r'\\overline', r'\\mu\b', r'\\text\{', r'frac\{', r'overline\{', r'ext\{']
found_bad = False
for p in math_patterns:
    m = re.findall(p, html)
    if m:
        print(f"   BAD PATTERN FOUND {p}: {len(m)}")
        found_bad = True
if not found_bad:
    print("   ZERO raw math artifacts in generated HTML!")

print("\n6. Registered images in page:")
imgs = soup.find_all('img')
for img in imgs:
    src = img.get('src')
    if 'intel_8051' in src:
        print("  ", src)
