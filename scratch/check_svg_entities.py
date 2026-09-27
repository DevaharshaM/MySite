import os, re

svg_dir = 'Images'
html_entities = re.compile(r'&([a-zA-Z]+);')
xml_standard = {'amp', 'lt', 'gt', 'apos', 'quot'}

for fname in os.listdir(svg_dir):
    if fname.endswith('.svg'):
        fpath = os.path.join(svg_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = html_entities.findall(content)
        non_std = [m for m in matches if m not in xml_standard]
        if non_std:
            print(f"File {fname} has non-standard XML entities: {set(non_std)}")
