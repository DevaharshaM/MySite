import os
import re
import xml.etree.ElementTree as ET

def test_phase1():
    print("=== STARTING PHASE 1 VALIDATION ===")
    errors = []
    warnings = []

    # 1. Navigation in index.html
    with open("index.html", "r", encoding="utf-8") as f:
        index_html = f.read()

    expected_nav_hrefs = [
        'href="/"',
        'href="/explorations/"',
        'href="/playground/"',
        'href="/products/"',
        'href="/about/"',
        'href="/contact/"'
    ]
    for h in expected_nav_hrefs:
        if h not in index_html:
            errors.append(f"index.html <nav> missing expected href: {h}")

    # Check footer links in index.html
    expected_footer_links = [
        'href="/about/"',
        'href="/contact/"',
        'href="/support/"',
        'href="/legal/#privacy"',
        'href="/legal/#terms"',
        'href="/sitemap.xml"'
    ]
    for fl in expected_footer_links:
        if fl not in index_html:
            errors.append(f"index.html footer missing expected link: {fl}")

    # Check home technology statement
    if "home-domains-overview" not in index_html or "home-tech-statement" not in index_html:
        errors.append("index.html missing .home-domains-overview / .home-tech-statement")
    for keyword in ["Technology is a system of connections.", "Modern technology is built from layers", "From computing foundations and embedded systems", "To continue exploring"]:
        if keyword not in index_html:
            errors.append(f"index.html missing technology statement keyword: {keyword}")

    # 2. Check Explorations Hub pre-rendering (explorations/index.html)
    with open("explorations/index.html", "r", encoding="utf-8") as f:
        blogs_html = f.read()

    start_idx = blogs_html.find('id="blogList"')
    end_idx = blogs_html.find('id="page-demos"', start_idx)
    bloglist_chunk = blogs_html[start_idx:end_idx] if start_idx != -1 and end_idx != -1 else ""

    cards = re.findall(r'<a href="[^"]*explorations/([^/]+)/"', bloglist_chunk)
    print(f"explorations/index.html pre-rendered {len(cards)} exploration cards: {cards}")
    if len(cards) < 6:
        errors.append(f"Expected at least 6 pre-rendered cards in explorations/index.html, found {len(cards)}")

    # 3. Check Demonstrations Hub pre-rendering (demonstrations/index.html)
    with open("demonstrations/index.html", "r", encoding="utf-8") as f:
        demos_html = f.read()

    start_demo = demos_html.find('id="demoList"')
    end_demo = demos_html.find('id="page-blog-post"', start_demo)
    demolist_chunk = demos_html[start_demo:end_demo] if start_demo != -1 and end_demo != -1 else ""

    demo_cards = re.findall(r'<a href="[^"]*demonstrations/([^/]+)/"', demolist_chunk)
    print(f"demonstrations/index.html pre-rendered {len(demo_cards)} demo cards: {demo_cards}")
    if "edge-ai-uno-mpu6050" not in demo_cards:
        errors.append("demonstrations/index.html missing edge-ai-uno-mpu6050 demo card")

    # 4. Check Journey pre-rendering (journey/index.html)
    with open("journey/index.html", "r", encoding="utf-8") as f:
        journey_html = f.read()

    if "Foundations" not in journey_html or "BTech · ECE" not in journey_html or "The Hardware Mental Model" not in journey_html:
        errors.append("journey/index.html does not contain static pre-rendered Node 0 (Foundations) content")

    # 5. Check Legal page (legal/index.html)
    with open("legal/index.html", "r", encoding="utf-8") as f:
        legal_html = f.read()

    required_legal_phrases = [
        "Google AdSense",
        "DoubleClick",
        "Google Analytics",
        "G-6Y8ZVQB1V0",
        "Terms of Use",
        "Privacy Policy",
        "contact@prajnaedge.dev",
        'id="terms"',
        'id="privacy"',
        'id="adsense-cookies"',
        'id="analytics"',
        'id="contact-rights"'
    ]
    for phrase in required_legal_phrases:
        if phrase not in legal_html:
            errors.append(f"legal/index.html missing mandatory disclosure phrase: {phrase}")

    # 6. Check Noindex Pages
    noindex_pages = [
        "domain-select/index.html",
        "foundation-select/index.html",
        "playground-on-device-ai/index.html",
        "products/index.html"
    ]
    for np in noindex_pages:
        if not os.path.exists(np):
            errors.append(f"Missing page file: {np}")
            continue
        with open(np, "r", encoding="utf-8") as f:
            content = f.read()
        if '<meta name="robots" content="noindex, follow" />' not in content:
            errors.append(f"{np} is missing '<meta name=\"robots\" content=\"noindex, follow\" />'")

    # Check index, follow pages
    index_pages = [
        "index.html",
        "about/index.html",
        "contact/index.html",
        "journey/index.html",
        "creator/index.html",
        "explorations/index.html",
        "demonstrations/index.html",
        "support/index.html",
        "legal/index.html",
        "playground/index.html",
        "playground-edge-ai/index.html"
    ]
    for ip in index_pages:
        if not os.path.exists(ip):
            errors.append(f"Missing page file: {ip}")
            continue
        with open(ip, "r", encoding="utf-8") as f:
            content = f.read()
        if '<meta name="robots" content="index, follow" />' not in content:
            errors.append(f"{ip} should have '<meta name=\"robots\" content=\"index, follow\" />'")

    # 7. Check Sitemap (sitemap.xml)
    if not os.path.exists("sitemap.xml"):
        errors.append("sitemap.xml does not exist")
    else:
        with open("sitemap.xml", "r", encoding="utf-8") as f:
            sitemap_content = f.read()

        try:
            root = ET.fromstring(sitemap_content)
            locs = [elem.text.strip() for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            print(f"sitemap.xml has {len(locs)} total URLs")

            # Check that excluded pages are NOT in sitemap
            excluded_routes = [
                "https://prajnaedge.dev/domain-select/",
                "https://prajnaedge.dev/foundation-select/",
                "https://prajnaedge.dev/playground-on-device-ai/",
                "https://prajnaedge.dev/products/",
                "https://prajnaedge.dev/bare-metal/",
                "https://prajnaedge.dev/operating-systems/"
            ]
            for er in excluded_routes:
                if er in locs:
                    errors.append(f"sitemap.xml should NOT contain excluded route: {er}")

            # Check that required indexable pages ARE in sitemap
            required_routes = [
                "https://prajnaedge.dev/",
                "https://prajnaedge.dev/about/",
                "https://prajnaedge.dev/contact/",
                "https://prajnaedge.dev/journey/",
                "https://prajnaedge.dev/creator/",
                "https://prajnaedge.dev/explorations/",
                "https://prajnaedge.dev/demonstrations/",
                "https://prajnaedge.dev/support/",
                "https://prajnaedge.dev/legal/",
                "https://prajnaedge.dev/playground/",
                "https://prajnaedge.dev/playground-edge-ai/",
                "https://prajnaedge.dev/demonstrations/edge-ai-uno-mpu6050/"
            ]
            for rr in required_routes:
                if rr not in locs:
                    errors.append(f"sitemap.xml is missing required route: {rr}")

            # Check duplicates
            if len(locs) != len(set(locs)):
                dups = [x for x in locs if locs.count(x) > 1]
                errors.append(f"sitemap.xml contains duplicates: {set(dups)}")

        except Exception as e:
            errors.append(f"Error parsing sitemap.xml: {e}")

    # Summary
    print("\n--- VALIDATION SUMMARY ---")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("[SUCCESS] ALL PHASE 1 VALIDATION CHECKS PASSED PERFECTLY!")

    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARNING] {w}")

if __name__ == "__main__":
    test_phase1()
