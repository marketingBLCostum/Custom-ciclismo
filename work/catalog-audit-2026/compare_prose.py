from pathlib import Path
import json,re,sys
D=Path('work/catalog-audit-2026');pages=json.loads((D/'pages.json').read_text(encoding='utf8'));refs=json.loads((D/'references.json').read_text(encoding='utf8'))
codes=sorted(refs)[int(sys.argv[1]):int(sys.argv[2])]
for code in codes:
 en=next(p for p in pages if p['code']==code and p['lang']=='en' and not ('RAGAZZI EN' in p['file'] and (code.startswith('W66') or code in ['W0274','W2632'])))
 print('\nCODE',code,en['eyebrow'])
 print('SOURCE RIGHT:',re.sub(r'\s+',' ',' '.join(e['right'] for e in refs[code])))
 print('SITE:', ' / '.join(b['body'] for b in en['blocks'] if b['title'] not in ['Technical features','Temperature']))
