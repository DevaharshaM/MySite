import os
import re
import json

root_dir = os.path.dirname(os.path.abspath(__file__))
blogs_content_dir = os.path.join(root_dir, "content", "explorations")
demos_content_dir = os.path.join(root_dir, "content", "demonstrations")
template_path = os.path.join(root_dir, "index.html")

# Define systemsTreeNodes category mapping for navigation builder
systemsTreeNodes = {
  "Matter": [
    "chemistry-intelligence-part1",
    "chemistry-intelligence-part2",
    "chemistry-intelligence-part3",
    "chemistry-intelligence-part4",
    "chemistry-intelligence-part5"
  ],
  "Computation": [
    "illusion-of-software",
    "the-architecture-of-memory",
    "the-hidden-geography-of-firmware",
    "the-first-instruction"
  ],
  "Interaction": [
    "why-systems-need-interfaces",
    "the-physical-edge-of-software",
    "why-embedded-systems-speak-in-protocols",
    "uart-structured-asynchronous-communication",
    "spi-shared-rhythm-of-machines",
    "i2c-the-shared-conversation",
    "can-the-language-of-many-voices",
    "the-roads-not-often-travelled"
  ],
  "Coordination": [
    "the-architecture-of-time",
    "when-machines-learned-to-observe",
    "when-machines-learned-to-speak-back",
    "the-tyranny-of-waiting",
    "when-hardware-learned-to-interrupt",
    "when-machines-learned-to-delegate"
  ],
  "Integration": [
    "when-machines-became-systems",
    "when-machines-learned-to-survive",
    "when-one-loop-was-enough",
    "when-one-processor-wasnt-enough"
  ],
  "Bare Metal": [
    "before-main",
    "the-infinite-loop-that-runs-a-machine",
    "teaching-time-to-an-infinite-loop",
    "when-behaviour-becomes-state"
  ],
  "Operating Systems": [
    "why-do-we-need-an-operating-system",
    "what-is-a-kernel",
    "what-is-a-process",
    "the-journey-between-moments",
    "who-goes-next",
    "the-rules-of-fairness",
    "when-one-rule-was-enough",
    "when-waiting-was-too-expensive",
    "remembering-the-moment",
    "the-great-swap",
    "scheduling-in-the-wild"
  ]
}

node_order = ["Matter", "Computation", "Interaction", "Coordination", "Integration", "Bare Metal"]

def esc_html(str_val):
    return str_val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def parse_text_formatting(text):
    # Inline code: `code` -> <code>
    parsed = re.sub(
        r'(?<!`)(`)([^`\n]+?)\1(?!`)',
        r'<code style="font-family:var(--mono); font-size:0.9rem; color:#A5F3FC; padding:0.1rem 0.3rem; background:rgba(30, 41, 59, 0.4); border:1px solid rgba(148,163,184,0.08); border-radius:4px;">\2</code>',
        text
    )
    # Bold: **text** -> <strong>text</strong>
    parsed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', parsed)
    
    # Internal links: [Text](target) -> onclick openItem and href
    def link_repl(match):
        label = match.group(1)
        target = match.group(2)
        if target == 'operating-systems':
            return f'<a href="../../operating-systems/" onclick="showPage(\'operating-systems\'); return false;" style="color:var(--blue); cursor:pointer; text-decoration:underline; font-style: normal;">{label}</a>'
        elif target.startswith('http') or target.startswith('mailto:') or target.startswith('/') or target.endswith('.html'):
            return f'<a href="{target}" target="_blank" rel="noopener noreferrer" style="color:var(--blue); text-decoration:underline;">{label}</a>'
        else:
            return f'<a href="../../explorations/{target}/" onclick="openItem(\'{target}\', \'blogs\')" style="color:var(--blue); cursor:pointer; text-decoration:underline; font-style: normal;">{label}</a>'
    
    parsed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, parsed)
    return parsed

def strip_quotes(val):
    val = val.strip()
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1].strip()
    return val

