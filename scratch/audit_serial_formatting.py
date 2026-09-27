import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepaths = [
    'content/explorations/the-8051-when-the-controller-learns-to-speak.md',
    'explorations/the-8051-when-the-controller-learns-to-speak/index.html'
]

latex_patterns = [
    r'\\frac',
    r'\\overline',
    r'\\mu[a-zA-Z]*',
    r'\\text\{',
    r'\\times',
    r'\\sum',
    r'frac\{',
    r'text\{',
    r'overline\{',
    r'\\left',
    r'\\right',
    r'\$[^$\n]+\$',
]

print("=== AUDITING SERIAL EXPLORATION FOR RAW LATEX / UNRENDERED MATH ===")
has_issues = False
for fp in filepaths:
    content = open(fp, 'r', encoding='utf-8').read()
    print(f"Checking {fp} ({len(content)} bytes)...")
    for pat in latex_patterns:
        matches = list(re.finditer(pat, content))
        if matches:
            has_issues = True
            print(f"  [WARNING] Found {len(matches)} match(es) for pattern '{pat}':")
            for m in matches[:5]:
                start = max(0, m.start() - 30)
                end = min(len(content), m.end() + 30)
                print(f"    ...{content[start:end].replace(chr(10), ' ')}...")

if not has_issues:
    print("\n[SUCCESS] Zero raw LaTeX or unrendered math patterns found in both Markdown and HTML!")
else:
    print("\n[NOTICE] Check warnings above.")
