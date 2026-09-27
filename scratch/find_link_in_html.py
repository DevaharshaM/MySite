import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('explorations/the-8051-where-software-touches-hardware/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'exploration-nav-grid' in line:
        for j in range(max(0, i-2), min(len(lines), i+16)):
            print(f"{j+1}: {lines[j].rstrip()[:120]}")
