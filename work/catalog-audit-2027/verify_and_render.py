from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageOps,ImageDraw
import json,re,sys
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf8')
D=Path('work/catalog-audit-2027');pdf=pdfium.PdfDocument(r'\\Serverbl\dati\Documenti Comuni\___LORENZO\___ da Massimo\BL_CC_Team_ENG_2027 - 27-10-2026 - new_CICLISMO.pdf')
nums=[9,10,37,38,39,40,41,42,44,45,46,47,48,49,67]
for n in nums:
 page=pdf[n-1];im=page.render(scale=1.3).to_pil();im.save(D/f'page-{n}.png');page.close()
for k in range(0,len(nums),4):
 group=nums[k:k+4];ims=[]
 for n in group:
  im=Image.open(D/f'page-{n}.png').convert('RGB');im.thumbnail((800,1050));ims.append(im)
 w=max(i.width for i in ims);h=max(i.height for i in ims)+30;sheet=Image.new('RGB',(w*2,h*2),'#bbbbbb');draw=ImageDraw.Draw(sheet)
 for j,(n,im) in enumerate(zip(group,ims)):
  x=(j%2)*w;y=(j//2)*h;sheet.paste(im,(x,y+25));draw.text((x+10,y+5),f'PDF page {n}',fill='black')
 sheet.save(D/f'visual-{k//4+1}.png')
class A(HTMLParser):
 def __init__(self):super().__init__();self.hrefs=[]
 def handle_starttag(self,t,a):
  if t=='a':self.hrefs.extend(v for k,v in a if k=='href')
langs=[('', ''),('INGLESE','_EN'),('FRANCESE','_FR'),('TEDESCO','_DE'),('SPAGNOLO','_ES')];res={}
for folder,suffix in langs:
 for cat in ['uomo','donna','ragazzi','accessori']:
  p=Path(folder)/f'{cat}{suffix}.html';parser=A();parser.feed(p.read_text(encoding='utf8'));codes=set()
  for href in parser.hrefs:
   m=re.search(r'\b(W\d{4})(?=[._-])',href)
   if m:codes.add(m[1])
  res[str(p)]=sorted(codes)
(D/'category-links.json').write_text(json.dumps(res,indent=2),encoding='utf8')
print('Rendered',nums)
for k,v in res.items():print(k,len(v))
print('OTHER TOKEN D110',[(p['page'],p['text'][max(0,p['text'].find('D110')-100):p['text'].find('D110')+160]) for p in json.loads((D/'pdf-pages.json').read_text(encoding='utf8')) if 'D110' in p['text']])
