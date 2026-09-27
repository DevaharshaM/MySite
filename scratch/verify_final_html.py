import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('explorations/the-8051-when-time-becomes-a-signal/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("1. Architecture of time link present:")
import re
arch_links = re.findall(r'<a[^>]*href="[^"]*the-architecture-of-time[^"]*"[^>]*>.*?</a>', content)
for l in arch_links:
    print("  ", l)

print("\n2. TMOD and TCON register frame diagrams present:")
print("   TMOD frame:", "TMOD (89H)" in content and "GATE" in content)
print("   TCON frame:", "TCON (88H)" in content and "TF0" in content)
print("   16-bit Counter 0 frame:", "TH0 (8CH)" in content and "TL0 (8AH)" in content)
print("   16-bit Counter 1 frame:", "TH1 (8DH)" in content and "TL1 (8BH)" in content)

print("\n3. EdgeCase configuration elements:")
print("   edgeCaseAction('set_source'):", "set_source" in content)
print("   edgeCaseAction('set_timer'):", "set_timer" in content)
print("   edgeCaseAction('set_mode'):", "set_mode" in content)
print("   pulse external pin button:", "tsim-btn-ext-pulse" in content)
