import re

def check_nav():
    with open('explorations/the-8051-memory-map/index.html', 'r', encoding='utf-8') as f:
        text = f.read()
        m = re.search(r'<div class="exploration-nav-grid">([\s\S]*?)</div>\s*</div>', text)
        if m:
            print('=== NAV in the-8051-memory-map ===')
            print(m.group(0))

    with open('explorations/the-8051-where-software-touches-hardware/index.html', 'r', encoding='utf-8') as f:
        text = f.read()
        m = re.search(r'<div class="exploration-nav-grid">([\s\S]*?)</div>\s*</div>', text)
        if m:
            print('=== NAV in the-8051-where-software-touches-hardware ===')
            print(m.group(0))

if __name__ == '__main__':
    check_nav()