def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid Front Matter in {filepath}")
    
    front_matter_raw = parts[1]
    body_raw = parts[2]
    
    metadata = {}
    current_key = None
    for line in front_matter_raw.splitlines():
        if not line.strip():
            continue
        
        # Check multiline list items
        if (line.startswith('  - ') or line.startswith(' - ')) and current_key:
            val = line.split('-', 1)[1].strip()
            val = strip_quotes(val)
            if current_key in metadata:
                if isinstance(metadata[current_key], list):
                    metadata[current_key].append(val)
                else:
                    metadata[current_key] = [metadata[current_key], val]
            else:
                metadata[current_key] = [val]
            continue
            
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if val.startswith('[') and val.endswith(']'):
                metadata[key] = [strip_quotes(item) for item in val[1:-1].split(',')]
            else:
                metadata[key] = strip_quotes(val)
                current_key = key
                
    # Parse Body Content
    sections = []
    current_section = None
    lines = body_raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('## '):
            heading = line[3:].strip()
            current_section = {
                "heading": heading,
                "content": []
            }
            sections.append(current_section)
            i += 1
            continue
            
        if not line.strip():
            i += 1
            continue
            
        if line.strip() == '---':
            i += 1
            continue
            
        # Check HTML block
        if line.strip().startswith('```html'):
            html_content = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                html_content.append(lines[i])
                i += 1
            i += 1 # skip closing backticks
            if current_section:
                current_section["content"].append({
                    "type": "html",
                    "html": '\n'.join(html_content)
                })
            continue
            
        # Check Quote block
        if line.startswith('> '):
            quote_text = line[2:].strip()
            if current_section:
                current_section["content"].append({
                    "type": "quote",
                    "text": quote_text
                })
            i += 1
            continue
            
        # Check Code block
        if line.strip().startswith('```c') or line.strip().startswith('```cpp') or line.strip().startswith('```assembly'):
            lang_match = re.match(r'^```(\w+)', line.strip())
            lang = lang_match.group(1) if lang_match else 'c'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1 # skip closing backticks
            code_block = f'```{lang}\n' + '\n'.join(code_lines) + '\n```'
            if current_section:
                current_section["content"].append({
                    "type": "p",
                    "text": code_block
                })
            continue
            
        # Standard paragraph block
        paragraph_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('## ') and not lines[i].startswith('> ') and not lines[i].strip().startswith('```'):
            paragraph_lines.append(lines[i])
            i += 1
            
        p_text = '\n'.join(paragraph_lines).strip()
        if p_text and current_section:
            # Check if it is an image block
            image_match = re.match(r'^!\[([\s\S]*?)\]\(([^)]+)\)$', p_text)
            if image_match:
                alt = image_match.group(1).replace('\n', ' ').strip()
                src = image_match.group(2).strip()
                if src.startswith('Images/'):
                    src = '../../' + src
                elif src.startswith('content/Images/'):
                    src = '../../Images/' + src.split('/')[-1]
                elif src.startswith('../Images/'):
                    src = '../../Images/' + src.split('/')[-1]
                current_section["content"].append({
                    "type": "image",
                    "src": src,
                    "alt": alt,
                    "caption": alt
                })
            else:
                edgecase_match = re.match(r'^<div id="([^"]+)" class="edgecase-container"></div>$', p_text)
                if edgecase_match:
                    current_section["content"].append({
                        "type": "edgecase",
                        "id": edgecase_match.group(1)
                    })
                else:
                    block = {
                        "type": "p",
                        "text": p_text
                    }
                    if p_text.startswith('<') and p_text.endswith('>'):
                        block["html"] = True
                    current_section["content"].append(block)
            
    metadata["sections"] = sections
    closing_p = metadata.get("closing_paragraphs", [])
    if isinstance(closing_p, str):
        closing_p = [closing_p]
        
    metadata["closing"] = {
        "heading": metadata.get("closing_heading", ""),
        "paragraphs": closing_p,
        "quote": metadata.get("closing_quote", "")
    }
    
    # Remove temp keys
    for k in ["closing_heading", "closing_paragraphs", "closing_quote"]:
        metadata.pop(k, None)
        
    return metadata

