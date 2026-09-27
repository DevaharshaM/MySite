with open('creator/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_url = "https://drive.google.com/file/d/1BXr4KyzmVKIraQVAOSr-tPsPYPG-GBk4/view?usp=sharing"

assert f'href="{target_url}"' in text, "Target URL missing or incorrect in creator/index.html"
assert 'target="_blank"' in text, "target='_blank' attribute missing"
assert 'rel="noopener noreferrer"' in text, "rel='noopener noreferrer' attribute missing"
assert 'View Resume' in text, "Button text 'View Resume' missing"

print("[SUCCESS] All Creator page View Resume requirements verified!")
