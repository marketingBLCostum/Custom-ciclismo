import os, re

base = r'c:\LORENZO\5 SPORT PER SITO CUSTOM\CICLISMO - Copia'

def get_all_html_files(dir_path):
    results = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if f.endswith('.html'):
                results.append(os.path.join(root, f))
    return results

html_files = get_all_html_files(base)
missing_images = []
missing_links = []
src_regex = re.compile(r'src\s*=\s*"([^"]+)"', re.IGNORECASE)
href_regex = re.compile(r'href\s*=\s*"([^"]+)"', re.IGNORECASE)

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    rel_dir = os.path.dirname(html_file)

    for match in src_regex.finditer(content):
        src = match.group(1)
        if src.startswith(('http://', 'https://', '//', 'mailto:', 'tel:', '#')):
            continue
        full_path = os.path.normpath(os.path.join(rel_dir, src))
        if not os.path.exists(full_path):
            missing_images.append((html_file, src, full_path))

    for match in href_regex.finditer(content):
        href = match.group(1)
        if href.startswith(('http://', 'https://', '//', 'mailto:', 'tel:', '#', 'javascript:')):
            continue
        full_path = os.path.normpath(os.path.join(rel_dir, href))
        if not os.path.exists(full_path):
            missing_links.append((html_file, href, full_path))

print('=== MISSING IMAGES ===')
for m in sorted(set(missing_images)):
    print(f"{m[0]} -> {m[1]} (resolved: {m[2]})")

print('\n=== MISSING LINKS ===')
for m in sorted(set(missing_links)):
    print(f"{m[0]} -> {m[1]} (resolved: {m[2]})")

print(f'\nTotal HTML files: {len(html_files)}')
print(f'Total missing images: {len(set(missing_images))}')
print(f'Total missing links: {len(set(missing_links))}')
