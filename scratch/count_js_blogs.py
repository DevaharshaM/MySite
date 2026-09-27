with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
in_blogposts = False
ids = []
for i, line in enumerate(lines):
    if 'const blogPosts = [' in line:
        in_blogposts = True
    if in_blogposts:
        if 'const demoPosts = [' in line:
            in_blogposts = False
            break
        # Match "id:" at indentation 2 or 4
        if line.strip().startswith('id:') or line.strip().startswith('"id":'):
            clean = line.strip().split(':', 1)[1].strip().strip('",\'')
            ids.append(clean)

print(f'Total blogPosts parsed in script.js: {len(ids)}')
