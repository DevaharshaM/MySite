import glob
import os
import xml.etree.ElementTree as ET

def check_placeholders():
    print("=== CHECK 1: PLACEHOLDER AUDIT ===")
    targets = [
        "// Coming soon",
        "Under construction",
        "coming soon",
        "lorem ipsum"
    ]
    html_files = glob.glob("**/*.html", recursive=True)
    print(f"Scanning {len(html_files)} HTML files...")
    
    findings = {t: [] for t in targets}
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        for t in targets:
            if t.lower() in content.lower():
                findings[t].append(file_path)
                
    for t, files in findings.items():
        print(f"Target '{t}': {len(files)} files matched")
        if files:
            for f in files[:5]:
                print(f"   - {f}")
    return findings

def check_sitemap():
    print("\n=== CHECK 2: SITEMAP.XML AUDIT ===")
    sitemap_path = "sitemap.xml"
    if not os.path.exists(sitemap_path):
        print("ERROR: sitemap.xml not found")
        return
        
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    
    locs = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]
    print(f"Total sitemap entries: {len(locs)}")
    
    expected_included = [
        "https://prajnaedge.dev/",
        "https://prajnaedge.dev/products/",
        "https://prajnaedge.dev/playground/",
        "https://prajnaedge.dev/playground-on-device-ai/",
        "https://prajnaedge.dev/playground-edge-ai/",
        "https://prajnaedge.dev/about/",
        "https://prajnaedge.dev/contact/",
        "https://prajnaedge.dev/explorations/",
        "https://prajnaedge.dev/demonstrations/"
    ]
    
    expected_excluded = [
        "https://prajnaedge.dev/domain-select/",
        "https://prajnaedge.dev/foundation-select/"
    ]
    
    for url in expected_included:
        status = "PASS" if url in locs else "FAIL"
        print(f"[{status}] Included: {url}")
        
    for url in expected_excluded:
        status = "PASS" if url not in locs else "FAIL"
        print(f"[{status}] Excluded: {url}")

def check_robots_meta():
    print("\n=== CHECK 3: ROBOTS META AUDIT ===")
    routes = {
        "products/index.html": "index, follow",
        "playground-on-device-ai/index.html": "index, follow",
        "domain-select/index.html": "noindex, follow",
        "foundation-select/index.html": "noindex, follow",
        "index.html": "index, follow"
    }
    
    for path, expected_robots in routes.items():
        if not os.path.exists(path):
            print(f"ERROR: {path} not found")
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        found = False
        for line in content.splitlines():
            if 'meta name="robots"' in line:
                found = True
                status = "PASS" if expected_robots in line else "FAIL"
                print(f"[{status}] {path} -> {line.strip()} (Expected: {expected_robots})")
                break
        if not found:
            print(f"[FAIL] {path} has no robots meta tag")

if __name__ == "__main__":
    check_placeholders()
    check_sitemap()
    check_robots_meta()
