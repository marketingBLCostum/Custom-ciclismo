from pathlib import Path
import json,re
from collections import Counter
root=Path.cwd();D=root/'work/catalog-audit-2026'
pages=json.loads((D/'pages.json').read_text(encoding='utf8'));browser=json.loads((D/'browser-issues.json').read_text(encoding='utf8'));links=json.loads((D/'link-issues.json').read_text(encoding='utf8'));refs=json.loads((D/'references.json').read_text(encoding='utf8'))
primary={p['file'] for p in pages if not ('RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']))}
def link(rel,line=None,label=None):
 return '['+(label or rel)+'](<'+(root/rel).as_posix()+(':'+str(line) if line else '')+'>)'
def prod(code,line=None):
 p=next(p for p in pages if p['lang']=='it' and p['code']==code)
 return link(p['file'],line,p['title'])
r=['# Verifica catalogo Custom Team 2026 — 21 ottobre 2026','',
'Controllo di 77 articoli nelle cinque lingue: 385 schede principali. Verificate anche le categorie, le home e le pagine duplicate: 424 file HTML in totale. Il sito non è stato modificato durante questa verifica.','',
'Fonte: BL-CC_Custom Team 2026_EN_H-Res.pdf, file indicato dall’utente. Le pagine PDF citate sotto sono le posizioni fisiche del file, non i numeri stampati.','',
'## Temperature da aggiornare','',
'Le seguenti differenze sono presenti in tutte e cinque le lingue.','',
'| Articolo | Sito attuale | Nuovo catalogo | Pagina PDF |','|---|---|---|---|']
for code,old,new,page in [('W6515','+18 / +35 °C','+15 / +30 °C',36),('W6047','+15 / +30 °C','+18 / +35 °C',36),('W7200','+18 / +35 °C','+15 / +30 °C',41),('W7201','+18 / +35 °C','+15 / +30 °C',40),('W7202','+18 / +30 °C','+15 / +30 °C',42),('W7203','+18 / +35 °C','+15 / +30 °C',42),('W7204','+18 / +35 °C','+15 / +30 °C',41),('W7205','+18 / +35 °C','+15 / +30 °C',43)]:
 r.append(f'| {prod(code)} | {old} | {new} | {page} |')
r+=['','W6047 è una scheda aggiunta nel passaggio precedente: in quell’inserimento è stata associata la tabella dell’articolo accanto. Il dato resta da correggere nelle cinque versioni.','',
'## Testi e specifiche da aggiornare','',
'- '+prod('W6005',637)+': la personalizzazione è ancora descritta come silicone bianco. Nel nuovo PDF (p. 15) è DTF bianco o materiale riflettente scuro. Il testo inglese contiene inoltre la formulazione obsoleta “Prize material”.',
'- '+prod('W6028',575)+': testo della versione precedente, con dettagli costruttivi non più presenti nella nuova descrizione. Mancano il tessuto da circa 190 g/m² e la costruzione alleggerita aggiornata. Le opzioni indicano ancora silicone bianco e solo navy/nero; il PDF (p. 15) prevede DTF e sei colori 2026/2027: Asphalt Grey, Plum, Burgundy, North Blue, Rider Green, Black.',
'- '+prod('W6036',636)+': nelle opzioni compaiono solo navy e nero, mentre il PDF (p. 31) prevede gli stessi sei colori 2026/2027. Descrizione da riallineare alla formulazione aggiornata del CYCLE-01.',
'- '+prod('W6514',570)+': descrizione ancora simile alla APEX uomo W6511. Il nuovo catalogo (p. 33) descrive una costruzione specifica femminile, tessuto a struttura aperta e pannello posteriore più fitto. Mancano le opzioni della tasca posteriore destra con zip verticale e del dettaglio riflettente.',
'- '+prod('W6515',571)+': oltre alla temperatura, la descrizione e le opzioni non precisano la nuova formulazione sulla vestibilità anatomica e sui fondelli nella configurazione femminile (PDF p. 36).',
'- '+prod('W6012')+': presenti le opzioni fondello, ma non le altre opzioni del PDF (p. 29): personalizzazione del logo bianca/riflettente scura e tessuto pantaloncino navy/nero.',
'- '+prod('W6518')+': manca tra le opzioni la personalizzazione bianca o in materiale riflettente scuro, indicata nel PDF (p. 27).',
'- '+prod('W6301',588)+': vestibilità visualizzata 5/5; nel PDF (p. 13) è 3/5. Le cinque lingue riportano lo stesso valore errato.',
'- '+prod('W6512',588)+': vestibilità ed elasticità visualizzate 4/5; nel PDF (p. 21) sono entrambe 5/5. Le cinque lingue riportano gli stessi valori errati.',
'- Le dodici schede aggiunte nel passaggio precedente hanno la temperatura e le caratteristiche descrittive, ma non mostrano le tre barre di vestibilità, traspirabilità ed elasticità presenti nel PDF. È una differenza di completezza rispetto alle schede precedenti.','',
'## Traduzioni','',
'In sei schede Accessori spagnole resta la dicitura tedesca “Größe:” al posto di “Talla:”. Nella W2632 resta anche “EINHEITSGRÖSSE” al posto di “TALLA ÚNICA”.','']
for code in ['W0274','W2632','W6600','W6601','W6602','W6603']:
 p=next(p for p in pages if p['code']==code and p['lang']=='es');r.append('- '+link(p['file'],541,p['title']))
