from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf8')
D=Path('work/catalog-audit-2027');pages=json.loads((D/'pdf-pages.json').read_text(encoding='utf8'))
source={'uomo':set(),'donna':set(),'bambino':set(),'accessori':set()}
for p in pages:
 n=p['page'];family='uomo' if 12<=n<=32 or 50<=n<=51 else 'donna' if 34<=n<=49 or 52<=n<=53 else 'bambino' if 55<=n<=60 else 'accessori' if 63<=n<=69 else None
 if family:source[family].update(p['codes'])
site={f:{} for f in source};unclassified=[]
for p in Path.cwd().rglob('*.html'):
 rel=p.relative_to(Path.cwd())
 if any(x in rel.parts for x in ['work','.git']):continue
 m=re.match(r'(W\d{4})(?=[_.-])',p.name)
 if not m:continue
 prefix=' '.join(rel.parts[:-1]).upper();family='donna' if 'DONNA' in prefix else 'uomo' if 'UOMO' in prefix else 'accessori' if 'ACCESSORI' in prefix else 'bambino' if 'BAMBIN' in prefix or 'RAGAZZI' in prefix else None
 if not family:unclassified.append(str(rel));continue
 # Ignore redundant English accessory pages filed under RAGAZZI.
 if family=='bambino' and m[1] in source['accessori']:continue
 lang=next((l for l,d in [('en','INGLESE'),('de','TEDESCO'),('fr','FRANCESE'),('es','SPAGNOLO')] if rel.parts[0]==d),'it')
 site[family].setdefault(m[1],{}).setdefault(lang,[]).append(str(rel))
res={f:{'catalogCount':len(source[f]),'siteCount':len(site[f]),'missing':sorted(source[f]-site[f].keys()),'siteOnly':sorted(site[f].keys()-source[f]),'languageGaps':{c:[l for l in ['it','en','de','fr','es'] if l not in site[f].get(c,{})] for c in source[f] if c in site[f] and len(site[f][c])!=5}} for f in source}
res['unclassified']=unclassified
(D/'category-presence.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(res,ensure_ascii=False,indent=2))
allsource=set().union(*source.values());allsite=set().union(*(set(v) for v in site.values()));print('UNIQUE SOURCE',len(allsource),'SITE',len(allsite),'NEW UNIQUE',sorted(allsource-allsite))
other=sorted(set(re.findall(r'\b[A-Z]{1,3}\d{3,6}\b',' '.join(p['text'] for p in pages)))-allsource);print('OTHER CODE-LIKE TOKENS',other)
for f in ['donna','accessori']:
 for c in res[f]['missing']:
  print(f,c,'PDF pages',[p['page'] for p in pages if c in p['codes'] and p['page']>10])
print('W6541 SITE',site['donna'].get('W6541'))
