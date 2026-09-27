with open('build.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'open(' in line and ('w' in line or 'write' in line):
            print(f"{i+1}: {line.strip()}")
        if 'script.js' in line or 'content.json' in line or 'sitemap.xml' in line:
            print(f"{i+1}: {line.strip()}")
