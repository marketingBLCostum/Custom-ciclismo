# Ricontrollo completo — 26 ottobre 2026

Il nuovo controllo ha verificato i file locali del sito e riletto il catalogo PDF 2026 sul server.

## Risultati

- 77 prodotti in cinque lingue: 385 schede principali, più 13 copie inglesi esistenti, per 398 schede prodotto e 424 HTML complessivi.
- Tutti i prodotti presenti nelle 20 sezioni di categoria: 39 Uomo, 14 Donna, 11 Bambino e 13 Accessori per ciascuna lingua. Nessuna omissione o duplicazione nelle categorie.
- Temperature e tre valutazioni tecniche confrontate nuovamente con le tabelle del PDF per tutti i 77 codici: nessuna difformità residua.
- Ricontrollati collegamenti locali, ancore, corrispondenza dei prodotti nel cambio lingua, nomi dei fondelli tra le lingue, contenuti mancanti e refusi già segnalati. Nessuna anomalia residua nei controlli effettuati.
- Verificata anche la corrispondenza maiuscole/minuscole dei percorsi, utile quando il sito viene trasferito su server Linux.
- Tutte le 424 pagine provate nel browser Edge a 320, 390, 768, 1024, 1280 e 1440 px: 2.544 controlli finali, nessun errore JavaScript o di sintassi, nessuna immagine locale mancante, nessuno sforamento orizzontale rilevato. Menu lingua e mobile, pannelli espandibili e FAQ funzionanti.
- Ulteriori 30 controlli su cinque pagine rappresentative a 769, 1100, 1200, 1201, 1366 e 1439 px: nessuna anomalia. Ispezionate visivamente una scheda tedesca a 1280 px e la home a 1024 px.

Ulteriori 20 verifiche delle intestazioni nelle cinque lingue a 769, 1024, 1200 e 1280 px dopo l'ultima correzione: nessuna sovrapposizione tra messaggio e azione.

## Ulteriori correzioni applicate

Il controllo alle larghezze intermedie ha individuato due problemi non emersi nelle dimensioni precedenti: larghezza minima di 1440 px nelle schede e menu desktop troppo largo a 1024 px. Le colonne sono ora fluide tra 1201 e 1439 px; sui tablet viene mostrato il menu compatto. Adeguata la priorità delle regole condivise agli stili già presenti nelle schede.

Risolta anche la sovrapposizione del messaggio della barra superiore con il collegamento al preventivo tra 769 e 1200 px. A queste larghezze la barra mostra il messaggio; il contatto resta disponibile dal menu.

Corretti inoltre due spazi mancanti nell'intestazione di 16 schede tedesche: “ab 10 Stück —”.

Le correzioni del layout sono in catalog-fixes.css, già collegato da tutte le pagine. Il foglio va mantenuto insieme al sito.

## Ambito della verifica

Verifiche eseguite sulla copia locale con Edge. Le risorse esterne sono state escluse dai test automatici. I moduli contatto non sono stati inviati e la consegna delle email non è stata verificata. Il PDF è rimasto invariato; restano valide le osservazioni sui refusi del catalogo già riportate in CORREZIONI.md.

I risultati dettagliati sono nei file safety-static-2026-10-26.json, safety-coverage-2026-10-26.json, safety-browser-2026-10-26.json safety-breakpoints-2026-10-26.json e safety-topbar-2026-10-26.json.
