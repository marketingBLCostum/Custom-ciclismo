from pathlib import Path
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, posixpath, re, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')
SOURCE=Path(r'C:\LORENZO\5 SPORT PER SITO CUSTOM\CICLISMO - Copia').resolve()
DESTINATION=Path(r'C:\LORENZO\5 SPORT PER SITO CUSTOM\DA CARICARE').resolve()
REPORT=SOURCE/'work/github-upload-2026-11-20'
DIRECTORIES=[
    'ACCESSORI SCHEDA PRODOTTO','DONNA SCHEDE PRODOTTO',
    'RAGAZZI SCHEDE PRODOTTO','UOMO SCHEDE PRODOTTO',
    'FRANCESE','INGLESE','SPAGNOLO','TEDESCO','images',
]
REQUIRED=['index.html','uomo.html','donna.html','ragazzi.html','accessori.html','catalog-fixes.css']
IMAGE_EXTENSIONS={'.png','.jpg','.jpeg','.webp','.gif','.svg','.avif','.bmp','.tif','.tiff','.ico'}

assert SOURCE!=DESTINATION
assert not DESTINATION.is_relative_to(SOURCE)
assert not SOURCE.is_relative_to(DESTINATION)
assert DESTINATION.parent==SOURCE.parent
assert DESTINATION.name=='DA CARICARE'
assert Path.cwd().resolve()==SOURCE
assert all((SOURCE/f).is_file() for f in REQUIRED)

def digest(file):
    h=hashlib.sha256()
    with file.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest()

selected={SOURCE/name for name in REQUIRED}
for directory in DIRECTORIES:
    folder=SOURCE/directory
    assert folder.is_dir(),str(folder)
    for file in folder.rglob('*'):
        relative=file.relative_to(SOURCE)
        if any(part in {'.git','work','node_modules','__pycache__'} for part in relative.parts):continue
        if file.name in {'Thumbs.db','desktop.ini','.DS_Store'}:continue
        assert not file.is_symlink(),'Unexpected source symlink: '+str(file)
        if file.is_file():selected.add(file)

files=sorted(selected,key=lambda f:f.relative_to(SOURCE).as_posix().casefold())
source_state={}
for file in files:
    stat=file.stat();rel=file.relative_to(SOURCE).as_posix()
    source_state[rel]={'sha256':digest(file),'bytes':stat.st_size,'mtime_ns':stat.st_mtime_ns}
print('Prepared',len(files),'production files;',round(sum(v['bytes'] for v in source_state.values())/1e6,2),'MB.',flush=True)

# Refuse to overwrite unrelated files already present in the named destination.
existing={f.relative_to(DESTINATION).as_posix():f for f in DESTINATION.rglob('*') if f.is_file()} if DESTINATION.exists() else {}
extra=sorted(set(existing)-set(source_state))
assert not extra,('Destination contains unrelated files; no files copied.',extra)
for rel,file in existing.items():
    assert digest(file)==source_state[rel]['sha256'],('Destination conflict; no files copied.',rel)

DESTINATION.mkdir(parents=True,exist_ok=True)
copied=0
for file in files:
    rel=file.relative_to(SOURCE).as_posix();target=(DESTINATION/rel)
    assert target.resolve().is_relative_to(DESTINATION)
    assert digest(file)==source_state[rel]['sha256'],('Source changed before copy',rel)
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(file,target)
        copied+=1
    assert digest(target)==source_state[rel]['sha256'],('Copied file mismatch',rel)
    if copied and copied%150==0:print('Copied',copied,'files.',flush=True)

# Re-read both sides after copying. No source file is moved or rewritten.
for rel,state in source_state.items():
    original=SOURCE/rel;copied_file=DESTINATION/rel
    assert digest(original)==digest(copied_file)==state['sha256'],('Final content mismatch',rel)
    assert original.stat().st_mtime_ns==state['mtime_ns'],('Original modification time changed',rel)
actual={f.relative_to(DESTINATION).as_posix() for f in DESTINATION.rglob('*') if f.is_file()}
assert actual==set(source_state)

class References(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if data.get('id'):self.ids.add(data['id'])
        if tag=='a' and data.get('name'):self.ids.add(data['name'])
        for attr in ['src','href','poster']:
            if data.get(attr):self.links.append((attr,data[attr]))
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)

documents={};issues=[];references_checked=0
for rel in sorted(actual):
    if Path(rel).suffix.lower()=='.html':
        parser=References();parser.feed((DESTINATION/rel).read_text(encoding='utf-8-sig'));documents[rel]=parser
case_lookup={rel.casefold():rel for rel in actual}
assert len(case_lookup)==len(actual),'Case-insensitive duplicate filenames'

def check_reference(rel,kind,value):
    global references_checked
    parsed=urlsplit(value)
    if parsed.scheme or parsed.netloc:return
    references_checked+=1
    if parsed.path.startswith('/'):
        issues.append({'file':rel,'value':value,'issue':'Root-absolute path is not portable to a project repository'})
        return
    target=posixpath.normpath(posixpath.join(posixpath.dirname(rel),unquote(parsed.path))) if parsed.path else rel
    if target.startswith('../'):
        issues.append({'file':rel,'value':value,'issue':'Path outside exported site'});return
    if target not in actual:
        if target.casefold() in case_lookup:
            issues.append({'file':rel,'value':value,'issue':'Filename case mismatch','actual':case_lookup[target.casefold()]})
        else:issues.append({'file':rel,'value':value,'issue':'Missing local file'})
        return
    if kind=='href' and parsed.fragment and target in documents:
        if unquote(parsed.fragment) not in documents[target].ids:
            issues.append({'file':rel,'value':value,'issue':'Missing local anchor'})

for rel,parser in documents.items():
    for kind,value in parser.links:check_reference(rel,kind,value)
    text=(DESTINATION/rel).read_text(encoding='utf-8-sig')
    for value in re.findall(r'url\(\s*["\x27]?([^\)"\x27]+)',text):
        if not value.startswith('#'):check_reference(rel,'css',value)
for rel in actual:
    if Path(rel).suffix.lower()=='.css':
        for value in re.findall(r'url\(\s*["\x27]?([^\)"\x27]+)',(DESTINATION/rel).read_text(encoding='utf-8-sig')):
            if not value.startswith('#'):check_reference(rel,'css',value)

counts=Counter(Path(rel).suffix.lower() for rel in actual)
result={
    'date':'2026-11-20','source':str(SOURCE),'destination':str(DESTINATION),
    'files':len(actual),'html':len(documents),
    'images':sum(counts[e] for e in IMAGE_EXTENSIONS),'videos':sum(counts[e] for e in ['.mp4','.webm','.mov']),
    'bytes':sum(v['bytes'] for v in source_state.values()),
    'newCopies':copied,'sha256Verified':True,'originalsUnchanged':True,
    'sourceModificationTimesPreserved':True,'referencesChecked':references_checked,
    'localReferenceIssues':issues,
    'excluded':['.git','work','temp_analyze.js','temp_analyze.py','work_pdf_compare_results.json','work_pdf_compare_results_v2.json','work_pdf_ita_inflated.txt'],
    'rootEntries':sorted(p.name for p in DESTINATION.iterdir()),
}
REPORT.mkdir(parents=True,exist_ok=True)
(REPORT/'files.json').write_text(json.dumps(source_state,ensure_ascii=False,indent=2),encoding='utf-8')
(REPORT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert not issues,'Exported copy has unresolved local references; see verification.json.'
