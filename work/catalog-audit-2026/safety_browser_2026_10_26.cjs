const fs=require('fs'),path=require('path'),vm=require('vm'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const root=process.cwd(),out='work/catalog-audit-2026',files=[];
function scan(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(['.git','images','work'].includes(e.name))continue;const p=path.join(dir,e.name);if(e.isDirectory())scan(p);else if(e.name.endsWith('.html'))files.push(path.relative(root,p));}}scan(root);
const syntax=[];
for(const file of files){const html=fs.readFileSync(file,'utf8');let n=0;for(const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)){n++;if(/type\s*=\s*["'](?:application\/ld\+json|application\/json)/i.test(m[1]))continue;try{new vm.Script(m[2],{filename:file+':script-'+n});}catch(e){syntax.push({file,error:e.message});}}}
const browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});let cursor=0,done=0,checks=0,issues=[];const completed=[];function save(){fs.writeFileSync(out+'/safety-browser-2026-10-26.json',JSON.stringify({date:'2026-10-26',pages:files.length,completed,checks,widths,syntax,issues},null,2));}const widths=[1440,1280,1024,768,390,320];
async function worker(){const page=await browser.newPage();await page.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());try{while(cursor<files.length){const file=files[cursor++];let errors=[];const listener=e=>errors.push(e.message);page.on('pageerror',listener);await page.setViewportSize({width:1440,height:1000});await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'domcontentloaded',timeout:60000});await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{},{timeout:10000}).catch(()=>{});
for(const width of widths){await page.setViewportSize({width,height:1000});const result=await page.evaluate(()=>{
const broken=[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.getAttribute('src'));
const langBtn=document.querySelector('#lang-toggle'),langMenu=document.querySelector('#lang-dropdown');langBtn?.click();const langOpen=!!langMenu?.classList.contains('open');const langCount=langMenu?.querySelectorAll('a').length;langBtn?.click();
document.querySelector('#hamburger')?.click();const mobileOpen=!!document.querySelector('#mobile-nav')?.classList.contains('open');document.querySelector('#mobile-close')?.click();
let accordionFailed=false,plainChanged=false;
for(const head of document.querySelectorAll('.acc-head')){const body=head.parentElement.querySelector('.acc-body');if(!body)continue;const initial=getComputedStyle(body).display;head.click();const after=getComputedStyle(body).display;if(head.querySelector('.acc-icon')){if(initial===after)accordionFailed=true;head.click();if(getComputedStyle(body).display!==initial)accordionFailed=true;}else if(initial!==after)plainChanged=true;}
let faqFailed=false;for(const b of document.querySelectorAll('.faq-btn')){b.click();if(!b.closest('.faq-item').classList.contains('open'))faqFailed=true;b.click();}
const sidebar=document.querySelector('.sidebar'),title=document.querySelector('h1.product-title');
return {broken,langOpen,langCount,mobileOpen,accordionFailed,plainChanged,faqFailed,htmlLang:document.documentElement.lang,overflow:document.documentElement.scrollWidth>innerWidth+1,scrollWidth:document.documentElement.scrollWidth,sidebarOverflow:!!sidebar&&sidebar.scrollWidth>sidebar.clientWidth+1,titleOverflow:!!title&&title.scrollWidth>title.clientWidth+1};
});checks++;const expected=file.startsWith('INGLESE')?'en':file.startsWith('FRANCESE')?'fr':file.startsWith('TEDESCO')?'de':file.startsWith('SPAGNOLO')?'es':'it';
if(errors.length||result.broken.length||!result.langOpen||result.langCount!==5||!result.mobileOpen||result.accordionFailed||result.plainChanged||result.faqFailed||result.htmlLang!==expected||result.overflow||result.sidebarOverflow||result.titleOverflow)issues.push({file,width,errors:[...errors],...result});}
page.off('pageerror',listener);done++;completed.push(file);save();if(done%60===0)console.log('Checked',done,'/',files.length,'pages;',checks,'viewport checks');
}}finally{await page.close();}}
try{await Promise.all([worker(),worker()]);}finally{await browser.close();}
const result={date:'2026-10-26',pages:files.length,checks,widths,syntax,issues};fs.writeFileSync(out+'/safety-browser-2026-10-26.json',JSON.stringify(result,null,2));const perWidth={};for(const i of issues)perWidth[i.width]=(perWidth[i.width]||0)+1;console.log(JSON.stringify({pages:files.length,checks,syntax,issueCases:issues.length,perWidth,examples:issues.slice(0,8)},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
