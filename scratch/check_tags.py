import json

with open('content/content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

missing_cat_in_tags = []
for b in data['blogs']:
    cat = b.get('category', '')
    tags = b.get('tags', [])
    if cat and cat not in tags:
        missing_cat_in_tags.append((b['id'], cat, tags))

print(f"Total blogs where category is NOT in tags: {len(missing_cat_in_tags)}")
for m in missing_cat_in_tags[:10]:
    print(m)
