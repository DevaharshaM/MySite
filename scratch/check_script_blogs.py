with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

print("Does script.js fetch content.json?", "content.json" in content)
print("Does script.js define blogPosts?", "const blogPosts =" in content)

import re
matches = re.findall(r'id:\s*["\']([^"\']+)["\']', content[:20000])
print("First few IDs in script.js:", matches[:10])

# Check if there are other exploration IDs in script.js
last_explorations = re.findall(r'id:\s*["\'](the-8051-[^"\']+)["\']', content)
print("8051 exploration IDs in script.js:", set(last_explorations))
