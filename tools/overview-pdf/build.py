import json, base64, os
from collections import Counter
SP='/tmp/claude-0/-home-claude/ab7b05ed-3efc-5836-bc78-61d94b36db0f/scratchpad'
moments=json.load(open(SP+'/kd/moments.json'))
names={1:"VW / Porsche Boxer-Urmotor",2:"VW 1 Millionster Volkswagen",3:"VW Bulli",4:"VW 1302 S Weltmeister",5:"VW Fusca 1300 Álcool",6:"VW Formel E",7:"VW T2 Elektrotransporter",8:"VW ID. Buzz mit BiDi-Laden",9:"VW XL1",10:"Audi A2 Karosserie",11:"VW Lupo 3L 1.2 TDI",12:"Porsche 909 Kugeltank",13:"Porsche Semper Vivus",14:"Porsche 919 Hybrid",15:"VW ID.R",16:"Audi RS Q e-tron",17:"VW Race Touareg TDI",18:"VW Stanley",19:"VW V10 TDI",20:"VW / Audi 1.9 TDI",21:"Audi Magnetic Ride",22:"Phaeton-Scharniere",23:"Golf IV Klarglasscheinwerfer",24:"Audi A8 Matrix LED",25:"Audi R8 LMX Laserlicht",26:"VW Digifiz",27:"VW Active Info Display",28:"AR-Head-up-Display",29:"Audi procon-ten",30:"VW ESVW 1",31:"Porsche PSCB",32:"Porsche Formel-E-Bremse",33:"Chiron 3D-Druck-Bremssattel",34:"Bugatti Chiron Rekord",35:"W16-Motor",36:"Bugatti Veyron",37:"Ehra-Lessien",38:"Nardò",39:"VW W12-Motor",40:"VW VR6-Motor",41:"Corrado Heckspoiler",42:"VW G60 G-Lader",43:"NSU-Wankelmotor",44:"Audi Fünfzylinder",45:"Audi Pikes Peak",46:"Audi RS7 piloted driving",47:"Porsche PDK",48:"Porsche 959",49:"Porsche Turbo-Twist-Felge",50:"Lamborghini Phone Dial",51:"VW Detroit-Felge",52:"Porsche 911",53:"VW Futura",54:"VW Chico",55:"VW NILS",56:"VW SEDRIC",57:"Audi AI:ME"}
chs=[(1,"Historie Aufstieg VW",1,4,"CDA220"),(2,"Sparsamkeit und alternative Antriebe",5,13,"518135"),(3,"Aus Hybriden wird Motorsport und Diesel",14,20,"9277E2"),(4,"Qualität, Licht und Digitale Technik",21,28,"3F9FD2"),(5,"Sicherheit und Bremsen",29,33,"2D559B"),(6,"Rekordfahrten, Motorenkonzepte und Motorsporttechnik für die Serie",34,48,"D32296"),(7,"Design",49,52,"D96534"),(8,"Auto von Morgen, Future Concepts",53,57,"732F00")]
def ch_of(n):
    for c in chs:
        if c[2]<=n<=c[3]: return c[0]
col={c[0]:c[4] for c in chs}
# classify
for m in moments:
    cnt=Counter(ch_of(n) for n in m['c']); m['cnt']=cnt
    tot=len(m['c'])
    if tot==0: m['fit']='ohne'
    else:
        top=max(cnt.values())/tot
        m['fit']='komplett' if top==1 else ('überwiegend' if top>=0.6 else 'verteilt')
print(Counter(m['fit'] for m in moments))
for m in moments: print(m['k'],m['m'],m['fit'],dict(m['cnt']))
origin={}
for m in moments:
    for n in m['c']: origin.setdefault(n,[]).append(f"{m['k']}·{m['m']}")
print('ohne Moment:',[n for n in range(1,58) if n not in origin])
json.dump({'fit':[m['fit'] for m in moments]},open('fit.json','w'))

