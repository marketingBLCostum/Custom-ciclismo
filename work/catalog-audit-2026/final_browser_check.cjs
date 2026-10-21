const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const dir='work/catalog-audit-2026',root=process.cwd(),metadata=JSON.parse(fs.readFileSync(dir+'/pages.json','utf8'));
const files=[...new Set(['index.html','INGLESE/index.html','FRANCESE/index.html','TEDESCO/index.html','SPAGNOLO/index.html',...metadata.filter(p=>['W6005','W6028','W7203','W6011','W6036'].includes(p.code)).map(p=>p.file),'DONNA SCHEDE PRODOTTO/W6514-APEX.html','RAGAZZI SCHEDE PRODOTTO/W2200-ECHELON.html','TEDESCO/ACCESSORI DE/W6604-GUANTI-ESTIVI-DE.html','DONNA SCHEDE PRODOTTO/W6047-ECHELON-AIR-CARGO.html','TEDESCO/DONNA DE/W6529-APEX-ULTRA_DE.html'])];
const browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});let next=0,issues=[],checks=0;
async function worker(){const page=await browser.newPage();await page.route('https://**/*',r=>r.abort());try{while(next<files.length){const file=files[next++];for(const width of [320,390,768,1440]){let errors=[];const listen=e=>errors.push(e.message);page.on('pageerror',listen);await page.setViewportSize({width,height:1000});await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'load'});const data=await page.evaluate(()=>{
let faqFailed=false;document.querySelectorAll('.faq-btn').forEach(b=>{b.click();if(!b.closest('.faq-item').classList.contains('open'))faqFailed=true;b.click();});const broken=[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src);
const plain=[...document.querySelectorAll('.acc-head')].filter(h=>!h.querySelector('.acc-icon'));
const visible=plain.map(h=>getComputedStyle(h.parentElement.querySelector('.acc-body')).display);
plain.forEach(h=>h.click());const plainChanged=plain.some((h,i)=>getComputedStyle(h.parentElement.querySelector('.acc-body')).display!==visible[i]);
const heads=[...document.querySelectorAll('.acc-head')].filter(h=>h.querySelector('.acc-icon'));heads.forEach(h=>h.click());const failed=heads.some(h=>getComputedStyle(h.parentElement.querySelector('.acc-body')).display==='none');
document.querySelector('#lang-toggle')?.click();const langOpen=document.querySelector('#lang-dropdown')?.classList.contains('open');document.querySelector('#lang-toggle')?.click();
document.querySelector('#hamburger')?.click();const mobileOpen=document.querySelector('#mobile-nav')?.classList.contains('open');document.querySelector('#mobile-close')?.click();
return {broken,plainChanged,failed,faqFailed,langOpen,mobileOpen,overflow:document.documentElement.scrollWidth>innerWidth+1};});
if(errors.length||data.broken.length||data.plainChanged||data.failed||data.faqFailed||!data.langOpen||!data.mobileOpen||data.overflow)issues.push({file,width,errors,...data});page.off('pageerror',listen);checks++;}
}}finally{await page.close();}}
await Promise.all([worker(),worker(),worker()]);
// Representative final images: product desktop, product mobile and home category buttons.
const shots=await browser.newPage();await shots.route('https://**/*',r=>r.abort());
for(const [file,width,label,target]of [['DONNA SCHEDE PRODOTTO/W6514-APEX.html',390,'women-mobile','.sidebar'],['UOMO SCHEDE PRODOTTO/W6028-ECHELON-AIR.html',1440,'echelon-air-desktop','.sidebar'],['index.html',390,'home-categories-mobile','.cat-grid']]){await shots.setViewportSize({width,height:1000});await shots.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'load'});await shots.locator(target).scrollIntoViewIfNeeded();await shots.screenshot({path:dir+'/final-'+label+'.png',animations:'disabled'});}
await browser.close();const result={pages:files.length,checks,widths:[320,390,768,1440],issues};fs.writeFileSync(dir+'/final-browser-check.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));if(issues.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});

