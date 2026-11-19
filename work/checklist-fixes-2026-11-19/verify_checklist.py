from pathlib import Path
from collections import Counter
import hashlib,json,re,zipfile,sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd();OUT=ROOT/'work/checklist-fixes-2026-11-19'
exec((ROOT/'work/catalog-audit-2026/audit.py').read_text(encoding='utf-8-sig').split('files=sorted')[0])
# The parser prefix sets OUT for its own audit; keep all new results in this task.
OUT=ROOT/'work/checklist-fixes-2026-11-19'
baseline=json.loads((OUT/'baseline.json').read_text(encoding='utf-8'))
events=json.loads((OUT/'changes.json').read_text(encoding='utf-8'));expected={x['file'] for x in events}
actual=set();images=0;media=0
IMAGE_EXTENSIONS={'.png','.jpg','.jpeg','.webp','.gif','.svg','.avif','.bmp','.tif','.tiff','.ico'}
for rel,before in baseline.items():
    f=ROOT/rel;after=hashlib.sha256(f.read_bytes()).hexdigest()
    if after!=before:actual.add(rel)
    if rel.lower().startswith('images/'):
        media+=1
        if Path(rel).suffix.lower() in IMAGE_EXTENSIONS:images+=1
        assert before==after,rel+' image changed'
assert actual==expected,(actual-expected,expected-actual)

trees={};pages=[];issues=[]
for f in sorted(ROOT.rglob('*.html')):
    rel=f.relative_to(ROOT)
    if any(p in {'.git','work'} for p in rel.parts):continue
    parser=P();parser.feed(f.read_text(encoding='utf-8-sig'));trees[rel.as_posix()]=parser.root
for rel,tree in trees.items():
    f=ROOT/rel
    for n in tree.findall():
        for attr in ['href','src']:
            value=n.a.get(attr)
            if not value:continue
            u=urlsplit(value)
            if u.scheme or u.netloc:continue
            target=(f.parent/unquote(u.path)).resolve() if u.path else f
            if not target.exists():issues.append((rel,attr,value))
            if attr=='href' and u.fragment and target.suffix=='.html' and target.is_relative_to(ROOT):
                t=trees.get(target.relative_to(ROOT).as_posix())
                if t and not any(x.a.get('id')==unquote(u.fragment) or x.a.get('name')==unquote(u.fragment) for x in t.findall()):issues.append((rel,'anchor',value))
    m=re.search(r'W\d{4}',f.name);side=tree.find(cls='sidebar')
    if not m or not side:continue
    code=m[0];lang=langof(Path(rel));blocks=[]
    for b in side.findall(cls='acc-item'):
        h=b.find(cls='acc-title');body=b.find(cls='acc-body')
        if h and body:blocks.append((h.text().upper(),body))
    if code in {'W2200','W2201','W2202','W2204','W2210','W2212','W2216','W2217','W2218','W2219','W6303'}:
        assert side.find(cls='sizes').text()=='104 116 128 140 152 164',rel
    if code=='W6012' and 'UOMO' in rel:
        option={'it':'OPZIONI','en':'OPTIONS','fr':'OPTIONS','de':'OPTIONEN','es':'OPCIONES'}[lang]
        assert not any(h==option for h,b in blocks),rel
        assert any(re.search('FONDELLO|CHAMOIS|PEAU|SITZPOLSTER|BADANA',h) for h,b in blocks),rel
    if code=='W6701' and 'UOMO' in rel:
        assert 'Camlock' in side.text() and not re.search(r'Cam\s*(?:&|-&-)\s*Lock',side.text()),rel
    if code=='W6009' and 'UOMO' in rel:
        assert not any(x in side.text() for x in ['raw-cut','taglio vivo','coupe franche','roh geschnitten','corte vivo']),rel
    accessory=code.startswith('W66') or code in {'W0274','W2632'}
    if accessory:
        temp=side.find(cls='temp-title')
        assert temp.text()=={'it':'Temperatura','en':'Temperature','fr':'Température','de':'Temperatur','es':'Temperatura'}[lang],(rel,temp.text())
        if lang=='es':
            visible=tree.text()
            assert not any(t in visible for t in ['Maßgefertigte','Angebot anfordern','Weitere Produkte','Ich möchte']),rel
        if lang!='de':assert not any(n.a.get('href')=='https://www.bicycle-line.com/de/' for n in tree.findall(tag='a')),rel
    if code in {'W6600','W6601'}:
        desc=side.find(cls='description').text()
        assert 'Qskin' in desc and 'Aero Channelled Speed' in desc,rel
        feature=[b for h,b in blocks if h in {'CARATTERISTICHE PRINCIPALI','MAIN FEATURES','CARACTÉRISTIQUES PRINCIPALES','HAUPTEIGENSCHAFTEN','CARACTERÍSTICAS PRINCIPALES'}]
        assert len(feature)==1 and len(feature[0].findall(tag='li'))==8,rel
        assert 'Qskin' in feature[0].text() and 'Aero Channelled Speed' in feature[0].text(),rel
    pages.append(rel)
assert not issues,issues[:20]

with zipfile.ZipFile(OUT/'before-html.zip') as backup:
    for rel in expected:
        old=backup.read(rel).decode('utf-8-sig');new=(ROOT/rel).read_bytes().decode('utf-8-sig')
        scripts=lambda s:re.findall(r'<script\b[^>]*>[\s\S]*?</script>',s,re.I)
        assert scripts(old)==scripts(new),rel+' script changed'
        oldtree=P();oldtree.feed(old);newtree=P();newtree.feed(new)
        oldgallery=oldtree.root.find(cls='gallery');newgallery=newtree.root.find(cls='gallery')
        assert [n.a for n in oldgallery.findall(tag='img')]==[n.a for n in newgallery.findall(tag='img')],rel+' gallery changed'
result={'htmlFiles':len(trees),'productPages':len(pages),'changedHtml':len(expected),'imagesVerifiedUnchanged':images,'mediaFilesVerifiedUnchanged':media,'localLinkIssues':issues,'scriptsAndGalleryUnchanged':True,'unrelatedFilesUnchanged':True}
(OUT/'static-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
