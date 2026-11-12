"""Ton aller Szenen (ab 5 s) und aller Kandidaten aus Airtable einordnen. Gleiche Logik wie ton_bewerten.py.
Aufruf (Terminal):  caffeinate -i python3 ton_alle.py   [optional: Pfad zu Blue Cube/Medien]
Ergebnis:
  Medien/_szenen/<NN>_<slug>/<Video>.ton.csv      je erkannte Szene ab 5 s
  Medien/_szenen/_ton/kandidaten.ton.csv            je Kandidat (genau Von–Bis aus Airtable)
  Medien/_szenen/_ton/hoerproben/<Nr>_<K>.mp3       Hörprobe je Kandidat
Bereits fertige Dateien werden übersprungen, Abbruch und Neustart sind also unkritisch.
Nur Vorsortierung, Entscheidung nach Gehör (Björn)."""
import sys, os, re, csv, json, glob, time, subprocess, tempfile
import numpy as np, soundfile as sf, torch
from transformers import AutoFeatureExtractor, ASTForAudioClassification
MED = sys.argv[1] if len(sys.argv) > 1 else "/Users/bjoern.mueller/Library/CloudStorage/SynologyDrive-0700_VW-FMW/4_Inhalte/3-6_Recherche/Blue Cube/Medien"
Q, SZ = f"{MED}/Quellen", f"{MED}/_szenen"
TON = f"{SZ}/_ton"; os.makedirs(f"{TON}/hoerproben", exist_ok=True)
M = 'MIT/ast-finetuned-audioset-10-10-0.4593'
print("Lade Modell (beim ersten Mal ca. 350 MB) …", flush=True)
fe = AutoFeatureExtractor.from_pretrained(M); mdl = ASTForAudioClassification.from_pretrained(M).eval(); lab = mdl.config.id2label
GRP = {'musik': r'Music|Musical|Song|Guitar|Drum|Piano|Synthesizer|Orchestra|Electronic music|Beat',
       'sprache': r'Speech|Narration|Conversation|Male speech|Female speech|Singing',
       'fahrzeug': r'Vehicle|Car|Engine|Motor|Race car|Accelerating|revving|Idling|Tire squeal|Skidding|Whir|Hum|Mechanisms|Whoosh|Wind|Electric'}
idx = {k: [i for i in range(len(lab)) if re.search(v, lab[i])] for k, v in GRP.items()}
KOPF = ['fahrzeug', 'musik', 'sprache', 'dbfs', 'vorschlag', 'top3']

def wav(video):
    t = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vn', '-ac', '1', '-ar', '16000', t])
    if r.returncode or os.path.getsize(t) < 1000: return None, t
    y, sr = sf.read(t); return y, t

def bewerte(y, a, b, sr=16000):
    seg = y[int(a*sr):int(min(b, a+10)*sr)].astype(np.float32)
    if len(seg) < sr: return None
    with torch.no_grad(): p = torch.sigmoid(mdl(**fe(seg, sampling_rate=16000, return_tensors='pt')).logits[0]).numpy()
    g = {k: float(max(p[i] for i in v)) for k, v in idx.items()}
    d = float(20*np.log10(np.sqrt(np.mean(seg**2))+1e-9))
    flag = 'ja' if g['fahrzeug'] > 0.15 and g['musik'] < 0.3 and g['sprache'] < 0.3 else 'nein'
    top = ', '.join(lab[i] for i in p.argsort()[::-1][:3])
    return [f"{g['fahrzeug']:.2f}", f"{g['musik']:.2f}", f"{g['sprache']:.2f}", f"{d:.1f}", flag, top]

# 1) alle erkannten Szenen ab 5 s
jobs = []
for c in sorted(glob.glob(f"{SZ}/*/*.szenen.csv")):
    obj = os.path.basename(os.path.dirname(c)); name = os.path.basename(c)[:-11]
    out = c[:-11] + '.ton.csv'
    vids = [v for v in glob.glob(f"{Q}/{obj}/{glob.escape(name)}.*") if not v.endswith('.part')]
    if os.path.exists(out) or not vids: continue
    jobs.append((c, out, vids[0]))
n_sz = sum(sum(1 for r in csv.DictReader(open(c), delimiter=';') if r['ab_5s'].strip() == 'True') for c, _, _ in jobs)
print(f"{len(jobs)} Videos, {n_sz} Szenen ab 5 s offen.", flush=True)
t0 = time.time(); fertig = 0
for i, (c, out, v) in enumerate(jobs, 1):
    rows = [r for r in csv.DictReader(open(c), delimiter=';') if r['ab_5s'].strip() == 'True']
    y, t = wav(v)
    with open(out + '.tmp', 'w', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['nr', 'von', 'bis'] + KOPF)
        for r in rows:
            res = bewerte(y, float(r['von']), float(r['bis'])) if y is not None else ['', '', '', '', 'kein Ton', '']
            if res: w.writerow([r['nr'], r['von'], r['bis']] + res)
            fertig += 1
    os.replace(out + '.tmp', out)
    if t and os.path.exists(t): os.remove(t)
    eta = (time.time()-t0)/max(fertig, 1)*(n_sz-fertig)/60
    print(f"[{i}/{len(jobs)}] {os.path.basename(v)[:60]}  ({len(rows)} Szenen)  noch ca. {eta:.0f} min", flush=True)

# 2) Kandidaten aus Airtable: genaues Fenster + Hörprobe
K = json.load(open(f"{TON}/kandidaten.json")); out = f"{TON}/kandidaten.ton.csv"
if not os.path.exists(out):
    print(f"Kandidaten: {len(K)} …", flush=True); cache = {}
    with open(out + '.tmp', 'w', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['rec', 'name', 'von', 'bis'] + KOPF)
        for k in K:
            v = f"{Q}/{k['video']}"
            if v not in cache: cache[v] = wav(v)
            y = cache[v][0]
            res = bewerte(y, k['von'], k['bis']) if y is not None else ['', '', '', '', 'kein Ton', '']
            w.writerow([k['rec'], k['name'], k['von'], k['bis']] + (res or ['']*6))
            dur = k['bis'] - k['von']
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(k['von']), '-t', f"{dur:.2f}", '-i', v, '-vn',
                            '-af', f"afade=t=in:d=0.15,afade=t=out:st={max(dur-0.3,0):.2f}:d=0.3", '-c:a', 'libmp3lame', '-b:a', '160k',
                            f"{TON}/hoerproben/{k['name']}.mp3"])
    os.replace(out + '.tmp', out)
    for y, t in cache.values():
        if os.path.exists(t): os.remove(t)
print(f"FERTIG nach {(time.time()-t0)/60:.0f} min. Ergebnisse in {SZ}", flush=True)
