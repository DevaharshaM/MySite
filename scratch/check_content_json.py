import json

with open('content/content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

blogs = data['blogs']
print(f"Total blogs in content.json: {len(blogs)}")

missing_fields = []
for b in blogs:
    for field in ['id', 'title', 'subtitle', 'date', 'tags', 'sections', 'closing']:
        if field not in b:
            missing_fields.append((b.get('id', 'unknown'), field))

print(f"Missing required fields: {len(missing_fields)}")
if missing_fields:
    print(missing_fields[:10])
