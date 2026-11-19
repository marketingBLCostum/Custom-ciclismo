from pathlib import Path
p=Path('work/catalog-audit-2026/css_loaded.cjs');s=p.read_text(encoding='utf-8-sig')
s=s.replace("(async()=>{", """(async()=>{const fs=require('fs'),path=require('path');const server=require('http').createServer((req,res)=>{const target=path.resolve(process.cwd(),'.'+decodeURIComponent(req.url.split('?')[0]));if(!target.startsWith(process.cwd()+path.sep)){res.writeHead(403);return res.end();}fs.readFile(target,(err,data)=>{if(err){res.writeHead(404);return res.end();}res.setHeader('Content-Type',target.endsWith('.css')?'text/css':'text/html');res.end(data);});});await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;""")
s=s.replace("r.request().url().startsWith('file:')", "r.request().url().startsWith(base)")
s=s.replace("pathToFileURL(process.cwd()+'/DONNA SCHEDE PRODOTTO/W6514-APEX.html').href", "base+'/DONNA%20SCHEDE%20PRODOTTO/W6514-APEX.html'")
s=s.replace('await b.close();','await b.close();server.close();')
p.with_name('css_http.cjs').write_text(s,encoding='utf-8')
