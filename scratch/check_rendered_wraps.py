import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('explorations/the-8051-when-time-becomes-a-signal/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
wraps = re.findall(r'<div class="blog-img-wrap">.*?</div>', content, re.DOTALL)
print(f"Found {len(wraps)} image wraps:")
for w in wraps:
    print(w)
