from pathlib import Path
from collections import Counter,defaultdict
import json,re,sys,pdfplumber,pypdfium2 as pdfium
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026');pages=json.loads((D/'pages.json').read_text(encoding='utf8'));refs=json.loads((D/'references.json').read_text(encoding='utf8'));browser=json.loads((D/'browser-issues.json').read_text(encoding='utf8'))
for code in sorted(refs):
 ps=[p for p in pages if p['code']==code and not ('RAGAZZI EN' in p['file'] and (code.startswith('W66') or code in ['W0274','W2632']))]
 normal=lambda p:sorted(set(re.findall(r'\d+(?:[.,]\d+)?',' '.join(x['body'] for x in p['blocks']))))
 nums={p['lang']:normal(p) for p in ps};en=nums['en']
 bad={k:v for k,v in nums.items() if v!=en}
 metrics={p['lang']:[n for label,n in p['metrics']] for p in ps};em=metrics['en'];mb={k:v for k,v in metrics.items() if v!=em}
 counts={p['lang']:[len(x['items']) for x in p['blocks'] if x['items']] for p in ps}
 if bad or mb or len({str(v) for v in counts.values()})>1:print('PARITY',code,'NUM',nums if bad else 'OK','METRICS',metrics if mb else 'OK','ITEMS',counts)
 if code.startswith('W66') or code in ['W0274','W2632']:
  print('SIZES',code,[(p['lang'],p['sizes']) for p in ps], 'PDF',re.findall(r'Sizes[^\n]*',' '.join(e['text'] for e in refs[code])))
print('BROWSER COUNTS',len(browser['issues']),Counter('runtime' if i.get('errors') else 'other' for i in browser['issues']))
print('SYNTAX',[(i['file'],i.get('errors')) for i in browser['issues'] if any('Unexpected' in e for e in i.get('errors',[]))])
over=[i['file'] for i in browser['issues'] if i.get('mobile',{}).get('overflow')];print('OVERFLOW',len(over),over)
src=r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf'
doc=pdfium.PdfDocument(src)
for pg in [15,31,36,41,42,43,47]:doc[pg-1].render(scale=1.6).to_pil().save(D/f'source-{pg}.png')
with pdfplumber.open(src) as pdf:
 p=pdf.pages[35]
 print('CHART RECTS',[(round(r['x0'],1),round(r['top'],1),round(r['width'],1),round(r['height'],1),r.get('fill'),r.get('non_stroking_color')) for r in p.rects if r['x0']>440 and r['height']<8])
