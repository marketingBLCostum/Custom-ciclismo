from pathlib import Path
from collections import Counter
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026');pages=json.loads((D/'pages.json').read_text(encoding='utf8'));issues=json.loads((D/'browser-issues.json').read_text(encoding='utf8'))['issues']
primary={p['file'] for p in pages if not ('RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']))}
print('PRIMARY',len(primary),'RUNTIME',sum(bool(i.get('errors')) and i['file'] in primary for i in issues),'MOBILE',sum(i.get('mobile',{}).get('overflow',False) and i['file'] in primary for i in issues))
for lang,bad in [('es',r'Beschreibung|Hauptmerkmale|Technische|Größe|EINHEITSGRÖSSE|Descrizione|Taglia'),('en',r'\bDescrizione\b|\bTaglia\b|CARATTERISTICHE PRINCIPALI|Scopri altri|Voglio maggiori|Tessuto|Bretelle'),('fr',r'\bDescrizione\b|\bTaglia\b|CARATTERISTICHE PRINCIPALI|Scopri altri|Voglio maggiori'),('de',r'\bDescrizione\b|\bTaglia\b|CARATTERISTICHE PRINCIPALI|Scopri altri|Voglio maggiori')]:
 for p in pages:
  if p['lang']!=lang or p['file'] not in primary:continue
  t=(Path.cwd()/p['file']).read_text(encoding='utf8')
  found=[(t[:m.start()].count('\n')+1,m[0]) for m in re.finditer(bad,t)]
  if found:print('LANGUAGE REMNANT',p['file'],found)
for code in ['W6005','W6028','W6036','W6514','W6515']:
 for p in pages:
  if p['code']==code and p['lang']=='it':print('REFERENCES',code,p['file'],[(b['title'],b['line']) for b in p['blocks']])
for code in ['W0274','W2200']:
 p=next(p for p in pages if p['code']==code and p['lang']=='it');t=(Path.cwd()/p['file']).read_text(encoding='utf8');print('JSREF',code,[(i+1,l.strip()) for i,l in enumerate(t.splitlines()) if 'accIcon.textContent' in l])
