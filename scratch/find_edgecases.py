import glob
import re

for fpath in glob.glob("content/explorations/*.md"):
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    if "edgecase" in text.lower() or "edge-case" in text.lower():
        print(fpath)
        for line in text.splitlines():
            if "edgecase" in line.lower() or "edge-case" in line.lower():
                print("  ", line[:100])
