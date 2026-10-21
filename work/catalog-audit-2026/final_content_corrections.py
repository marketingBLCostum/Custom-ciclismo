from pathlib import Path
import re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('work/catalog-audit-2026')
# Load only the editing helpers; the full mutation script must not be run twice.
source=(D/'apply_corrections.py').read_text(encoding='utf-8-sig')
exec(source.split('NEW_CODES=')[0])
from correction_content import ECHELON_DETAILS,PAD_MESH
for lang in LANGS:
 f=pp('W7203',lang);write(f,update_metrics(read(f),'W7203',lang))
 f=pp('W6005',lang);t=read(f);items=getitems(t,'features',lang)
 for i,s in enumerate(items):
  if 'Ghost Air Gel' in s:items[i]=AIR_FEATURES[4][lang]
 items.extend([v[lang] for v in ECHELON_DETAILS]);items.append(PAD_MESH[lang]);write(f,body(t,'features',lang,list_html(items)))
 f=pp('W6028',lang);t=read(f);items=getitems(t,'features',lang);items.append(PAD_MESH[lang]);write(f,body(t,'features',lang,list_html(items)))
print('Corrected W7203 five-segment scale and completed Echelon technical details in five languages.')
