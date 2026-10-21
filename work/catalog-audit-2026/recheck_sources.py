from pathlib import Path
import json,re,zipfile,hashlib,sys
import pdfplumber,pypdfium2 as pdfium
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd();out=root/'work/catalog-audit-2026';src=Path(r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf')
refs=json.loads((out/'references.json').read_text(encoding='utf8'))
targets=['W6005','W6028','W6036','W6514','W6515','W6012','W6518','W6047','W7200','W7201','W7202','W7203','W7204','W7205','W6301','W6512','W6009','W2212','W2218']
rechecked={}
with pdfplumber.open(src) as pdf:
 for code in targets:
  e=refs[code][0];p=pdf.pages[e['page']-1];text=p.crop((0,max(0,e['top']-2),p.width,e['bottom'])).extract_text() or ''
  rechecked[code]={'page':e['page'],'text':text}
  print(code,'PDF',e['page'],'TEMPERATURE',re.findall(r'Temperature\s*([^\n]+)',text))
(out/'rechecked-sources.json').write_text(json.dumps(rechecked,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(out/'before-fixes.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
 files=[f for f in root.rglob('*.html') if 'work' not in f.relative_to(root).parts]
 for f in files:z.write(f,f.relative_to(root))
(out/'before-fixes-hashes.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2),encoding='utf8')
print('Backed up',len(files),'HTML files. PDF bytes:',src.stat().st_size)
doc=pdfium.PdfDocument(str(src))
for pg in [15,31,33,36]:doc[pg-1].render(scale=1.4).to_pil().save(out/f'rechecked-page-{pg}.png')
