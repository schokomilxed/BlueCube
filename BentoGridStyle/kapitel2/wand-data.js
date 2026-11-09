/* Blauer Kubus · Wandabwicklung A · B · C – Snapshot aus Airtable (Base appd9oVo78FNTrPDd), Stand 15.10.2026
   Nur Exponate mit „Aktiv“. Raster: Modul 80 × 60 cm, 7 Reihen; Reihe 0 (oben) und 6 (unten) sind keine Fächer mehr.
   Fach-ID „W-S-N“: Wand, Spalte (Buchstabe), Reihe N von unten (1 = unten) – Anker = obere linke Ecke.
   Fußabdruck wie in kubus-live.html: größte zwei Maße (+ Luft, Standard 5 cm), gedreht = getauscht. */
(function(root){
const WALLS={A:{off:0,w:8},B:{off:8,w:21},C:{off:29,w:6}};
const COLS=35,ROWS=7,FIELD_ROWS=[1,5];          // Fächer nur in den Reihen 1–5
const MEDIA={c0:14,c1:20,y0:1,y1:5};             // Abzüge: Medienfläche B g6–m2
const DOOR={c0:26,c1:27,y0:3,y1:6};              // Abzüge: Fluchtwegtür B s4–t1

// [Name, Fach-ID, L, B, H (cm, geschätzt), gedreht, Luft, Cluster, StoryCluster, Jahr]
const EXPONATE=[
 ['VW G60 Schneckenkompressor Corrado','A-F-2',30,25,28,0,5,'Corrado-Technik','3',1986],
 ['VW T2 Elektro Transporter','B-C-4',35,20,20,0,5,'Bulli-Elektro','1',1979],
 ['Porsche 919 Hybrid Rennwagen','B-U-4',40,40,5,1,5,'Porsche Hybrid','14',2019],
 ['Audi AI:ME Modell','B-F-5',43,19,15,0,5,'Autonomes Fahren','3',2019],
 ['Audi A8 Matrix LED Scheinwerfer','B-S-6',40,45,25,0,5,'Lichttechnik','3',2013],
 ['VW Sedric Modell','B-E-6',65,30,35,0,5,'Autonomes Fahren','3',2016],
 ['Bugatti Veyron Rekord','C-E-4',150,35,25,1,5,'Rekordfahrten','4',2005],
 ['VW Nils concept Modell','B-B-6',32,14,12,0,5,'Konzeptstudien','3',2011],
 ['Audi 5 Zylinder Turbo Motor','B-P-3',70,85,75,0,5,'Rallye & Bergrennen','41',1985],
 ['Audi Procon-Ten Sicherheitssystem','C-C-5',110,45,45,1,5,'Sicherheit','2',1985],
 ['VW Augmented Reality Head Up Display','B-U-5',25,22,12,0,5,'Digitalcockpit','3',2020],
 ['Audi Pikes Peak Rennwagen','B-Q-4',42,18,12,1,5,'Rallye & Bergrennen','4',1987],
 ['Porsche 909 Kugeltank','B-R-5',35,35,45,0,5,'Rallye & Bergrennen','4',1970],
 ['VW Active Info Display','B-U-6',20,40,25,1,5,'Digitalcockpit','3',2012],
 ['VW W12 Motor','B-E-3',65,70,75,0,20,'Motoren – VR/W','1',2002],
 ['VW / Porsche Boxer Ur-Motor','B-A-5',50,90,60,1,5,'Motoren – Boxer/911','1',1938],
 ['VW Race Touareg Rallye Dakar','C-F-5',35,35,12,0,5,'Rallye & Bergrennen','41',2005],
 ['1.9 TDI','C-C-3',50,60,70,1,5,'Motoren – TDI','1',1998],
 ['Audi LMX Laser Scheinwerfer','B-R-6',40,45,25,0,5,'Lichttechnik','3',2014],
 ['VW ESVW 1 experimental Safety Vehicle US','A-G-6',47,18,14,0,5,'Sicherheit','2',1972],
 ['Porsche Felge Turbo Twist','A-D-2',46,46,30,0,5,'Felgen','2',1995],
 ['Lamborghini Felge „Phone Dial“ Pair','A-A-2',44,80,44,0,5,'Felgen','2',1985],
 ['Skoda Simply Clever Eiskratzer Türkantenschutz','A-E-2',15,8,3,0,5,'Skoda Simply Clever','',2025],
 ['VW 1 Millionster Volkswagen','C-B-6',10,145,24,0,5,'Wirtschaftswunder','4',1955],
 ['VW Testgelände Ehra-Lessien','C-F-4',160,50,5,1,5,'Rekordfahrten','4',1969],
 ['VW Stanley','B-F-4',20,16,16,0,5,'Autonomes Fahren','34',2005],
 ['Audi RS-Q e-tron Rallyefahrzeug','B-Q-5',45,23,20,0,5,'Rallye & Bergrennen','4',2024],
 ['VW Phaeton (Kofferraum Scharniere)','C-B-4',70,45,35,0,5,'Luxus/Verarbeitung','4',2001],
 ['VW VR6 Motor','B-A-3',52,42,68,0,15,'Motoren – VR/W','1',1985],
 ['VW ID.R Pikes Peak','B-R-3',35,20,12,0,5,'Rallye & Bergrennen','4',2018],
 ['Porsche Semper Vivus mit Radnabenmotoren','B-U-3',35,35,25,0,5,'Porsche Hybrid','14',1900],
 ['VW Corrado Heckspoiler','A-H-4',20,90,15,1,5,'Corrado-Technik','3',1995],
 ['VW W16 Motor','B-C-3',100,80,80,0,5,'Motoren – VR/W','1',2005],
 ['VW Fusca 1300 Álcool Brasilien','C-F-6',41,16,15,0,5,'Antriebstechnik – Sonderbauformen','14',1977],
 ['Porsche 959','B-R-2',28,45,45,0,5,'Rallye & Bergrennen','4',1986],
 ['VW W12 Nardo','C-E-5',44,19,11,0,5,'Rekordfahrten','4',1997],
 ['VW V10 TDI Motor','C-A-3',100,90,90,0,5,'Motoren – TDI','1',2003],
 ['Audi Magnetic Ride (TT)','B-E-5',20,20,60,1,5,'Fahrwerk','2',2007],
 ['VW Futura Modell','B-D-6',43,18,15,0,5,'Konzeptstudien','3',1989],
 ['VW Chicco Concept','B-C-6',31,16,15,1,5,'Konzeptstudien','3',1982],
 ['Audi NSU Wankelmotor','A-G-4',30,11,37,0,5,'Antriebstechnik – Sonderbauformen','1',1969],
 ['VW Digifiz','B-T-6',30,12,9,0,5,'Digitalcockpit','3',1980],
 ['Porsche PDK Getriebe','A-G-3',45,121,55,1,5,'Antriebstechnik – Sonderbauformen','1',1988],
 ['Bidi Laden ID.Buzz','B-B-4',50,50,50,1,5,'Bulli-Elektro','1',2022],
 ['VW Bulli','C-D-6',42,17,19,0,5,'Wirtschaftswunder','4',1955],
 ['VW Formel E Spritsparmodelle','B-P-6',45,35,25,1,5,'Effizienz','1',1980],
 ['Porsche PSCB Surface Coated Brakes','C-A-6',41,41,11,1,5,'Bremsen','2',2017],
 ['VW Golf 4 Klarglasscheinwerfer','B-Q-6',25,50,30,0,5,'Lichttechnik','3',1997],
 ['Audi RS7 Piloted Driving','B-F-6',60,24,18,0,5,'Autonomes Fahren','3',2016],
 ['VW Lupo 3L – Motor 1.2 TDI','B-P-5',60,45,55,0,10,'Effizienz','1',1999],
 ['Bugatti Chiron 3D gedruckte Bremse','C-A-5',15,45,50,1,5,'Bremsen','24',2018],
 ['Audi A2 Karosse','A-A-6',430,167,155,0,25,'Leichtbau','2',1999],
 ['Porsche 919 Hybrid Rekuperator','B-U-2',20,45,25,1,5,'Porsche Hybrid','14',2019],
 ['VW 1972 Weltrekordkäfer','C-E-6',41,15,15,0,5,'Wirtschaftswunder','4',1972],
 ['VW XL1 Monocoque','B-N-6',185,150,118,1,5,'Effizienz','1',2013],
 ['VW Detroit Felge','A-C-2',46,20,46,0,5,'Felgen','2',2004],
 ['Porsche Bremse Formel E Rennwagen','C-A-4',10,29,33,0,5,'Bremsen','2',2025],
 ['Porsche 911 Windkanalmodell','B-B-5',96,38,24,0,5,'Motoren – Boxer/911','12',1963],
 ['Bugatti Chiron Rekord','C-D-4',140,35,25,1,5,'Rekordfahrten','42',2019],
];
const CLCOL={"Motoren – VR/W":"#6f93e6","Motoren – TDI":"#5fa6e6","Motoren – Boxer/911":"#45c2d4","Porsche Hybrid":"#22b0a0",
"Corrado-Technik":"#6fbf5b","Lichttechnik":"#e6bf46","Digitalcockpit":"#e8cf5c","Bremsen":"#ee9440","Fahrwerk":"#f0a960",
"Leichtbau":"#808d99","Effizienz":"#8ed06f","Rekordfahrten":"#e94b3c","Autonomes Fahren":"#9d6fd0","Felgen":"#9aa6b2",
"Wirtschaftswunder":"#f2872e","Sicherheit":"#d76b6b","Rallye & Bergrennen":"#ec86b6","Bulli-Elektro":"#58c6d6",
"Konzeptstudien":"#b98fd9","Luxus/Verarbeitung":"#e9a6cb","Skoda Simply Clever":"#5fa6e6","Antriebstechnik – Sonderbauformen":"#5fa6e6"};

function fach(id){const m=id.match(/^([A-C])-([A-Z])-(\d)$/);const w=WALLS[m[1]];return{wall:m[1],col:w.off+m[2].charCodeAt(0)-65,row:ROWS-parseInt(m[3],10)}}
function foot(L,B,H,rot,air){const ds=[L,B,H].filter(d=>d>0).sort((a,b)=>b-a);const d0=ds[0],d1=ds[1]||ds[0];
  const wcm=(rot?d1:d0)+air,hcm=(rot?d0:d1)+air;return[Math.max(1,Math.ceil(wcm/80)),Math.max(1,Math.ceil(hcm/60))]}

/* place every exhibit: anchor at its Fach, spread over its footprint inside its wall and inside the field rows,
   never over media, door or another exhibit (largest first, like kubus-live) */
function layout(){
  const blocked=[...Array(ROWS)].map((_,y)=>[...Array(COLS)].map((_,x)=>
    y<FIELD_ROWS[0]||y>FIELD_ROWS[1]||(x>=MEDIA.c0&&x<=MEDIA.c1&&y>=MEDIA.y0&&y<=MEDIA.y1)||(x>=DOOR.c0&&x<=DOOR.c1&&y>=DOOR.y0&&y<=DOOR.y1)));
  const owner=blocked.map(r=>r.map(()=>-1));
  const objs=EXPONATE.map(([name,id,L,B,H,rot,air,cluster,story,year],i)=>{const f=fach(id);const [cols,rows]=foot(L,B,H,rot,air);
    return{i,name,id,wall:f.wall,col:f.col,row:f.row,cols,rows,cluster,color:CLCOL[cluster]||'#9aa6b2',story,year,cells:[]}});
  const warn=[];
  [...objs].sort((a,b)=>b.cols*b.rows-a.cols*a.rows).forEach(o=>{
    const w=WALLS[o.wall],wl=w.off,wr=w.off+w.w-1;
    for(let y=o.row;y<Math.min(o.row+o.rows,FIELD_ROWS[1]+1);y++)for(let x=o.col;x<=Math.min(o.col+o.cols-1,wr);x++)
      if(!blocked[y][x]&&owner[y][x]<0){owner[y][x]=o.i;o.cells.push([x,y])}
    if(!o.cells.length){warn.push(o.id+' '+o.name+': Fach belegt');if(!blocked[o.row][o.col]){o.cells.push([o.col,o.row])}}
  });
  objs.forEach(o=>{const xs=o.cells.map(c=>c[0]),ys=o.cells.map(c=>c[1]);
    o.rect=o.cells.length?{x:Math.min(...xs),y:Math.min(...ys),w:Math.max(...xs)-Math.min(...xs)+1,h:Math.max(...ys)-Math.min(...ys)+1}:null});
  return{objs,warn,owner,blocked};
}
const api={WALLS,COLS,ROWS,FIELD_ROWS,MEDIA,DOOR,EXPONATE,CLCOL,fach,layout};
if(typeof module!=='undefined')module.exports=api;else root.WAND=api;
})(this);
