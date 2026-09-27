import re

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('const blogPosts = [')
end = text.find('const demoPosts = [')
block = text[start:end]

posts = re.findall(r'id:\s*["\']([^"\']+)["\'],\s*category:\s*["\']([^"\']+)["\']', block)
print(f"Total found in script.js blogPosts: {len(posts)}")
from collections import Counter
print(Counter([p[1] for p in posts]))
for p in posts:
    print(f"  {p[1]}: {p[0]}")