FD='node_modules/@fontsource/'
def face(pkg,fam,w):
    p=f"{FD}{pkg}/files/{pkg}-latin-{w}-normal.woff2"
    b=base64.b64encode(open(p,'rb').read()).decode()
    p2=f"{FD}{pkg}/files/{pkg}-latin-ext-{w}-normal.woff2"
    b2=base64.b64encode(open(p2,'rb').read()).decode()
    return (f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}}"
            f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b2}) format('woff2');unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF;}}")
css_fonts=''.join(face('barlow','Barlow',w) for w in (400,500,600,700))+''.join(face('barlow-condensed','Barlow Condensed',w) for w in (500,600,700))

kt={1:"Antrieb & Energie",2:"Fahrdynamik & Sicherheit",3:"Digitalisierung & Zukunftstechnik",4:"Motorsport, Rekorde & Markengeschichte"}
fitlabel={'komplett':'passt komplett','überwiegend':'überwiegend','verteilt':'verteilt','ohne':'ohne Exponat'}
fitglyph={'komplett':'<i class="gl full"></i>','überwiegend':'<i class="gl half"></i>','verteilt':'<i class="gl ring"></i>','ohne':'<i class="gl none"></i>'}
def dark(hexc): return hexc in ('CDA220',)
def dot(n,c):
    d=3.3+0.55*(n-1)
    tc='#1a1a1a' if dark(col[c]) else '#fff'
    return f'<span class="dot" style="width:{d}mm;height:{d}mm;background:#{col[c]};color:{tc}">{n}</span>'
rows=''
cur=None
for i,m in enumerate(moments):
    if m['k']!=cur:
        cur=m['k']
        rows+=f'<tr class="grp"><td colspan="11"><b>Unser Kapitel {cur}</b> · {kt[cur]}</td></tr>'
    cells=''.join(f'<td class="c">{dot(m["cnt"][c],c) if m["cnt"].get(c) else ""}</td>' for c in range(1,9))
    outs=', '.join(o.replace('Lamborghini ','').replace('Bentley ','') for o in m['out'])
    note=f'<span class="out">Entfällt: {outs}</span>' if outs else ''
    rows+=(f'<tr class="mr {m["fit"]}"><td class="id">{m["k"]}·{m["m"]}</td><td class="t">{m["t"]}</td>{cells}'
           f'<td class="f">{fitglyph[m["fit"]]} {fitlabel[m["fit"]]}</td><td class="n">{note}</td></tr>')
heads=''.join(f'<th class="c"><span class="chn" style="background:#{c[4]};color:{"#1a1a1a" if dark(c[4]) else "#fff"}">{c[0]}</span></th>' for c in chs)

# page 2
cards=''
for c in chs:
    items=''
    for n in range(c[2],c[3]+1):
        o=' · '.join(origin.get(n,[]))
        items+=f'<li><span class="nr">{n:02d}</span><span class="nm">{names[n]}</span><span class="or">{o}</span></li>'
    cards+=(f'<section class="card" data-c="{c[0]}"><header><span class="chn big" style="background:#{c[4]};color:{"#1a1a1a" if dark(c[4]) else "#fff"}">{c[0]}</span>'
            f'<h3>{c[1]}</h3></header><ul>{items}</ul></section>')
outbox=f'<section class="outbox"><h4>Laut Kunde entfällt</h4><ul>'+''.join(f'<li>{o}</li>' for o in ["VW MQB","Terzo Millennio","Quattro","V12 TDI","Lamborghini Carbonteile","Aventador Pushrod-Fahrwerk","Bentley Stone Veneers","Chiron 3D-Druck-Bremse"])+'</ul></section>'
cards=cards.replace('</ul></section><section class="card" data-c="8">','</ul>'+outbox+'</section><section class="card" data-c="8">')
multi=sorted(n for n,v in origin.items() if len(v)>1)
print('mehrfach',[(n,origin[n]) for n in multi])

