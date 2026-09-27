import os
import xml.etree.ElementTree as ET

svg_dir = 'Images'
failed = []
passed = 0

for fname in sorted(os.listdir(svg_dir)):
    if fname.endswith('.svg'):
        fpath = os.path.join(svg_dir, fname)
        try:
            tree = ET.parse(fpath)
            passed += 1
        except Exception as e:
            failed.append((fname, str(e)))

print(f"Validated {passed + len(failed)} SVGs. Passed: {passed}, Failed: {len(failed)}")
for fname, err in failed:
    print(f"FAILED: {fname} -> {err}")
