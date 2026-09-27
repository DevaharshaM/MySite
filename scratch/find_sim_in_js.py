with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)')
if idx != -1:
    print(f"Found timerSimAction at character offset {idx}")
    print(content[idx:idx+300])
else:
    print("Not found")
