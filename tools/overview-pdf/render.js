const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.cwd()+'/overview.html');await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'overview.pdf',width:'297mm',height:'210mm',printBackground:true});await b.close();})();
