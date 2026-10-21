const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,channel:'msedge'}),page=await browser.newPage({viewport:{width:390,height:900}});await page.route('https://**/*',r=>r.abort());
const cases=[['DONNA SCHEDE PRODOTTO/W6514-APEX.html','mobile-w6514'],['RAGAZZI SCHEDE PRODOTTO/W2200-ECHELON.html','mobile-w2200'],['TEDESCO/ACCESSORI DE/W6604-GUANTI-ESTIVI-DE.html','mobile-de-gloves'],['index.html','mobile-home']];
for(const [file,label]of cases){await page.goto(pathToFileURL(path.join(process.cwd(),file)).href,{waitUntil:'load'});const size=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,offscreen:[...document.querySelectorAll('body *')].map(e=>({tag:e.tagName,cls:e.className,w:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right,txt:e.textContent.trim().slice(0,60)})).filter(e=>e.right>innerWidth+10&&e.w>0).slice(0,15)}));console.log(JSON.stringify({file,...size}));}
await browser.close();})();

