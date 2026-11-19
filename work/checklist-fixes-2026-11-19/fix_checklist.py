from pathlib import Path
from collections import Counter
from html import escape, unescape
import re, json, hashlib, zipfile, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd(); OUT=ROOT/'work/checklist-fixes-2026-11-19'
OUT.mkdir(parents=True,exist_ok=True)
KIDS={'W2200','W2201','W2202','W2204','W2210','W2212','W2216','W2217','W2218','W2219','W6303'}
OPTIONS={'it':'OPZIONI','en':'OPTIONS','fr':'OPTIONS','de':'OPTIONEN','es':'OPCIONES'}
FEATURES={'it':'CARATTERISTICHE PRINCIPALI','en':'MAIN FEATURES','fr':'CARACTÉRISTIQUES PRINCIPALES','de':'HAUPTEIGENSCHAFTEN','es':'CARACTERÍSTICAS PRINCIPALES'}

def language(rel):return {'INGLESE':'en','FRANCESE':'fr','TEDESCO':'de','SPAGNOLO':'es'}.get(rel.parts[0],'it')
def plain(s):return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',s))).strip()
def divs(text,cls):
    pat=re.compile(r'<div\b[^>]*\bclass=["\'][^"\']*\b'+re.escape(cls)+r'\b[^"\']*["\'][^>]*>',re.I)
    for m in pat.finditer(text):
        depth=1
        for end in re.finditer(r'</?div\b[^>]*>',text[m.end():],re.I):
            depth+=-1 if end[0].lower().startswith('</') else 1
            if depth==0:
                yield (m.start(),m.end()+end.end(),m.end(),m.end()+end.start())
                break
        else:raise AssertionError('Unclosed '+cls)

def heading(block):
    a,b,c,d=next(divs(block,'acc-title'));return plain(block[c:d]).upper()

def update_description(text,new):
    a,b,c,d=next(divs(text,'description'))
    return text[:c]+'\n              '+escape(new,quote=False)+'\n            '+text[d:]

AERO={
 'it':{
  'description':'Calzino a gambale alto sviluppato grazie all’esperienza con i team professionisti. La costruzione combina il tessuto aerodinamico Aero Channelled Speed sul gambale con il tessuto Qskin nella parte del piede. La punta rinforzata, l’imbottitura in spugna su punta e pianta e la costruzione a rete traspirante offrono comfort durante la pedalata. Il grip mantiene stabile l’altezza del calzino.',
  'features':['Gambale alto 18 cm','Tessuto Qskin nella parte del piede','Punta e pianta imbottite in spugna','Punta rinforzata','Costruzione a rete traspirante','Gambale in tessuto Aero Channelled Speed','Grip per mantenere stabile l’altezza del calzino','Cuciture piatte per aumentare il comfort']},
 'en':{
  'description':'Long-cuff sock developed through experience with professional teams. The construction combines aerodynamic Aero Channelled Speed fabric on the cuff with Qskin fabric in the foot section. The reinforced toe, terry padding on the toe and sole, and breathable mesh construction provide comfort while riding. A bonded gripper keeps the cuff securely in place.',
  'features':['18 cm cuff','Qskin fabric in the foot section','Terry-padded toe and sole','Reinforced toe box','Breathable mesh construction','Aero Channelled Speed fabric on the cuff','Bonded gripper for secure sock height','Flatlock stitching for increased comfort']},
 'fr':{
  'description':'Chaussette haute développée grâce à l’expérience acquise avec les équipes professionnelles. Sa construction associe le tissu aérodynamique Aero Channelled Speed sur la tige et le tissu Qskin au niveau du pied. La pointe renforcée, le rembourrage en éponge à la pointe et sous le pied et la construction en maille respirante offrent du confort pendant le pédalage. La bande de maintien stabilise la hauteur de la chaussette.',
  'features':['Tige de 18 cm','Tissu Qskin au niveau du pied','Pointe et semelle rembourrées en éponge','Pointe renforcée','Construction en maille respirante','Tige en tissu Aero Channelled Speed','Bande de maintien pour stabiliser la hauteur de la chaussette','Coutures plates pour davantage de confort']},
 'de':{
  'description':'Socke mit hohem Schaft, entwickelt aus der Erfahrung mit Profiteams. Die Konstruktion kombiniert aerodynamisches Aero Channelled Speed-Gewebe am Schaft mit Qskin-Gewebe im Fußbereich. Die verstärkte Zehenpartie, die Frotteepolsterung an Zehen und Sohle sowie die atmungsaktive Netzstruktur bieten Komfort beim Radfahren. Der Haftabschluss hält den Schaft sicher in Position.',
  'features':['18 cm hoher Schaft','Qskin-Gewebe im Fußbereich','Frotteepolsterung an Zehen und Sohle','Verstärkte Zehenpartie','Atmungsaktive Netzstruktur','Schaft aus Aero Channelled Speed-Gewebe','Haftabschluss für eine sichere Schafthöhe','Flache Nähte für mehr Komfort']},
 'es':{
  'description':'Calcetín de caña alta desarrollado gracias a la experiencia con equipos profesionales. Su construcción combina el tejido aerodinámico Aero Channelled Speed en la caña con el tejido Qskin en la zona del pie. La puntera reforzada, el acolchado de felpa en la puntera y la planta y la construcción de malla transpirable ofrecen comodidad durante el pedaleo. El agarre mantiene estable la altura del calcetín.',
  'features':['Caña de 18 cm','Tejido Qskin en la zona del pie','Puntera y planta acolchadas en felpa','Puntera reforzada','Construcción de malla transpirable','Caña de tejido Aero Channelled Speed','Agarre para mantener estable la altura del calcetín','Costuras planas para mayor comodidad']},
}

