from pathlib import Path
from collections import defaultdict,Counter
from urllib.parse import urlsplit,unquote
import json,re,sys,pdfplumber
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026');root=Path.cwd();pages=json.loads((D/'pages.json').read_text(encoding='utf8'));refs=json.loads((D/'references.json').read_text(encoding='utf8'))
source=r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf'
ratings={};ratingissues=[]
with pdfplumber.open(source) as pdf:
 for code,entries in refs.items():
  e=entries[0];p=pdf.pages[e['page']-1]
  rects=[r for r in p.rects if 450<r['x0']<550 and 7<r['width']<16 and 1<r['height']<5 and e['top']-3<r['top']<e['bottom']]
  rows=defaultdict(list)
  for r in rects: rows[round(r['top'],1)].append(r)
  groups=[v for k,v in sorted(rows.items()) if len(v)==5]
  if len(groups)>=3:
   values=[sum(bool(r.get('fill')) and r.get('non_stroking_color') not in [(1,),(1,1,1),(0,0,0,0)] for r in g) for g in groups[:3]]
   ratings[code]=values
   for page in pages:
    if page['code']==code and page['lang']=='it' and page['metrics'] and [v for k,v in page['metrics']]!=values:
     ratingissues.append(dict(code=code,pdf=values,web=page['metrics'],file=page['file']))
print('RATINGS EXTRACTED',len(ratings),'DIFFERENCES',ratingissues)
(D/'ratings.json').write_text(json.dumps(dict(ratings=ratings,issues=ratingissues),ensure_ascii=False,indent=2),encoding='utf8')
caseissues=[]; cache={}
for f in root.rglob('*.html'):
 if 'work' in f.relative_to(root).parts:continue
 for match in re.finditer(r'(?:src|href)\s*=\s*"([^"]+)"',f.read_text(encoding='utf8')):
  link=match[1];u=urlsplit(link)
  if u.scheme or u.netloc or not u.path:continue
  p=(f.parent/unquote(u.path)).resolve()
  if not p.exists() or not p.is_relative_to(root):continue
  current=root
  for part in p.relative_to(root).parts:
   key=str(current)
   if key not in cache:cache[key]={n.name.lower():n.name for n in current.iterdir()}
   actual=cache[key].get(part.lower(),part)
   if actual!=part:caseissues.append(dict(file=str(f.relative_to(root)),line=f.read_text(encoding='utf8')[:match.start()].count('\n')+1,href=link,asked=part,actual=actual))
   current=current/actual
(D/'case-issues.json').write_text(json.dumps(caseissues,ensure_ascii=False,indent=2),encoding='utf8')
print('CASE ISSUES',len(caseissues),dict(Counter((x['asked'],x['actual']) for x in caseissues)))
print('EXAMPLES',caseissues[:12])
