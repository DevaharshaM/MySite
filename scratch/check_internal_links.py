import os
import re

def check_all_links():
    root = os.getcwd()
    html_files = []
    for dirpath, _, filenames in os.walk(root):
        if "scratch" in dirpath or ".git" in dirpath:
            continue
        for f in filenames:
            if f.endswith(".html"):
                html_files.append(os.path.join(dirpath, f))

    print(f"Scanning {len(html_files)} HTML files for internal links...")

    broken_links = []
    total_links = 0

    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all href and src
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        srcs = re.findall(r'src=["\']([^"\']+)["\']', content)

        rel_dir = os.path.dirname(file_path)

        for target in hrefs + srcs:
            # Ignore external, anchor-only, mailto, javascript, or placeholders
            if (target.startswith("http://") or target.startswith("https://") or
                target.startswith("#") or target.startswith("mailto:") or
                target.startswith("javascript:") or target.startswith("data:") or
                target == ""):
                continue

            total_links += 1

            clean_target = target.split("#")[0].split("?")[0]
            if not clean_target:
                continue

            # Handle root-relative vs relative
            if clean_target.startswith("/"):
                # E.g. /about/ -> root/about/index.html
                candidate1 = os.path.join(root, clean_target.lstrip("/"))
                candidate2 = os.path.join(root, clean_target.lstrip("/"), "index.html")
            else:
                candidate1 = os.path.normpath(os.path.join(rel_dir, clean_target))
                candidate2 = os.path.normpath(os.path.join(rel_dir, clean_target, "index.html"))

            if not (os.path.exists(candidate1) or os.path.exists(candidate2)):
                broken_links.append((os.path.relpath(file_path, root), target))

    print(f"Checked {total_links} internal references across {len(html_files)} pages.")
    if broken_links:
        print(f"Found {len(broken_links)} broken links:")
        for source, link in broken_links[:20]:
            print(f"  In {source}: {link}")
    else:
        print("[SUCCESS] All internal links and asset references resolve successfully!")

if __name__ == "__main__":
    check_all_links()
