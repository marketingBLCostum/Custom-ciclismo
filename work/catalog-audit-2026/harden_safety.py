from pathlib import Path
p=Path('work/catalog-audit-2026/safety_browser_2026_10_26.cjs')
s=p.read_text(encoding='utf-8')
s=s.replace("let cursor=0,done=0,checks=0,issues=[];", "let cursor=0,done=0,checks=0,issues=[];const completed=[];function save(){fs.writeFileSync(out+'/safety-browser-2026-10-26.json',JSON.stringify({date:'2026-10-26',pages:files.length,completed,checks,widths,syntax,issues},null,2));}")
s=s.replace("await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'load'});", "await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'domcontentloaded',timeout:60000});await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{},{timeout:10000}).catch(()=>{});")
s=s.replace("page.off('pageerror',listener);done++;", "page.off('pageerror',listener);done++;completed.push(file);save();")
s=s.replace("Promise.all([worker(),worker(),worker(),worker()])", "Promise.all([worker(),worker()])")
p.write_text(s,encoding='utf-8')
