from pathlib import Path
from collections import Counter
import json,re

ROOT=Path.cwd();OUT=ROOT/'work/checklist-fixes-2026-11-19'
static=json.loads((OUT/'static-verification.json').read_text(encoding='utf-8'))
browser=json.loads((OUT/'browser-verification.json').read_text(encoding='utf-8'))
changes=json.loads((OUT/'changes.json').read_text(encoding='utf-8'))
assert static['changedHtml']==114 and static['imagesVerifiedUnchanged']==441 and not static['localLinkIssues']
assert browser['completed']==browser['pages']==114 and browser['checks']==456 and not browser['issues']

report='''# Correzioni della checklist - 19 novembre 2026

Correzioni applicate alla copia locale del sito. Le immagini sono rimaste tutte invariate, come richiesto dall'utente durante l'intervento.

## Correzioni completate

- Taglie Bambino aggiornate a 104, 116, 128, 140, 152 e 164 per tutti gli 11 prodotti, nelle cinque lingue: 55 schede.
- W6012 Uomo: rimosso il blocco OPZIONI con personalizzazione del logo e tessuto interno blu navy/nero. Conservate le opzioni del fondello, nelle cinque lingue.
- W6701 Uomo: uniformato il nome del cursore a Camlock nelle cinque lingue.
- W6009 Uomo: sostituita la frase sulle cuciture/costruzione a taglio vivo con il riferimento alle cuciture ridotte al minimo, gia presente nelle caratteristiche del catalogo. Mantenuto il taglio ergonomico, nelle cinque lingue.
- W6600 e W6601: descrizioni e caratteristiche allineate al catalogo: Qskin nella parte del piede e Aero Channelled Speed sul gambale, con otto caratteristiche in ciascuna scheda. Aggiornate anche le copie inglesi esistenti nella cartella Ragazzi.
- Corrette 26 etichette temperatura residue nelle schede accessori francesi, spagnole e inglesi, comprese le copie inglesi.
- Corretti la barra superiore tedesca in sette schede accessori spagnole e i pulsanti inferiori tedeschi in sei schede.
- Corretti 28 collegamenti del logo che nelle pagine tradotte degli accessori aprivano la home tedesca invece della lingua corrente.

## Verifiche

- 114 HTML modificati, con backup in before-html.zip.
- Tutte le 424 pagine HTML controllate per file locali e ancore: nessun collegamento non valido.
- Tutte le 441 immagini verificate tramite SHA-256 e rimaste identiche alla situazione precedente a questo intervento.
- Script, fogli di stile incorporati e attributi delle immagini delle gallerie rimasti invariati.
- Altri file di produzione invariati rispetto al controllo iniziale.
- 114 pagine provate in Edge a 1440, 1280, 390 e 320 px: 456 controlli, nessuno sforamento orizzontale, nessuna immagine mancante, nessun errore JavaScript. Menu lingua, menu mobile e pannelli espandibili funzionanti; verificate anche le nuove sei taglie.
- Controllo visivo di cinque schermate: taglie KID a 320 px, intestazione e pulsanti spagnoli, testi Aero e opzioni W6012 su mobile.

Le verifiche del browser sono locali; non sono stati inviati moduli. Nessuna modifica al sito sul server.

## Lavoro fotografico lasciato all'utente

Il dettaglio dei punti fotografici e nel documento FOTO-DA-RIVEDERE.md. In questo intervento non sono state generate, ritoccate o sostituite immagini.

## Elenco delle pagine aggiornate

| Pagina | Correzioni |
|---|---|
'''
for item in changes:
 report+='| `'+item['file']+'` | '+'; '.join(item['reasons'])+' |\n'
(OUT/'CORREZIONI.md').write_text(report,encoding='utf-8')

