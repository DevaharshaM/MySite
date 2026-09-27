import json
import re
import datetime

with open('content/content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

blogs = data['blogs']

def parse_date_epoch_py(date_str):
    if not date_str:
        return 0
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str).strip()
    for fmt in ('%d %B %Y', '%d %b %Y'):
        try:
            return datetime.datetime.strptime(cleaned, fmt).timestamp()
        except Exception:
            pass
    return 0

# Python current sort:
py_blogs = [b for b in blogs if b.get('type') != 'hidden' and b.get('category') != 'Hidden Exploration']
py_blogs.sort(key=lambda x: parse_date_epoch_py(x.get('date', '')), reverse=True)
print("build.py first 6:")
for b in py_blogs[:6]:
    print(f"  {b['id']} ({b.get('date')})")

# script.js sort:
systemsTreeNodes = {
  "Matter": ["chemistry-intelligence-part1", "chemistry-intelligence-part2", "chemistry-intelligence-part3", "chemistry-intelligence-part4", "chemistry-intelligence-part5"],
  "Computation": ["illusion-of-software", "the-architecture-of-memory", "the-hidden-geography-of-firmware", "the-first-instruction"],
  "Interaction": ["why-systems-need-interfaces", "the-physical-edge-of-software", "why-embedded-systems-speak-in-protocols", "uart-structured-asynchronous-communication", "spi-shared-rhythm-of-machines", "i2c-the-shared-conversation", "can-the-language-of-many-voices", "the-roads-not-often-travelled"],
  "Coordination": ["the-architecture-of-time", "when-machines-learned-to-observe", "when-machines-learned-to-speak-back", "the-tyranny-of-waiting", "when-hardware-learned-to-interrupt", "when-machines-learned-to-delegate"],
  "Integration": ["when-machines-became-systems", "when-machines-learned-to-survive", "when-one-loop-was-enough", "when-one-processor-wasnt-enough"],
  "Bare Metal": ["before-main", "the-infinite-loop-that-runs-a-machine", "teaching-time-to-an-infinite-loop", "when-behaviour-becomes-state"],
  "Operating Systems": ["why-do-we-need-an-operating-system", "what-is-a-kernel", "what-is-a-process", "the-journey-between-moments", "who-goes-next", "the-rules-of-fairness", "when-one-rule-was-enough", "when-waiting-was-too-expensive", "remembering-the-moment", "the-great-swap", "scheduling-in-the-wild", "one-brain-wasnt-enough", "when-silence-wasnt-an-option", "when-sharing-became-dangerous", "when-nobody-could-move", "when-importance-wasnt-enough", "the-illusion-of-ownership", "the-invisible-translator", "the-language-of-pages", "when-the-page-wasnt-there", "choosing-what-to-forget", "segmentation", "there-is-no-perfect-fit", "where-does-a-file-actually-live", "the-file-isnt-open", "the-name-is-not-the-file", "how-does-the-filesystem-keep-track", "a-file-is-not-stored-as-a-file", "the-disk-has-no-files", "when-the-disk-becomes-the-bottleneck", "when-the-power-goes-out", "the-boundary-between-software-and-hardware", "not-every-os-has-the-same-job", "when-time-becomes-a-requirement"],
  "Processor": ["microprocessor-the-brain-behind-computation", "inside-the-microprocessor-from-instruction-to-execution", "von-neumann-architecture-where-instructions-and-data-meet"],
  "Controller": ["microcontroller-the-computer-inside-the-machine", "two-paths-one-controller", "inside-the-controller", "the-8051-the-controller-that-started-a-generation", "inside-the-8051", "the-8051-memory-map"]
}

nodeOrder = ["Matter", "Computation", "Interaction", "Coordination", "Integration", "Bare Metal", "Operating Systems", "Processor", "Controller"]
chrono_index = {}
idx = 0
for n in nodeOrder:
    for item_id in systemsTreeNodes[n]:
        chrono_index[item_id] = idx
        idx += 1

def js_sort_key(b):
    # In JS: timeB - timeA; if equal, indexB - indexA (so higher epoch first, higher chrono_index first)
    return (parse_date_epoch_py(b.get('date', '')), chrono_index.get(b['id'], 999))

js_blogs = [b for b in blogs if b.get('type') != 'hidden' and b.get('category') != 'Hidden Exploration']
js_blogs.sort(key=js_sort_key, reverse=True)
print("\nscript.js first 6:")
for b in js_blogs[:6]:
    print(f"  {b['id']} ({b.get('date')})")
