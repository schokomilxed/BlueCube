import os, json, glob, subprocess, time, sys
ROOT=os.path.expanduser("~/mnt/Blue Cube/Medien"); OUT=ROOT+"/_szenen"
t0=time.time(); B=float(sys.argv[1]); rest=0
for j in sorted(glob.glob(OUT+"/*/*.szenen.json")):
    d=json.load(open(j)); fn=os.path.basename(j)[:-len(".szenen.json")]
    td=os.path.dirname(j)+"/thumbs/"+fn; os.makedirs(td,exist_ok=True)
    src=os.path.join(ROOT,d["datei"])
    for s in d["szenen"]:
        if not s["ab_5s"]: continue
        o=f"{td}/{s['nr']:03d}.jpg"
        if os.path.exists(o): continue
        if time.time()-t0>B: rest+=1; continue
        m=(s["von"]+s["bis"])/2
        subprocess.run(["ffmpeg","-v","error","-ss",f"{m:.2f}","-i",src,"-frames:v","1","-vf","scale=320:-2","-q:v","4",o])
print("offen:",rest)
