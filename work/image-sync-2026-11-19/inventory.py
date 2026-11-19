from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, sys, time

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path.cwd()
SOURCE = Path(r'\\Serverbl\dati\Documenti Comuni\___LORENZO\SITI CUSTOM\CICLISMO')
OUT = ROOT / 'work/image-sync-2026-11-19'
OUT.mkdir(parents=True, exist_ok=True)
EXT = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif', '.bmp', '.tif', '.tiff', '.ico'}

def inventory(root):
    result = {}
    for p in root.rglob('*'):
        rel = p.relative_to(root)
        if any(part.lower() in {'.git', 'work', 'node_modules'} for part in rel.parts):
            continue
        if p.is_file() and p.suffix.lower() in EXT:
            s = p.stat()
            result[rel.as_posix().casefold()] = {'path': rel.as_posix(), 'size': s.st_size, 'mtime_ns': s.st_mtime_ns}
    return result

class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('src', 'poster'):
            if a.get(key):
                self.refs.append((tag, a[key]))
        if tag == 'img' and a.get('srcset'):
            self.refs.extend((tag, part.strip().split()[0]) for part in a['srcset'].split(',') if part.strip())

def references(root):
    refs = defaultdict(list)
    pages = {}
    for p in root.rglob('*.html'):
        rel = p.relative_to(root)
        if any(part.lower() in {'.git', 'work', 'node_modules'} for part in rel.parts):
            continue
        content = p.read_text(encoding='utf-8-sig')
        parser = Images()
        parser.feed(content)
        urls = parser.refs + [('css', m) for m in re.findall(r'url\([\"\x27]?([^\)\"\x27]+)', content)]
        for tag, value in urls:
            u = urlsplit(value)
            if u.scheme or u.netloc or not u.path:
                continue
            target = (p.parent / unquote(u.path)).resolve()
            if target.is_relative_to(root):
                key = target.relative_to(root).as_posix().casefold()
                if target.suffix.lower() in EXT:
                    refs[key].append({'html': rel.as_posix(), 'tag': tag, 'url': value})
        pages[rel.as_posix()] = [v for tag, v in parser.refs if tag == 'img']
    return dict(refs), pages

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

local = inventory(ROOT)
remote = inventory(SOURCE)
local_refs, local_pages = references(ROOT)
remote_refs, remote_pages = references(SOURCE)
common = sorted(local.keys() & remote.keys())
print('Image inventory:', len(local), 'local,', len(remote), 'server;', len(common), 'common.', flush=True)

def compare(k):
    a, b = local[k], remote[k]
    ha = digest(ROOT / a['path'])
    hb = digest(SOURCE / b['path'])
    return k, ha, hb

different = []
with ThreadPoolExecutor(max_workers=4) as pool:
    for i, (k, ha, hb) in enumerate(pool.map(compare, common), 1):
        local[k]['sha256'] = ha
        remote[k]['sha256'] = hb
        if ha != hb:
            different.append({'key': k, 'local': local[k], 'source': remote[k], 'sourceNewer': remote[k]['mtime_ns'] > local[k]['mtime_ns'], 'localRefs': local_refs.get(k, []), 'sourceRefs': remote_refs.get(k, [])})
        if i % 100 == 0:
            print('Hashed', i, '/', len(common), flush=True)

result = {'root': str(ROOT), 'source': str(SOURCE), 'local': local, 'remote': remote, 'different': different, 'localOnly': sorted(local.keys() - remote.keys()), 'sourceOnly': sorted(remote.keys() - local.keys()), 'localRefs': local_refs, 'sourceRefs': remote_refs, 'localPages': local_pages, 'sourcePages': remote_pages}
(OUT / 'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'different': [{'path': d['local']['path'], 'sourceNewer': d['sourceNewer'], 'localBytes': d['local']['size'], 'sourceBytes': d['source']['size'], 'localPages': len(d['localRefs']), 'sourcePages': len(d['sourceRefs'])} for d in different], 'sourceOnly': result['sourceOnly'], 'localOnly': result['localOnly']}, ensure_ascii=False, indent=2))
