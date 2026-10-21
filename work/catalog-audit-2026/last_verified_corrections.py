from pathlib import Path
D=Path('work/catalog-audit-2026');source=(D/'apply_corrections.py').read_text(encoding='utf-8-sig');exec(source.split('NEW_CODES=')[0])
for code in ['W6011','W6036']:
 for lang in LANGS:
  f=pp(code,lang);write(f,update_metrics(read(f),code,lang))
f=ROOT/'TEDESCO/index.html';t=read(f);old='Produktion italiana con controllo diretto, strutture specializzate e attenzione costante alla qualità finale.';assert old in t
write(f,t.replace(old,'Italienische Produktion mit direkter Kontrolle, spezialisierten Fertigungsstätten und kontinuierlichem Augenmerk auf die Qualität des Endprodukts.'))
print('Aligned all technical scales to five segments and corrected the mixed-language sentence in the German home.')
