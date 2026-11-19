from pathlib import Path
from PIL import Image, ImageOps, ImageChops, ImageStat, ImageDraw
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json, hashlib, shutil, re, datetime, sys, math

sys.stdout.reconfigure(encoding='utf8')
ROOT=Path.cwd(); OUT=ROOT/'work/image-sync-2026-11-19'
data=json.loads((OUT/'inventory.json').read_text(encoding='utf8'))
SOURCE=Path(data['source'])

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''):h.update(b)
    return h.hexdigest()

extras=[k for k in data['sourceOnly'] if not any(t in k for t in ('non usare','/no/'))]
items=[dict(d,kind='matching-path') for d in data['different']]
items += [dict(key=k,source=data['remote'][k],local=None,kind='unreferenced-candidate') for k in extras]

def inspect(item):
    item=dict(item); rel=item['source']['path']; src=SOURCE/rel; staged=OUT/'staging'/rel
    staged.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,staged)
    actual=digest(staged)
    if item['source'].get('sha256'):assert actual==item['source']['sha256'],rel
    item['source']['sha256']=actual
    with Image.open(staged) as im:
        item['sourceImage']={'size':list(im.size),'format':im.format,'mode':im.mode}
        im.load(); s=ImageOps.exif_transpose(im).convert('RGBA')
    if item['local']:
        with Image.open(ROOT/item['local']['path']) as im:
            item['localImage']={'size':list(im.size),'format':im.format,'mode':im.mode}
            im.load(); l=ImageOps.exif_transpose(im).convert('RGBA')
        item['identicalPixels']=l.size==s.size and l.tobytes()==s.tobytes()
        a=l.resize((256,256)).convert('RGB'); b=s.resize((256,256)).convert('RGB')
        item['meanDifference']=round(sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3,3)
        item['aspectChanged']=abs(l.width/l.height-s.width/s.height)>0.005
    return item

with ThreadPoolExecutor(max_workers=4) as pool:
    inspected=[]
    for i,item in enumerate(pool.map(inspect,items),1):
        inspected.append(item)
        if i%60==0:print('Decoded and staged',i,'/',len(items),flush=True)
(OUT/'inspection.json').write_text(json.dumps(inspected,ensure_ascii=False,indent=2),encoding='utf8')

def thumb(p,size=(175,205)):
    with Image.open(p) as im:
        im=ImageOps.exif_transpose(im).convert('RGBA'); im.thumbnail(size)
        bg=Image.new('RGB',size,'#e7e7e7'); bg.paste(im,((size[0]-im.width)//2,(size[1]-im.height)//2),im)
        return bg

for start in range(0,len(inspected),12):
    chunk=inspected[start:start+12]; sheet=Image.new('RGB',(1100,1040),'white');draw=ImageDraw.Draw(sheet)
    for j,item in enumerate(chunk):
        x=(j%3)*366; y=(j//3)*260
        label=item['source']['path'].replace('images/','')
        draw.text((x+4,y+3),label,fill='black')
        draw.text((x+4,y+18),'LOCAL',fill='black');draw.text((x+186,y+18),'SERVER',fill='black')
        if item['local']:sheet.paste(thumb(ROOT/item['local']['path']),(x+4,y+35))
        else:draw.text((x+10,y+90),'NEW FILE / WORKING COPY',fill='black')
        sheet.paste(thumb(OUT/'staging'/item['source']['path']),(x+186,y+35))
        if item['local']:draw.text((x+4,y+242),f"{item['localImage']['size']} -> {item['sourceImage']['size']}  diff={item['meanDifference']}",fill='black')
    sheet.save(OUT/f'comparison-{start//12+1:02}.jpg',quality=94)

print('Changed pixels',sum(not i.get('identicalPixels',False) for i in inspected if i['local']),'identical pixels',sum(i.get('identicalPixels',False) for i in inspected))
print('Aspect changes',[(i['source']['path'],i['localImage']['size'],i['sourceImage']['size']) for i in inspected if i.get('aspectChanged')])
print('Biggest normalized differences',[(i['source']['path'],i['meanDifference']) for i in sorted((i for i in inspected if i['local']),key=lambda i:-i['meanDifference'])[:30]])
for i in inspected:
    if not i['local']:
        folder=Path(i['source']['path']).parent
        code=re.search(r'w\d{4}',str(folder),re.I)
        if not code:continue
        active=[v for k,v in data['remote'].items() if k.startswith(str(folder).replace('\\','/').casefold().split('/nuove')[0]+'/') and len(Path(v['path']).parts)==4]
        print('EXTRA',i['source']['path'],datetime.datetime.fromtimestamp(i['source']['mtime_ns']/1e9).isoformat(),'active latest',max((datetime.datetime.fromtimestamp(v['mtime_ns']/1e9).isoformat() for v in active),default='NONE'))
print('Comparison sheets',(len(inspected)+11)//12)
