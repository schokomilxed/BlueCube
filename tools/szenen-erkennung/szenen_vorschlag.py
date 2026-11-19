#!/usr/bin/env python3
"""Szenen-Vorschläge aus Medien (Szenen-Chat, 19.11.2026).

Schritt 1 (fenster): je Medien-Zeile ein Fenster 5–10 s bestimmen.
  - mit Zeitmarke des Kunden: Von bis Bis, gekürzt auf 8 s, wenn länger als 10 s
  - ohne Zeitmarke: längste Szene >= 5 s aus der Szenenerkennung (nicht die erste,
    nicht in den letzten 8 % des Videos), Fenster ab Szenenstart + 0,3 s, max. 8 s
  Dazu drei Vorschaubilder (Anfang/Mitte/Ende), eine Hörprobe (MP3) und die
  Lautheit (mittlere dBFS). Ergebnis: fenster.json + Prüfbogen JPG.
Aufruf: python3 szenen_vorschlag.py fenster <MEDIEN> <szjobs.json> <ausgabeordner>
"""
import csv, glob, io, json, os, re, subprocess, sys

def sek(t):
    if t is None or str(t).strip() == '':
        return None
    m = re.search(r'\d+(?::\d+)*(?:[.,]\d+)?', str(t))
    if not m:
        return None
    s = 0.0
    for x in m.group(0).replace(',', '.').split(':'):
        s = s * 60 + float(x)
    return s

def dauer(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                        'default=nw=1:nk=1', p], capture_output=True, text=True).stdout
    try:
        return float(o)
    except ValueError:
        return 0.0

def szenen_csv(medien, datei):
    stamm = os.path.splitext(os.path.basename(datei))[0]
    ordner = os.path.basename(os.path.dirname(datei))
    for p in [os.path.join(medien, '_szenen', ordner, stamm + '.szenen.csv')] + \
             glob.glob(os.path.join(medien, '_szenen', '*', glob.escape(stamm) + '.szenen.csv')):
        if os.path.exists(p):
            return [(float(r['von']), float(r['bis'])) for r in csv.DictReader(open(p), delimiter=';')]
    return None

def fenster(job, medien):
    q = os.path.join(medien, job['datei'])
    d = dauer(q)
    a, b = sek(job['von']), sek(job['bis'])
    if a is not None:
        if b is None or b <= a:
            b = a + 8
        if b - a > 10:
            b = a + 8
        quelle = 'Zeitmarke'
    else:
        sz = szenen_csv(medien, job['datei'])
        kand = [(e - s, s, e) for i, (s, e) in enumerate(sz or []) if e - s >= 5 and i > 0 and s < d * 0.92]
        if not kand and sz:
            kand = [(e - s, s, e) for (s, e) in sz if e - s >= 3]
        if not kand:
            a, b, quelle = min(5.0, d / 3), min(5.0, d / 3) + 8, 'ohne Szenen'
        else:
            _, s, e = max(kand)
            a, b = s + 0.3, min(e - 0.3, s + 8.3)
            quelle = 'Szene'
    if d:
        b = min(b, d - 0.1)
    return round(a, 2), round(b, 2), quelle

def main():
    _, cmd, medien, jobsdatei, aus = sys.argv
    os.makedirs(os.path.join(aus, 'vorschau'), exist_ok=True)
    os.makedirs(os.path.join(aus, 'hoerproben'), exist_ok=True)
    ergebnis_p = os.path.join(aus, 'fenster.json')
    erg = json.load(open(ergebnis_p)) if os.path.exists(ergebnis_p) else {}
    for job in json.load(open(jobsdatei)):
        if job['med'] in erg:
            continue
        q = os.path.join(medien, job['datei'])
        a, b, quelle = fenster(job, medien)
        name = f"{job['nr']}_{job['k']}"
        for tag, t in (('1_anfang', a + 0.2), ('2_mitte', (a + b) / 2), ('3_ende', b - 0.2)):
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', q, '-frames:v', '1',
                            '-vf', 'scale=960:-2', '-q:v', '3', os.path.join(aus, 'vorschau', f'{name}_{tag}.jpg')])
        d = b - a
        mp3 = os.path.join(aus, 'hoerproben', f'{name}.mp3')
        r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-t', f'{d:.2f}', '-i', q, '-vn',
                            '-af', f'afade=t=in:d=0.15,afade=t=out:st={max(0, d - 0.3):.2f}:d=0.3',
                            '-c:a', 'libmp3lame', '-b:a', '160k', mp3], capture_output=True)
        ton = os.path.exists(mp3) and r.returncode == 0
        lv = subprocess.run(['ffmpeg', '-nostdin', '-ss', f'{a:.2f}', '-t', f'{d:.2f}', '-i', q, '-vn', '-af', 'volumedetect',
                             '-f', 'null', '-'], capture_output=True, text=True).stderr
        m = re.search(r'mean_volume: (-?[\d.]+)', lv)
        erg[job['med']] = dict(job, a=a, b=b, quelle=quelle, ton=ton, dbfs=float(m.group(1)) if m else None)
        json.dump(erg, open(ergebnis_p, 'w'), ensure_ascii=False, indent=0)
        print(name, a, b, quelle, erg[job['med']]['dbfs'])

if __name__ == '__main__':
    main()
