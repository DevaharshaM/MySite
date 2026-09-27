import os
import re

dir_path = 'content/explorations'
files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

cats = {}
for fname in files:
    with open(os.path.join(dir_path, fname), 'r', encoding='utf-8') as f:
        txt = f.read()
    cat_match = re.search(r'category:\s*["\']?([^"\'\n]+)', txt)
    cat = cat_match.group(1).strip() if cat_match else 'Unknown'
    cats[cat] = cats.get(cat, 0) + 1

print(f"Total markdown explorations: {len(files)}")
for c, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {cnt}")