TIGHTS={
 'it':[
  ('La costruzione a taglio vivo offre un eccellente comfort strutturale.','Le cuciture ridotte al minimo migliorano il comfort durante la pedalata.'),
  ('Taglio ergonomico valorizzato dalla costruzione a taglio vivo','Taglio ergonomico')],
 'en':[
  ('The raw-cut seam construction offers excellent structural comfort.','Minimal seams improve comfort while riding.'),
  ('Ergonomic cut enhanced by raw-cut construction','Ergonomic cut')],
 'fr':[
  ('La construction des coutures à coupe franche offre un excellent confort structurel.','Les coutures réduites au minimum améliorent le confort pendant le pédalage.'),
  ('Coupe ergonomique améliorée par une construction à coupe franche','Coupe ergonomique')],
 'de':[
  ('Die roh geschnittene Nahtkonstruktion bietet ausgezeichneten strukturellen Komfort.','Auf ein Minimum reduzierte Nähte erhöhen den Komfort beim Radfahren.'),
  ('Ergonomischer Schnitt, optimiert durch roh geschnittene Konstruktion','Ergonomischer Schnitt')],
 'es':[
  ('La construcción de las costuras con corte vivo ofrece un excelente confort estructural.','Las costuras reducidas al mínimo mejoran la comodidad durante el pedaleo.'),
  ('Corte ergonómico optimizado por la construcción de corte vivo','Corte ergonómico')],
}

