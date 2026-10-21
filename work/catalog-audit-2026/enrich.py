from pathlib import Path
import json,re,pdfplumber
D=Path('work/catalog-audit-2026');refs=json.loads((D/'references.json').read_text(encoding='utf8'))
refs={k:[e for e in v if e['page']>=11] for k,v in refs.items()}
src=r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf'
with pdfplumber.open(src) as pdf:
 p=pdf.pages[16];seg=p.crop((0,50,p.width,419));refs['W6308']=[dict(page=17,top=50,bottom=419,text=seg.extract_text() or '',right=seg.crop((365,50,p.width,419)).extract_text() or '')]
(D/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf8')
pages=json.loads((D/'pages.json').read_text(encoding='utf8'));facts=json.loads((D/'facts.json').read_text(encoding='utf8'))
for code in sorted(refs):
 ps=[p for p in pages if p['code']==code and not ('RAGAZZI EN' in p['file'] and (code.startswith('W66') or code in ['W0274','W2632']))]
 en=next(p for p in ps if p['lang']=='en');source=' '.join(e['text'] for e in refs[code]);text=' '.join(b['body'] for b in en['blocks'])
 refnumbers=sorted(set(re.findall(r'\d+(?:[.,]\d+)?',source)));webnumbers=sorted(set(re.findall(r'\d+(?:[.,]\d+)?',text)))
 temps=re.findall(r'Temperature\s*([^\n]+)',source)
 pads={p['lang']:facts[p['file']]['pad'] for p in ps}
 normalize=lambda xs:sorted(set(re.sub(r'[^a-z0-9]','',x.lower()) for x in xs))
 ppad=normalize(re.findall(r'(?i)road\s*performance\s*force|ghost\s*air\s*gel|x[\s-]*stra|core\s*evo|doge',source))
 epad=normalize(facts[en['file']]['pad'])
 bad={lang:vals for lang,vals in pads.items() if normalize(vals)!=epad}
 print(code,'PDFTEMP',temps,'EXTRA NUMBERS',sorted(set(webnumbers)-set(refnumbers)),'MISSING NUMBERS',sorted(set(refnumbers)-set(webnumbers)),'PAD SOURCE/SITE',ppad,epad,'LANGDIFF',bad)

