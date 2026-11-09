/* Bento-Film · Kapitel 2 – Fahrdynamik & Sicherheit
   Inhalte + Engine, gemeinsam genutzt von index.html (nur Film) und wand.html (Wand + Licht + Film).
   Erwartet: CHOREO (choreo.js) und ein Element #stage (1680 × 900 px = 7 × 5 Zellen à 240 × 180 px).
   Optional: window.ASSETS = {datei: dataURI} für die eigenständige Version. */
const FILM=(function(){
const W=1680,H=900,COLS=CHOREO.COLS,ROWS=CHOREO.ROWS;
const src=f=>(window.ASSETS&&window.ASSETS[f])||('assets/'+f);

/* ---------- content building blocks ---------- */
const img=(f,o={})=>`<div class="layer media-l"><div class="media ${o.cls||''} ${o.kb===false?'':'kb'}"><img src="${src(f)}" style="object-position:${o.pos||'50% 50%'}">${o.chip?`<span class="chip">${o.chip}</span>`:''}${o.fx?`<canvas class="fx" data-fx="${o.fx}"></canvas>`:''}</div></div>`;
const vid=(f,o={})=>`<div class="layer media-l"><div class="media ${o.cls||''}"><video src="${src(f)}" muted loop playsinline preload="auto" style="object-position:${o.pos||'50% 50%'}"></video>${o.chip?`<span class="chip">${o.chip}</span>`:''}</div></div>`;
const sil=(f,pos)=>`<div class="layer sil"><div class="media"><img src="${src(f)}" style="object-position:${pos||'50% 50%'}"></div></div>`;
const quo=(head,text,o={})=>`<div class="layer txt ${o.cls||''}"><div class="kick">${head}</div><div class="q ${o.size||''}">„${text}“</div></div>`;
const nar=(text,o={})=>`<div class="layer txt dark ${o.cls||''}">${o.kick?`<div class="kick">${o.kick}</div>`:''}<div class="n ${o.size||''}">${text}</div></div>`;
const lab=(name,meta,o={})=>`<div class="layer txt ${o.cls||'bot'}"><div class="h ${o.size||'m'}">${name}</div><div class="meta">${meta}</div></div>`;
const fact=(num,unit,o={})=>`<div class="layer txt ${o.cls||''}">${o.kick?`<div class="kick">${o.kick}</div>`:''}<div class="num ${o.size||''}">${num}</div><div class="unit">${unit}</div></div>`;
const gfx=type=>`<div class="layer"><canvas class="fx" data-fx="${type}"></canvas></div>`;
const cnt=(v,fmt)=>`<span data-count="${v}" data-fmt="${fmt}">0</span>`;

const C={
 // silhouettes for the ambient base grid (nur aktive Exponate)
 's:a2':sil('a2.jpg'),'s:pd':sil('phonedial.jpg'),'s:pscb':sil('pscb.jpg'),'s:procon':sil('procon_still.jpg'),
 's:det':sil('detroit.jpg','30% 60%'),'s:tt':sil('turbotwist.jpg','45% 50%'),'s:mr':sil('magride.jpg'),'s:bremse':sil('p1_bremse.jpg'),

 title:`<div class="layer txt dark"><div class="kick">Kapitel 2</div><div class="h xl">Fahrdynamik<br>&amp; Sicherheit</div><div class="n s" style="margin-top:26px;opacity:.85">Wie beherrscht man die Kräfte, die man selbst erzeugt?</div></div>`,

 // M1 Leichtbau
 a2:img('a2.jpg',{chip:'Audi Space Frame'}),
 a2lab:lab('Audi A2','Space Frame · 1999'),
 a2q:quo('Audi A2 · 1999','Ich bin aus Aluminium gebaut, wo andere auf Stahl beharrten – jedes eingesparte Kilo ist mein Argument gegen die Trägheit der Masse.'),

 // M2 Kontaktpunkt
 det:img('detroit.jpg',{pos:'30% 60%',chip:'VW „Detroit“'}),
 detlab:lab('VW „Detroit“','Felge · 2004'),
 detq:quo('VW „Detroit“-Felge · 2004','Ich sehe nicht nach viel aus, aber ich halte das Auto in der Spur, wenn es darauf ankommt. Meine Linien sind Kult – meine Aufgabe ist Haftung.',{size:'l'}),
 tt:img('turbotwist.jpg',{pos:'49% 50%',chip:'Porsche Turbo Twist'}),
 ttq:quo('Porsche „Turbo Twist“ · 1995','Ich drehe mich nicht nur – ich zeichne die Kurve, bevor sie kommt. Meine Speichen tragen das Gewicht der Geschwindigkeit und geben es als Haftung an den Asphalt zurück.',{size:'l'}),
 pd:img('phonedial.jpg',{chip:'Lamborghini „Phone Dial“'}),
 pdq:quo('Lamborghini „Phone Dial“ · 1985','Man hält mich für Zierde, doch ich bin das letzte Glied zwischen Wahnsinn und Straße. Was der Motor entfesselt, muss durch mich hindurch – oder es geschieht gar nicht.'),
 n2:nar('Leichtbau und Motorkraft enden hier – am letzten Zentimeter zwischen Auto und Asphalt.',{size:'s'}),

 // M3 Kraft kontrollierbar machen
 mrimg:img('magride.jpg',{cls:'white contain',kb:false}),
 mrvid:vid('magride.mp4',{chip:'Audi Magnetic Ride'}),
 mrq:quo('Audi Magnetic Ride · 2007','Ich fühle jede Unebenheit, bevor du sie spürst. Ein Magnetfeld genügt, und aus weich wird straff – ich bin das Fahrwerk, das mit dir mitdenkt.'),
 mrf:`<div class="layer txt"><div class="kick">Prinzip</div><div class="h s">Magneto&shy;rheologisch.</div><div class="q" style="margin-top:16px">Unter Strom ändert die Dämpferflüssigkeit ihre Härte – in Millisekunden.</div></div>`,
 n3:nar('Kraftkontrolle durch Aerodynamik statt Mechanik.',{size:'s'}),
 air:gfx('airflow'),
 airq:quo('Porsche 911 · Windkanalmodell','Ich bin nur sechs Kilo schwer und keinen Meter lang, doch im Windkanal entscheide ich, welche Linie den Sturm übersteht. Bevor der erste Motor läuft, kenne ich schon den Weg der Luft.'),
 airf:fact(`${cnt(96,'int')} CM`,'Länge · rund 6 kg<br>Glasfaser-Modell',{kick:'Windkanalmodell'}),

 // M4 Bremse
 pscb:img('pscb.jpg',{cls:'white contain',kb:false,chip:'Porsche PSCB'}),
 pscbq:quo('Porsche Surface Coated Brake','Ich bin hart wie Diamant und sauber wie kein Bremssystem vor mir – ich bringe die Kraft zum Stehen, ohne Spuren zu hinterlassen.',{size:'l'}),
 pscbf:fact('WOLFRAM&shy;KARBID','Beschichtung – härter als Stahl, fast ohne Bremsstaub',{size:'s',kick:'Oberfläche'}),
 discs:gfx('discs'),
 feq:quo('Porsche Formel-E-Bremse · 2025','Man erwartet mich wuchtig, doch ich bin winzig – weil ich das Bremsen mit dem Motor teile. Was du für Schwäche hältst, ist meine effizienteste Form.'),
 n4:nar('Die eine bremst mit roher Härte, die andere fast gar nicht mehr selbst – beides ist Fortschritt.',{size:'s'}),
 chpass:vid('chiron_pass.mp4',{chip:'Ehra-Lessien · 2. August 2019'}),
 f490:fact(`${cnt(490.48,'dec2')}`,'km/h · Bugatti Chiron<br>Super Sport 300+',{kick:'Rekord 2019'}),
 n5:nar('Ein Rekord, der eine Bremse braucht, die es vorher nicht gab.',{size:'s'}),
 bremse:img('p1_bremse.jpg',{cls:'contain sheen',kb:false}),
 btitle:`<div class="layer txt"><div class="h m">Leichter.<br>Komplexer.<br>Belastbarer.</div><div class="meta">Bugatti Chiron · 3D-gedruckter Titan-Bremssattel · 2018</div></div>`,
 bq:quo('Bugatti Chiron Bremse','Man hat mich nicht gegossen, man hat mich Schicht für Schicht gedacht. Ich bin fast halb so leicht wie mein geschmiedeter Vorgänger – und halte trotzdem stand, wenn andere längst kapitulieren.'),
 bdet:img('p2_detail.jpg',{cls:'sheen'}),
 b29:fact(`${cnt(2.9,'dec')} KG`,'Titan'),
 b2213:fact(`${cnt(2213,'int')}`,'gedruckte<br>Schichten'),
 n490:nar('490 km/h zu erreichen ist die eine Hälfte der Geschichte. Aus 490 km/h wieder herunterzukommen – diese hier.',{size:'l'}),
 bk:`<div class="layer txt"><div class="q">Ich kämpfe gegen Masse und Hitze. Ich muss standhalten, ohne unnötig schwer zu werden.</div></div>`,
 fire:img('p3_feuer.jpg',{cls:'fire',fx:'sparks',kb:false}),
 chrear:vid('chiron_rear.mp4'),
 bvon:`<div class="layer txt"><div class="h s">Von Höchst&shy;geschwindig&shy;keit zu Kontrolle.</div></div>`,
 bz1:`<div class="layer txt"><div class="q">Ich zeige die andere Seite extremer Performance: Wie kommt ein Fahrzeug sicher wieder zum Stillstand?</div></div>`,
 bz2:`<div class="layer txt"><div class="q">Zwischen Fahrdynamik, Sicherheit und Motorsport verbinde ich den Rekord mit der Herausforderung, Geschwindigkeit zu beherrschen.</div></div>`,
 rad:img('p4_rad.jpg'),

 // M5 Sicherheit
 pccrash:vid('procon_crash.mp4',{chip:'Audi Procon-Ten · Crashtest'}),
 pcmech:vid('procon_mech.mp4'),
 pcq:quo('Audi Procon-Ten · 1985','Wenn es kracht, ziehe ich mich zurück – nicht aus Feigheit, sondern aus Kalkül. Meine Drahtseile spannen sich, und in dem Moment, in dem alles zu spät scheint, schaffe ich den entscheidenden Zentimeter Freiraum.'),
 pcf:`<div class="layer txt"><div class="kick">Prinzip</div><div class="h s">Rein mechanisch.</div><div class="q" style="margin-top:18px">Der Motor wird beim Aufprall nach hinten gedrückt, ein Stahlseil zieht das Lenkrad vom Fahrer weg und strafft die Gurte.</div></div>`,
 esvw:`<div class="layer txt"><div class="kick">Experimental Safety Volkswagen · 1972</div><div class="h xxl">ESVW 1</div><div class="rule"></div><div class="q l" style="max-width:1100px">„Ich bin nicht gebaut, um zu gefallen – ich bin gebaut, um zu bewahren. Jede meiner Beulen ist eine Antwort auf die Frage, was ein Körper aushält.“</div></div>`,
 n6:nar('Dieselbe Physik, die im Motor Kraft erzeugt, muss hier wieder eingefangen werden.'),

 // M6 Klammer
 k1:img('a2.jpg',{chip:'Leichtbau'}),
 k2:img('phonedial.jpg',{chip:'Kontaktpunkt'}),
 k3:vid('magride.mp4',{chip:'Fahrwerk'}),
 k4:img('p1_bremse.jpg',{cls:'contain',kb:false,chip:'Bremse'}),
 k5:vid('procon_crash.mp4',{chip:'Sicherheitszelle'}),
 kq:nar('Wie beherrscht man die Kräfte, die man selbst erzeugt?',{size:'s',kick:'Kapitel 2'}),
 n7:nar('Leichtbau, Kontaktpunkt, Fahrwerk, Bremse, Sicherheitszelle – fünf Antworten auf eine Kraft, die das Kapitel zuvor selbst erzeugt hat.',{size:'l'}),
};

/* ---------- engine ----------
   Jeder Beat = Folge von Schritten (choreo.js); in jedem Schritt bewegt sich jede Kachel nur auf
   einer Achse. Danach steht der Inhalt so lange, wie man zum Lesen braucht. */
const {MOMENTS,BEATS,SLOTS:NS,collapsed}=CHOREO;
const SLOTS=[...Array(NS)].map((_,i)=>i);
const STEP=850,GAP=60,REVEAL=900;
const stage=document.getElementById('stage');
const tiles={};
const P0=Object.values(CHOREO.P);
const hooks={beat:null,show:null,step:null};
SLOTS.forEach(i=>{const t=document.createElement('div');t.className='tile';t._layers={};t._key=null;t._shownAt=0;stage.appendChild(t);tiles[i]=t});
function initTiles(){SLOTS.forEach(i=>{const t=tiles[i];t._r=i<8?P0[i].slice():[COLS,ROWS,COLS,ROWS];place(t,t._r,true)})}

function layerFor(t,key){
  if(!t._layers[key]){const w=document.createElement('div');w.innerHTML=C[key];const l=w.firstElementChild;l.dataset.key=key;t.appendChild(l);t._layers[key]=l}
  return t._layers[key];
}
const css=v=>parseFloat(getComputedStyle(document.documentElement).getPropertyValue(v));
function place(t,r,instant){
  const g=css('--gap'),p=css('--pad'),cw=(W-2*p-(COLS-1)*g)/COLS,ch=(H-2*p-(ROWS-1)*g)/ROWS;
  const w=Math.max(0,(r[2]-r[0])*cw+(r[2]-r[0]-1)*g),h=Math.max(0,(r[3]-r[1])*ch+(r[3]-r[1]-1)*g);
  if(instant)t.style.transition='none';
  t.style.left=p+r[0]*(cw+g)+'px';t.style.top=p+r[1]*(ch+g)+'px';t.style.width=w+'px';t.style.height=h+'px';
  t.classList.toggle('collapsed',w===0||h===0);
  if(instant){t.offsetWidth;t.style.transition=''}
}
const relayout=()=>SLOTS.forEach(i=>place(tiles[i],tiles[i]._r));

/* reading time: words of all newly revealed text */
const words=key=>{const d=document.createElement('div');d.innerHTML=C[key]||'';return (d.textContent.trim().match(/\S+/g)||[]).length};
BEATS.forEach(b=>{
  const n=Object.values(b.c).reduce((s,k)=>s+(k.startsWith('s:')?0:words(k)),0);
  b.holdS=b.hold??Math.min(11,Math.max(4.5,2.5+n/3)); // ~3 words per second, 4.5–11 s
  b.revealAt=200+b.steps.length*(STEP+GAP);            // ms after beat start when new content appears
});
let TEMPO=1; // multiplies only the standing time, never the transitions
const durOf=b=>b.revealAt+REVEAL+b.holdS*1000*TEMPO;

let cur=-1,timers=[],timer=null,playing=true,beatStart=0;
const later=(fn,ms)=>timers.push(setTimeout(fn,ms));

function countUp(el,beat){
  const to=parseFloat(el.dataset.count),fmt=el.dataset.fmt,t0=performance.now()+300,d=1600;
  const f=v=>fmt==='dec'?v.toFixed(1).replace('.',','):fmt==='dec2'?v.toFixed(2).replace('.',','):Math.round(v).toLocaleString('de-DE');
  (function step(now){const k=Math.min(1,Math.max(0,(now-t0)/d));el.textContent=f(to*(1-Math.pow(1-k,3)));if(k<1&&cur===beat)requestAnimationFrame(step)})(performance.now());
}
/* canvas effects */
const FX={
  sparks(cv,alive){const ctx=cv.getContext('2d');let ps=[];(function loop(){if(!alive())return;const w=cv.width=cv.clientWidth,h=cv.height=cv.clientHeight;
    for(let i=0;i<6;i++)ps.push({x:w*(.42+Math.random()*.12),y:h*(.55+Math.random()*.2),vx:(Math.random()*2-.6)*9,vy:-Math.random()*9-2,l:1});
    ctx.globalCompositeOperation='lighter';ps=ps.filter(p=>p.l>0);
    for(const p of ps){p.x+=p.vx;p.y+=p.vy;p.vy+=.35;p.l-=.022;ctx.strokeStyle=`rgba(255,${150+Math.random()*80|0},40,${p.l})`;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-p.vx*1.6,p.y-p.vy*1.6);ctx.stroke()}
    requestAnimationFrame(loop)})()},
  airflow(cv,alive){const ctx=cv.getContext('2d');const t0=performance.now();(function loop(now){if(!alive())return;const w=cv.width=cv.clientWidth*2,h=cv.height=cv.clientHeight*2,t=(now-t0)/1000;
    ctx.fillStyle='#151517';ctx.fillRect(0,0,w,h);
    const base=h*.72,cx=w*.5,L=w*.62;
    // simplified sports-car profile: hood, roof, fastback
    const prof=x=>{const u=(x-(cx-L/2))/L;if(u<0||u>1)return 0;const hood=.10*Math.sin(Math.PI*Math.min(1,u/.35)*.5);const roof=.30*Math.exp(-Math.pow((u-.52)/.2,2));return h*Math.max(hood,roof)*.9+h*.06*Math.sin(Math.PI*u)};
    ctx.beginPath();ctx.moveTo(cx-L/2,base);for(let x=cx-L/2;x<=cx+L/2;x+=4)ctx.lineTo(x,base-prof(x));ctx.lineTo(cx+L/2,base);ctx.closePath();ctx.fillStyle='#e9e9e9';ctx.fill();
    ctx.lineWidth=3;
    // streamlines hug the body near the surface and relax with distance
    for(let i=0;i<14;i++){const off=h*.03+i*h*.04,decay=Math.exp(-off/(h*.32));ctx.beginPath();
      for(let x=0;x<=w;x+=6)ctx.lineTo(x,base-off-prof(x)*decay);
      ctx.setLineDash([60,40]);ctx.lineDashOffset=-t*260-i*23;ctx.strokeStyle=`rgba(120,200,255,${.8-i*.045})`;ctx.stroke()}
    ctx.setLineDash([]);ctx.fillStyle='#f2f2f2';ctx.font=`600 ${h*.045}px Barlow`;ctx.fillText('PORSCHE 911 · WINDKANALMODELL',w*.05,h*.1);
    ctx.font=`500 ${h*.035}px Barlow`;ctx.globalAlpha=.7;ctx.fillText('Grafik-Platzhalter – Modellfoto fehlt',w*.05,h*.16);ctx.globalAlpha=1;
    requestAnimationFrame(loop)})(t0)},
  discs(cv,alive){const ctx=cv.getContext('2d');const t0=performance.now();(function loop(now){if(!alive())return;const w=cv.width=cv.clientWidth*2,h=cv.height=cv.clientHeight*2,k=Math.min(1,(now-t0)/1400),e=1-Math.pow(1-k,3);
    ctx.fillStyle='#151517';ctx.fillRect(0,0,w,h);
    const disc=(cx,cy,r,label,sub,col)=>{ctx.lineWidth=r*.18;ctx.strokeStyle=col;ctx.beginPath();ctx.arc(cx,cy,r*.82,-Math.PI/2,-Math.PI/2+Math.PI*2*e);ctx.stroke();
      ctx.lineWidth=4;ctx.strokeStyle='#666';ctx.beginPath();ctx.arc(cx,cy,r*.35,0,Math.PI*2);ctx.stroke();
      ctx.fillStyle='#f2f2f2';ctx.textAlign='center';ctx.font=`700 ${h*.042}px Barlow`;ctx.fillText(label,cx,cy+r+h*.06);ctx.font=`500 ${h*.03}px Barlow`;ctx.globalAlpha=.7;ctx.fillText(sub,cx,cy+r+h*.1);ctx.globalAlpha=1};
    disc(w*.5,h*.3,w*.3,'PSCB','Serie · Porsche','#d9d9d9');
    disc(w*.5,h*.73,w*.12,'FORMEL E','bremst mit dem Motor','#ffb347');
    requestAnimationFrame(loop)})(t0)},
};

function showContent(t,key,bi,instant){
  const old=t._key?t._layers[t._key]:null;const l=layerFor(t,key);t._key=key;t._shownAt=performance.now()-(instant?1e4:0);
  if(old&&old!==l){old.classList.remove('on');const v=old.querySelector('video');if(v)setTimeout(()=>v.pause(),600)}
  t.appendChild(l); // newest layer on top so its wipe covers the old one
  if(instant){l.style.transition='none';l.classList.add('on');l.offsetWidth;l.style.transition='';}
  else{
    l.querySelectorAll('img').forEach(im=>{im.style.animation='none';im.offsetWidth;im.style.animation=''});
    l.classList.add('on');
    l.querySelectorAll('[data-count]').forEach(el=>countUp(el,bi));
    l.querySelectorAll('canvas.fx').forEach(cv=>FX[cv.dataset.fx]?.(cv,()=>t._key===key&&l.classList.contains('on')));
  }
  const v=l.querySelector('video');if(v){if(!instant)v.currentTime=0;v.play().catch(()=>{})}
  hooks.show?.(t,key,instant);
}

function go(bi){
  timers.forEach(clearTimeout);timers=[];clearTimeout(timer);
  cur=bi;const B=BEATS[bi];
  const changed=Object.entries(B.c).filter(([id,k])=>tiles[id]._key!==k).map(([id])=>+id);
  // old text leaves before the move; old images stay in their frames while the grid moves
  changed.forEach(id=>{const t=tiles[id];if(t._key){const l=t._layers[t._key];if(!l.classList.contains('media-l')){l.classList.remove('on');t._fading=true}}});
  let at=200;
  B.steps.forEach(st=>{
    later(()=>{const moves=[];st.forEach(x=>{const t=tiles[x.id];
      if(x.f&&collapsed(t._r)){t._r=x.f.slice();place(t,t._r,true)} // park at entry edge, invisible
      moves.push({id:x.id,from:t._r.slice(),to:x.r.slice()});
      t._r=x.r.slice();place(t,t._r)});
      hooks.step?.(moves,STEP)},at);
    at+=STEP+GAP;
  });
  later(()=>changed.forEach((id,n)=>setTimeout(()=>{tiles[id]._fading=false;showContent(tiles[id],B.c[id],bi)},n*110)),at);
  beatStart=performance.now();
  hooks.beat?.(B,bi);
  if(playing)timer=setTimeout(next,durOf(B));
}
// browsers occasionally pause a freshly revealed clip; keep every visible clip running
setInterval(()=>document.querySelectorAll('.layer.on video').forEach(v=>{if(v.paused)v.play().catch(()=>{})}),1000);
// the last beat looks exactly like beat 0, so the loop re-syncs invisibly and continues with the title
let range=null; // [first,last] beat – loops just this section when set
function next(){
  if(range){if(cur+1>range[1]||cur<range[0])jump(range[0]);else go(cur+1);return}
  if(cur+1<BEATS.length)go(cur+1);else{resetToStart();go(1)}}
function setRange(r){range=r}
function resetToStart(){timers.forEach(clearTimeout);initTiles();SLOTS.forEach(i=>{const t=tiles[i];t._fading=false;const k=BEATS[0].c[i];if(k)showContent(t,k,0,true);else{if(t._key)t._layers[t._key].classList.remove('on');t._key=null}})}
// jumping: rebuild the exact grid state before beat bi without animation, then play bi
function jump(bi){
  bi=Math.max(0,Math.min(BEATS.length-1,bi));
  resetToStart();
  for(let k=1;k<bi;k++){BEATS[k].steps.forEach(st=>st.forEach(x=>{tiles[x.id]._r=x.r.slice();place(tiles[x.id],x.r,true)}));
    Object.entries(BEATS[k].c).forEach(([id,key])=>{if(tiles[id]._key!==key)showContent(tiles[id],key,k,true)})}
  go(bi);
}
function setPlaying(p){playing=p;if(playing)go(cur);else clearTimeout(timer)}
function setTempo(t){TEMPO=t}
const totalSec=()=>Math.round(BEATS.reduce((s,b)=>s+durOf(b),0)/1000);
function start(){initTiles();resetToStart();setTimeout(()=>go(0),300)}

return {W,H,COLS,ROWS,STEP,C,BEATS,MOMENTS,SLOTS,tiles,hooks,start,go,next,jump,relayout,setPlaying,setTempo,setRange,durOf,totalSec,collapsed,
  get range(){return range},
  get cur(){return cur},get playing(){return playing},get beatStart(){return beatStart},get tempo(){return TEMPO}};
})();
