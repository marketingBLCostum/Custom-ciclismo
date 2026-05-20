# -*- coding: utf-8 -*-
import os

base_dir = r"c:\LORENZO\5 SPORT PER SITO CUSTOM\CICLISMO\TEDESCO\ACCESSORI SCHEDA PRODOTTO"

files = [
    "W0274-CALZINI-ESTIVI-13CM.html",
    "W2632-SCALDACOLLO.html",
    "W6600-CALZINI-ESTIVI-AERO-PIEDE-NERO.html",
    "W6601-CALZINI-ESTIVI-AERO-PIEDE-BIANCO.html",
    "W6602-MANICOTTI-INVERNALI.html",
    "W6603-GAMBALI-INVERNALI.html",
    "W6604-GUANTI-ESTIVI.html",
    "W6605-GUANTI-LUNGHI-ESTIVI.html",
    "W6606-GUANTI-INVERNALI.html",
    "W6607-MANICOTTI-INVERNALI-STAMPABILI.html",
    "W6608-GAMBALI-INVERNALI-STAMPABILI.html",
    "W6610-CALZINI-ESTIVI-18CM.html",
    "W6612-BERRETTINO-ESTIVO-AIR-CAP.html",
]

common = {
    '<html lang="it">': '<html lang="de">',

    # Topbar
    'Ordini personalizzati da <strong>10 pezzi</strong> — Produzione 100% Italiana': 'Maßgeschneiderte Bestellungen ab <strong>10 Stück</strong> — 100% Italienische Produktion',
    'Richiedi preventivo →': 'Angebot anfordern →',

    # Nav
    'Come Funziona': 'Wie funktioniert\'s',
    'Uomo': 'Herren',
    'Donna': 'Damen',
    'Accessori': 'Zubehör',
    'Ragazzi': 'Kinder',
    'Contatti': 'Kontakt',

    # Language selector button
    '<img src="../images/BANDIERE/italia.jpg" alt="IT">': '<img src="../images/BANDIERE/Deutsch.jpg" alt="DE">',
    '<span>IT</span>': '<span>DE</span>',

    # Breadcrumbs
    'HOME': 'STARTSEITE',
    'ACCESSORI': 'ZUBEHÖR',

    # Product meta
    'Disponibile per Unisex': 'Verfügbar für Unisex',
    'Taglia:': 'Größe:',
    'GUIDA ALLE TAGLIE': 'GRÖSSENFÜHRER',
    'TAGLIA UNICA': 'EINHEITSGRÖSSE',

    # Accordion titles
    'Descrizione': 'Beschreibung',
    'Caratteristiche tecniche': 'Technische Merkmale',
    'Vestibilità': 'Passform',
    'Traspirabilità': 'Atmungsaktivität',
    'Elasticità': 'Elastizität',
    'Temperatura': 'Temperatur',
    'CARATTERISTICHE PRINCIPALI': 'HAUPTMERKMALE',
    'OPZIONI': 'OPTIONEN',

    # Size Guide Popup
    '<h2 class="text-2xl font-bold mb-6 text-center">GUIDA ALLE TAGLIE</h2>': '<h2 class="text-2xl font-bold mb-6 text-center">GRÖSSENFÜHRER</h2>',
    'alt="Guida alle taglie"': 'alt="Größentabelle"',
    'Clicca sulla "X" in alto a destra per chiudere': 'Klicke auf das „X“ oben rechts, um zu schließen',

    # Promo buttons
    'Scopri altri prodotti': 'Weitere Produkte entdecken',
    'Voglio maggiori informazioni': 'Ich möchte weitere Informationen',

    # Footer titles
    'BICYCLE LINE': 'BICYCLE LINE',
    'Brand': 'Marke',
    'Storia': 'Geschichte',
    'Sostenibilità': 'Nachhaltigkeit',
    'Contattaci': 'Kontaktiere uns',
    'SHOP': 'SHOP',
    'Bambino': 'Kinder',
    'Offerte': 'Angebote',
    'Guida allo shopping online': 'Online-Shopping-Anleitung',
    'LINK UTILI': 'NÜTZLICHE LINKS',
    'Spedizione': 'Versand',
    'Pagamento': 'Zahlung',
    'Guida alle taglie': 'Größentabelle',
    'Utilizzo del prodotto e garanzia': 'Produktverwendung und Garantie',
    'Resi': 'Rückgaben',
    'NOTE LEGALI': 'RECHTLICHE HINWEISE',
    'Privacy Policy': 'Datenschutzerklärung',
    'Cookie policy': 'Cookie-Richtlinie',
    'Termini e condizioni': 'Allgemeine Geschäftsbedingungen',
    'CONTATTACI': 'KONTAKT',

    # Alt text common
    'vista frontale': 'Vorderansicht',
}