def build_navigation_html(post, all_posts_dict):
    category = post["category"]
    post_id = post["id"]
    
    # If the post doesn't belong to our systemsTreeNodes (like demos), return empty
    if category not in systemsTreeNodes:
        return ""
        
    post_ids = systemsTreeNodes[category]
    if post_id not in post_ids:
        return ""
        
    currentIndex = post_ids.index(post_id)
    prevExpId = post_ids[currentIndex - 1] if currentIndex > 0 else None
    nextExpId = post_ids[currentIndex + 1] if currentIndex < len(post_ids) - 1 else None
    
    categoryIndex = node_order.index(category) if category in node_order else -1
    
    prev_html = ""
    if prevExpId and prevExpId in all_posts_dict:
        prev_title = all_posts_dict[prevExpId]["title"]
        prev_html = f"""
            <span class="nav-dir-label">Previous</span>
            <a class="nav-link active" href="../../explorations/{prevExpId}/" onclick="openItem('{prevExpId}', 'blogs')">← {esc_html(prev_title)}</a>
        """
    elif category == "Bare Metal":
        prev_html = """
            <span class="nav-dir-label">Previous</span>
            <a class="nav-link active" href="../../bare-metal/" onclick="showPage('bare-metal')">← Return to Bare Metal</a>
        """
    elif category == "Operating Systems":
        prev_html = """
            <span class="nav-dir-label">Previous</span>
            <a class="nav-link active" href="../../operating-systems/" onclick="showPage('operating-systems')">← Return to Operating Systems</a>
        """
    elif categoryIndex > 0:
        prev_category = node_order[categoryIndex - 1]
        prev_html = f"""
            <span class="nav-dir-label">Previous</span>
            <a class="nav-link active" href="../../explorations/" onclick="filterNodeRoute('{prev_category}')">← Return to {esc_html(prev_category)}</a>
        """
    else:
        prev_html = """
            <span class="nav-dir-label">Previous</span>
            <span class="nav-link locked">None</span>
        """
        
    next_html = ""
    if nextExpId and nextExpId in all_posts_dict:
        next_title = all_posts_dict[nextExpId]["title"]
        next_html = f"""
            <span class="nav-dir-label">Next</span>
            <a class="nav-link active" href="../../explorations/{nextExpId}/" onclick="openItem('{nextExpId}', 'blogs')">{esc_html(next_title)} →</a>
        """
    elif category == "Operating Systems":
        if post_id == "why-do-we-need-an-operating-system":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked" style="display:inline-flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                  The Silent Conductor →
                  <span style="font-size:0.55rem; color:var(--blue); border:1px solid var(--blue); border-radius:4px; padding:1px 4px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; background:var(--blue-glow);">Coming Soon</span>
                </span>
            """
        elif post_id == "what-is-a-kernel":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked" style="display:inline-flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                  When Code Comes Alive →
                  <span style="font-size:0.55rem; color:var(--blue); border:1px solid var(--blue); border-radius:4px; padding:1px 4px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; background:var(--blue-glow);">Coming Soon</span>
                </span>
            """
        elif post_id == "what-is-a-process":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked" style="display:inline-flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                  The Journey Between Moments →
                  <span style="font-size:0.55rem; color:var(--blue); border:1px solid var(--blue); border-radius:4px; padding:1px 4px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; background:var(--blue-glow);">Coming Soon</span>
                </span>
            """
        elif post_id == "the-journey-between-moments":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked" style="display:inline-flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                  Who Goes Next? →
                  <span style="font-size:0.55rem; color:var(--blue); border:1px solid var(--blue); border-radius:4px; padding:1px 4px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; background:var(--blue-glow);">Coming Soon</span>
                </span>
            """
        elif post_id == "scheduling-in-the-wild":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked" style="display:inline-flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                  Real-Time Scheduling →
                  <span style="font-size:0.55rem; color:var(--blue); border:1px solid var(--blue); border-radius:4px; padding:1px 4px; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; background:var(--blue-glow);">Coming Soon</span>
                </span>
            """
        else:
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked">None</span>
            """
    elif categoryIndex != -1 and categoryIndex < len(node_order) - 1:
        next_category = node_order[categoryIndex + 1]
        next_html = f"""
            <span class="nav-dir-label">Next</span>
            <a class="nav-link active" href="../../explorations/" onclick="filterNodeRoute('{next_category}')">Advance to {esc_html(next_category)} →</a>
        """
    else:
        if category == "Bare Metal":
            next_html = """
                <span class="nav-dir-label">Next</span>
                <a class="nav-link active" href="../../operating-systems/" onclick="showPage('operating-systems')">New path is awakening →</a>
            """
        else:
            next_html = """
                <span class="nav-dir-label">Next</span>
                <span class="nav-link locked">None</span>
            """
        
    nav_next_id_str = ' class="nav-next"'
    if post_id == "who-goes-next":
        nav_next_id_str = ' class="nav-next" id="exploration-nav-next" style="display: none;"'
    else:
        nav_next_id_str = ' class="nav-next" id="exploration-nav-next"'

    nav_html = f"""
      <div class="exploration-nav-block">
        <div class="exploration-nav-grid">
          <div class="nav-prev">{prev_html}</div>
          <div{nav_next_id_str}>{next_html}</div>
        </div>
      </div>
    """
    return nav_html

