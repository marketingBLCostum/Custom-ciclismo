const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=process.cwd(),out='work/checklist-fixes-2026-11-19';
const files=JSON.parse(fs.readFileSync(out+'/changes.json','utf8'));
const widths=[1440,1280,390,320];let cursor=0,done=0,checks=0;const issues=[],results=[];
function save(){fs.writeFileSync(out+'/browser-verification.json',JSON.stringify({pages:files.length,completed:done,checks,widths,issues,results},null,2));}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});
 async function worker(){
  const page=await browser.newPage();await page.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
  try{while(cursor<files.length){
   const item=files[cursor++],errors=[];const listener=e=>errors.push(e.message);page.on('pageerror',listener);
   await page.setViewportSize({width:1440,height:1000});
   await page.goto(pathToFileURL(path.join(root,item.file)).href,{waitUntil:'domcontentloaded',timeout:60000});
   await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{},{timeout:30000});
   for(const width of widths){
    await page.setViewportSize({width,height:1000});
    const r=await page.evaluate(()=>{
     const side=document.querySelector('.sidebar'),acc=[];
     for(const x of side.querySelectorAll('.acc-item')){
      const h=x.querySelector('.acc-head'),b=x.querySelector('.acc-body'),icon=x.querySelector('.acc-icon');if(!h||!b)continue;
      const before=getComputedStyle(b).display;let after=before,restored=before;
      if(icon){h.click();after=getComputedStyle(b).display;h.click();restored=getComputedStyle(b).display;}
      acc.push({heading:x.querySelector('.acc-title')?.textContent.trim(),expandable:!!icon,before,after,restored});
     }
     const toggle=document.querySelector('#lang-toggle'),menu=document.querySelector('#lang-dropdown');toggle.click();const languageOpen=menu.classList.contains('open');toggle.click();
     document.querySelector('#hamburger').click();const mobileOpen=document.querySelector('#mobile-nav').classList.contains('open');document.querySelector('#mobile-close').click();
     return {lang:document.documentElement.lang,overflow:document.documentElement.scrollWidth>innerWidth+1,sidebarOverflow:side.scrollWidth>side.clientWidth+1,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),acc,languageOpen,languageCount:menu.querySelectorAll('a').length,mobileOpen,sizes:[...side.querySelectorAll('.sizes .size')].map(x=>x.textContent.trim()),bodyText:document.body.innerText};
    });
    const failures=r.acc.filter(a=>a.expandable&&(a.before!=='none'||a.after==='none'||a.restored!==a.before));
    const translated=!(item.lang==='es'&&/(?:Maßgefertigte|Angebot anfordern|Weitere Produkte entdecken|Ich möchte weitere Informationen)/.test(r.bodyText))&&!/\bTemperaturea\b/.test(r.bodyText)&&!(['es','fr'].includes(item.lang)&&/\bTemperatur\b/.test(r.bodyText));
    const kid=item.reasons.includes('Taglie KID 104-164');const sizesOk=!kid||r.sizes.join(',')==='104,116,128,140,152,164';
    const row={file:item.file,width,overflow:r.overflow,sidebarOverflow:r.sidebarOverflow,broken:r.broken,accordionFailures:failures,languageOpen:r.languageOpen,languageCount:r.languageCount,mobileOpen:r.mobileOpen,translated,sizesOk,errors:[...errors]};
    results.push(row);checks++;
    if(row.overflow||row.sidebarOverflow||row.broken.length||failures.length||!row.languageOpen||row.languageCount!==5||!row.mobileOpen||!translated||!sizesOk||errors.length)issues.push(row);
   }
   page.off('pageerror',listener);done++;save();if(done%25===0)console.log('Checked',done,'/',files.length,'pages;',checks,'viewport checks');
  }}finally{await page.close();}
 }
 try{await Promise.all([worker(),worker()]);}finally{await browser.close();save();}
 console.log(JSON.stringify({pages:files.length,completed:done,checks,issues:issues.length,examples:issues.slice(0,8)},null,2));
 if(issues.length)process.exitCode=1;
})().catch(e=>{save();console.error(e);process.exitCode=1});
