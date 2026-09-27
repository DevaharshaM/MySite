import re

with open('explorations/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=== TEST A: STATIC HTML INSPECTION (BEFORE JS) ===')
start_tag = 'id="blogList"'
start_idx = html.find(start_tag)
if start_idx == -1:
    print('[FAIL] Could not find #blogList in explorations/index.html')
    exit(1)

content_start = html.find('>', start_idx) + 1
end_idx = html.find('<div class="page" id="page-demos">', content_start)
# Backtrack to the </div> closing #blogList
blog_block = html[content_start:end_idx]

cards = re.findall(r'<a href="([^"]+)" class="blog-card"[^>]*>(.*?)</a>', blog_block, re.DOTALL)
print(f'[PASS] Found {len(cards)} pre-rendered cards in #blogList')

for idx, (href, body) in enumerate(cards):
    title_m = re.search(r'class="blog-title"[^>]*>([^<]+)<', body)
    subtitle_m = re.search(r'class="blog-subtitle"[^>]*>([^<]+)<', body)
    date_m = re.search(r'<span>([^<]+)</span>', body)
    tags_m = re.findall(r'class="tag">([^<]+)</span>', body)
    print(f'  Card {idx+1}:')
    print(f'    Title: {title_m.group(1).strip() if title_m else "MISSING"}')
    print(f'    Subtitle: {subtitle_m.group(1).strip() if subtitle_m else "MISSING"}')
    print(f'    Date: {date_m.group(1).strip() if date_m else "MISSING"}')
    print(f'    Tags: {tags_m}')
    print(f'    href: {href}')