def build_post_html(post, all_posts_dict):
    sections_html_parts = []
    for sec in post["sections"]:
        blocks_html = []
        for b in sec["content"]:
            if b["type"] == 'p':
                code_match = re.match(r'^```(\w*)\n([\s\S]*?)\n```$', b["text"])
                if code_match:
                    code_content = code_match.group(2)
                    blocks_html.append(f'<div class="blog-code" style="color:#A5F3FC; white-space:pre-wrap;">{esc_html(code_content)}</div>')
                else:
                    p_content = b["text"]
                    if b.get("html"):
                        blocks_html.append(p_content)
                    else:
                        p_content = esc_html(p_content)
                        blocks_html.append(f'<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem;white-space:pre-line">{parse_text_formatting(p_content)}</p>')
            elif b["type"] == 'quote':
                blocks_html.append(f'<div class="blog-quote">{esc_html(b["text"])}</div>')
            elif b["type"] == 'code':
                blocks_html.append(f'<div class="blog-code" style="color:#A5F3FC; white-space:pre-wrap;">{esc_html(b["text"])}</div>')
            elif b["type"] == 'html':
                blocks_html.append(b["html"])
            elif b["type"] == 'edgecase':
                blocks_html.append(f'<div id="{esc_html(b["id"])}" class="edgecase-container"></div>')
            elif b["type"] in ('image', 'img'):
                caption_html = f'<div class="blog-img-caption">{esc_html(b["caption"])}</div>' if b.get("caption") else ""
                blocks_html.append(f'<div class="blog-img-wrap"><img src="{esc_html(b["src"])}" alt="{esc_html(b.get("alt", ""))}">{caption_html}</div>')
        
        sections_html_parts.append(
            f'<div style="margin-bottom:2.5rem">'
            f'<h2 style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:1.15rem;color:#fff;margin-bottom:1rem">{esc_html(sec["heading"])}</h2>'
            f'{"".join(blocks_html)}'
            f'</div>'
        )
        
    sections_html = "".join(sections_html_parts)
    nav_html = build_navigation_html(post, all_posts_dict)
    
    closing_p_html = "".join([f'<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem">{parse_text_formatting(esc_html(p))}</p>' for p in post["closing"]["paragraphs"]])
    
    post_html = f"""
    <div style="font-family:var(--mono);font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">{esc_html(post["category"])}</div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.6rem,3vw,2.4rem);line-height:1.15;letter-spacing:-0.03em;color:#fff;margin-bottom:1rem">{esc_html(post["title"])}</h1>
    <p style="color:#64748B;font-size:1rem;line-height:1.75;font-weight:300;margin-bottom:1rem">{esc_html(post["subtitle"])}</p>
    <div class="tags" style="margin-bottom:3rem">{"".join([f'<span class="tag">{esc_html(t)}</span>' for t in post["tags"]])}</div>
    <div style="border-top:1px solid var(--border);margin-bottom:3rem"></div>
    {sections_html}
    <div style="margin-bottom:2.5rem">
      <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.15rem;color:#fff;margin-bottom:1rem">{esc_html(post["closing"]["heading"])}</h2>
      {closing_p_html}
      <div class="blog-quote">{esc_html(post["closing"]["quote"])}</div>
    </div>
    {nav_html}
    """
    return post_html

