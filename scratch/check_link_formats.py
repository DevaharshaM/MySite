import os, re

for fname in os.listdir('content/explorations'):
    if fname.endswith('.md'):
        with open(os.path.join('content/explorations', fname), 'r', encoding='utf-8') as f:
            content = f.read()
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in links:
            if 'the-8051' in url or 'architecture-of-time' in url or 'operating-systems' in url:
                print(f"{fname}: [{text}]({url})")
