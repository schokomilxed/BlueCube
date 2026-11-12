"""Ton je Szene einordnen (AudioSet-Klassifikator AST): Fahrzeug, Musik, Sprache + Lautheit (dBFS).
Aufruf: python3 ton_bewerten.py <quelle_mono16k.wav> <Video.szenen.csv>
Vorbereitung: ffmpeg -i <Quelle.mp4> -vn -ac 1 -ar 16000 <quelle_mono16k.wav>; pip install torch transformers soundfile
Nur Vorsortierung, Entscheidung nach Gehör (Björn)."""
import sys, re, csv, numpy as np, soundfile as sf, torch
from transformers import AutoFeatureExtractor, ASTForAudioClassification
M='MIT/ast-finetuned-audioset-10-10-0.4593'; fe=AutoFeatureExtractor.from_pretrained(M); mdl=ASTForAudioClassification.from_pretrained(M).eval(); lab=mdl.config.id2label
GRP={'musik':r'Music|Musical|Song|Guitar|Drum|Piano|Synthesizer|Orchestra|Electronic music|Beat',
     'sprache':r'Speech|Narration|Conversation|Male speech|Female speech|Singing',
     'fahrzeug':r'Vehicle|Car|Engine|Motor|Race car|Accelerating|revving|Idling|Tire squeal|Skidding|Whir|Hum|Mechanisms|Whoosh|Wind|Electric'}
idx={k:[i for i in range(len(lab)) if re.search(v,lab[i])] for k,v in GRP.items()}
y,sr=sf.read(sys.argv[1]); rows=[r for r in csv.DictReader(open(sys.argv[2]),delimiter=';') if r['ab_5s']=='True']
print('Szene  von–bis        Fahrzeug Musik Sprache  dBFS  | Top')
for r in rows:
    a,b=float(r['von']),float(r['bis']); seg=y[int(a*sr):int(min(b,a+10)*sr)].astype(np.float32)
    if len(seg)<sr: continue
    with torch.no_grad(): p=torch.sigmoid(mdl(**fe(seg,sampling_rate=16000,return_tensors='pt')).logits[0]).numpy()
    g={k:max(p[i] for i in v) for k,v in idx.items()}; d=20*np.log10(np.sqrt(np.mean(seg**2))+1e-9)
    top=', '.join(lab[i] for i in p.argsort()[::-1][:3])
    flag='★' if g['fahrzeug']>0.15 and g['musik']<0.3 and g['sprache']<0.3 else ' '
    print(f"{flag}{int(r['nr']):4d}  {a:6.1f}–{b:6.1f}   {g['fahrzeug']:.2f}    {g['musik']:.2f}  {g['sprache']:.2f}  {d:6.1f} | {top}")
