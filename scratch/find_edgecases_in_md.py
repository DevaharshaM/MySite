import os

found = []
for fname in os.listdir("content/explorations"):
    if fname.endswith(".md"):
        fpath = os.path.join("content/explorations", fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if "```html" in content or "edgecase" in content:
            found.append((fname, "```html" in content, "edgecase" in content))

print(f"Total found: {len(found)}")
for item in found[:10]:
    print(item)
