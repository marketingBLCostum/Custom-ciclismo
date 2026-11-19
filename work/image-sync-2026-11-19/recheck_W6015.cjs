const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});const p=await b.newPage({viewport:{width:1440,height:1000}});
 await p.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
 await p.goto(pathToFileURL(path.join(process.cwd(),'UOMO SCHEDE PRODOTTO/W6015-ECHELON.html')).href,{waitUntil:'load'});
 await p.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));});
 await p.screenshot({path:'work/image-sync-2026-11-19/body-W6015-desktop.png'});
 const info=await p.evaluate(()=>({title:document.querySelector('h1').textContent,titleRect:document.querySelector('h1').getBoundingClientRect().toJSON(),sidebarRect:document.querySelector('.sidebar').getBoundingClientRect().toJSON(),overflow:document.documentElement.scrollWidth>innerWidth+1}));
 fs.writeFileSync('work/image-sync-2026-11-19/W6015-repaint-check.json',JSON.stringify(info,null,2));console.log(info);await b.close();
})().catch(e=>{console.error(e);process.exitCode=1});
