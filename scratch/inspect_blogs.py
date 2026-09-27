import json
import re

with open('content/content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
blogs = data['blogs']
print(f'Total blogs in content.json: {len(blogs)}')

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all id: "..." in script.js blogPosts
bp_match = re.search(r'const blogPosts = \[(.*?)\n\];', text, re.DOTALL)
if bp_match:
    bp_content = bp_match.group(1)
    ids_js = re.findall(r'id:\s*["\']([^"\']+)["\']', bp_content)
    print(f'Total blogPosts in script.js: {len(ids_js)}')
    
    # Let's check which categories are in script.js blogPosts
    categories = re.findall(r'category:\s*["\']([^"\']+)["\']', bp_content)
    from collections import Counter
    print('Categories in script.js blogPosts:', Counter(categories))
    
    ids_json = [b['id'] for b in blogs]
    diff = set(ids_json) - set(ids_js)
    print(f'IDs in content.json but NOT in script.js ({len(diff)}):')
    for d in sorted(diff):
        print('  -', d)


