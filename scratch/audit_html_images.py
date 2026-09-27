import os, re
from bs4 import BeautifulSoup

html_path = 'explorations/the-8051-when-time-becomes-a-signal/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

imgs = soup.find_all('img')
print(f"Total img tags in page: {len(imgs)}")

for idx, img in enumerate(imgs):
    src = img.get('src')
    alt = img.get('alt', '')
    # Resolve src relative to html_path's dir
    rel_dir = os.path.dirname(html_path)
    abs_path = os.path.normpath(os.path.join(rel_dir, src))
    exists = os.path.exists(abs_path)
    size = os.path.getsize(abs_path) if exists else 0
    print(f"[{idx+1}] src: '{src}' | exists: {exists} ({size} bytes) | alt: '{alt}'")
