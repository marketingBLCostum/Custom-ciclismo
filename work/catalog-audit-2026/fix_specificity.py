from pathlib import Path
p=Path('catalog-fixes.css');s=p.read_text(encoding='utf8');s=s.replace('  body { min-width: 0; }','  :root body { min-width: 0; }');s=s.replace('  main.page {','  :root main.page {');s=s.replace('  .nav {','  :root .nav {').replace('  .nav-links {','  :root .nav-links {').replace('  .hamburger {','  :root .hamburger {');p.write_text(s,encoding='utf8')
