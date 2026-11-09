/* Kapitel 2 – Fahrdynamik & Sicherheit · Grid-Choreografie
   Medienfläche: 7 × 5 Zellen à 80 × 60 cm (560 × 300 cm). Rects sind [x0,y0,x1,y1] in Zellen.
   x0==x1 oder y0==y1 = eingeklappt an einer Kante (unsichtbar).

   Jeder Beat besteht aus Schritten. In einem Schritt bewegt sich jede Kachel nur auf EINER Achse.
   Namen P1–P8 meinen die Positionen des Grundrasters; alle anderen Namen sind Kacheln, die in
   diesem Moment neu hereingeschoben werden ({r, f}: f = Startkante, an der sie eingeklappt warten). */
(function(root){
const COLS=7,ROWS=5,SLOTS=18;
const P={P1:[0,0,2,3],P2:[2,0,5,2],P3:[5,0,7,3],P4:[2,2,3,3],P5:[3,2,5,3],P6:[0,3,3,5],P7:[3,3,4,5],P8:[4,3,7,5]};
// Grundraster: stille Silhouetten nur aktiver Kapitel-2-Exponate (gleiche Belegung bei jeder Rückfaltung)
const SIL={P1:'s:a2',P2:'s:mr',P3:'s:pd',P4:'s:det',P5:'s:tt',P6:'s:pscb',P7:'s:bremse',P8:'s:procon'};
// silhouettes keyed by the logical names a fold ends with: [P1,P2,P3,P4,P5,P6,P7,P8]
const sil=(...n)=>Object.fromEntries(n.map((k,i)=>[k,Object.values(SIL)[i]]));
const e=(r,f)=>({r,f});

const MOMENTS=['Grundraster','M1 · Leichtbau als erste Antwort','M2 · Der Kontaktpunkt zur Straße','M3 · Kraft kontrollierbar machen','M4 · Die Bremse wird Hightech','M5 · Sicherheit von Grund auf','M6 · Rückkehr zur Ausgangsfrage'];

/* folding back to the base grid from the two most common end states */
const foldFromLeftBlock=(L,R1,R2)=>[ // L = big block [0,0,4,5]; R1/R2 = right column halves
  {[L]:[0,0,4,3],z1:e([0,3,4,5],[0,5,4,5])},
  {[L]:[0,0,2,3],[R1]:[2,0,5,3],z2:e([5,0,7,3],[7,0,7,3]),z1:[0,3,3,5],z3:e([3,3,4,5],[4,3,4,5])},
  {[R1]:[2,0,5,2],z4:e([2,2,3,3],[2,3,3,3]),z5:e([3,2,5,3],[3,3,5,3])},
];

const BEATS=[
 {m:0,rebind:true,t:'Grundraster – stille Silhouetten',reg:'ambient',spot:'ruht',hold:3,steps:[],c:{...SIL}},
 {m:0,t:'Kapitel-Titel',reg:'Erzählerin',spot:'ruht',steps:[
   {P1:[0,0,5,3],P2:[5,0,5,2],P4:[5,2,5,3],P5:[5,2,5,3]}],c:{P1:'title'}},

 // M1 Leichtbau
 {m:1,t:'Kachel öffnet sich: Audi A2 Karosse',reg:'Ich-Form',spot:'A-A-6 (Audi A2)',steps:[
   {P1:[0,0,4,3],P3:[4,0,7,3]},
   {P1:[0,0,4,5],P6:[0,5,3,5],P7:[3,5,4,5],P3:[4,0,7,2],P8:[4,2,7,5]}],
   c:{P1:'a2',P3:'a2lab',P8:'a2q'}},
 {m:1,t:'Grid faltet sich zurück',reg:'ambient',spot:'ruht',hold:2.5,steps:[
   {P1:[0,0,4,3],z1:e([0,3,4,5],[0,5,4,5]),P3:[4,0,7,3],P8:[4,3,7,5]},
   {P1:[0,0,2,3],P3:[2,0,5,3],z2:e([5,0,7,3],[7,0,7,3]),z1:[0,3,3,5],z3:e([3,3,4,5],[4,3,4,5])},
   {P3:[2,0,5,2],z4:e([2,2,3,3],[2,3,3,3]),z5:e([3,2,5,3],[3,3,5,3])}],
   c:sil('P1','P3','z2','z4','z5','z1','z3','P8')},

 // M2 Kontaktpunkt
 {m:2,rebind:true,t:'Kachel öffnet sich: VW Detroit Felge',reg:'Ich-Form',spot:'A-C-2 (Detroit)',steps:[
   {P1:[0,0,4,3],P2:[4,0,4,2],P4:[4,2,4,3],P5:[4,2,4,3],P3:[4,0,7,3],P6:[0,3,5,5],P7:[5,3,5,5],P8:[5,3,7,5]}],
   c:{P1:'det',P3:'detq',P6:'detlab',P8:'tt'}},
 {m:2,t:'Zweite Kachel daneben: Porsche Turbo Twist',reg:'Ich-Form',spot:'A-D-2 (Turbo Twist)',steps:[
   {P6:[0,3,4,5],P8:[4,3,7,5]},
   {P8:[4,0,7,5],P3:[4,0,7,0]}],c:{P6:'ttq'}},
 {m:2,t:'Dritte Kachel, Vollbild: Lamborghini Phone Dial',reg:'Bild',spot:'A-A-2 (Phone Dial)',hold:4,steps:[
   {P8:[0,0,7,5],P1:[0,0,0,3],P6:[0,3,0,5]}],c:{P8:'pd'}},
 {m:2,t:'Phone Dial spricht · Erzählerin schließt',reg:'Ich-Form + Erzählerin',spot:'A-A-2 (Phone Dial)',steps:[
   {P8:[0,0,4,5],q:e([4,0,7,3],[7,0,7,3]),n:e([4,3,7,5],[7,3,7,5])}],c:{q:'pdq',n:'n2'}},
 {m:2,t:'Grid faltet sich zurück',reg:'ambient',spot:'ruht',hold:2.5,steps:foldFromLeftBlock('P8','q','n'),
   c:sil('P8','q','z2','z4','z5','z1','z3','n')},

 // M3 Kraft kontrollierbar machen
 {m:3,rebind:true,t:'Kachel öffnet sich: Audi Magnetic Ride',reg:'Ich-Form',spot:'B-E-5 (Magnetic Ride)',steps:[
   {P1:[0,0,5,3],P2:[5,0,5,2],P4:[5,2,5,3],P5:[5,2,5,3],P6:[0,3,4,5],P7:[4,3,4,5]}],
   c:{P1:'mrvid',P3:'mrq',P6:'mrimg',P8:'mrf'}},
 {m:3,t:'Zweite Kachel: Porsche 911 Windkanalmodell',reg:'Ich-Form · Rückverweis Kap. 1',spot:'B-B-5 (911) · Lichtbrücke → B-A-5 (Boxer Ur-Motor, Kap. 1) und zurück',
   warn:'Kein Bild des Modells im Footage – Strömungsgrafik als Platzhalter',bridge:{from:'B-B-5',to:'B-A-5'},steps:[
   {P1:[0,0,2,3],w1:e([2,0,5,3],[5,0,5,3]),w2:e([0,3,5,5],[0,3,0,5]),P6:[5,3,5,5],P8:[5,3,7,5]}],
   c:{w1:'airf',P3:'airq',w2:'air',P8:'n3'}},
 {m:3,t:'Grid faltet sich zurück',reg:'ambient',spot:'ruht',hold:2.5,steps:[
   {w2:[0,3,3,5],v3:e([3,3,4,5],[5,3,5,5]),P8:[4,3,7,5]},
   {w1:[2,0,5,2],v1:e([2,2,3,3],[2,3,3,3]),v2:e([3,2,5,3],[3,3,5,3])}],
   c:sil('P1','w1','P3','v1','v2','w2','v3','P8')},

 // M4 Bremse
 {m:4,rebind:true,t:'Kachel öffnet sich: Porsche PSCB',reg:'Ich-Form',spot:'C-A-6 (PSCB)',steps:[
   {P1:[0,0,4,3],P2:[4,0,4,2],P4:[4,2,4,3],P5:[4,2,4,3],P3:[4,0,7,3],P6:[0,3,4,5],P7:[4,3,4,5]},
   {P1:[0,0,4,5],P6:[0,5,4,5]}],c:{P1:'pscb',P3:'pscbq',P8:'pscbf'}},
 {m:4,t:'Kontrast: Porsche Formel-E-Bremse',reg:'Ich-Form + Erzählerin',spot:'C-A-4 (Formel E)',
   warn:'Kein Bild der Formel-E-Bremse – Größenvergleich als Grafik',steps:[
   {P1:[0,0,2,5],u:e([2,0,4,5],[4,0,4,5])}],c:{u:'discs',P3:'feq',P8:'n4'}},
 {m:4,t:'Vorverweis: Bugatti Chiron Rekord',reg:'Fakt + Erzählerin',spot:'C-D-4 (Chiron Heckspoiler)',steps:[
   {P1:[0,0,4,5],u:[4,0,4,5]}],c:{P1:'chpass',P3:'f490',P8:'n5'}},
 {m:4,t:'Vierte Kachel, Vollbild: Bugatti 3D-Bremse',reg:'Bild',spot:'C-A-5 (Bremse)',hold:4,steps:[
   {P1:[0,0,7,5],P3:[7,0,7,3],P8:[7,3,7,5]}],c:{P1:'bremse'}},
 {m:4,t:'Bremse · Steckbrief',reg:'Ich-Form',spot:'C-A-5 (Bremse)',steps:[
   {P1:[2,0,7,5],s1:e([0,0,2,2],[0,0,0,2]),s2:e([0,2,2,5],[0,2,0,5])},
   {P1:[2,0,7,3],s3:e([2,3,4,5],[2,5,4,5]),s4:e([4,3,7,5],[4,5,7,5])}],
   c:{P1:'bdet',s1:'btitle',s2:'bq',s3:'b29',s4:'b2213'}},
 {m:4,t:'Bremse · Konflikt',reg:'Erzählerin',spot:'C-A-5 (Bremse)',steps:[
   {s1:[0,0,2,3],s2:[0,3,2,5]},
   {s1:[0,0,5,3],P1:[5,0,7,3],s2:[0,3,7,5],s3:[7,3,7,5],s4:[7,3,7,5]}],
   c:{s1:'n490',P1:'bk',s2:'fire'}},
 {m:4,t:'Bremse · Beziehung – Vorverweis Kapitel 4',reg:'Ich-Form',spot:'C-A-5 → Lichtbrücke C-D-4 (Chiron Rekord, Kap. 4) und zurück',bridge:{from:'C-A-5',to:'C-D-4'},steps:[
   {s1:[0,0,4,3],P1:[4,0,7,3],s2:[0,3,3,5],r1:e([3,3,5,5],[7,3,7,5]),r2:e([5,3,7,5],[7,3,7,5])}],
   c:{s1:'chrear',P1:'bvon',s2:'bz1',r1:'bz2',r2:'rad'}},
 {m:4,t:'Grid faltet sich zurück',reg:'ambient',spot:'ruht',hold:2.5,steps:[
   {s1:[0,0,2,3],P1:[2,0,5,3],q2:e([5,0,7,3],[7,0,7,3]),r1:[3,3,4,5],r2:[4,3,7,5]},
   {P1:[2,0,5,2],q3:e([2,2,3,3],[2,3,3,3]),q4:e([3,2,5,3],[3,3,5,3])}],
   c:sil('s1','P1','q2','q3','q4','s2','r1','r2')},

 // M5 Sicherheit
 {m:5,rebind:true,t:'Kachel öffnet sich: Audi Procon-Ten',reg:'Ich-Form',spot:'C-C-5 (Procon-Ten)',steps:[
   {P1:[0,0,4,3],P2:[4,0,4,2],P4:[4,2,4,3],P5:[4,2,4,3],P3:[4,0,7,3],P6:[0,3,4,5],P7:[4,3,4,5]}],
   c:{P1:'pccrash',P3:'pcq',P6:'pcmech',P8:'pcf'}},
 {m:5,t:'Zweite Kachel, Vollbild: VW ESVW 1',reg:'Ich-Form',spot:'A-G-6 (ESVW 1)',warn:'Kein ESVW-Bild im Footage – typografisch gesetzt',steps:[
   {P8:[0,3,7,5],P6:[0,3,0,5]},
   {P8:[0,0,7,5],P1:[0,0,4,0],P3:[4,0,7,0]}],c:{P8:'esvw'}},
 {m:5,t:'Fusion: Erzählerin schlägt Brücke zu Kapitel 1',reg:'Erzählerin',spot:'C-C-5 + A-G-6',steps:[
   {P8:[0,0,4,5],nb:e([4,0,7,5],[7,0,7,5])}],c:{nb:'n6'}},
 {m:5,t:'Grid faltet sich zurück',reg:'ambient',spot:'ruht',hold:2.5,steps:[
   {P8:[0,0,4,3],nb:[4,0,7,3],m1:e([0,3,4,5],[0,5,4,5]),m2:e([4,3,7,5],[4,5,7,5])},
   {P8:[0,0,2,3],m3:e([2,0,5,3],[4,0,4,3]),nb:[5,0,7,3],m1:[0,3,3,5],m4:e([3,3,4,5],[4,3,4,5])},
   {m3:[2,0,5,2],m5:e([2,2,3,3],[2,3,3,3]),m6:e([3,2,5,3],[3,3,5,3])}],
   c:sil('P8','m3','nb','m5','m6','m1','m4','m2')},

 // M6 Klammer
 {m:6,rebind:true,t:'Fünf Antworten',reg:'Erzählerin',spot:'alle Kapitel-2-Fächer nacheinander',steps:[],
   c:{P1:'kq',P2:'k1',P3:'k2',P4:'s:det',P5:'k3',P6:'k4',P7:'s:tt',P8:'k5'}},
 {m:6,t:'Vollbild: Erzählerin schließt',reg:'Erzählerin',spot:'Raum gesamt',steps:[
   {P1:[0,0,7,3],P2:[7,0,7,2],P4:[7,2,7,3],P5:[7,2,7,3],P3:[7,0,7,3]},
   {P1:[0,0,7,5],P6:[0,5,3,5],P7:[3,5,4,5],P8:[4,5,7,5]}],c:{P1:'n7'}},
 {m:6,t:'Rückkehr zum Grundraster – Cluster-Ende',reg:'ambient',spot:'ruht',hold:3,steps:[
   {P1:[0,0,7,3],l1:e([0,3,3,5],[0,5,3,5]),l2:e([3,3,4,5],[3,5,4,5]),l3:e([4,3,7,5],[4,5,7,5])},
   {P1:[0,0,2,3],l4:e([2,0,5,3],[7,0,7,3]),l5:e([5,0,7,3],[7,0,7,3])},
   {l4:[2,0,5,2],l6:e([2,2,3,3],[2,3,3,3]),l7:e([3,2,5,3],[3,3,5,3])}],
   c:sil('P1','l4','l5','l6','l7','l1','l2','l3')},
];

/* resolve logical names to physical tiles */
const collapsed=r=>r[0]===r[2]||r[1]===r[3];
function build(){
  const order=Object.keys(P);
  const pos=[...Array(SLOTS)].map((_,i)=>i<8?P[order[i]].slice():[COLS,ROWS,COLS,ROWS]);
  let bind={};
  return BEATS.map((b,bi)=>{
    if(b.rebind){bind={};for(const k of order){const i=pos.findIndex(r=>r.join()===P[k].join());if(i<0)throw Error(`Beat ${bi}: base position ${k} not occupied`);bind[k]=i}}
    const get=name=>{if(!(name in bind)){const used=new Set(Object.values(bind));const i=pos.findIndex((r,i)=>collapsed(r)&&!used.has(i));if(i<0)throw Error(`Beat ${bi}: no free tile for ${name}`);bind[name]=i}return bind[name]};
    const steps=b.steps.map(st=>Object.entries(st).map(([name,v])=>({id:get(name),name,r:(Array.isArray(v)?v:v.r).slice(),f:Array.isArray(v)?null:v.f})));
    steps.forEach(st=>st.forEach(x=>{pos[x.id]=x.r.slice()}));
    const c={};for(const [name,key] of Object.entries(b.c||{}))c[get(name)]=key;
    return {...b,steps,c};
  });
}
const api={COLS,ROWS,SLOTS,P,MOMENTS,BEATS:build(),collapsed};
if(typeof module!=='undefined')module.exports=api;else root.CHOREO=api;
})(this);
