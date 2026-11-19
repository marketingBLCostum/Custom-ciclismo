from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, shutil, os, sys, datetime

sys.stdout.reconfigure(encoding='utf8')
ROOT=Path.cwd().resolve();OUT=ROOT/'work/image-sync-2026-11-19'
SOURCE=Path(r'\\Serverbl\dati\Documenti Comuni\___LORENZO\SITI CUSTOM\CICLISMO')
plan=json.loads((OUT/'plan.json').read_text(encoding='utf8'))
items=plan['replacements'];BACKUP=OUT/'before';JOURNAL=OUT/'applied.json'

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def preflight(item):
 dst=(ROOT/item['destination']['path']).resolve()
 assert dst.is_relative_to(ROOT/'images'),str(dst)
 staged=OUT/'staging'/item['source']['path']
 assert digest(dst)==item['destination']['sha256'],str(dst)+' local changed'
 assert digest(staged)==item['source']['sha256'],str(staged)+' staged changed'
 assert digest(SOURCE/item['source']['path'])==item['source']['sha256'],item['source']['path']+' server changed'
 with Image.open(staged) as im:im.verify()
 return True

with ThreadPoolExecutor(max_workers=4) as pool:assert all(pool.map(preflight,items))
print('All',len(items),'source/staged/destination preflight checks passed.',flush=True)

# Back up every destination before replacing any image.
for item in items:
 dst=ROOT/item['destination']['path'];backup=BACKUP/item['destination']['path']
 backup.parent.mkdir(parents=True,exist_ok=True)
 assert not backup.exists(),'Refusing to overwrite an existing backup: '+str(backup)
 shutil.copy2(dst,backup)
 assert digest(backup)==item['destination']['sha256']
print('All original images backed up and verified.',flush=True)

applied=[]
for item in items:
 dst=ROOT/item['destination']['path'];staged=OUT/'staging'/item['source']['path']
 assert digest(dst)==item['destination']['sha256'],str(dst)+' changed during backup'
 os.replace(staged,dst)
 assert digest(dst)==item['source']['sha256'],str(dst)+' copy mismatch'
 applied.append(item)
 JOURNAL.write_text(json.dumps({'applied':applied},ensure_ascii=False,indent=2),encoding='utf8')
print('Replaced and checked',len(applied),'images.',flush=True)

def verify(item):
 dst=ROOT/item['destination']['path'];src=SOURCE/item['source']['path']
 assert digest(dst)==digest(src)==item['source']['sha256'],str(dst)+' final mismatch'
 assert digest(BACKUP/item['destination']['path'])==item['destination']['sha256']
 with Image.open(dst) as im:im.load()
 return True

with ThreadPoolExecutor(max_workers=4) as pool:assert all(pool.map(verify,items))
destinations={i['destination']['path']:i for i in items};unchanged=0
for rel,original in plan['baseline'].items():
 expected=destinations[rel]['source']['sha256'] if rel in destinations else original
 assert digest(ROOT/rel)==expected,rel+' unexpected file change'
 if rel not in destinations:unchanged+=1

result={'date':'2026-11-19','replaced':len(items),'affectedPages':len(plan['affectedPages']),'unchangedProductionFiles':unchanged,'sourceAndDestinationHashesMatch':True,'allImagesDecode':True,'backupsVerified':True,'htmlCssJsUnchanged':True,'sourceModified':False,'issues':[]}
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
