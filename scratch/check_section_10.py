with open('content/explorations/the-8051-when-time-becomes-a-signal.md', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('## 10. The Deeper Realization')
print(content[start:])
