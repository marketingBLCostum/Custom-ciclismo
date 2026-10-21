from pathlib import Path
import json,re,sys,pypdfium2 as pdfium
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026');root=Path.cwd();refs=json.loads((D/'references.json').read_text(encoding='utf8'));pages=json.loads((D/'pages.json').read_text(encoding='utf8'))
source=r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf'
doc=pdfium.PdfDocument(source)
canvas=Image.new('RGB',(800,440),'white');draw=ImageDraw.Draw(canvas)
for i,code in enumerate(['W6301','W6512']):
 e=refs[code][0];im=doc[e['page']-1].render(scale=3).to_pil();box=(400,max(0,e['top']-5),570,e['top']+90)
 crop=im.crop(tuple(round(v*3) for v in box));crop.thumbnail((720,175));canvas.paste(crop,(0,i*220+30));draw.text((5,i*220+5),code,fill='black')
canvas.save(D/'ratings-source.png')
# Exact inbound links to duplicate English accessory pages.
from urllib.parse import urlsplit,unquote
incoming={}
for f in root.rglob('*.html'):
 if 'work' in f.relative_to(root).parts:continue
 for link in re.findall(r'href\s*=\s*"([^"]+)"',f.read_text(encoding='utf8')):
  u=urlsplit(link)
  if u.scheme or u.netloc or not u.path:continue
  t=(f.parent/unquote(u.path)).resolve()
  if not t.is_relative_to(root):continue
  rel=str(t.relative_to(root))
  if rel.startswith('INGLESE\\RAGAZZI EN\\') and re.search(r'W(?:0274|2632|66\d\d)',rel):
   if t!=f:incoming.setdefault(rel,[]).append(str(f.relative_to(root)))
print('DUPLICATE NON-SELF INCOMING',incoming)
for code in ['W6012','W6514','W6518']:
 print('OPTION INVENTORY',code,[(p['lang'],[b['body'] for b in p['blocks'] if b['title'].lower() in ['options','opzioni','optionen','opciones']]) for p in pages if p['code']==code])
for p in pages:
 if p['code']=='W6009':print('W6009DESC',p['lang'],p['blocks'][0]['body'][:200])
print('METRIC COUNT EXAMPLES',[(p['code'],p['lang'],p['metrics']) for p in pages if p['code'] in ['W6301','W6512']])
