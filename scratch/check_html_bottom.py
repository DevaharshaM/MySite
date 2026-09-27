with open('explorations/the-8051-when-time-becomes-a-signal/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)-60, len(lines)):
    print(f"{i+1}: {lines[i].rstrip()[:120]}")
