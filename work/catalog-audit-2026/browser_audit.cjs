const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const root=process.cwd(),dir='work/catalog-audit-2026';
const products=JSON.parse(fs.readFileSync(dir+'/pages.json','utf8'));
const all=[];function scan(d){for(const f of fs.readdirSync(d,{withFileTypes:true})){if(f.name==='.git'||f.name==='images'||f.name==='work')continue;const p=path.join(d,f.name);if(f.isDirectory())scan(p);else if(f.name.endsWith('.html'))all.push(path.relative(root,p));}}scan(root);
const browser=await chromium.launch({headless:true,channel:'msedge'}),page=await browser.newPage({viewport:{width:1440,height:1000}});
await page.route('https://**/*',r=>r.abort());
const issues=[];let done=0;
for(const rel of all){
 let errs=[];const listener=e=>errs.push(e.message);page.on('pageerror',listener);
 await page.goto(pathToFileURL(path.join(root,rel)).href,{waitUntil:'load'});
 const data=await page.evaluate(()=>{
 const imgs=[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src'));
 const menu=document.querySelector('#lang-toggle'),drop=document.querySelector('#lang-dropdown');
 if(menu)menu.click();const langOpen=!!drop?.classList.contains('open');
 if(menu)menu.click();
 const heads=[...document.querySelectorAll('.acc-head')],icons=heads.filter(h=>h.querySelector('.acc-icon'));
 icons.forEach(h=>h.click());const accFailed=icons.filter(h=>getComputedStyle(h.parentElement.querySelector('.acc-body')).display==='none').length;
 // Read-only section headings should not produce runtime exceptions.
 heads.filter(h=>!h.querySelector('.acc-icon')).forEach(h=>h.click());
 return {imgs,langOpen,accFailed,htmlLang:document.documentElement.lang};
 });
 await page.setViewportSize({width:390,height:900});
 const mobile=await page.evaluate(()=>{
 const ham=document.querySelector('#hamburger'),nav=document.querySelector('#mobile-nav');
 if(ham)ham.click();const open=!!nav?.classList.contains('open');document.querySelector('#mobile-close')?.click();
 const title=document.querySelector('h1.product-title'),r=title?.getBoundingClientRect();
 return {menuOpen:open,overflow:document.documentElement.scrollWidth>innerWidth+1,titleOverflow:r?title.scrollWidth>title.clientWidth+1:false};
 });
 if(data.imgs.length||!data.langOpen||data.accFailed||!mobile.menuOpen||mobile.overflow||mobile.titleOverflow||errs.length)issues.push({file:rel,...data,mobile,errors:errs});
 const expected=rel.startsWith('INGLESE')?'en':rel.startsWith('TEDESCO')?'de':rel.startsWith('FRANCESE')?'fr':rel.startsWith('SPAGNOLO')?'es':'it';
 if(data.htmlLang!==expected)issues.push({file:rel,wrongHtmlLang:data.htmlLang,expected});
 page.off('pageerror',listener);await page.setViewportSize({width:1440,height:1000});done++;
 if(done%75===0)console.log('Checked',done,'of',all.length);
}
fs.writeFileSync(dir+'/browser-issues.json',JSON.stringify({total:all.length,issues},null,2));
const groups={};for(const i of issues){for(const e of i.errors||[])groups[e]=(groups[e]||0)+1;}
console.log(JSON.stringify({total:all.length,issuePages:issues.length,runtimeErrors:groups,other:issues.filter(i=>i.imgs?.length||i.accFailed||i.mobile?.overflow||i.mobile?.titleOverflow||i.wrongHtmlLang||!i.langOpen||!i.mobile?.menuOpen).map(i=>({...i,errors:undefined})).slice(0,35)},null,2));
await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
