from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone
import json, re, sys

sys.stdout.reconfigure(encoding='utf8')
ROOT=Path.cwd();OUT=ROOT/'work/image-sync-2026-11-19'
plan=json.loads((OUT/'plan.json').read_text(encoding='utf8'))
verification=json.loads((OUT/'verification.json').read_text(encoding='utf8'))
browser=json.loads((OUT/'browser-verification.json').read_text(encoding='utf8'))
captures=json.loads((OUT/'visual-captures.json').read_text(encoding='utf8'))
assert verification['replaced']==227 and not verification['issues']
assert browser['completed']==browser['pages']==282 and browser['checks']==564 and not browser['issues']
assert len(captures)==8
items=plan['replacements'];groups=defaultdict(list)
for i in items:
 rel=i['destination']['path'];category=rel.split('/')[1];code=re.search(r'W\d{4}',rel,re.I)[0].upper();groups[(category,code)].append(i)

text='''# Aggiornamento immagini dal sito sul server

Verifica e sostituzioni completate il 19 novembre 2026.

Sorgente letta: \\\\Serverbl\\dati\\Documenti Comuni\\___LORENZO\\SITI CUSTOM\\CICLISMO

Copia aggiornata: C:\\LORENZO\\5 SPORT PER SITO CUSTOM\\CICLISMO - Copia

## Risultato

- Confrontate 441 immagini locali e 700 immagini sul server, incluse le copie di lavorazione; 413 percorsi immagine erano comuni.
- Trovati 245 file differenti allo stesso percorso, tutti con data server successiva a quella locale. Il confronto ha incluso SHA-256, decodifica, dimensioni e revisione visiva affiancata.
- Conservati 24 file gia identici a livello di pixel e una vista posteriore per la quale il server conteneva un duplicato errato del fronte.
- Sostituiti 227 file immagine relativi a 52 prodotti, comprese le versioni NUOVE di W6012/W6015 confermate dall'utente e il file aggiornato W6301/4_.png associato alla corrispondente vista locale 4.png.
- Le differenze comprendono ritocchi visibili, nuove pose/inquadrature e originali PNG dello stesso scatto precedentemente disponibile in WebP.
- Tutti i 227 file copiati coincidono esattamente con le sorgenti selezionate. Ogni originale locale sostituito e conservato nella sottocartella before, con hash verificato.
- I 646 altri file di produzione sono rimasti identici al controllo iniziale; HTML, CSS, JavaScript e video inclusi. I percorsi immagine locali sono stati mantenuti.
- Il sito sul server e rimasto invariato. Gli aggiornamenti sono nella copia locale.

## Verifiche dopo le sostituzioni

- Verifica dei file sorgente, dei file preparati e degli originali locali prima di intervenire.
- Backup verificato prima della prima sostituzione; sostituzione atomica e confronto hash dopo ogni copia.
- Secondo confronto diretto con il server e controllo dei backup dopo tutte le sostituzioni; decodifica riuscita per tutte le immagini.
- 282 pagine interessate verificate in Edge nelle cinque lingue, a 1440 e 390 px: 564 verifiche, nessuna immagine mancante, dimensioni naturali coerenti con la sorgente, nessun errore JavaScript o sforamento orizzontale.
- Controllo visivo delle 24 tavole di confronto, approfondimento delle immagini dubbie, otto acquisizioni dal sito aggiornato e ulteriore ricontrollo del rendering W6015.

## Modifiche visive piu evidenti

- W6012 e W6015: nuovi set fotografici NUOVE, con il modello giovane. Per W6015 la prima foto e la versione del 16 settembre, piu recente delle alternative numerate; aggiornate anche le due viste del capo isolato.
- W6516 Donna: nuove foto e nuova immagine della maglia isolata, inclusa l'anteprima di categoria.
- W6517 Donna: immagini posteriori e viste della maglia/gilet aggiornate.
- W7205 Donna: nuova immagine frontale del capo isolato; vista verificata a ingrandimento.
- W2201 Bambino: foto principale con il capo a manica lunga, coerente con il prodotto.
- W2212/W2218 Bambino: foto principali aggiornate; W2218 e W2219 hanno anche nuove immagini per la categoria.
- W6303 Bambino: nuova vista posteriore della maglia isolata.
- W6006, W6100 e W6519 Uomo: immagini posteriori del capo isolato aggiornate.
- W6521 Uomo: aggiornate le immagini e l'ordine delle prime due viste rispetto alla versione locale.
- W6301 Uomo: usata la foto posteriore aggiornata denominata 4_.png nel server, mantenendo il percorso locale 4.png.

## Eccezione W2212

Il file server images/RAGAZZI/W2212/6.png ripete la vista frontale della salopette invece di mostrare il retro. La foto posteriore locale 6.png e stata conservata per mantenere entrambe le viste corrette. Le altre cinque immagini aggiornate di W2212 sono state copiate.

## Formato e peso dei file

Le sostituzioni sono copie esatte dei file del grafico, prevalentemente PNG. I 227 file sostituiti passano complessivamente da circa 28,27 MB a 241,99 MB; molte copie locali precedenti erano compresse in WebP pur avendo estensione .png. Questo aumento del peso puo incidere sul tempo di caricamento online. I test sono stati eseguiti sulla copia locale.

## Elenco completo dei prodotti e dei file sostituiti

| Sezione | Prodotto | File aggiornati | Quantita |
|---|---|---|---:|
'''
names={'UOMO':'Uomo','DONNA':'Donna','RAGAZZI':'Bambino','ACCESSORI':'Accessori'}
for (category,code),values in sorted(groups.items()):
 files=', '.join('`'+Path(v['destination']['path']).name+'`' for v in values)
 text+=f'| {names[category]} | {code} | {files} | {len(values)} |\n'

text+='''
## Corrispondenze con nomi o cartelle diversi

I seguenti file sono stati assegnati alla vista dello stesso prodotto, verificando il capo e l'inquadratura:

| File sul server | File nella copia locale |
|---|---|
'''
for i in items:
 if i['source']['path'].casefold()!=i['destination']['path'].casefold():
  text+=f"| `{i['source']['path']}` | `{i['destination']['path']}` |\n"

text+='''
## Materiale per il ricontrollo

- plan.json: corrispondenze complete, date, hash, pagine interessate e hash iniziali di tutti i file di produzione.
- applied.json: registro delle sostituzioni eseguite.
- verification.json: esito dei controlli sui file e sui backup.
- browser-verification.json: esito delle 564 verifiche delle pagine.
- before/: copia degli originali locali sostituiti, con gli stessi percorsi relativi del sito.
- comparison-01.jpg ... comparison-24.jpg: confronti tra le immagini precedenti e quelle del server, incluse le varianti esaminate.

Immagini del sito dopo l'aggiornamento:

'''
for capture in captures:
 p=(OUT/capture['name']).as_posix();text+=f"- [{capture['name']}](<{p}>)\n"

(OUT/'RAPPORTO-IMMAGINI.md').write_text(text,encoding='utf8')
print('Report saved:',OUT/'RAPPORTO-IMMAGINI.md')
print('Verified:',len(items),'images;',len(groups),'products;',browser['checks'],'browser checks.')
