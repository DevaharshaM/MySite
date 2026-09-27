import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING NAVIGATION LINKS FOR SERIAL EXPLORATION ===")

p1 = open('explorations/the-8051-when-hardware-decides-to-interrupt/index.html', encoding='utf-8').read()
m_next1 = re.search(r'<div class="nav-next"[^>]*>([\s\S]*?)</div>', p1)
print("\n--- INTERRUPT -> NEXT BLOCK ---")
print(m_next1.group(0) if m_next1 else "None")

p2 = open('explorations/the-8051-when-the-controller-learns-to-speak/index.html', encoding='utf-8').read()
m_prev2 = re.search(r'<div class="nav-prev"[^>]*>([\s\S]*?)</div>', p2)
print("\n--- SERIAL -> PREV BLOCK ---")
print(m_prev2.group(0) if m_prev2 else "None")

m_next2 = re.search(r'<div class="nav-next"[^>]*>([\s\S]*?)</div>', p2)
print("\n--- SERIAL -> NEXT BLOCK ---")
print(m_next2.group(0) if m_next2 else "None")
