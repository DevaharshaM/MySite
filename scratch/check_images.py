import os, re

with open('content/explorations/the-8051-when-time-becomes-a-signal.md', 'r', encoding='utf-8') as f:
    content = f.read()

images = re.findall(r'!\[.*?\]\((.*?)\)', content)
print("Found images:", images)

for img in images:
    # clean path
    img_clean = img.strip()
    exists = os.path.exists(img_clean)
    size = os.path.getsize(img_clean) if exists else 0
    print(f"Image: {img_clean} | Exists: {exists} | Size: {size} bytes")
