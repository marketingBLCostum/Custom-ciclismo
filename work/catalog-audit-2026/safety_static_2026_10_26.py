from pathlib import Path
from collections import defaultdict,Counter
import json,re,sys,pdfplumber,hashlib
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd();out=root/'work/catalog-audit-2026'
# Reparse all current HTML and validate local paths, anchors and language destinations.
code=(out/'audit.py').read_text(encoding='utf-8-sig');exec(code.split('refs={}; pdfpages=[]')[0])
source=SOURCE;refs=json.loads((out/'references.json').read_text(encoding='utf8'));fresh={};errors=[]
with pdfplumber.open(source) as pdf:
 for sku,entries in refs.items():
  e=entries[0];p=pdf.pages[e['page']-1];area=p.crop((0,max(0,e['top']-2),p.width,e['bottom']));text=area.extract_text() or ''
  temp=re.search(r'Temperature\s*([+-]\d+)\s*/\s*([+-]\d+)',text)
  rects=[r for r in p.rects if 450<r['x0']<550 and 7<r['width']<16 and 1<r['height']<5 and e['top']-3<r['top']<e['bottom']]
  rows=defaultdict(list)
  for r in rects:rows[round(r['top'],1)].append(r)
  groups=[v for k,v in sorted(rows.items()) if len(v)==5]
  bars=[sum(bool(r.get('fill')) and r.get('non_stroking_color') not in [(1,),(1,1,1),(0,0,0,0)] for r in g) for g in groups[:3]]
  if not temp or len(bars)!=3:errors.append(dict(type='pdf-extraction',code=sku))
  fresh[sku]=dict(page=e['page'],temperature=list(map(int,temp.groups())) if temp else [],bars=bars,text=text)
for p in pages:
 expected=fresh[p['code']];values=[n for label,n in p['metrics']]
 if values!=expected['bars']:errors.append(dict(type='technical-bars',file=p['file'],actual=values,expected=expected['bars']))
 ts=re.findall(r'([+-]\d+)\s*/\s*([+-]\d+)\s*°?C',' '.join(b['body'] for b in p['blocks']))
 if not ts or any(list(map(int,t))!=expected['temperature'] for t in ts):errors.append(dict(type='temperature',file=p['file'],actual=ts,expected=expected['temperature']))
 # Visible, untranslated size labels and broken text encoding.
 for term in ['\ufffd','Größe:','EINHEITSGRÖSSE']:
  if term in (root/p['file']).read_text(encoding='utf8') and (term=='\ufffd' or p['lang']=='es'):errors.append(dict(type='text-encoding-or-language',file=p['file'],term=term))
main=[p for p in pages if not ('RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']))]
groups=defaultdict(list)
for p in main:groups[p['code']].append(p)
normal=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
for sku,ps in groups.items():
 if sorted(p['lang'] for p in ps)!=['de','en','es','fr','it']:errors.append(dict(type='product-language-coverage',code=sku))
 pads={p['lang']:sorted(set(normal(m) for m in re.findall(r'(?i)road[\s-]*performance[\s-]*force|ghost[\s-]*air[\s-]*gel|x[\s-]*stra|core[\s-]*evo|doge|super[\s-]*kid',' '.join(b['body'] for b in p['blocks'])))) for p in ps}
 if len({tuple(v) for v in pads.values()})!=1:errors.append(dict(type='pad-language-parity',code=sku,values=pads))
 # Product identity, images and catalogue cards.
 for p in ps:
  if not p['gallery']:errors.append(dict(type='empty-gallery',file=p['file']))
  if not p['blocks'] or not p['blocks'][0]['body']:errors.append(dict(type='empty-description',file=p['file']))
  tree=trees[p['file']];ids=[n.a['id'] for n in tree.findall() if n.a.get('id')]
  dup=[k for k,v in Counter(ids).items() if v>1]
  if dup:errors.append(dict(type='duplicate-id',file=p['file'],values=dup))
for rel,tree in trees.items():
 if re.search(r'W\d{4}',Path(rel).name):continue
 cards=tree.findall(cls='card');codes=[]
 for card in cards:
  a=card.find(cls='product-photo');h=card.find(cls='product-name')
  if a and h:
   c=re.search(r'W\d{4}',a.a.get('href',''));shown=re.search(r'W\d{4}',h.text())
   if not c or not shown or c[0]!=shown[0]:errors.append(dict(type='card-identity',file=rel))
   if c:codes.append(c[0])
 if len(codes)!=len(set(codes)):errors.append(dict(type='duplicate-card',file=rel))
result=dict(date='2026-10-26',html=len(trees),mainProducts=len(main),codes=len(groups),pdfCodes=len(fresh),linkIssues=issues,issues=errors)
(out/'safety-static-2026-10-26.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
(out/'safety-source-2026-10-26.json').write_text(json.dumps(fresh,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
