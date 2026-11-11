import os, json, glob, csv, subprocess
ROOT=os.path.expanduser("~/mnt/Blue Cube/Medien"); OUT=ROOT+"/_szenen"
summary=[]
for w in sorted(glob.glob(os.path.expanduser("~/sd/work/*"))):
    base=os.path.basename(w); obj,_,slug=base.partition("__")
    chunks=[json.load(open(f)) for f in sorted(glob.glob(w+"/c*.json"))]
    p=chunks[0]["path"]; fps=chunks[0]["fps"]
    sc=[]
    for c in chunks:
        for a,b in c["scenes"]:
            if sc and abs(sc[-1][1]-a)<0.05 and abs(a-c["start"])<0.05: sc[-1][1]=b
            else: sc.append([a,b])
    pr=subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",p]).decode().strip()
    W,H=map(int,pr.split(","))
    rows=[{"nr":i+1,"von":round(a,2),"bis":round(b,2),"dauer":round(b-a,2),"ab_5s":(b-a)>=5} for i,(a,b) in enumerate(sc)]
    d=f"{OUT}/{obj}"; os.makedirs(d,exist_ok=True)
    fn=os.path.splitext(os.path.basename(p))[0]
    json.dump({"datei":os.path.relpath(p,ROOT),"fps":fps,"breite":W,"hoehe":H,"verfahren":"PySceneDetect ContentDetector thr 27, min 0.5 s","status":"Vorschlag","szenen":rows},open(f"{d}/{fn}.szenen.json","w"),ensure_ascii=False,indent=1)
    with open(f"{d}/{fn}.szenen.csv","w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=["nr","von","bis","dauer","ab_5s"],delimiter=";"); wr.writeheader(); wr.writerows(rows)
    summary.append((obj,fn[:45],f"{W}x{H}",len(rows),sum(r["ab_5s"] for r in rows)))
for s in summary: print(" | ".join(map(str,s)))
print("gesamt",sum(s[3] for s in summary),"davon >=5s",sum(s[4] for s in summary))