r+=['','## Collegamenti e cambio lingua','',
'- Nelle 385 schede principali, i cinque collegamenti delle lingue esistono e puntano allo stesso codice articolo. Anche la lingua dichiarata nell’HTML corrisponde alla cartella.',
'- Il pulsante superiore per richiedere un preventivo punta a #contatti o #kontakt nella stessa pagina, dove la sezione non esiste. Il difetto coinvolge tutte le schede principali e le categorie. Va indirizzato alla sezione contatti della home della lingua corrente. Esempio: '+link('UOMO SCHEDE PRODOTTO/W6005-ECHELON.html',456)+'.',
'- Altri 30 collegamenti “Maggiori informazioni” negli Accessori tradotti puntano al catalogo Uomo con #kontakt, anch’esso inesistente. Esempio: '+link('INGLESE/ACCESSORI EN/W0274-CALZINI-ESTIVI-13CM-EN.html',620)+'.',
'- Esistono 13 copie di accessori dentro INGLESE/RAGAZZI EN: quattro cambi lingua per copia portano al catalogo Bambino anziché alla scheda dell’articolo. Non sono collegate dalle normali pagine del sito, quindi il problema non coinvolge la navigazione principale.',
'- Una di queste copie, INGLESE/RAGAZZI EN/W6608-GAMBALI-INVERNALI-STAMPABILI-EN.html, contiene anche un errore di sintassi JavaScript che impedisce il funzionamento dei suoi menu.',
'- Nessun file HTML o immagine locale referenziato risulta mancante. Nessuna differenza fra maiuscole/minuscole nei percorsi dei file.','',
'## Interazioni e visualizzazione mobile','',
'- In 230 delle 385 schede principali, cliccare un’intestazione non espandibile, come Descrizione o Caratteristiche tecniche, genera l’errore JavaScript “Cannot set properties of null (setting textContent)”. Il gestore tenta di aggiornare un’icona che non esiste. I pannelli dotati di + si aprono; il problema riguarda il gestore condiviso e può anche nascondere impropriamente il contenuto cliccato. Esempio: '+link('ACCESSORI SCHEDA PRODOTTO/W0274-CALZINI-ESTIVI-13CM.html',721)+'.',
'- In 98 schede principali il layout supera uno schermo da 390 px: tutte le 8 schede Donna precedenti nelle 5 lingue (40), tutte le 11 schede Bambino nelle 5 lingue (55) e le tre schede Guanti tedesche W6604/W6605/W6606 (3). Le verifiche dirette mostrano galleria e testo larghi 520 px. Esempi: '+link('DONNA SCHEDE PRODOTTO/W6514-APEX.html')+' e '+link('RAGAZZI SCHEDE PRODOTTO/W2200-ECHELON.html')+'.',
'- Le home italiana, inglese, francese e tedesca mostrano inoltre piccoli sforamenti orizzontali nella sezione iniziale a 390 px.','',
'## Incongruenze già presenti nel PDF da chiarire','',
'- PDF p. 47: nella descrizione W2218 si parla di bretelle anche se titolo e immagini mostrano la calzamaglia senza bretelle. I paragrafi descrittivi di W2212 e W2218 appaiono scambiati. Le schede del sito distinguono già correttamente la presenza delle bretelle: non va copiata automaticamente l’incongruenza.',
'- PDF p. 27: W6009 è descritta in inglese come “Winter running tights”, pur essendo una calzamaglia da ciclismo con fondello. Il sito riprende il riferimento al running in EN/FR/DE/ES; l’italiano evita il termine. È opportuno correggere la formulazione anche alla fonte.',
'- PDF p. 30: la descrizione W6011 usa “X-Strap”, mentre le caratteristiche indicano X-Stra. Il sito usa già X-Stra.','',
'## Elenco completo delle schede con errore nelle intestazioni','']
for i in browser['issues']:
 if i['file'] in primary and i.get('errors'):r.append('- '+link(i['file']))
r+=['','## Elenco completo delle schede con sforamento mobile','']
for i in browser['issues']:
 if i['file'] in primary and i.get('mobile',{}).get('overflow'):r.append('- '+link(i['file']))
r+=['','## Altri collegamenti informazioni non validi','']
for i in links:
 if i['type']=='missing-anchor' and i.get('value') not in ['#contatti','#kontakt']:r.append('- '+link(i['file'],i['line'])+' → `'+i['value']+'`')
r+=['','## Limiti della verifica','',
'Test locali su file HTML con Microsoft Edge: menu lingua, menu mobile, caricamento immagini e apertura dei pannelli. I collegamenti locali sono stati verificati; la disponibilità dei siti esterni non è stata testata. Le traduzioni sono state confrontate per corrispondenza di articolo, dati numerici, fondelli, materiali e struttura dei contenuti; non costituiscono una revisione stilistica professionale madrelingua. Le discrepanze sulle temperature e le barre citate sono state confermate sulle pagine renderizzate del PDF.']
(D/'RISULTATI.md').write_text('\n'.join(r)+'\n',encoding='utf8')
print('Report saved:',D/'RISULTATI.md')
print('Source files of the website were not modified.')
