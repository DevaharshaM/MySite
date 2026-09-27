with open('script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Check matching parentheses, braces, brackets in the appended code
marker = '// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)'
idx = code.find(marker)
sim_part = code[idx:]

stack = []
pairs = {')': '(', '}': '{', ']': '['}
in_string = False
str_char = ''

for line_no, line in enumerate(sim_part.split('\n')):
    i = 0
    while i < len(line):
        ch = line[i]
        if in_string:
            if ch == '\\':
                i += 1
            elif ch == str_char:
                in_string = False
        else:
            if ch in ("'", '"', '`'):
                in_string = True
                str_char = ch
            elif ch in ('(', '{', '['):
                stack.append((ch, line_no + 1))
            elif ch in (')', '}', ']'):
                if not stack:
                    print(f"Error: unexpected {ch} at line {line_no+1}")
                else:
                    top, l = stack.pop()
                    if pairs[ch] != top:
                        print(f"Error: mismatched {ch} at line {line_no+1}, expected {top} from line {l}")
        i += 1

if stack:
    print(f"Unclosed items: {stack}")
else:
    print("All brackets, braces, and parentheses match perfectly in timerSimAction!")
