from pathlib import Path
import zipfile,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026')
with zipfile.ZipFile(D/'verification-snapshot.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for name in ['pages.json','link-issues.json','browser-issues.json','facts.json','ratings.json']:
  z.write(D/name,name)
source=(D/'audit.py').read_text(encoding='utf-8-sig')
exec(source.split('refs={}; pdfpages=[]')[0])
print('RECHECKED HTML',len(trees),'PRODUCT PAGES',len(pages),'LINK ISSUES',len(issues))
for i in issues[:20]:print(i)
assert not issues
ratings=json.loads((D/'ratings.json').read_text(encoding='utf8'))['ratings']
problems=[]
for p in pages:
 t=(Path.cwd()/p['file']).read_text(encoding='utf8');tree=P();tree.feed(t)
 side=tree.root.find(cls='sidebar');metrics=side.findall(cls='metric')
 actual=[]
 for m in metrics:
  spans=m.find(cls='bars').findall(tag='span');actual.append((sum('on' in s.a.get('class','').split() for s in spans),len(spans)))
 if len(actual)!=3 or any(total!=5 for on,total in actual) or any(abs(on/total-ref/5)>0.01 for (on,total),ref in zip(actual,ratings[p['code']])):problems.append((p['file'],'metrics',actual,ratings[p['code']]))
 code=p['code'];alltext=' '.join(b['body'] for b in p['blocks']);source_entries=json.loads((D/'references.json').read_text(encoding='utf8'))[code]
 expected=re.search(r'Temperature\s*([+-]\d+)\s*/\s*([+-]\d+)',' '.join(e['text'] for e in source_entries))
 temps=re.findall(r'([+-]\d+)\s*/\s*([+-]\d+)\s*°?C',alltext)
 if expected and (not temps or any(tuple(map(int,v))!=tuple(map(int,expected.groups())) for v in temps)):problems.append((p['file'],'temperature',temps,expected.groups()))
print('TECHNICAL DATA ERRORS',problems)
assert not problems
print('All local files, contact anchors, language destinations, temperatures and technical bars are valid.')