def make_paths_relative(html_content, depth=1):
    prefix = "../" * depth
    html_content = html_content.replace('href="style.css"', f'href="{prefix}style.css"')
    html_content = html_content.replace('src="script.js"', f'src="{prefix}script.js"')
    html_content = re.sub(r'src="Images/', f'src="{prefix}Images/', html_content)
    html_content = re.sub(r'href="Images/', f'href="{prefix}Images/', html_content)
    html_content = re.sub(r'href="HomepageAnimation/', f'href="{prefix}HomepageAnimation/', html_content)
    html_content = re.sub(r'src="HomepageAnimation/', f'src="{prefix}HomepageAnimation/', html_content)
    html_content = re.sub(r'<source src="HomepageAnimation/', f'<source src="{prefix}HomepageAnimation/', html_content)
    return html_content

def main():
    print("--- STARTING HYBRID PRE-RENDERER GENERATION ---")
    
    # 1. Parse explorations (blogs)
    blogs = []
    if os.path.exists(blogs_content_dir):
        for fname in os.listdir(blogs_content_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(blogs_content_dir, fname)
                post = parse_markdown_file(fpath)
                blogs.append(post)
                
    # 2. Parse demonstrations (demos)
    demos = []
    if os.path.exists(demos_content_dir):
        for fname in os.listdir(demos_content_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(demos_content_dir, fname)
                post = parse_markdown_file(fpath)
                demos.append(post)
                
    all_posts_dict = {p["id"]: p for p in (blogs + demos)}
    
    # 3. Write compiled JSON database for client consumption
    content_json_path = os.path.join(root_dir, "content", "content.json")
    with open(content_json_path, 'w', encoding='utf-8') as f:
        json.dump({"blogs": blogs, "demos": demos}, f, indent=2)
    print(f"Wrote compiled content cache: {content_json_path}")
    
    # Read layout template
    if not os.path.exists(template_path):
        print(f"Error: Master template index.html not found.")
        return
    with open(template_path, 'r', encoding='utf-8') as f:
        master_template = f.read()
        
    # 4. Generate Pre-rendered Explorations
    explorations_dir = os.path.join(root_dir, "explorations")
    for post in blogs:
        post_id = post["id"]
        post_dir = os.path.join(explorations_dir, post_id)
        os.makedirs(post_dir, exist_ok=True)
        
        post_html = build_post_html(post, all_posts_dict)
        
        pre_rendered_html = master_template
        pre_rendered_html = pre_rendered_html.replace('<div class="page active" id="page-home">', '<div class="page" id="page-home">')
        pre_rendered_html = pre_rendered_html.replace('<div class="page" id="page-blog-post">', '<div class="page active" id="page-blog-post">')
        pre_rendered_html = pre_rendered_html.replace('<div id="blog-post-content"></div>', f'<div id="blog-post-content">{post_html}</div>')
        pre_rendered_html = pre_rendered_html.replace('<title>PrajnaEdge | Devaharsha Meesarapu</title>', f'<title>{post["title"]} | PrajnaEdge</title>')
        pre_rendered_html = pre_rendered_html.replace('<link rel="canonical" href="https://prajnaedge.dev/" />', f'<link rel="canonical" href="https://prajnaedge.dev/explorations/{post_id}/" />')
        pre_rendered_html = make_paths_relative(pre_rendered_html, depth=2)
        
        out_filepath = os.path.join(post_dir, "index.html")
        with open(out_filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(pre_rendered_html)
        print(f"Pre-rendered exploration: {post_id}")
        
    # 5. Generate Pre-rendered Demonstrations
    demonstrations_dir = os.path.join(root_dir, "demonstrations")
    for post in demos:
        post_id = post["id"]
        post_dir = os.path.join(demonstrations_dir, post_id)
        os.makedirs(post_dir, exist_ok=True)
        
        post_html = build_post_html(post, all_posts_dict)
        
        pre_rendered_html = master_template
        pre_rendered_html = pre_rendered_html.replace('<div class="page active" id="page-home">', '<div class="page" id="page-home">')
        pre_rendered_html = pre_rendered_html.replace('<div class="page" id="page-blog-post">', '<div class="page active" id="page-blog-post">')
        pre_rendered_html = pre_rendered_html.replace('<div id="blog-post-content"></div>', f'<div id="blog-post-content">{post_html}</div>')
        pre_rendered_html = pre_rendered_html.replace('<title>PrajnaEdge | Devaharsha Meesarapu</title>', f'<title>{post["title"]} | PrajnaEdge</title>')
        pre_rendered_html = pre_rendered_html.replace('<link rel="canonical" href="https://prajnaedge.dev/" />', f'<link rel="canonical" href="https://prajnaedge.dev/demonstrations/{post_id}/" />')
        pre_rendered_html = make_paths_relative(pre_rendered_html, depth=2)
        
        out_filepath = os.path.join(post_dir, "index.html")
        with open(out_filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(pre_rendered_html)
        print(f"Pre-rendered demonstration: {post_id}")
        
    # 6. Generate Pre-rendered static pages: about, contact, journey, explorations, demonstrations
    page_configs = [
        {"id": "about", "title": "About | PrajnaEdge", "route": "about/"},
        {"id": "contact", "title": "Contact | PrajnaEdge", "route": "contact/"},
        {"id": "journey", "title": "Interactive Career Journey | PrajnaEdge", "route": "journey/"},
        {"id": "blogs", "title": "Explorations | PrajnaEdge", "route": "explorations/"},
        {"id": "demos", "title": "Demonstrations | PrajnaEdge", "route": "demonstrations/"},
        {"id": "bare-metal", "title": "Bare Metal | PrajnaEdge", "route": "bare-metal/"},
        {"id": "operating-systems", "title": "Operating Systems | PrajnaEdge", "route": "operating-systems/"}
    ]
    
    for cfg in page_configs:
        cfg_dir = os.path.join(root_dir, cfg["route"])
        os.makedirs(cfg_dir, exist_ok=True)
        
        pre_rendered_html = master_template
        pre_rendered_html = pre_rendered_html.replace('<div class="page active" id="page-home">', '<div class="page" id="page-home">')
        pre_rendered_html = pre_rendered_html.replace(f'<div class="page" id="page-{cfg["id"]}">', f'<div class="page active" id="page-{cfg["id"]}">')
        pre_rendered_html = pre_rendered_html.replace('<title>PrajnaEdge | Devaharsha Meesarapu</title>', f'<title>{cfg["title"]}</title>')
        pre_rendered_html = pre_rendered_html.replace('<link rel="canonical" href="https://prajnaedge.dev/" />', f'<link rel="canonical" href="https://prajnaedge.dev/{cfg["route"]}" />')
        pre_rendered_html = make_paths_relative(pre_rendered_html, depth=1)
        
        out_filepath = os.path.join(cfg_dir, "index.html")
        with open(out_filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(pre_rendered_html)
        print(f"Pre-rendered core page: {cfg['id']}")
        
    # 7. Generate clean sitemap.xml
    sitemap_entries = [
        '  <url>\n    <loc>https://prajnaedge.dev/</loc>\n    <lastmod>2026-07-28</lastmod>\n  </url>'
    ]
    for cfg in page_configs:
        sitemap_entries.append(f'  <url>\n    <loc>https://prajnaedge.dev/{cfg["route"]}</loc>\n    <lastmod>2026-07-28</lastmod>\n  </url>')
    for post in blogs:
        sitemap_entries.append(f'  <url>\n    <loc>https://prajnaedge.dev/explorations/{post["id"]}/</loc>\n    <lastmod>2026-07-28</lastmod>\n  </url>')
    for post in demos:
        sitemap_entries.append(f'  <url>\n    <loc>https://prajnaedge.dev/demonstrations/{post["id"]}/</loc>\n    <lastmod>2026-07-28</lastmod>\n  </url>')
        
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""
    sitemap_filepath = os.path.join(root_dir, "sitemap.xml")
    with open(sitemap_filepath, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    print(f"Generated clean sitemap: {sitemap_filepath}")
    print("--- HYBRID PRE-RENDERER MIGRATION COMPLETE ---")

if __name__ == "__main__":
    main()