specific = {
    "W0274-CALZINI-ESTIVI-13CM.html": {
        'BL - W0274 CALZINI ESTIVI 13CM': 'BL - W0274 SOMMERSOCKEN 13CM',
        'W0274 CALZINI ESTIVI 13CM vista frontale': 'W0274 SOMMERSOCKEN 13CM Vorderansicht',
        'CALZINI ESTIVI 13CM': 'SOMMERSOCKEN 13CM',
        'W0274 CALZINI ESTIVI 13CM': 'W0274 SOMMERSOCKEN 13CM',
        'Calzino estivo in microfibra antibatterica per un comfort ottimale. È realizzato con fasce elastiche che mantengono fermo il piede durante la pedalata. Polsino alto 13 cm.': 'Sommersocke aus antibakterieller Mikrofaser für optimalen Komfort. Mit elastischen Bändern, die den Fuß während des Radfahrens festhalten. 13 cm hoher Schaft.',
        'Trattamento antibatterico': 'Antibakterielle Behandlung',
        'Tessuto Skinlife®': 'Skinlife® Gewebe',
        'Costruzione a rete traspirante': 'Atmungsaktive Netzkonstruktion',
        'Polsino elastico sulla caviglia': 'Elastischer Schaft am Knöchel',
        'Costruzione con filati elastici per impedire lo scivolamento del calzino': 'Konstruktion mit elastischen Garnen, um das Verrutschen der Socke zu verhindern',
        'Cucitura impalpabile sulla punta del piede': 'Unsichtbare Naht an der Fußspitze',
    },
    "W2632-SCALDACOLLO.html": {
        'BL - W2632 SCALDACOLLO': 'BL - W2632 HALSWÄRMER',
        'W2632 SCALDACOLLO vista frontale': 'W2632 HALSWÄRMER Vorderansicht',
        'SCALDACOLLO': 'HALSWÄRMER',
        'W2632 SCALDACOLLO': 'W2632 HALSWÄRMER',
        'Scaldacollo realizzato in tessuto leggero, confortevole ed elastico con finitura a taglio vivo per una migliore regolazione. Ottima vestibilità e diverse possibilità di utilizzo: scaldacollo, bandana, maschera facciale o sottocasco.': 'Halswärmer aus leichtem, bequemem und elastischem Stoff mit Rohschnittkante für bessere Anpassung. Hervorragende Passform und vielseitige Verwendungsmöglichkeiten: Halswärmer, Bandana, Gesichtsmaske oder Helmunterzieher.',
        'Super elastico e confortevole': 'Super elastisch und bequem',
        'Per ulteriore protezione termica': 'Für zusätzlichen Wärmeschutz',
        'Molto traspirante': 'Sehr atmungsaktiv',
        'Multiuso': 'Mehrzweck',
        'Personalizzazione con tecnica di sublimazione digitale': 'Personalisierung mit digitaler Sublimationstechnik',
    },
    "W6600-CALZINI-ESTIVI-AERO-PIEDE-NERO.html": {
        'BL - W6600 CALZINI ESTIVI AERO PIEDE NERO': 'BL - W6600 SOMMERSOCKEN AERO FUß SCHWARZ',
        'W6600 CALZINI ESTIVI AERO PIEDE NERO vista frontale': 'W6600 SOMMERSOCKEN AERO FUß SCHWARZ Vorderansicht',
        'CALZINI ESTIVI AERO PIEDE NERO': 'SOMMERSOCKEN AERO FUß SCHWARZ',
        'W6600 CALZINI ESTIVI AERO PIEDE NERO': 'W6600 SOMMERSOCKEN AERO FUß SCHWARZ',
        'Calzino estivo in microfibra antibatterica per un comfort ottimale. È realizzato con fasce elastiche che mantengono fermo il piede durante la pedalata. Polsino alto 18 cm.': 'Sommersocke aus antibakterieller Mikrofaser für optimalen Komfort. Mit elastischen Bändern, die den Fuß während des Radfahrens festhalten. 18 cm hoher Schaft.',
        'Trattamento antibatterico': 'Antibakterielle Behandlung',
        'Tessuto Skinlife®': 'Skinlife® Gewebe',
        'Costruzione a rete traspirante': 'Atmungsaktive Netzkonstruktion',
        'Polsino elastico sulla caviglia': 'Elastischer Schaft am Knöchel',
        'Costruzione con filati elastici per impedire lo scivolamento del calzino': 'Konstruktion mit elastischen Garnen, um das Verrutschen der Socke zu verhindern',
        'Cucitura impalpabile sulla punta del piede': 'Unsichtbare Naht an der Fußspitze',
    },
    "W6601-CALZINI-ESTIVI-AERO-PIEDE-BIANCO.html": {
        'BL - W6601 CALZINI ESTIVI AERO PIEDE BIANCO': 'BL - W6601 SOMMERSOCKEN AERO FUß WEIß',
        'W6601 CALZINI ESTIVI AERO PIEDE BIANCO vista frontale': 'W6601 SOMMERSOCKEN AERO FUß WEIß Vorderansicht',
        'CALZINI ESTIVI AERO PIEDE BIANCO': 'SOMMERSOCKEN AERO FUß WEIß',
        'W6601 CALZINI ESTIVI AERO PIEDE BIANCO': 'W6601 SOMMERSOCKEN AERO FUß WEIß',
        'Calzino a collo alto permutato dall\'esperienza con i teams professionisti. Realizzato in 2 tessuti molto diversi per permettere a comfort e tecnicità di coabitare assieme: la parte del collo del piede è realizzata in una fibra elasticizzata per la massima aerodinamicità del movimento ed invece il piede con la punta rinforzata risiede in una morbida spugna di filato confortevole e traspirante. Consigliato per la strada e per chi cerca in ogni dettaglio la massima velocità e performance.': 'Hochschaft-Socke, entwickelt aus Erfahrungen mit Profi-Teams. Hergestellt aus 2 sehr unterschiedlichen Stoffen, damit Komfort und Technik zusammengehen: Der Fußrücken besteht aus einem elastischen Faser für maximale Aerodynamik der Bewegung, während der Fuß mit verstärkter Zehenpartie in einem weichen, bequemen und atmungsaktiven Garnschwamm sitzt. Empfohlen für die Straße und für alle, die in jedem Detail maximale Geschwindigkeit und Leistung suchen.',
        'Altezza 18 cm.': 'Höhe 18 cm.',
        'Tessuto Lycra MITI - Qskin': 'Lycra MITI - Qskin Stoff',
        'Punta e base imbottite in spugna': 'Zehen- und Fersenbereich mit Schwammpolsterung',
        'Punta rinforzata': 'Verstärkte Zehenpartie',
        'Tessuti aerodinamici aderenti sulla gamba': 'Aerodynamische, eng anliegende Stoffe am Bein',
        'Silicone interno antiscivolo confortevole': 'Bequemes, rutschfestes Innensilikon',
        'Cucitura piatta per aumentare il comfort': 'Flache Naht für mehr Komfort',
    },
    "W6602-MANICOTTI-INVERNALI.html": {
        'BL - W6602 MANICOTTI INVERNALI': 'BL - W6602 WINTERSTULPEN',
        'W6602 MANICOTTI INVERNALI vista frontale': 'W6602 WINTERSTULPEN Vorderansicht',
        'MANICOTTI INVERNALI': 'WINTERSTULPEN',
        'W6602 MANICOTTI INVERNALI': 'W6602 WINTERSTULPEN',
        'Ti presentiamo i nostri manicotti da ciclismo invernali: essenziali per affrontare le pedalate più fredde. Realizzati in tessuto Miti premium, offrono calore e traspirabilità. Grazie alla vestibilità ergonomica si integra perfettamente con la tua maglia. Completi di un elastico in silicone nella parte superiore, questi manicotti rimangono fermi per una pedalata senza distrazioni.': 'Hier sind unsere Winter-Radstulpen: unverzichtbar für die kältesten Ausfahrten. Hergestellt aus hochwertigem Miti-Stoff, bieten sie Wärme und Atmungsaktivität. Dank der ergonomischen Passform fügen sie sich perfekt in dein Trikot ein. Mit einem Silikonband am oberen Rand bleiben diese Stulpen sicher sitzen, damit du dich voll und ganz aufs Radfahren konzentrieren kannst.',
        'Eccellenti proprietà traspiranti': 'Hervorragende atmungsaktive Eigenschaften',
        'Tessuto termico Mititech': 'Mititech Thermostoff',
        'Ottima protezione termica': 'Hervorragender Wärmeschutz',
        'Compressione attiva': 'Aktive Kompression',
        'Fondo elastico siliconato sulla parte superiore e finitura a taglio vivo sul polso': 'Silikonisiertes elastisches Band am oberen Rand und Rohschnittkante am Handgelenk',
        'Grande elasticità': 'Hohe Elastizität',
        'Personalizzazione con 1 logo su lato esterno del manicotto': 'Personalisierung mit 1 Logo auf der Außenseite der Stulpe',
        'Personalizzazione disponibile in materiale bianco o reflex grigio scuro': 'Personalisierung verfügbar in weißem Material oder dunkelgrauem Reflexmaterial',
    },
    "W6603-GAMBALI-INVERNALI.html": {
        'BL - W6603 GAMBALI INVERNALI': 'BL - W6603 WINTERBEINLINGE',
        'W6603 GAMBALI INVERNALI vista frontale': 'W6603 WINTERBEINLINGE Vorderansicht',
        'GAMBALI INVERNALI': 'WINTERBEINLINGE',
        'W6603 GAMBALI INVERNALI': 'W6603 WINTERBEINLINGE',
        'Gambali per protezione termica elevata e taglio anatomico, sono realizzati con materiale Mititech Thermal di M.I.T.I. Grip in silicone per garantire stabilità e inserti riflettenti per la visibilità in situazioni buie. Disponibili in un elegante design monocolore, questi gambali sono perfetti per mostrare l\'identità della tua squadra attraverso loghi termoapplicati di precisione.': 'Beinlinge mit hervorragendem Wärmeschutz und anatomischem Schnitt, hergestellt aus Mititech Thermal Material von M.I.T.I. Silikongriff für Stabilität und reflektierende Einsätze für Sichtbarkeit bei Dunkelheit. In einem eleganten einfarbigen Design erhältlich, sind diese Beinlinge perfekt, um die Identität deines Teams durch präzise thermoapplizierte Logos zu zeigen.',
        'Eccellenti proprietà traspiranti': 'Hervorragende atmungsaktive Eigenschaften',
        'Tessuto termico Mititech': 'Mititech Thermostoff',
        'Ottima protezione termica': 'Hervorragender Wärmeschutz',
        'Compressione attiva': 'Aktive Kompression',
        'Fondo elastico siliconato sulla parte superiore e finitura a taglio vivo sul polso': 'Silikonisiertes elastisches Band am oberen Rand und Rohschnittkante am Handgelenk',
        'Grande elasticità': 'Hohe Elastizität',
        'Personalizzazione con 1 logo su lato esterno del manicotto': 'Personalisierung mit 1 Logo auf der Außenseite der Stulpe',
        'Personalizzazione disponibile in materiale bianco o reflex grigio scuro': 'Personalisierung verfügbar in weißem Material oder dunkelgrauem Reflexmaterial',
    },
    "W6604-GUANTI-ESTIVI.html": {
        'BL - W6604 GUANTI ESTIVI': 'BL - W6604 SOMMERHANDSCHUHE',
        'W6604 GUANTI ESTIVI vista frontale': 'W6604 SOMMERHANDSCHUHE Vorderansicht',
        'GUANTI ESTIVI': 'SOMMERHANDSCHUHE',
        'W6604 GUANTI ESTIVI': 'W6604 SOMMERHANDSCHUHE',
        'Eccezionali guanti da strada con vestibilità aerodinamica e leggera. Imbottitura minima sul palmo per un utilizzo tecnico e una manovrabilità ottimali.': 'Außergewöhnliche Straßenhandschuhe mit aerodynamischer und leichter Passform. Minimale Polsterung auf der Handfläche für optimale technische Nutzung und Handhabung.',
        'Tessuto sul dorso traspirante e bi-elasticizzato': 'Atmungsaktiver und bi-elastischer Stoff auf dem Handrücken',
        'Vestibilità aerodinamica': 'Aerodynamische Passform',
        'Palmo con imbottitura ottimizzata': 'Handfläche mit optimierter Polsterung',
        'Dorso completamente personalizzabile': 'Vollständig personalisierbarer Handrücken',
    },
    "W6605-GUANTI-LUNGHI-ESTIVI.html": {
        'BL - W6605 GUANTI LUNGHI ESTIVI': 'BL - W6605 LANGE SOMMERHANDSCHUHE',
        'W6605 GUANTI LUNGHI ESTIVI vista frontale': 'W6605 LANGE SOMMERHANDSCHUHE Vorderansicht',
        'GUANTI LUNGHI ESTIVI': 'LANGE SOMMERHANDSCHUHE',
        'W6605 GUANTI LUNGHI ESTIVI': 'W6605 LANGE SOMMERHANDSCHUHE',
        'Guanti gravel realizzati con un materiale molto traspirante e resistente per ogni avventura. Imbottitura minima sul palmo per un utilizzo tecnico e una manovrabilità ottimali.': 'Gravel-Handschuhe aus sehr atmungsaktivem und strapazierfähigem Material für jedes Abenteuer. Minimale Polsterung auf der Handfläche für optimale technische Nutzung und Handhabung.',
        'Tessuto sul dorso traspirante e bi-elasticizzato': 'Atmungsaktiver und bi-elastischer Stoff auf dem Handrücken',
        'Vestibilità aerodinamica': 'Aerodynamische Passform',
        'Palmo con imbottitura ottimizzata': 'Handfläche mit optimierter Polsterung',
        'Dorso completamente personalizzabile': 'Vollständig personalisierbarer Handrücken',
    },
    "W6606-GUANTI-INVERNALI.html": {
        'BL - W6606 GUANTI INVERNALI': 'BL - W6606 WINTERHANDSCHUHE',
        'W6606 GUANTI INVERNALI vista frontale': 'W6606 WINTERHANDSCHUHE Vorderansicht',
        'GUANTI INVERNALI': 'WINTERHANDSCHUHE',
        'W6606 GUANTI INVERNALI': 'W6606 WINTERHANDSCHUHE',
        'Guanti elastici che offrono un\'eccellente protezione in condizioni fredde e ventose. Un ottimo compromesso tra guanti leggeri e guanti invernali più spessi. Un pannello antivento lo protegge dal vento e dal freddo, con un interno foderato in pile che assicura che le tue mani rimangano calde durante la corsa.': 'Elastische Handschuhe, die bei kaltem und windigem Wetter hervorragenden Schutz bieten. Ein optimaler Kompromiss zwischen leichten Handschuhen und dickeren Winterhandschuhen. Eine winddichte Paneel schützt vor Wind und Kälte, während das fleecegefütterte Innere dafür sorgt, dass deine Hände während der Fahrt warm bleiben.',
        'Tessuto sul dorso traspirante e bi-elasticizzato': 'Atmungsaktiver und bi-elastischer Stoff auf dem Handrücken',
        'Vestibilità aerodinamica': 'Aerodynamische Passform',
        'Palmo con imbottitura ottimizzata': 'Handfläche mit optimierter Polsterung',
        'Dorso completamente personalizzabile': 'Vollständig personalisierbarer Handrücken',
    },
    "W6607-MANICOTTI-INVERNALI-STAMPABILI.html": {
        'BL - W6607 MANICOTTI INVERNALI STAMPABILI': 'BL - W6607 BEDRUCKBARE WINTERSTULPEN',
        'W6607 MANICOTTI INVERNALI STAMPABILI vista frontale': 'W6607 BEDRUCKBARE WINTERSTULPEN Vorderansicht',
        'MANICOTTI INVERNALI STAMPABILI': 'BEDRUCKBARE WINTERSTULPEN',
        'W6607 MANICOTTI INVERNALI STAMPABILI': 'W6607 BEDRUCKBARE WINTERSTULPEN',
        'Nuovi manicotti invernali personalizzabili: un must per affrontare le pedalate fredde con il tuo stile unico. Realizzati in tessuto Miti di altissima qualità, offrono ottimo isolamento termico e traspirabilità. Grazie alla vestibilità ergonomica si integra perfettamente con la tua maglia. Perfetto per la mattina presto o per gli allenamenti a fine giornata.': 'Neue personalisierbare Winter-Stulpen: ein Muss, um kalte Ausfahrten mit deinem einzigartigen Stil zu bestreiten. Hergestellt aus hochwertigstem Miti-Stoff, bieten sie hervorragende Wärmeisolierung und Atmungsaktivität. Dank der ergonomischen Passform fügen sie sich perfekt in dein Trikot ein. Perfekt für frühe Morgen oder Abendtrainings.',
        'Eccellenti proprietà traspiranti': 'Hervorragende atmungsaktive Eigenschaften',
        'Tessuto termico Miti Full Black Endurance': 'Miti Full Black Endurance Thermostoff',
        'Ottima protezione termica': 'Hervorragender Wärmeschutz',
        'Compressione attiva': 'Aktive Kompression',
        'Fondo elastico siliconato sulla parte superiore e finitura a taglio vivo sul polso': 'Silikonisiertes elastisches Band am oberen Rand und Rohschnittkante am Handgelenk',
        'Grande elasticità': 'Hohe Elastizität',
        'Personalizzazione con tecnica di sublimazione digitale': 'Personalisierung mit digitaler Sublimationstechnik',
    },
    "W6608-GAMBALI-INVERNALI-STAMPABILI.html": {
        'BL - W6608 GAMBALI INVERNALI STAMPABILI': 'BL - W6608 BEDRUCKBARE WINTERBEINLINGE',
        'W6608 GAMBALI INVERNALI STAMPABILI vista frontale': 'W6608 BEDRUCKBARE WINTERBEINLINGE Vorderansicht',
        'GAMBALI INVERNALI STAMPABILI': 'BEDRUCKBARE WINTERBEINLINGE',
        'W6608 GAMBALI INVERNALI STAMPABILI': 'W6608 BEDRUCKBARE WINTERBEINLINGE',
        'Gambali termici personalizzabili: essenziali per le tue uscite invernali con i colori della tua squadra. Realizzati in tessuto termico di alta qualità, offrono calore e traspirabilità. Con la possibilità di personalizzazione tramite sublimazione, questi gambali riflettono il tuo stile unico. Perfetti per la mattina presto o allenamenti all\'imbrunire, abbraccia il freddo con sicurezza e comfort.': 'Personalisierbare Thermo-Beinlinge: unverzichtbar für deine Winterausfahrten in den Farben deines Teams. Hergestellt aus hochwertigem Thermostoff, bieten sie Wärme und Atmungsaktivität. Mit der Möglichkeit der Personalisierung durch Sublimation spiegeln diese Beinlinge deinen einzigartigen Stil wider. Perfekt für frühe Morgen oder Dämmerungstrainings, meistere die Kälte mit Sicherheit und Komfort.',
        'Eccellenti proprietà traspiranti': 'Hervorragende atmungsaktive Eigenschaften',
        'Tessuto termico Miti Full Black Endurance': 'Miti Full Black Endurance Thermostoff',
        'Ottima protezione termica': 'Hervorragender Wärmeschutz',
        'Compressione attiva': 'Aktive Kompression',
        'Fondo elastico siliconato sulla parte superiore e finitura a taglio vivo sul polso': 'Silikonisiertes elastisches Band am oberen Rand und Rohschnittkante am Handgelenk',
        'Grande elasticità': 'Hohe Elastizität',
        'Personalizzazione con tecnica di sublimazione digitale': 'Personalisierung mit digitaler Sublimationstechnik',
    },
    "W6610-CALZINI-ESTIVI-18CM.html": {
        'BL - W6610 CALZINI ESTIVI 18CM': 'BL - W6610 SOMMERSOCKEN 18CM',
        'W6610 CALZINI ESTIVI 18CM vista frontale': 'W6610 SOMMERSOCKEN 18CM Vorderansicht',
        'CALZINI ESTIVI 18CM': 'SOMMERSOCKEN 18CM',
        'W6610 CALZINI ESTIVI 18CM': 'W6610 SOMMERSOCKEN 18CM',
        'Calzino estivo in microfibra antibatterica per un comfort ottimale. È realizzato con fasce elastiche che mantengono fermo il piede durante la pedalata. Polsino alto 18 cm.': 'Sommersocke aus antibakterieller Mikrofaser für optimalen Komfort. Mit elastischen Bändern, die den Fuß während des Radfahrens festhalten. 18 cm hoher Schaft.',
        'Trattamento antibatterico': 'Antibakterielle Behandlung',
        'Tessuto Skinlife®': 'Skinlife® Gewebe',
        'Costruzione a rete traspirante': 'Atmungsaktive Netzkonstruktion',
        'Polsino elastico sulla caviglia': 'Elastischer Schaft am Knöchel',
        'Costruzione con filati elastici per impedire lo scivolamento del calzino': 'Konstruktion mit elastischen Garnen, um das Verrutschen der Socke zu verhindern',
        'Cucitura impalpabile sulla punta del piede': 'Unsichtbare Naht an der Fußspitze',
    },
    "W6612-BERRETTINO-ESTIVO-AIR-CAP.html": {
        'BL - W6612 BERRETTINO ESTIVO AIR-CAP': 'BL - W6612 SOMMERMÜTZE AIR-CAP',
        'W6612 BERRETTINO ESTIVO AIR-CAP vista frontale': 'W6612 SOMMERMÜTZE AIR-CAP Vorderansicht',
        'BERRETTINO ESTIVO AIR-CAP': 'SOMMERMÜTZE AIR-CAP',
        'W6612 BERRETTINO ESTIVO AIR-CAP': 'W6612 SOMMERMÜTZE AIR-CAP',
        'BL Air-cap è perfetto per tutti gli sport all\'aria aperta: ciclismo, corsa, trail running e altro ancora. Realizzato in tessuto elastico traforato, il berretto BL migliora la dissipazione del calore, garantendo traspirabilità e leggerezza ottimali.': 'Die BL Air-cap ist perfekt für alle Outdoor-Sportarten: Radfahren, Laufen, Trailrunning und mehr. Hergestellt aus elastischem perforiertem Stoff, verbessert die BL-Mütze die Wärmeableitung und garantiert optimale Atmungsaktivität und Leichtigkeit.',
        'Buona protezione UPF (15+)': 'Guter UPF-Schutz (15+)',
        'Fascia elastica interna più morbida per migliorare il comfort': 'Weicheres elastisches Innenband für mehr Komfort',
        "L'inserto in rete garantisce una corretta traspirabilità e il tessuto in microfibra Premium offre un tocco di morbidezza e garantisce un'asciugatura rapida": 'Das Netzeinsatz sorgt für richtige Atmungsaktivität und der Premium-Mikrofaserstoff bietet eine weiche Haptik und garantiert schnelle Trocknung',
        'Visiera in materiale resistente': 'Schirm aus widerstandsfähigem Material',
        'Personalizzazione con tecnica di sublimazione digitale': 'Personalisierung mit digitaler Sublimationstechnik',
    },
}

for f in files:
    path = os.path.join(base_dir, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Apply common translations
    for old, new in common.items():
        content = content.replace(old, new)

    # Apply file-specific translations
    if f in specific:
        for old, new in specific[f].items():
            content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Translated: {f}")

print("All files translated successfully.")
