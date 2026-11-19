from pathlib import Path
from collections import Counter, defaultdict
import hashlib, json, re, sys

sys.stdout.reconfigure(encoding='utf8')
ROOT=Path.cwd();OUT=ROOT/'work/image-sync-2026-11-19'
inv=json.loads((OUT/'inventory.json').read_text(encoding='utf8'))
ins=json.loads((OUT/'inspection.json').read_text(encoding='utf8'))
bykey={i['key']:i for i in ins};plan={};skipped=[]

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def add(sourcekey,destkey,reason):
 src=bykey[sourcekey];dst=inv['local'][destkey]
 sourcecode=re.findall(r'w\d{4}',sourcekey)
 destcode=re.findall(r'w\d{4}',destkey)
 assert sourcecode and destcode and sourcecode[0]==destcode[0],(sourcekey,destkey)
 assert src['source']['mtime_ns']>dst['mtime_ns'],(sourcekey,'not newer')
 assert inv['localRefs'].get(destkey),(destkey,'not used')
 assert digest(ROOT/dst['path'])==dst.get('sha256',digest(ROOT/dst['path'])),(destkey,'local changed')
 assert digest(OUT/'staging'/src['source']['path'])==src['source']['sha256']
 plan[destkey]={'source':src['source'],'destination':dict(dst,sha256=digest(ROOT/dst['path'])),'reason':reason,'pages':inv['localRefs'][destkey]}

for i in ins:
 if not i.get('local'):continue
 key=i['key']
 if i.get('identicalPixels'):
  skipped.append({'path':i['local']['path'],'reason':'Raster identico: differisce soltanto il file/contenitore.'});continue
 if key=='images/ragazzi/w2212/6.png':
  skipped.append({'path':i['local']['path'],'reason':'La versione server ripete la vista frontale di 5.png, eliminando la foto del retro. Conservata la vista posteriore locale.'});continue
 if not inv['localRefs'].get(key):
  skipped.append({'path':i['local']['path'],'reason':'Immagine non usata nelle pagine locali.'});continue
 add(key,key,'Immagine server attiva, piu recente, stesso percorso e prodotto.')

# User explicitly confirmed use of the newer NUOVE photo sets.
for number in range(1,5):
 add(f'images/uomo/w6012/nuove/{number}_.png',f'images/uomo/w6012/{number}.png','Set NUOVE approvato dall\'utente; variante numerata piu recente, stesso body W6012.')

new6015={1:'nuove/6801f56d-b1fe-4d12-98f7-c1f48cebb607.png',2:'nuove/2_.png',3:'nuove/3_.png',4:'nuove/4_.png',5:'5_.png',6:'6_.png'}
for number,suffix in new6015.items():
 add(f'images/uomo/w6015/{suffix}',f'images/uomo/w6015/{number}.png','Set W6015 aggiornato: foto NUOVE approvate; fronte principale del 16 settembre e viste di dettaglio corrispondenti.')

add('images/uomo/w6301/4_.png','images/uomo/w6301/4.png','Vista posteriore W6301: il file server aggiornato ha il suffisso _, verificata la corrispondenza visiva.')

# Record all existing production content, not only the replacement targets.
baseline={}
for p in ROOT.rglob('*'):
 rel=p.relative_to(ROOT)
 if any(x.lower() in {'.git','work','node_modules'} for x in rel.parts):continue
 if p.is_file():baseline[rel.as_posix()]=digest(p)

ordered=sorted(plan.values(),key=lambda p:p['destination']['path'].casefold())
affected=sorted({r['html'] for p in ordered for r in p['pages']})
(OUT/'plan.json').write_text(json.dumps({'replacements':ordered,'skipped':skipped,'affectedPages':affected,'baseline':baseline},ensure_ascii=False,indent=2),encoding='utf8')
groups=defaultdict(list)
for p in ordered:
 rel=p['destination']['path'];parts=rel.split('/');category=parts[1];code=re.search(r'W\d{4}',rel,re.I)[0].upper();groups[category+'/'+code].append(Path(rel).name)
print('Replacement images',len(ordered),'products/categories',len(groups),'affected HTML',len(affected),'skipped',len(skipped))
print('By category',dict(Counter(p['destination']['path'].split('/')[1] for p in ordered)))
for g,v in groups.items():print(g,', '.join(v))
print('Total original/new MB',round(sum(p['destination']['size'] for p in ordered)/1e6,2),round(sum(p['source']['size'] for p in ordered)/1e6,2))