baseline={};originals={};changes={};events=[]
for f in sorted(ROOT.rglob('*')):
    rel=f.relative_to(ROOT)
    if any(p in {'.git','work','node_modules'} for p in rel.parts) or not f.is_file():continue
    raw=f.read_bytes();baseline[rel.as_posix()]=hashlib.sha256(raw).hexdigest()
    if f.suffix.lower()!='.html':continue
    originals[rel.as_posix()]=raw
    text=raw.decode('utf-8-sig');before=text;lang=language(rel);match=re.search(r'W\d{4}',f.name)
    if not match:continue
    code=match[0];is_men=any('UOMO' in p for p in rel.parts)
    is_accessory=code.startswith('W66') or code in {'W0274','W2632'}
    reasons=[]

    if code in KIDS:
        a,b,c,d=next(divs(text,'sizes'))
        assert plain(text[c:d])=='XS S M L XL',(rel,plain(text[c:d]))
        buttons='\n'+'\n'.join('          <button class="size">'+str(v)+'</button>' for v in [104,116,128,140,152,164])+'\n        '
        text=text[:c]+buttons+text[d:];reasons.append('Taglie KID 104-164')

    if code=='W6012' and is_men:
        targets=[(a,b) for a,b,c,d in divs(text,'acc-item') if heading(text[a:b])==OPTIONS[lang]]
        assert len(targets)==1,(rel,targets)
        a,b=targets[0];text=text[:a]+text[b:];reasons.append('Rimosse opzioni non pertinenti W6012')

    if code=='W6701' and is_men:
        text,n=re.subn(r'Cam(?:\s*&(?:amp;)?\s*|-\s*&(?:amp;)?\s*-)Lock','Camlock',text)
        assert n==1,(rel,n);reasons.append('Nome cursore Camlock')

    if code=='W6009' and is_men:
        for old,new in TIGHTS[lang]:
            assert text.count(old)==1,(rel,old)
            text=text.replace(old,new)
        reasons.append('W6009: cuciture minime e taglio ergonomico')

    if is_accessory:
        if lang in {'en','fr','es'}:
            label={'en':'Temperature','fr':'Température','es':'Temperatura'}[lang]
            temp=list(divs(text,'temp-title'))
            assert len(temp)==1,rel
            a,b,c,d=temp[0];old=plain(text[c:d])
            if old in {'Temperatur','Temperaturea'}:
                text=text[:c]+label+text[d:];reasons.append('Etichetta temperatura tradotta')
        if lang=='es':
            replacements={
              'Maßgefertigte Produkte ab <strong>10 Stück</strong> – 100 % italienische Produktion':'Pedidos personalizados desde <strong>10 piezas</strong> — Producción 100 % italiana',
              'Angebot anfordern':'Solicitar presupuesto',
              'Weitere Produkte entdecken':'Descubre otros productos',
              'Ich möchte weitere Informationen':'Quiero más información',
            }
            for old,new in replacements.items():
                if old in text:
                    assert text.count(old)==1,(rel,old)
                    text=text.replace(old,new);reasons.append('Interfaccia spagnola: '+plain(new))
        if lang!='de':
            wrong='href="https://www.bicycle-line.com/de/"'
            if wrong in text:
                text=text.replace(wrong,'href="https://www.bicycle-line.com/'+lang+'/"')
                reasons.append('Logo collegato alla lingua corrente')

    if code in {'W6600','W6601'}:
        text=update_description(text,AERO[lang]['description'])
        targets=[(a,b) for a,b,c,d in divs(text,'acc-item') if heading(text[a:b])==FEATURES[lang]]
        assert len(targets)==1,(rel,targets)
        a,b=targets[0];block=text[a:b]
        ul=re.search(r'(<ul\b[^>]*>)([\s\S]*?)(</ul>)',block)
        assert ul,rel
        li='\n'+'\n'.join('                <li style="margin-bottom: 8px;">• '+escape(v,quote=False)+'</li>' for v in AERO[lang]['features'])+'\n              '
        block=block[:ul.start(2)]+li+block[ul.end(2):]
        text=text[:a]+block+text[b:];reasons.append('Calzini Aero: Qskin piede e Aero Channelled Speed gambale')

    if text!=before:
        changes[rel.as_posix()]=text;events.append({'file':rel.as_posix(),'code':code,'lang':lang,'reasons':reasons})

assert len([e for e in events if e['code'] in KIDS])==55
assert len([e for e in events if e['code']=='W6012'])==5
assert len([e for e in events if e['code']=='W6701'])==5
assert len([e for e in events if e['code']=='W6009'])==5
assert len([e for e in events if e['code'] in {'W6600','W6601'}])==12

# Preserve the pre-change state before touching any production file.
backup=OUT/'before-html.zip'
assert not backup.exists(),'Existing backup: do not rerun this mutation script.'
with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(changes):z.writestr(rel,originals[rel])
(OUT/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
for rel,text in changes.items():
    file=ROOT/rel
    assert hashlib.sha256(file.read_bytes()).hexdigest()==baseline[rel],rel+' changed during preparation'
    # Retain each file's existing newline convention.
    if b'\r\n' in originals[rel]:text=text.replace('\r\n','\n').replace('\n','\r\n')
    file.write_bytes(text.encode('utf-8'))
(OUT/'changes.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated HTML:',len(changes));print('Per language:',dict(Counter(e['lang'] for e in events)))
print('Reason counts:',dict(Counter(reason for e in events for reason in e['reasons'])))
print('Images unchanged by this script. Backup:',backup)
