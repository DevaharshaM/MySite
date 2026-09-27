import glob
import os
import re
import xml.etree.ElementTree as ET

def verify_all():
    print("=" * 60)
    print("PRAJNAEDGE VERIFICATION SUITE")
    print("=" * 60)
    
    # 1. Products Page Checks
    print("\n[TEST 1] PRODUCTS PAGE VERIFICATION")
    with open("products/index.html", "r", encoding="utf-8") as f:
        prod_html = f.read()
        
    # Extract page-products section
    prod_section = prod_html.split('id="page-products"')[1].split('id="page-playground"')[0]
    
    assert "Technology, made tangible." in prod_section, "Missing 'Technology, made tangible.' title"
    assert "PrajnaEdge products and technology experiences are currently in development." in prod_section, "Missing development subtitle"
    assert "In Development" in prod_section, "Missing 'In Development' badge"
    
    # Verify no buttons linking to playground or demonstrations inside page-products
    assert "showPage('demos')" not in prod_section, "Found showPage('demos') in #page-products"
    assert "showPage('playground')" not in prod_section, "Found showPage('playground') in #page-products"
    assert "Explore Demonstrations" not in prod_section, "Found 'Explore Demonstrations' in #page-products"
    assert "Try the Playground" not in prod_section, "Found 'Try the Playground' in #page-products"
    assert "/demonstrations/" not in prod_section, "Found /demonstrations/ in #page-products"
    assert "pricing" not in prod_section.lower(), "Found pricing in #page-products"
    
    # Verify no fake products or product cards
    assert "product-pillar-card" not in prod_section, "Found old product-pillar-card in products"
    assert "products-pillars-grid" not in prod_section, "Found old products-pillars-grid in products"
    print(" -> Products page: PASS (No buttons, no fake claims, clean future surface)")

    # 2. Playground Verification
    print("\n[TEST 2] PLAYGROUND VERIFICATION")
    with open("playground/index.html", "r", encoding="utf-8") as f:
        play_html = f.read()

    assert "Playground" in play_html, "Missing Playground title"
    assert "Experiment with intelligence beyond the cloud." in play_html, "Missing Playground intro"
    
    # Check Edge AI card active
    assert "playground-pane-edge-ai" in play_html, "Missing playground-pane-edge-ai"
    assert "Image Classification" in play_html, "Missing Image Classification card"
    assert "showPage('playground-edge-ai')" in play_html, "Missing link to playground-edge-ai"
    assert "Open Experiment →" in play_html, "Missing Open Experiment action"
    
    # Check On-device AI disabled
    assert "playground-card-disabled" in play_html, "Missing playground-card-disabled class"
    assert "Coming later" in play_html, "Missing 'Coming later' badge in disabled card"
    assert "showPage('playground-on-device-ai')" not in play_html, "On-device AI card should not navigate directly"
    print(" -> Playground page: PASS (Edge AI active, On-device AI disabled)")

    # 3. Terminology Check
    print("\n[TEST 3] TERMINOLOGY VERIFICATION")
    edge_desc = "AI runs closer to where data is generated — reducing dependence on distant cloud infrastructure and enabling faster, more responsive systems."
    on_device_desc = "AI runs directly on the device where data is generated, bringing intelligence into the device itself while operating within its compute, memory, power and latency constraints."
    
    assert edge_desc in play_html, f"Missing accurate Edge AI description in HTML"
    assert on_device_desc in play_html, f"Missing accurate On-Device AI description in HTML"
    
    with open("script.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    assert edge_desc in js_content, "Missing accurate Edge AI description in script.js"
    assert on_device_desc in js_content, "Missing accurate On-Device AI description in script.js"
    print(" -> Terminology: PASS (Both descriptions updated and exact in HTML and script.js)")

    # 4. On-Device AI Dedicated Page
    print("\n[TEST 4] ON-DEVICE AI PAGE VERIFICATION")
    with open("playground-on-device-ai/index.html", "r", encoding="utf-8") as f:
        on_dev_html = f.read()
        
    assert "Playground · Future Area" in on_dev_html, "Missing Future Area badge"
    assert "On-Device AI" in on_dev_html, "Missing title"
    assert "Coming later" in on_dev_html, "Missing 'Coming later' badge"
    assert "showPage('playground')" in on_dev_html, "Missing return to playground button"
    # Ensure large educational sections removed
    assert "Direct Silicon Execution" not in on_dev_html, "Found old section 1 in on-device-ai page"
    assert "The Physics of Constraints" not in on_dev_html, "Found old section 2 in on-device-ai page"
    assert "Why On-Device Differs from Cloud AI" not in on_dev_html, "Found old section 3 in on-device-ai page"
    assert "Upcoming Experimentation Surfaces" not in on_dev_html, "Found old section 4 in on-device-ai page"
    print(" -> On-Device AI direct page: PASS (Clean intentional unavailable state, no theory dump)")

    # 5. Placeholder scan
    print("\n[TEST 5] PLACEHOLDER SCAN (93 HTML files)")
    html_files = glob.glob("**/*.html", recursive=True)
    bad_patterns = ["// Coming soon", "// coming soon", "Under construction", "lorem ipsum"]
    for fpath in html_files:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        for p in bad_patterns:
            if p.lower() in c.lower():
                raise AssertionError(f"Forbidden placeholder '{p}' found in {fpath}")
    print(f" -> Scanned {len(html_files)} HTML files: PASS (0 placeholders found)")

    # 6. Robots & Sitemap Checks
    print("\n[TEST 6] ROBOTS META & SITEMAP AUDIT")
    tree = ET.parse("sitemap.xml")
    root = tree.getroot()
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]
    
    assert "https://prajnaedge.dev/products/" not in locs, "/products/ should not be in sitemap"
    assert "https://prajnaedge.dev/playground-on-device-ai/" not in locs, "/playground-on-device-ai/ should not be in sitemap"
    assert "https://prajnaedge.dev/playground/" in locs, "/playground/ must be in sitemap"
    assert "https://prajnaedge.dev/playground-edge-ai/" in locs, "/playground-edge-ai/ must be in sitemap"
    
    with open("products/index.html", "r", encoding="utf-8") as f:
        assert '<meta name="robots" content="noindex, follow" />' in f.read(), "/products/ must be noindex"
    with open("playground-on-device-ai/index.html", "r", encoding="utf-8") as f:
        assert '<meta name="robots" content="noindex, follow" />' in f.read(), "/playground-on-device-ai/ must be noindex"
    with open("playground/index.html", "r", encoding="utf-8") as f:
        assert '<meta name="robots" content="index, follow" />' in f.read(), "/playground/ must be index"
    with open("playground-edge-ai/index.html", "r", encoding="utf-8") as f:
        assert '<meta name="robots" content="index, follow" />' in f.read(), "/playground-edge-ai/ must be index"
        
    print(f" -> Sitemap & Robots: PASS (products/ & playground-on-device-ai/ are noindex & excluded from sitemap; playground/ & playground-edge-ai/ are indexed)")

    # 7. Direct Load / Pre-rendered Activation Check
    print("\n[TEST 7] DIRECT LOAD / PRE-RENDERED ACTIVATION CHECK")
    routes = {
        'index.html': 'page-home',
        'about/index.html': 'page-about',
        'contact/index.html': 'page-contact',
        'products/index.html': 'page-products',
        'playground/index.html': 'page-playground',
        'playground-edge-ai/index.html': 'page-playground-edge-ai',
        'playground-on-device-ai/index.html': 'page-playground-on-device-ai',
        'explorations/index.html': 'page-blogs',
        'demonstrations/index.html': 'page-demos',
        'legal/index.html': 'page-legal',
        'support/index.html': 'page-support'
    }
    for route, page_id in routes.items():
        with open(route, 'r', encoding='utf-8') as f:
            html = f.read()
        needle = f'class="page active" id="{page_id}"'
        assert needle in html, f"Pre-rendered route {route} does not have active class on {page_id}"
    print(" -> Direct load activation: PASS (All core routes have exact active pre-rendered container)")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    verify_all()
