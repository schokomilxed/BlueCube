const {chromium}=require('playwright');const fs=require('fs');
const DUR=+process.argv[2]||282000;
(async()=>{const b=await chromium.launch({args:['--disable-gpu']});const p=await b.newPage({viewport:{width:1728,height:1000}});
p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('file://'+process.cwd()+'/probe.html');await p.waitForTimeout(800);
await p.evaluate(()=>{
  window.LOG={t0:null,beats:[],ids:Object.keys(EX),samples:[]};
  const hb=FILM.hooks.beat;
  FILM.hooks.beat=(B,bi)=>{if(bi===0&&LOG.t0===null)LOG.t0=performance.now();LOG.beats.push({bi,t:performance.now()});hb&&hb(B,bi)};
  const cells=LOG.ids.map(id=>{const r=EX[id].o.rect,l=[];for(let y=r.y;y<r.y+r.h;y++)for(let x=r.x;x<r.x+r.w;x++){const i=SWI[x+','+y];if(i!==undefined)l.push(i)}return l});
  window.CELLS=cells;
  setInterval(()=>{const now=performance.now();if(LOG.t0===null)return;
    const row=[Math.round((now-LOG.t0))];
    LOG.ids.forEach((id,k)=>{const e=EX[id];const c=CELLS[k];let mx=0,sm=0;for(const i of c){const v=Math.min(1,SWC[i].v);if(v>mx)mx=v;sm+=v}
      row.push(+Math.min(1,e.level).toFixed(3),+mx.toFixed(3),c.length?+(sm/c.length).toFixed(3):0)});
    LOG.samples.push(row)},40);
  FILM.setRange(null);FILM.start();
});
await p.waitForTimeout(DUR);
const out=await p.evaluate(()=>({beats:LOG.beats.map(x=>({bi:x.bi,t:Math.round(x.t-LOG.t0)})),ids:LOG.ids,samples:LOG.samples,cells:CELLS.map(c=>c.length),
  info:Object.fromEntries(LOG.ids.map(id=>[id,{name:EX[id].o.name,rect:EX[id].o.rect}])),total:FILM.totalSec()}));
fs.writeFileSync('sampled_full.json',JSON.stringify(out));
console.log(out.samples.length,'samples',out.beats.length,'beats total',out.total);
await b.close()})()
