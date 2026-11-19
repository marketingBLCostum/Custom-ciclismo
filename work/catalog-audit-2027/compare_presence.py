from pathlib import Path
import json,re,sys
import pypdfium2 as pdfium
sys.stdout.reconfigure(encoding='utf8')
root=Path.cwd();out=root/'work/catalog-audit-2027'
pdfpath=Path(r'\\Serverbl\dati\Documenti Comuni\___LORENZO\___ da Massimo\BL_CC_Team_ENG_2027 - 27-10-2026 - new_CICLISMO.pdf')
pdf=pdfium.PdfDocument(str(pdfpath));pages=[];bycode={}
for i in range(len(pdf)):
 page=pdf[i];tp=page.get_textpage();text=tp.get_text_range();codes=sorted(set(re.findall(r'\bW\s*\d{4}\b',text)))
 codes=[re.sub(r'\s','',c) for c in codes];pages.append({'page':i+1,'text':text,'codes':codes})
 for c in codes:bycode.setdefault(c,[]).append(i+1)
 tp.close();page.close()
langs={'it':root,'en':root/'INGLESE','de':root/'TEDESCO','fr':root/'FRANCESE','es':root/'SPAGNOLO'};site={};allfiles=[]
for p in root.rglob('*.html'):
 rel=p.relative_to(root)
 if any(x in rel.parts for x in ['work','.git']):continue
 m=re.match(r'(W\d{4})(?:[-_])',p.name)
 if not m:continue
 lang=next((k for k,v in langs.items() if k!='it' and rel.parts[0]==v.name),'it')
 site.setdefault(m[1],{}).setdefault(lang,[]).append(str(rel));allfiles.append(str(rel))
result={'pdf':str(pdfpath),'pageCount':len(pdf),'catalogCodes':bycode,'siteCodes':site,'missing':sorted(set(bycode)-set(site)),'siteOnly':sorted(set(site)-set(bycode)),'missingLanguages':{c:[l for l in langs if l not in site.get(c,{})] for c in bycode if any(l not in site.get(c,{}) for l in langs)}}
(out/'pdf-pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
(out/'product-presence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ['siteCodes','catalogCodes']},ensure_ascii=False,indent=2))
print('CATALOG CODES',len(bycode),'SITE CODES',len(site),'PRODUCT HTML',len(allfiles))
for p in pages:
 print('PAGE',p['page'],'CODES',','.join(p['codes']),'START',re.sub(r'\s+',' ',p['text'])[:150])
for c in result['missing']:
 print('\nMISSING',c)
 for p in pages:
  if c in p['codes']:
   for m in re.finditer(c,p['text']):print('PAGE',p['page'],re.sub(r'\s+',' ',p['text'][max(0,m.start()-80):m.start()+450]))
