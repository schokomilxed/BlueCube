import json, math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table
d=json.load(open('sampled.json')); film=json.load(open('film_data.json'))
cues=json.load(open('cues.json')); L=d['LOG']; t0=L['t0']; EX=d['EXinfo']; W=d['wand']
MO=dict(x=W['MEDIA']['c0'],y=W['MEDIA']['y0'],w=W['MEDIA']['c1']-W['MEDIA']['c0']+1,h=W['MEDIA']['y1']-W['MEDIA']['y0']+1)
beats=[((b['t']-t0)/1000,b['bi']) for b in L['beats']]
BT={b['i']:b['t'] for b in film['beats']}
def beat_at(t):
    cur=0
    for bt,bi in beats:
        if bt<=t+0.05: cur=bi
    return cur
FONT='Arial'
f=lambda **k:Font(name=FONT,size=k.pop('size',10),**k)
hdr_fill=PatternFill('solid',fgColor='1A1A1A'); hdr_font=f(bold=True,color='FFFFFF')
inp_fill=PatternFill('solid',fgColor='FFF2CC'); grp_fill=PatternFill('solid',fgColor='EDEDED')
thin=Side(style='thin',color='D0D0D0'); bd=Border(bottom=thin)
wb=Workbook()

# ---------- Hinweise (Parameter) – zuerst anlegen, damit Formeln darauf zeigen ----------
H=wb.active; H.title='Hinweise'
# ---------- Cueliste ----------
C=wb.create_sheet('Cueliste',0)
C['A1']='Blauer Kubus · Wand-Licht-Cueliste · Film 00:00–01:00 (Kapitelstart, Beat 0–5)'; C['A1'].font=f(bold=True,size=14)
C['A2']='Quelle: HTML-Mockup „BlauerKubus_Kapitel2_Wand_1.html“, Licht = Film (Fach-Helligkeit pro Fach-ID). Zeit 0 = Start des ersten Beats. Grau hinterlegt = neue Cue-Gruppe. Parameter und Annahmen: Blatt „Hinweise“.'
C['A2'].font=f(italic=True,color='555555',size=9)
heads=['Cue','Zeit (s)','Zeit mm:ss.s','Beat','Beat-Titel','Fach-ID','Exponat','Aktion','Von %','Auf %','Dauer im Mockup (s)','Fade (s)','Auf DMX 8-bit','Typ','Hinweis']
R0=4
for i,h in enumerate(heads,1):
    c=C.cell(R0,i,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
C.row_dimensions[R0].height=30
# group cue numbers by time
groups=[];
for c in cues:
    if groups and abs(c['t']-groups[-1][0])<0.16: groups[-1][1].append(c)
    else: groups.append([c['t'],[c]])
routes=[r for r in L['routes'] if r['will'] and 0<=(r['t']-t0)/1000<=60]
def route_note(fid,t):
    for r in routes:
        rt=(r['t']-t0)/1000
        if r['id']==fid and -0.1<=t-rt<=1.5: return f'Weg-Welle ab {rt:.1f} s (Blatt „Wege“); Fach geht erst bei Ankunft an'
    return ''
row=R0+1; gi=0
for gt,items in groups:
    gi+=1
    for c in items:
        fid=c['fid']; bi=beat_at(c['t'])
        up=c['to']>c['frm']
        if c['to']<0.02: act='Aus'
        elif c['to']>0.25 and up: act='Highlight an'
        elif up: act='Grundlicht auf'
        else: act='Absenken'
        typ='Highlight' if max(c['to'],c['frm'])>0.25 else 'Grundlicht'
        vals=[gi,c['t'],None,bi,film['beats'][bi]['t'],fid,EX[fid]['name'],act,c['frm'],c['to'],c['dur'],None,None,typ,route_note(fid,c['t'])]
        for j,v in enumerate(vals,1): C.cell(row,j,v).font=f()
        C.cell(row,3,f'=TEXT(B{row}/86400,"mm:ss.0")')
        C.cell(row,12,f'=IF(K{row}<0.2,IF(J{row}>I{row},Hinweise!$B$12,Hinweise!$B$13),K{row})')
        C.cell(row,13,f'=ROUND(J{row}*255,0)')
        for j in (9,10): C.cell(row,j).number_format='0%'
        for j in (2,11,12): C.cell(row,j).number_format='0.00'
        for j in range(1,16):
            C.cell(row,j).border=bd
            if items[0] is c: C.cell(row,j).fill=grp_fill
        for j in (3,4,6,8,14): C.cell(row,j).alignment=Alignment(horizontal='center')
        row+=1
last=row-1
for col,w in zip('ABCDEFGHIJKLMNO',[6,9,13,6,44,9,40,15,8,8,12,9,11,12,66]): C.column_dimensions[col].width=w
C.freeze_panes=C.cell(R0+1,1)
C.auto_filter.ref=f'A{R0}:O{last}'
C.cell(last+2,1,'DMX-Spalte = linear Auf % × 255, ohne Dimmkurve und ohne Max-Level-Begrenzung pro Exponat (siehe Hinweise).').font=f(italic=True,size=9,color='555555')

# ---------- Wellen ----------
Wv=wb.create_sheet('Wellen',1)
Wv['A1']='Bewegungslicht: Wellen, die von der Medienfläche in die Nachbarfächer laufen'; Wv['A1'].font=f(bold=True,size=14)
Wv['A2']='Jede Kachelbewegung erzeugt ein Wellenfeld (Zellen 80 × 60 cm, volle Flächen, keine Glows). Für die Anlage empfohlen: als Pixel-Video ausspielen, nicht als Cueliste. Diese Liste zeigt, wann welche Welle wohin läuft.'
Wv['A2'].font=f(italic=True,size=9,color='555555')
wh=['Nr','Zeit (s)','Zeit mm:ss.s','Beat','Kachel','Kante','Bewegung (Medien-Zellen)','Seite der Welle','Wandspalten','Wandreihen','Dauer (s)','Reichweite (Spalten)']
for i,h in enumerate(wh,1):
    c=Wv.cell(4,i,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
Wv.row_dimensions[4].height=30
def collapsed(r): return (r[2]-r[0])<=0 or (r[3]-r[1])<=0
r_=5; n=0; seen_keys=set()
for st in L['steps']:
    ts=(st['t']-t0)/1000
    if ts>60: continue
    bi=beat_at(ts)
    names={x['id']:x['name'] for s in film['beats'][bi]['steps'] for x in s}
    seen=set()
    for mv in st['moves']:
        fr,to=mv['from'],mv['to']
        if collapsed(fr) and collapsed(to): continue
        for axis,i0,i1,p0,p1 in (('x',0,2,1,3),('y',1,3,0,2)):
            for i in (i0,i1):
                if fr[i]==to[i]: continue
                a,b=fr[i],to[i]; span=(fr[p0],fr[p1])
                if span[1]-span[0]<=0: continue
                key=(axis,a,b,span)
                if key in seen: continue
                seen.add(key)
                n+=1
                dist=abs(b-a); dr=1 if b>a else -1
                if axis=='x':
                    side='rechts der Medienfläche' if dr>0 else 'links der Medienfläche'
                    kante='rechte Kante' if i==2 else 'linke Kante'
                    cols=f'{MO["x"]+MO["w"]}…{MO["x"]+MO["w"]+int(dist*1.8)}' if dr>0 else f'{MO["x"]-int(dist*1.8)}…{MO["x"]-1}'
                    rows=f'{MO["y"]+span[0]}…{MO["y"]+span[1]-1}'
                    reach=round(dist*1.8,1)
                else:
                    side='beidseitig (je 3 Spalten)'
                    kante='obere Kante' if i==1 else 'untere Kante'
                    cols=f'{MO["x"]-3}…{MO["x"]-1} und {MO["x"]+MO["w"]}…{MO["x"]+MO["w"]+2}'
                    rows=f'{MO["y"]+min(a,b)}…{MO["y"]+max(a,b)}'
                    reach=3
                vals=[n,round(ts,2),None,bi,names.get(mv['id'],str(mv['id'])),kante,f'{a} → {b} (Achse {axis}, Spanne {span[0]}–{span[1]})',side,cols,rows,round(st['dur']/1000,2),reach]
                for j,v in enumerate(vals,1):
                    cc=Wv.cell(r_,j,v); cc.font=f(); cc.border=bd
                Wv.cell(r_,3,f'=TEXT(B{r_}/86400,"mm:ss.0")'); Wv.cell(r_,2).number_format='0.00'; Wv.cell(r_,11).number_format='0.00'
                r_+=1
for col,w in zip('ABCDEFGHIJKL',[5,9,13,6,10,14,38,26,26,16,10,18]): Wv.column_dimensions[col].width=w
Wv.freeze_panes='A5'

# ---------- Wege ----------
Wg=wb.create_sheet('Wege',2)
Wg['A1']='Wege zum Highlight: Füllung läuft Spalte für Spalte zum Exponat, das Fach geht erst bei Ankunft an'; Wg['A1'].font=f(bold=True,size=14)
Wg['A2']='Nur Wege, die im Zeitfenster tatsächlich ausgelöst wurden. Zeit pro Spalte und Nachlauf stehen in den Hinweisen.'; Wg['A2'].font=f(italic=True,size=9,color='555555')
gh=['Nr','Zeit (s)','Zeit mm:ss.s','Beat','Fach-ID','Exponat','Ursprung','Spalten durchlaufen','Wandreihen','Dauer (s)','Fach geht an (s)']
for i,h in enumerate(gh,1):
    c=Wg.cell(4,i,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
rr=5
for k,r in enumerate(routes,1):
    rt=(r['t']-t0)/1000; e=EX[r['id']]; rc=e['rect']
    o=MO
    if rc['x']+rc['w']<=o['x']: cols=list(range(o['x']-1,rc['x']+rc['w']-1,-1))
    elif rc['x']>=o['x']+o['w']: cols=list(range(o['x']+o['w'],rc['x']))
    else: cols=[]
    vals=[k,round(rt,2),None,beat_at(rt),r['id'],e['name'],'Medienfläche',len(cols),f'{rc["y"]}…{rc["y"]+rc["h"]-1}',None,None]
    for j,v in enumerate(vals,1):
        cc=Wg.cell(rr,j,v); cc.font=f(); cc.border=bd
    Wg.cell(rr,3,f'=TEXT(B{rr}/86400,"mm:ss.0")')
    Wg.cell(rr,10,f'=H{rr}*Hinweise!$B$14/1000+Hinweise!$B$15/1000')
    Wg.cell(rr,11,f'=B{rr}+H{rr}*Hinweise!$B$14/1000+Hinweise!$B$15/1000')
    for j in (2,10,11): Wg.cell(rr,j).number_format='0.00'
    rr+=1
for col,w in zip('ABCDEFGHIJK',[5,9,13,6,9,40,16,18,14,10,16]): Wg.column_dimensions[col].width=w
Wg.freeze_panes='A5'

# ---------- Fächer-Patch ----------
P=wb.create_sheet('Fächer-Patch',3)
P['A1']='Fach-Patch: Zuordnung Fach-ID → Leuchte (vom Lichtplaner auszufüllen)'; P['A1'].font=f(bold=True,size=14)
P['A2']='Gelbe Spalten ausfüllen. Beispiel: Universum 1 · Startkanal 101 · Leuchtentyp „LED-Pixelstrip 60/m“ · Max-Level 40 %. Fach-ID ist der Schlüssel zu Airtable (Fach-ID) und Mockup.'
P['A2'].font=f(italic=True,size=9,color='555555')
ph=['Fach-ID','Exponat','Wand','Spalte x','Reihe y','Breite (Zellen)','Höhe (Zellen)','Maße B×H (cm)','Cues im Fenster','Universum','Startkanal','Leuchtentyp','Max-Level %']
for i,h in enumerate(ph,1):
    c=P.cell(4,i,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
P.row_dimensions[4].height=30
def wand(x): return 'A' if x<8 else ('B' if x<29 else 'C')
pr=5
for fid,e in sorted(EX.items(),key=lambda kv:(kv[1]['rect']['x'],kv[1]['rect']['y'])):
    rc=e['rect']
    vals=[fid,e['name'],wand(rc['x']),rc['x'],rc['y'],rc['w'],rc['h'],None,None,None,None,None,None]
    for j,v in enumerate(vals,1):
        cc=P.cell(pr,j,v); cc.font=f(); cc.border=bd
    P.cell(pr,8,f'=F{pr}*80&" × "&G{pr}*60')
    P.cell(pr,9,f'=COUNTIF(Cueliste!$F${R0+1}:$F${last},A{pr})')
    for j in (10,11,12,13): P.cell(pr,j).fill=inp_fill
    P.cell(pr,13).number_format='0%'
    for j in (3,4,5,6,7,9): P.cell(pr,j).alignment=Alignment(horizontal='center')
    pr+=1
for col,w in zip('ABCDEFGHIJKLM',[9,46,6,9,8,12,12,14,12,11,11,22,12]): P.column_dimensions[col].width=w
P.freeze_panes='A5'; P.auto_filter.ref=f'A4:M{pr-1}'

# ---------- Hinweise ----------
H['A1']='Hinweise, Parameter und Annahmen'; H['A1'].font=f(bold=True,size=14)
lines=[
('Zeitfenster','Film 00:00–01:00 ab Start des Kapitels (Beat 0 bis 5, Beat 6 beginnt bei 59,5 s). Zeit 0 = Beginn Beat 0.'),
('Entstehung','Das Mockup wurde real durchlaufen; pro Fach-ID wurde der Soll-Wert des Lichts (0–100 %) alle 40 ms mitgeschrieben und zu Cues verdichtet (Änderungen > 3 %).'),
('Level','1,0 = volle Helligkeit des Highlights, 0,22 = Titel-Grundlicht aller Fächer, 0,16 = stilles Raster (Silhouetten). Wert hängt von Kachelgröße und Einblendung ab.'),
('Nur 12 Fächer','Im Mockup sind für Kapitel 2 (Test) 12 Fächer mit Licht belegt (K2-Liste). Die übrigen Fächer bleiben aus und sind im Blatt „Fächer-Patch“ nur gelistet.'),
]
for i,(a,b) in enumerate(lines,3):
    H.cell(i,1,a).font=f(bold=True); H.cell(i,2,b).font=f(); H.cell(i,2).alignment=Alignment(wrap_text=True,vertical='top')
H['A9']='Parameter (gelb = änderbar, Cueliste und Wege rechnen damit)'; H['A9'].font=f(bold=True,size=11)
params=[('Fade auf, wenn das Mockup springt (s)',0.43,'Mockup blendet mit Rate 7/s auf (≈ 3·τ)'),
        ('Fade ab, wenn das Mockup springt (s)',1.15,'Mockup blendet mit Rate 2,6/s ab (≈ 3·τ)'),
        ('Wellengeschwindigkeit Weg (ms pro Spalte)',60,'ROUTE.cellMs im Mockup'),
        ('Nachlauf Weg bis Fach geht an (ms)',120,'ROUTE.settle im Mockup')]
for i,(a,v,n_) in enumerate(params,12):
    H.cell(i,1,a).font=f(); c=H.cell(i,2,v); c.font=f(color='0000FF'); c.fill=inp_fill; H.cell(i,3,n_).font=f(italic=True,size=9,color='555555')
H['A17']='Offen / nicht enthalten'; H['A17'].font=f(bold=True,size=11)
more=[
('Dimmkurve','Deckkraft im Browser ist keine Beleuchtungsstärke. Dimmkurve (Gamma) und Max-Level pro Exponat (Objektschutz) fehlen noch; die DMX-Spalte ist linear.'),
('Farbtemperatur','Das Mockup kennt nur Helligkeit (warmweißer Rahmen). Farbe/CCT pro Fach muss der Lichtplaner festlegen.'),
('Wellen','Die Wellen haben im Mockup leichten Zufall (Deckkraft je Zelle). Für die Anlage Zufall festlegen (seed) und als Pixel-Video rendern.'),
('Synchronisation','Zeit 0 = Beat 0. Für die Anlage braucht es Timecode oder denselben Player wie der Film; Loop-Neustart und Ruhezustand sind nicht Teil dieser Liste.'),
('Fehlende Exponate','Skoda Eiskratzer (A-E-2) und 919 Rekuperator (B-U-2) sind im Fach-Patch gelistet, stehen beim Kunden aber nicht in der Abfolge (offen).'),
]
for i,(a,b) in enumerate(more,18):
    H.cell(i,1,a).font=f(bold=True); H.cell(i,2,b).font=f(); H.cell(i,2).alignment=Alignment(wrap_text=True,vertical='top')
H.column_dimensions['A'].width=40; H.column_dimensions['B'].width=95; H.column_dimensions['C'].width=48
for r in range(3,23): H.row_dimensions[r].height=30 if H.cell(r,2).value and isinstance(H.cell(r,2).value,str) and len(H.cell(r,2).value)>95 else 16
wb.save('/mnt/user-data/outputs/Blauer_Kubus_Lichtcueliste_Kapitel2_0-60s.xlsx')
print('cues',len(cues),'groups',len(groups),'rows',last-R0,'wellen',n,'wege',len(routes))
