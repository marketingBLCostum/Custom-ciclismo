from pathlib import Path
p=Path('work/catalog-audit-2026/write_safety_report.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("assert len(breakpoints)==30", "topbar=json.loads((D/'safety-topbar-2026-10-26.json').read_text(encoding='utf8'))\nassert len(topbar)==20 and not any(x['overlap'] for x in topbar)\nassert len(breakpoints)==30")
s=s.replace('## Ulteriori correzioni applicate','Ulteriori 20 verifiche delle intestazioni nelle cinque lingue a 769, 1024, 1200 e 1280 px dopo l\'ultima correzione: nessuna sovrapposizione tra messaggio e azione.\n\n## Ulteriori correzioni applicate')
s=s.replace('Corretti inoltre due spazi mancanti', 'Risolta anche la sovrapposizione del messaggio della barra superiore con il collegamento al preventivo tra 769 e 1200 px. A queste larghezze la barra mostra il messaggio; il contatto resta disponibile dal menu.\n\nCorretti inoltre due spazi mancanti')
s=s.replace('e safety-breakpoints-2026-10-26.json.', 'safety-breakpoints-2026-10-26.json e safety-topbar-2026-10-26.json.')
p.write_text(s,encoding='utf8')
