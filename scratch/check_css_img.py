with open('style.css', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'img' in line:
            print(f"{i+1}: {line.strip()}")
