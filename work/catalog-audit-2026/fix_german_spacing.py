from pathlib import Path
changes=[]
for p in Path('TEDESCO').rglob('*.html'):
 s=p.read_text(encoding='utf8')
 old='Bestellungen ab<strong>10 Stück</strong>—'
 if old in s:
  p.write_text(s.replace(old,'Bestellungen ab <strong>10 Stück</strong> —'),encoding='utf8');changes.append(str(p))
print('German announcement spacing corrected:',len(changes))
