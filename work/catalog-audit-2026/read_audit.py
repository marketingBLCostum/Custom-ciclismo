from pathlib import Path
from collections import Counter,defaultdict
import json,sys,re
D=Path('work/catalog-audit-2026')
pages=json.loads((D/'pages.json').read_text(encoding='utf8'))
refs=json.loads((D/'references.json').read_text(encoding='utf8')) if (D/'references.json').exists() else {}
facts=json.loads((D/'facts.json').read_text(encoding='utf8')) if (D/'facts.json').exists() else {}
mode=sys.argv[1] if len(sys.argv)>1 else 'links'
if mode=='links':
    issues=json.loads((D/'link-issues.json').read_text(encoding='utf8'))
    groups=defaultdict(list)
    for p in issues:groups[(p['type'],p.get('value',''))].append(p)
    for (typ,value),items in groups.items():
        print(typ,repr(value),'COUNT',len(items),'EXAMPLES',[(x['file'],x.get('line')) for x in items[:3]])
elif mode=='text':
    en=sorted([p for p in pages if p['lang']=='en' and not ('RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']))],key=lambda p:p['code'])
    start=int(sys.argv[2]);end=int(sys.argv[3])
    for p in en[start:end]:
        print('\n===',p['code'],p['title'],p['eyebrow'],p['file'],'===')
        print('PDF',json.dumps(refs.get(p['code']),ensure_ascii=False))
        print('SITE',json.dumps(p['blocks'],ensure_ascii=False))
        it=next((q for q in pages if q['code']==p['code'] and q['lang']=='it'),None)
        print('ITALIAN',it['eyebrow'] if it else '?',json.dumps(it['blocks'] if it else [],ensure_ascii=False))
elif mode=='facts':
    groups=defaultdict(list)
    for p in pages:groups[p['code']].append(p)
    for code,ps in sorted(groups.items()):
        texts={p['lang']:' '.join(x['body'] for x in p['blocks']) for p in ps}
        pads={p['lang']:facts[p['file']]['pad'] for p in ps}
        brands={p['lang']:facts[p['file']]['brand'] for p in ps}
        normalized=lambda xs: sorted(set(re.sub(r'[^a-z0-9]','',x.lower()) for x in xs))
        if len({str(normalized(v)) for v in pads.values()})>1:print('PAD DIFFERENCE',code,pads)
        if len({str(normalized(v)) for v in brands.values()})>1:print('BRAND DIFFERENCE',code,brands)
        print('SUMMARY',code,[(p['lang'],p['eyebrow'],p['sizes'],p['metrics'],[(x['title'],len(x['body']),len(x['items'])) for x in p['blocks']]) for p in ps if not ('RAGAZZI EN' in p['file'] and int(code[1:])>=2600)])
elif mode=='detail':
    codes=sys.argv[2:]
    for code in codes:
        print('\nSOURCE',code,json.dumps(refs.get(code),ensure_ascii=False))
        for p in pages:
            if p['code']==code:print('PAGE',json.dumps(p,ensure_ascii=False))
elif mode=='compact':
    for code in sorted(set(p['code'] for p in pages)):
        source=' '.join(x['text'] for x in refs.get(code,[]))
        src_temp=re.findall(r'Temperature\s*([^\n]+)',source)
        print(code,'PDFTEMP',src_temp)
        for p in pages:
            if p['code']!=code:continue
            text=' '.join(x['body'] for x in p['blocks'])
            temp=re.findall(r'\+\s*\d+\s*(?:°C)?\s*[/—–-]\s*\+?\s*\d+\s*°?C?',text)
            print(p['lang'],'TEMP',temp,'FACTS',facts.get(p['file'],{}))

