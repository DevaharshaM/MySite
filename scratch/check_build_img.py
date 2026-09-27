with open('build.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'blog-img-wrap' in line or '![' in line:
            print(f"{i+1}: {line.strip()}")