photos='''# Foto da rivedere - elenco per il lavoro grafico

Le immagini del sito sono state lasciate invariate per esplicita richiesta dell'utente. Questo elenco distingue un difetto visibile confermato dalle segnalazioni di modellistica che richiedono un riferimento approvato.

## Problema visibile confermato: scarpe nelle calzamaglie KID

- W2212: images/RAGAZZI/W2212/1.png
- W2218: images/RAGAZZI/W2218/1.png

Le due immagini sono identiche e mostrano il modello con scarpe grigie tipo sneaker. Il punto segnalato sulle scarpe e ancora presente. Per ricrearle, utilizzare scarpe da ciclismo coerenti con il servizio fotografico approvato, mantenendo il prodotto corrispondente: W2212 con bretelle, W2218 senza bretelle.

Le foto 2 e 3 dei due articoli e di W2210 mostrano gia il bordo nero ai polsi: quel punto risulta corretto.

## Body: verifica e ricreazione della modellistica

La segnalazione originale riguarda tutte le foto dei seguenti quattro prodotti. Senza un campione o una scheda modellistica approvata non e possibile indicare con certezza quale singola cucitura o pannello sia sbagliato. I punti sotto sono le specifiche del prodotto da rispettare, non ulteriori difetti presunti.

| Codice | Riferimento da rispettare | Foto attuali |
|---|---|---|
| W6012 ECHELON | Body crono a manica lunga completamente stampabile, compreso il pantaloncino | images/UOMO/W6012/1.png - 6.png |
| W6015 ECHELON | Body crono a manica lunga; parte superiore personalizzabile e pantaloncino in microfibra tinta unita, personalizzabile con loghi in silicone | images/UOMO/W6015/1.png - 6.png |
| W6024 ECHELON | Body crono a manica corta, pantaloncino tinta unita con loghi in silicone | images/UOMO/W6024/1.png - 6.png |
| W6011 APEX | Body strada a manica corta, due tasche posteriori; personalizzazione sui pannelli laterali e posteriori della parte inferiore | images/UOMO/W6011/1.png - 6.png |

Per W6012 e W6015 le foto 1-4 provengono dai set NUOVE caricati nel precedente intervento. Questo aggiornamento non costituisce un'approvazione della modellistica. Per W6024 e W6011 il set e sostanzialmente quello della segnalazione precedente.

La numerazione attuale usa le viste fotografiche 1-4 e le viste del capo isolato 5-6. Mantenere questa corrispondenza, o segnalare un diverso ordine; i percorsi sono condivisi dalle cinque lingue.

## Attenzione al retro W2212 sul server

Nel confronto precedente, il file server images/RAGAZZI/W2212/6.png duplicava la vista frontale di 5.png. Nel sito locale e stata conservata la foto posteriore corretta. Nel nuovo export verificare che 5.png sia il fronte e 6.png il retro.

## Punti fotografici gia corretti nella copia attuale

- W6516 Donna: zip frontale visibile e polsi magenta.
- W6517 Donna: foto 4 con retro aggiornato, coerente con l'impostazione della foto 6.
- W2201 Bambino: foto 1 a manica lunga.
- W2210/W2212/W2218: bordi neri ai polsi nelle foto 2-3.
- W6600/W6601: immagini complete; visualizzazione del sito senza ritaglio.

## Cartelle locali da usare

'''
for code,family,names in [('W2212','RAGAZZI',['1.png']),('W2218','RAGAZZI',['1.png']),('W6012','UOMO',[f'{i}.png' for i in range(1,7)]),('W6015','UOMO',[f'{i}.png' for i in range(1,7)]),('W6024','UOMO',[f'{i}.png' for i in range(1,7)]),('W6011','UOMO',[f'{i}.png' for i in range(1,7)])]:
 photos+=f'\n**{code}**\n\n'
 for name in names:
  file=ROOT/'images'/family/code/name
  photos+=f'- [{name}](<{file.as_posix()}>)\n'
(OUT/'FOTO-DA-RIVEDERE.md').write_text(photos,encoding='utf-8')
print('Saved correction report and image handoff list.')
