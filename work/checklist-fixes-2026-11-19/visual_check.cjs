const path=require('path'),fs=require('fs'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=process.cwd(),out='work/checklist-fixes-2026-11-19',browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});
 const page=await browser.newPage();await page.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
 const cases=[
  {file:'RAGAZZI SCHEDE PRODOTTO/W2212.html',width:320,target:'.sizes',name:'kid-sizes-320.png'},
  {file:'SPAGNOLO/ACCESSORI ES/W6602-MANICOTTI-INVERNALI-ES.html',width:1440,name:'spanish-header.png'},
  {file:'SPAGNOLO/ACCESSORI ES/W6602-MANICOTTI-INVERNALI-ES.html',width:390,target:'.promo-links',name:'spanish-links-mobile.png'},
  {file:'ACCESSORI SCHEDA PRODOTTO/W6600-CALZINI-ESTIVI-AERO-PIEDE-NERO.html',width:390,target:'.sidebar',name:'aero-materials-mobile.png'},
  {file:'INGLESE/UOMO EN/W6012-ECHELON_EN.html',width:390,target:'.sidebar',name:'W6012-options-mobile.png'},
 ];
 for(const item of cases){
  await page.setViewportSize({width:item.width,height:1000});await page.goto(pathToFileURL(path.join(root,item.file)).href,{waitUntil:'load',timeout:60000});
  await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;});
  if(item.target)await page.locator(item.target).scrollIntoViewIfNeeded();
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  await page.screenshot({path:out+'/'+item.name,timeout:60000});
 }
 await browser.close();fs.writeFileSync(out+'/visual-captures.json',JSON.stringify(cases,null,2));console.log('Saved',cases.length,'visual checks.');
})().catch(e=>{console.error(e);process.exitCode=1});
