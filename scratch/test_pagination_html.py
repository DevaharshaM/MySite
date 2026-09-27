import re

with open('explorations/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pag_match = re.search(r'<div id="blogPagination"[^>]*>(.*?)</div>', html, re.DOTALL)
if not pag_match:
    print('[FAIL] #blogPagination not found in explorations/index.html')
    exit(1)

pag_content = pag_match.group(1).strip()
print('[PASS] Found #blogPagination in explorations/index.html!')
buttons = re.findall(r'<button[^>]*>([^<]+)</button>', pag_content)
print(f'Total buttons in pagination: {len(buttons)}')
safe_buttons = [b.encode('ascii', 'replace').decode('ascii') for b in buttons]
print(f'Buttons: {safe_buttons}')

# Check active page 1 button
assert '1' in buttons, "Page 1 button missing"
assert '13' in buttons, "Page 13 button missing"
assert 'Next →' in buttons, "Next button missing"
assert 'onclick="renderBlogs(2)"' in pag_content, "onclick renderBlogs(2) missing"
print('[SUCCESS] Pre-rendered pagination verified completely!')
