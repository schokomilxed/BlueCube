#!/usr/bin/env python3
"""Legt Szenen-Kandidaten aus fenster.json + entscheid.json in Airtable an (Szenen-Chat, 19.11.2026).
Wiederaufnehmbar über angelegt.json. Schlüssel nur aus Umgebungsvariable PAT.
Aufruf: PAT=... python3 szenen_anlegen.py <runde-ordner> [max_sekunden]
"""
import base64, json, os, re, sys, time, urllib.error, urllib.request

BASE, TAB = 'appd9oVo78FNTrPDd', 'tblrZADeAl29MG8tx'
F = dict(name='fldHzUwl7BmLz6pCK', medium='fld1DHWc1wDCUcV3N', exponat='fldYAcXwJ1Wi9JDzF', von='fldBv2AERlQGFHcnv',
         bis='fldkUh5wnznQpooX1', loop='fldRS9uBjdcI6EG1B', score='fldD8i9fxhu0mjcX2', grund='fldnpAFAkP2TlAnTX',
         formate='fldQFC9qnTMr01ooS', status='fldw7LmEHhx49w228', laut='fldBuLuhunBT89soE', otv='fldGuy4XqkA6O7wDO',
         ots='fldOSn9Skr8IPkhqH', vorschau='fld4Kok754kycAoDc', hoer='fldXcbVJeUuMC9QaQ')


def req(url, daten=None, methode='GET'):
    r = urllib.request.Request(url, json.dumps(daten).encode() if daten is not None else None,
                               {'Authorization': 'Bearer ' + os.environ['PAT'], 'Content-Type': 'application/json'},
                               method=methode)
    for v in range(4):
        try:
            return json.load(urllib.request.urlopen(r, timeout=60))
        except urllib.error.HTTPError as e:
            raise RuntimeError(e.read()[:300])
        except Exception:
            if v == 3:
                raise
            time.sleep(3 * (v + 1))


def upload(rec, feld, pfad, ct):
    return req(f'https://content.airtable.com/v0/{BASE}/{rec}/{feld}/uploadAttachment',
               {'contentType': ct, 'filename': os.path.basename(pfad),
                'file': base64.b64encode(open(pfad, 'rb').read()).decode()}, 'POST')


def sortkey(j):
    n = j['nr']
    return (int(re.sub('a', '', n)) * 10 + (5 if 'a' in n else 0), int(j['k'][1:]))


def main():
    ordner = sys.argv[1]
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 140
    fen = json.load(open(os.path.join(ordner, 'fenster.json')))
    ent = json.load(open(os.path.join(ordner, 'entscheid.json')))
    ang_p = os.path.join(ordner, 'angelegt.json')
    ang = json.load(open(ang_p)) if os.path.exists(ang_p) else {}
    neu_k = {}
    jobs = sorted(fen.values(), key=sortkey)
    t0 = time.time()
    for j in jobs:
        alt = f"{j['nr']}_{j['k']}"
        e = ent.get(alt)
        if not e:
            continue
        neu_k[j['nr']] = neu_k.get(j['nr'], 0) + 1
        kenn = j['k'] if os.environ.get('KEEPK') else f"K{neu_k[j['nr']]}"
        if alt in ang and ang[alt].get('fertig'):
            continue
        if time.time() - t0 > budget:
            break
        titel, warn, score = e
        quelle = j['datei'].split('/', 1)[-1]
        if len(quelle) > 70:
            quelle = quelle[:67] + '…'
        herkunft = 'Zeitmarke des Kunden (Media Links)' if j['quelle'] == 'Zeitmarke' else 'automatisch gewählte Szene (Szenenerkennung)'
        grund = f"{titel}. Fenster: {herkunft}.\n\nKachelgrößen: M, L\nAuflösung: siehe Medium\nQuelle: {quelle}\n"
        if warn:
            grund += '\n' + warn + '\n'
        grund += '\nTon noch nicht klassifiziert (nur Lautheit).'
        dbfs = j.get('dbfs')
        felder = {F['name']: f"{j['nr']} · {kenn} {titel}", F['medium']: [j['med']], F['exponat']: [j['ex']],
                  F['von']: j['a'], F['bis']: j['b'], F['loop']: round(j['b'] - j['a'], 1), F['score']: score,
                  F['grund']: grund, F['formate']: ['quer'], F['status']: 'Kandidat', F['ots']: 'ungeprüft'}
        if dbfs is not None:
            felder[F['laut']] = dbfs
            if dbfs < -60:
                felder[F['otv']] = 'nein'
        if not j.get('ton'):
            felder[F['otv']] = 'kein Ton'
        rec = ang.get(alt, {}).get('rec')
        if not rec:
            r = req(f'https://api.airtable.com/v0/{BASE}/{TAB}', {'records': [{'fields': felder}], 'typecast': True}, 'POST')
            rec = r['records'][0]['id']
            ang[alt] = {'rec': rec, 'kenn': kenn}
            json.dump(ang, open(ang_p, 'w'), indent=0)
        done = ang[alt].setdefault('up', [])
        for tag in ('1_anfang', '2_mitte', '3_ende'):
            if tag not in done:
                upload(rec, F['vorschau'], os.path.join(ordner, 'vorschau', f'{alt}_{tag}.jpg'), 'image/jpeg')
                done.append(tag)
                json.dump(ang, open(ang_p, 'w'), indent=0)
        mp3 = os.path.join(ordner, 'hoerproben', f'{alt}.mp3')
        if 'mp3' not in done and j.get('ton') and os.path.exists(mp3):
            upload(rec, F['hoer'], mp3, 'audio/mpeg')
            done.append('mp3')
        ang[alt]['fertig'] = True
        json.dump(ang, open(ang_p, 'w'), indent=0)
        print('ok', alt, '->', j['nr'], kenn, rec)
    offen = sum(1 for j in jobs if ent.get(f"{j['nr']}_{j['k']}") and not ang.get(f"{j['nr']}_{j['k']}", {}).get('fertig'))
    print('offen', offen)


if __name__ == '__main__':
    main()
