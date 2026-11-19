#!/usr/bin/env python3
"""Vorschau-Clips für die Tabelle Medien (Szenen-Chat, 18.11.2026).

Liest jobs.json (rec, datei, von, bis, out, typ), erzeugt je Zeile eine kleine
Vorschau (854x480, H.264, AAC mono leise, max. 5 MB) und hängt sie per
Airtable-API an das Feld "Anhang" (fldrrNdmVLCxCLmKM). Vorhandene Anhänge
werden nicht ersetzt (jobs.json enthält nur Zeilen ohne Anhang).

Wiederaufnehmbar: erledigte Zeilen stehen in done.log, Fehler in fehler.log.
Aufruf:  PAT=... python3 vorschau_medien.py <MEDIEN-Ordner> <jobs.json> [max_sekunden]
Der Zugangsschlüssel kommt nur aus der Umgebungsvariable PAT.
"""
import base64, json, os, subprocess, sys, time, urllib.error, urllib.request

BASE = 'appd9oVo78FNTrPDd'
FELD_ANHANG = 'fldrrNdmVLCxCLmKM'
MAX_BYTES = 5 * 1024 * 1024
OHNE_MARKE_S = 30.0
MAX_DAUER_S = 90.0


def sek(t):
    if t is None or str(t).strip() == '':
        return None
    import re
    m = re.search(r'\d+(?::\d+)*(?:[.,]\d+)?', str(t))
    if not m:
        return None
    teile = [float(x) for x in m.group(0).replace(',', '.').split(':')]
    s = 0.0
    for x in teile:
        s = s * 60 + x
    return s


def dauer(pfad):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'default=nw=1:nk=1', pfad], capture_output=True, text=True).stdout
    try:
        return float(o.strip())
    except ValueError:
        return None


def hat_video(pfad):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries',
                        'stream=codec_type', '-of', 'csv=p=0', pfad], capture_output=True, text=True).stdout
    return 'video' in o


def bauen(job, medien, ziel):
    quelle = os.path.join(medien, job['datei'])
    if not os.path.exists(quelle):
        raise RuntimeError('Datei fehlt: ' + job['datei'])
    gesamt = dauer(quelle) or 0
    if job['datei'].startswith('Clips/'):
        a, b = 0.0, None
    else:
        a, b = sek(job['von']) or 0.0, sek(job['bis'])
    if b is None or b <= a:
        b = a + OHNE_MARKE_S
    if gesamt:
        b = min(b, gesamt)
    d = max(1.0, min(b - a, MAX_DAUER_S))
    video = hat_video(quelle)
    if not video:
        ziel = ziel[:-4] + '.m4a'
        cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-t', f'{d:.2f}', '-i', quelle,
               '-vn', '-ac', '1', '-c:a', 'aac', '-b:a', '96k', ziel]
        subprocess.run(cmd, check=True)
        return ziel, 'audio/mp4'
    kbps = int(MAX_BYTES * 8 / d / 1000 * 0.85) - 48
    kbps = max(250, min(kbps, 1800))
    for versuch in range(3):
        cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-t', f'{d:.2f}', '-i', quelle,
               '-vf', 'scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2,setsar=1',
               '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', f'{kbps}k', '-maxrate', f'{int(kbps*1.2)}k',
               '-bufsize', f'{kbps*2}k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
               '-af', 'volume=-12dB', '-ac', '1', '-c:a', 'aac', '-b:a', '48k', ziel]
        subprocess.run(cmd, check=True)
        if os.path.getsize(ziel) <= MAX_BYTES:
            return ziel, 'video/mp4'
        kbps = int(kbps * 0.7)
    raise RuntimeError('zu groß nach 3 Versuchen')


def hat_anhang(rec, pat):
    url = f'https://api.airtable.com/v0/{BASE}/tblCalNontccPQ6kp/{rec}?returnFieldsByFieldId=true'
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + pat})
    for versuch in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=30))
            return bool(d.get('fields', {}).get(FELD_ANHANG))
        except urllib.error.HTTPError:
            raise
        except Exception:
            time.sleep(3)
    return False


def hochladen(rec, pfad, ct, pat):
    daten = json.dumps({'contentType': ct, 'filename': os.path.basename(pfad),
                        'file': base64.b64encode(open(pfad, 'rb').read()).decode()}).encode()
    req = urllib.request.Request(f'https://content.airtable.com/v0/{BASE}/{rec}/{FELD_ANHANG}/uploadAttachment',
                                 daten, {'Authorization': 'Bearer ' + pat, 'Content-Type': 'application/json'})
    for versuch in range(4):
        try:
            urllib.request.urlopen(req, timeout=60).read()
            return
        except urllib.error.HTTPError:
            raise
        except Exception:
            if versuch == 3:
                raise
            time.sleep(3 * (versuch + 1))


def main():
    medien, jobsdatei = sys.argv[1], sys.argv[2]
    budget = float(sys.argv[3]) if len(sys.argv) > 3 else 150
    pat = os.environ['PAT']
    ordner = os.path.dirname(os.path.abspath(jobsdatei))
    done_p, err_p = os.path.join(ordner, 'done.log'), os.path.join(ordner, 'fehler.log')
    fertig = set(open(done_p).read().split()) if os.path.exists(done_p) else set()
    fehler = set(l.split('\t')[0] for l in open(err_p)) if os.path.exists(err_p) else set()
    jobs = json.load(open(jobsdatei))
    t0 = time.time()
    n = 0
    for job in jobs:
        if job['rec'] in fertig or job['rec'] in fehler:
            continue
        if time.time() - t0 > budget:
            break
        try:
            if hat_anhang(job['rec'], pat):
                open(done_p, 'a').write(job['rec'] + '\n')
                print('schon da', job['out'])
                continue
            pfad, ct = bauen(job, medien, os.path.join(ordner, job['out'] + '.mp4'))
            hochladen(job['rec'], pfad, ct, pat)
            open(done_p, 'a').write(job['rec'] + '\n')
            n += 1
            print('ok', job['out'], os.path.getsize(pfad) // 1024, 'kB')
        except Exception as e:
            open(err_p, 'a').write(f"{job['rec']}\t{job['out']}\t{e}\n")
            print('FEHLER', job['out'], e)
    rest = len([j for j in jobs if j['rec'] not in fertig and j['rec'] not in fehler]) - n
    print(f'{n} neu, offen {rest}')


if __name__ == '__main__':
    main()
