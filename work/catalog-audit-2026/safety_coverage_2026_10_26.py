from pathlib import Path
from collections import defaultdict,Counter
from urllib.parse import urlsplit,unquote
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd();out=root/'work/catalog-audit-2026';code=(out/'audit.py').read_text(encoding='utf-8-sig');exec(code.split('files=sorted')[0])
metadata=json.loads((out/'pages.json').read_text(encoding='utf8'));expected=defaultdict(dict)
for p in metadata:
 if 'RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']):continue
 section=next(part.split()[0] for part in Path(p['file']).parts if part.split()[0] in ['UOMO','DONNA','RAGAZZI','ACCESSORI'])
 expected[(p['lang'],section)][p['code']]=p['file']
errors=[];counts={};caseissues=[];cache={};texts=[]
for file in root.rglob('*.html'):
 rel=file.relative_to(root)
 if 'work' in rel.parts:continue
 raw=file.read_text(encoding='utf8');parser=P();parser.feed(raw);tree=parser.root;lang=langof(rel)
 if re.fullmatch(r'(uomo|donna|ragazzi|accessori)(?:_[A-Z]{2})?\.html',file.name):
  section=file.name.split('_')[0].split('.')[0].upper();cards=[]
  for card in tree.findall(cls='card'):
   a=card.find(cls='product-photo')
   if not a:continue
   m=re.search(r'W\d{4}',a.a.get('href',''))
   if m:cards.append(m[0])
  want=expected[(lang,section)];counts[str(rel)]=len(cards)
  if set(cards)!=set(want):errors.append(dict(file=str(rel),missing=sorted(set(want)-set(cards)),extra=sorted(set(cards)-set(want))))
 for n in tree.findall():
  for attr in ['href','src']:
   link=n.a.get(attr,'');u=urlsplit(link)
   if u.scheme or u.netloc or not u.path:continue
   p=(file.parent/unquote(u.path)).resolve()
   if not p.exists() or not p.is_relative_to(root):continue
   current=root
   for part in p.relative_to(root).parts:
    k=str(current)
    if k not in cache:cache[k]={x.name.lower():x.name for x in current.iterdir()}
    actual=cache[k].get(part.lower(),part)
    if actual!=part:caseissues.append(dict(file=str(rel),value=link,expected=actual,actual=part))
    current=current/actual
 def visible(n):
  if n.tag in ['script','style']:return ''
  return ' '.join(c if isinstance(c,str) else visible(c) for c in n.c)
 if lang!='it':
  body=tree.find(tag='body');txt=re.sub(r'\s+',' ',visible(body or tree))
  for pattern in [r'Produzione italiana',r'Richiedi preventivo',r'Scopri altri prodotti',r'Voglio maggiori informazioni',r'Come Funziona',r'Caratteristiche principali',r'\bTaglia:',r'\bDescrizione\b']:
   for match in re.finditer(pattern,txt,re.I):texts.append(dict(file=str(rel),phrase=match[0]))
result=dict(date='2026-10-26',categories=counts,coverageIssues=errors,caseIssues=caseissues,untranslatedItalian=texts)
(out/'safety-coverage-2026-10-26.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