todo=[
("Skoda Eiskratzer fehlt","Das Exponat („simply clever“) steht weder in den 57 noch unter „Entfällt“. Raus oder bewusst vergessen?"),
("919 Rekuperator fehlt","Gleiches gilt für den Porsche 919 Rekuperator – weder nummeriert noch gestrichen."),
("MQB entfällt – bestätigen","Wir haben den Modularen Querbaukasten laut Kundenliste gestrichen. Bitte kurz bestätigen."),
("Chiron-Bremse doppelt?","Unter „Entfällt“ steht „Chiron 3D-Druck-Bremse“, in Kapitel 5 gleichzeitig Nr. 33 „Chiron 3D-Druck-Bremssattel“. Dublette oder zwei Objekte?"),
("Nr. 14: 919 Hybrid statt PCCB","Der Kunde nennt den Porsche 919 Hybrid, unser Datensatz heißt noch „Ceramic Coated Brakes“. Wir korrigieren Titel und Inhalt nach Bestätigung."),
("Nr. 46 RS7 in Kapitel 6","Piloted Driving steht bei „Rekordfahrten“, thematisch gehört es eher zu Kapitel 8 (Auto von Morgen). Absicht?"),
("120-Jahre-Volte getrennt","Semper Vivus (Nr. 13, Kap. 2) und 919 Hybrid (Nr. 14, Kap. 3) tragen bei uns gemeinsam einen Moment. In der neuen Abfolge liegen sie in zwei Kapiteln."),
("Zwei Momente ohne Exponat","„Der offene Ausblick“ (Terzo Millennio entfällt) und die Klammer in Kapitel 2 haben keine Objekte mehr. Streichen oder mit Text/Film tragen?"),
("Abfolge = Abspielreihenfolge?","Gilt die Nummerierung 01–57 als Reihenfolge im Film? Und gibt es einen Film pro Kapitel, oder läuft alles durch?"),
("Zwei Nummerierungen","Kundennummer 01–57 und unsere Graphic-ID 1–60 laufen parallel. Vorschlag: Kundennummer führend, Graphic-ID intern. Im Airtable stehen beide."),
("Objekte in mehreren Momenten",f"Bei uns kommen {len(multi)} Objekte in zwei Momenten vor (Nr. {', '.join(str(n) for n in multi)}). In der Kundenabfolge steht jedes nur einmal."),
]
checks=''.join(f'<li><span class="box"></span><div><b>{a}</b><p>{b}</p></div></li>' for a,b in todo)
half=(len(todo)+1)//2
c1=''.join(f'<li><span class="box"></span><div><b>{a}</b><p>{b}</p></div></li>' for a,b in todo[:half])
c2=''.join(f'<li><span class="box"></span><div><b>{a}</b><p>{b}</p></div></li>' for a,b in todo[half:])
outlist=["VW MQB","Terzo Millennio","Quattro","V12 TDI","Lamborghini Carbonteile","Aventador Pushrod-Fahrwerk","Bentley Stone Veneers","Chiron 3D-Druck-Bremse"]
outhtml=''.join(f'<li>{o}</li>' for o in outlist)

