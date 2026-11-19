const path=require('path'),fs=require('fs'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=process.cwd(),out='work/image-sync-2026-11-19';
 const b=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});
 const page=await b.newPage();await page.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
 async function open(file,width=1440){await page.setViewportSize({width,height:1000});await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'domcontentloaded',timeout:60000});await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{},{timeout:30000});}
 const captures=[];
 for(const [file,name,width] of [
  ['UOMO SCHEDE PRODOTTO/W6012-ECHELON.html','body-W6012-desktop.png',1440],
  ['UOMO SCHEDE PRODOTTO/W6015-ECHELON.html','body-W6015-desktop.png',1440],
  ['DONNA SCHEDE PRODOTTO/W6516-APEX.html','W6516-desktop.png',1280],
  ['DONNA SCHEDE PRODOTTO/W6516-APEX.html','W6516-mobile.png',390],
 ]){await open(file,width);await page.screenshot({path:out+'/'+name,timeout:60000});captures.push({file,name,width});}
 for(const [file,code,name] of [
  ['donna.html','W6516','card-W6516.png'],
  ['ragazzi.html','W2218','card-W2218.png'],
  ['uomo.html','W6015','card-W6015-preview.png'],
 ]){
  await open(file,1440);const card=page.locator('.card').filter({has:page.locator('a[href*="'+code+'"]')}).first();
  await card.scrollIntoViewIfNeeded();if(code==='W6015'){await card.hover();await page.waitForTimeout(400);}
  await card.screenshot({path:out+'/'+name,timeout:60000});captures.push({file,name,width:1440});
 }
 await open('RAGAZZI SCHEDE PRODOTTO/W2212.html');await page.locator('.gallery').screenshot({path:out+'/W2212-front-and-back.png',timeout:60000});captures.push({file:'RAGAZZI SCHEDE PRODOTTO/W2212.html',name:'W2212-front-and-back.png',width:1440});
 fs.writeFileSync(out+'/visual-captures.json',JSON.stringify(captures,null,2));await b.close();console.log('Saved',captures.length,'visual checks.');
})().catch(e=>{console.error(e);process.exitCode=1});
