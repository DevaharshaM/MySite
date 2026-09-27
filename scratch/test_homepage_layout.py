import os
import re

def verify_homepage_paragraphs():
    print("=== VERIFYING HOMEPAGE RESTRUCTURED ORDER & 3 SUBSTANTIVE PARAGRAPHS ===")
    errors = []

    # 1. Read index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Find the #page-home content
    home_match = re.search(r'<div class="page active" id="page-home">(.*?)</div>\s*</div>\s*<div class="page" id="page-products">', html, re.DOTALL)
    if not home_match:
        home_match = re.search(r'id="page-home">(.*?)id="page-products"', html, re.DOTALL)
        if not home_match:
            errors.append("Could not isolate #page-home section in index.html")
            return errors

    home_content = home_match.group(1)

    # 2. Check Order of elements
    idx_title = home_content.find("PrajnaEdge")
    idx_subline = home_content.find("A curiosphere for curious minds who want to understand")
    idx_tech_heading = home_content.find("Technology is a system of connections.")
    idx_p1 = home_content.find("Modern technology is built from layers that continuously interact with one another.")
    idx_p2 = home_content.find("But computation does not exist in isolation.")
    idx_p3 = home_content.find("PrajnaEdge explores these connections as one continuous technology landscape")
    idx_continue = home_content.find("To continue exploring")
    idx_actions = home_content.find("explore-options-grid")

    indices = [
        ("1. PrajnaEdge Title", idx_title),
        ("2. Small Identity Subline", idx_subline),
        ("3. Tech Heading", idx_tech_heading),
        ("4. Paragraph 1", idx_p1),
        ("5. Paragraph 2", idx_p2),
        ("6. Paragraph 3", idx_p3),
        ("7. 'To continue exploring'", idx_continue),
        ("8. Three Actions Grid", idx_actions)
    ]

    for label, idx in indices:
        if idx == -1:
            errors.append(f"Missing element: {label}")

    # Verify chronological order
    for i in range(len(indices) - 1):
        if indices[i][1] != -1 and indices[i+1][1] != -1:
            if indices[i][1] >= indices[i+1][1]:
                errors.append(f"Incorrect order: {indices[i][0]} (idx {indices[i][1]}) is not before {indices[i+1][0]} (idx {indices[i+1][1]})")

    # 3. Check exact required text in the 3 paragraphs
    required_phrases = [
        "Modern technology is built from layers that continuously interact with one another.",
        "electronic devices transform electrical signals into digital information.",
        "Digital logic turns that information into computation, while processors, memory and communication interfaces provide the machinery needed to execute instructions and move data.",
        "sensors, controllers, actuators and real-time software.",
        "Operating systems coordinate hardware and software, firmware gives specialized machines their behaviour, and communication protocols allow independent systems to exchange information.",
        "machine learning is moving beyond the cloud into edge and on-device systems, where models must operate within real constraints such as memory, processing power, latency and energy consumption.",
        "PrajnaEdge explores these connections as one continuous technology landscape",
        "and takes them beyond explanation.",
        "From computing foundations and embedded systems to intelligent machines and edge AI",
        "ideas can be understood, experimented with, and eventually turned into technology that can be experienced in the real world."
    ]
    for phrase in required_phrases:
        norm_phrase = phrase.replace("—", "&mdash;")
        if phrase not in home_content and norm_phrase not in home_content:
            errors.append(f"Missing required phrase: {phrase}")

    # 4. Verify old conceptual one-line statements are REMOVED
    removed_items = [
        "A signal becomes information.",
        "Information becomes computation.",
        "Computation becomes a machine.",
        "// INSIDE THE CURIOsphere",
        "Where Technology Begins to Connect",
        "Currently exploring:"
    ]
    for rem in removed_items:
        if rem in home_content:
            errors.append(f"Item should have been REMOVED but is still present: {rem}")

    # 5. Check CSS classes
    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()

    for cls in [".home-tech-statement", ".home-tech-heading", ".home-tech-body"]:
        if cls not in css:
            errors.append(f"Missing CSS class in style.css: {cls}")

    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("[SUCCESS] All homepage narrative order and 3 substantive paragraphs verified with 0 errors!")

if __name__ == "__main__":
    verify_homepage_paragraphs()