html=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
{css_fonts}
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Barlow',sans-serif;color:#1a1a1a;font-size:8pt;line-height:1.3}}
.pg{{width:297mm;height:210mm;padding:13mm 14mm 11mm 14mm;position:relative;page-break-after:always;overflow:hidden;display:grid;grid-template-columns:56mm 1fr;column-gap:10mm}}
.pg:last-child{{page-break-after:auto}}
.side h1{{font-family:'Barlow Condensed';font-weight:600;font-size:25pt;line-height:1.02;letter-spacing:-.2pt}}
.side .lead{{margin-top:4mm;font-size:8.5pt;color:#333}}
.kf{{margin-top:7mm}}
.kf div{{display:flex;align-items:baseline;gap:2.5mm;border-top:.3mm solid #1a1a1a;padding:1.6mm 0}}
.kf b{{font-family:'Barlow Condensed';font-weight:600;font-size:21pt;line-height:1;min-width:13mm}}
.kf span{{font-size:8pt;color:#333}}
.kf small{{display:block;font-size:6.8pt;color:#666}}
.foot{{position:absolute;left:14mm;bottom:8mm;font-size:6.5pt;color:#777;width:56mm}}
.main{{min-width:0}}
table{{border-collapse:collapse;width:100%;table-layout:fixed}}
th{{font-weight:500;font-size:6.8pt;color:#555;text-align:left;vertical-align:bottom;padding-bottom:1.4mm;border-bottom:.3mm solid #1a1a1a}}
td{{height:5.35mm;border-bottom:.15mm solid #ddd;vertical-align:middle}}
td.id{{font-family:'Barlow Condensed';font-weight:600;font-size:8pt;color:#666;width:9mm}}
td.t{{font-size:7.8pt;width:68mm;white-space:nowrap;padding-right:2mm}}
.c{{text-align:center;width:9.5mm}}
td.f{{font-size:7pt;width:24mm;color:#333;white-space:nowrap}}
td.n{{font-size:6.3pt;color:#8a2a2a;width:22mm;line-height:1.15;white-space:nowrap}}
.gl{{display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%;border:.3mm solid #1a1a1a;margin-right:1.4mm;vertical-align:-.3mm}}.gl.full{{background:#1a1a1a}}.gl.half{{background:linear-gradient(90deg,#1a1a1a 50%,#fff 50%)}}.gl.none{{border:none;background:none;height:.3mm;width:2.4mm;border-top:.3mm solid #999;vertical-align:.5mm}}
tr.grp td{{height:6.2mm;padding-top:1.8mm;font-size:7.6pt;border-bottom:.3mm solid #1a1a1a;color:#1a1a1a;vertical-align:bottom}}
tr.grp td b{{font-family:'Barlow Condensed';font-weight:600;font-size:9pt;letter-spacing:.2pt}}
tr.ohne td.t,tr.ohne td.id{{color:#999}}
.dot{{display:inline-flex;align-items:center;justify-content:center;border-radius:50%;font-weight:600;font-size:6.2pt;line-height:1}}
.chn{{display:inline-flex;align-items:center;justify-content:center;width:5.2mm;height:5.2mm;border-radius:50%;font-family:'Barlow Condensed';font-weight:700;font-size:9pt}}
.chn.big{{width:8mm;height:8mm;font-size:14pt;flex:none}}
.legend{{margin-top:2.6mm;font-size:6.8pt;color:#555;display:flex;gap:8mm}}.legend span+span .gl{{margin-left:2.5mm}}.legend span+span .gl:first-child{{margin-left:0}}
/* page 2 */
.grid{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:auto;gap:7mm 6mm;align-content:start}}
.card header{{display:flex;gap:2.4mm;align-items:center;border-bottom:.3mm solid #1a1a1a;padding-bottom:2mm;min-height:13mm}}
.card h3{{font-family:'Barlow Condensed';font-weight:600;font-size:10.5pt;line-height:1.05}}
.card ul{{list-style:none;margin-top:1.4mm}}
.card li{{display:grid;grid-template-columns:5mm 1fr auto;column-gap:1.6mm;padding:.95mm 0;border-bottom:.15mm solid #e2e2e2;font-size:7.4pt;line-height:1.2}}
.card .nr{{font-family:'Barlow Condensed';font-weight:600;color:#777}}
.card .or{{font-family:'Barlow Condensed';font-weight:500;font-size:6.8pt;color:#777;white-space:nowrap}}
.card.span2{{grid-column:span 1}}
.outbox{{margin-top:6mm}}
.outbox h4{{font-family:'Barlow Condensed';font-weight:600;font-size:10.5pt;border-bottom:.3mm solid #1a1a1a;padding-bottom:2mm;min-height:13mm;display:flex;align-items:center}}
.outbox ul{{list-style:none;margin-top:1.4mm}}
.card .outbox li{{display:block;grid-template-columns:none;padding:.95mm 0;border-bottom:.15mm solid #e2e2e2;font-size:7.4pt;color:#8a2a2a}}
/* page 3 */
.todo{{display:grid;grid-template-columns:1fr 1fr;column-gap:9mm}}
.todo ul{{list-style:none}}
.todo li{{display:flex;gap:3mm;padding:4.2mm 0;border-top:.15mm solid #cfcfcf}}
.todo li:first-child{{border-top:.3mm solid #1a1a1a}}
.box{{flex:none;width:3.6mm;height:3.6mm;border:.35mm solid #1a1a1a;margin-top:.6mm}}
.todo b{{font-weight:600;font-size:10pt}}
.todo p{{font-size:8.8pt;color:#333;margin-top:.8mm}}
</style></head><body>

<div class="pg">
 <div class="side">
  <h1>Kundenabfolge<br>vs. unsere Momente</h1>
  <p class="lead">Die meisten unserer 27 Momente überleben die neue Struktur. Wir müssen sie neu auf die acht Kundenkapitel verteilen, nicht neu erfinden.</p>
  <div class="kf">
   <div><b>57</b><span>Objekte in der Kundenliste</span></div>
   <div><b>8</b><span>Kundenkapitel statt 4 bei uns</span></div>
   <div><b>27</b><span>unsere Momente<small>17 passen komplett · 5 überwiegend · 3 verteilt · 2 ohne Exponat</small></span></div>
   <div><b>8</b><span>Objekte „Entfällt“</span></div>
   <div><b>2</b><span>Objekte fehlen in der Liste</span></div>
  </div>
 </div>
 <div class="main">
  <table>
   <colgroup><col style="width:9mm"><col style="width:68mm">{'<col style="width:9.5mm">'*8}<col style="width:24mm"><col style="width:22mm"></colgroup>
   <tr><th></th><th>Unser Moment</th>{heads}<th>Passung</th><th>Hinweis</th></tr>
   {rows}
  </table>
  <div class="legend"><span>Spalten = Kundenkapitel 1–8 · Zahl im Punkt = Anzahl Objekte des Moments in diesem Kapitel</span><span><i class="gl full"></i>alle in einem Kapitel <i class="gl half"></i>mind. 60 % <i class="gl ring"></i>verteilt</span></div>
 </div>
 <div class="foot">Blauer Kubus · FMW · Stand 29.10.2026 · Quelle: Kapitel_1-8_Abfolge.pptx</div>
</div>

<div class="pg">
 <div class="side">
  <h1>Die acht<br>Kundenkapitel</h1>
  <p class="lead">Objekte in Kundenreihenfolge. Rechts neben jedem Namen: in welchem unserer Momente (Kapitel·Moment) das Objekt heute vorkommt.</p>
  <div class="kf"><div><b>57</b><span>Objekte, alle in mindestens einem unserer Momente</span></div></div>
 </div>
 <div class="main">
  <div class="grid">
   {cards}
  </div>
 </div>
 <div class="foot">Blauer Kubus · FMW · Stand 29.10.2026</div>
</div>

<div class="pg">
 <div class="side">
  <h1>Offene<br>Punkte</h1>
  <p class="lead">Elf Dinge, die wir vor dem Umbau der Momentlisten mit dem Kunden klären sollten. Die ersten fünf blockieren konkrete Objekte.</p>
 </div>
 <div class="main todo">
  <ul>{c1}</ul>
  <ul>{c2}</ul>
 </div>
 <div class="foot">Blauer Kubus · FMW · Stand 29.10.2026</div>
</div>
</body></html>'''
open('overview.html','w').write(html)
