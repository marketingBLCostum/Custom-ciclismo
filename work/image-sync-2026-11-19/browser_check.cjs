const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Libia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=process.cwd(),out='work/image-sync-2026-11-19';
const plan=JSON.parse(fs.readFileSync(out+'/plan.json','utf8'));
const inspection=JSON.parse(fs.readFileSync(out+'/inspection.json','utf8'));
const sourceImages=new Map(inspection.map(i=>[i.source.path.toLowerCase(),i.sourceImage]));
const changed=new Map(plan.replacements.map(i=>[i.destination.path.toLowerCase(),sourceImages.get(i.source.path.toLowerCase())]));
const files=plan.affectedPages;
let cursor=0,checks=0,done=0;const results=[],issues=[];
function save(){fs.writeFileSync(out+'/browser-verification.json',JSON.stringify({date:'2026-11-19',pages:files.length,completed:done,checks,widths:[1440,390],issues,results},null,2));}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge',args:['--disable-gpu']});
 async function worker(){
  const page=await browser.newPage();
  await page.route('**/*',r=>r.request().url().startsWith('file:')?r.continue():r.abort());
  try{while(cursor<files.length){
   const file=files[cursor++];const errors=[];const listener=e=>errors.push(e.message);page.on('pageerror',listener);
   await page.setViewportSize({width:1440,height:1000});
   await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'domcontentloaded',timeout:60000});
   await page.waitForFunction(()=>[...document.images].every(i=>i.complete),{},{timeout:30000});
   for(const width of [1440,390]){
    await page.setViewportSize({width,height:1000});
    const r=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].map(i=>({src:i.getAttribute('src'),complete:i.complete,width:i.naturalWidth,height:i.naturalHeight})),galleryCount:document.querySelector('.gallery')?.querySelectorAll('img').length||0,languageLinks:document.querySelector('#lang-dropdown')?.querySelectorAll('a').length||0}));
    const broken=r.images.filter(i=>!i.complete||!i.width);const mismatches=[];let updated=0;
    for(const img of r.images){
     if(!img.src||/^(https?:|data:)/.test(img.src))continue;
     const key=path.relative(root,path.resolve(path.dirname(path.join(root,file)),decodeURIComponent(img.src))).split(path.sep).join('/').toLowerCase();
     if(changed.has(key)){
      updated++;const expected=changed.get(key).size;
      if(img.width!==expected[0]||img.height!==expected[1])mismatches.push({src:img.src,actual:[img.width,img.height],expected});
     }
    }
    const result={file,width,updatedImages:updated,imageCount:r.images.length,overflow:r.overflow,broken,mismatches,errors:[...errors],languageLinks:r.languageLinks};
    results.push(result);checks++;
    if(r.overflow||broken.length||mismatches.length||errors.length||r.languageLinks!==5)issues.push(result);
   }
   page.off('pageerror',listener);done++;save();if(done%40===0)console.log('Checked',done,'/',files.length,'pages;',checks,'viewport checks');
  }}finally{await page.close();}
 }
 try{await Promise.all([worker(),worker()]);}finally{await browser.close();save();}
 console.log(JSON.stringify({pages:files.length,completed:done,checks,issueCases:issues.length,examples:issues.slice(0,5)},null,2));
 if(issues.length)process.exitCode=1;
})().catch(e=>{save();console.error(e);process.exitCode=1});
