import os, sys, json, time, glob, subprocess, re
ROOT=os.path.expanduser("~/mnt/Blue Cube/Medien")
OUT=os.path.join(ROOT,"_szenen")
BUDGET=float(sys.argv[1]) if len(sys.argv)>1 else 140
CH=600.0
t0=time.time()
vids=sorted(glob.glob(ROOT+"/Quellen/*/*.mp4"))
def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())
todo=0
for p in vids:
    obj=os.path.basename(os.path.dirname(p)); name=os.path.splitext(os.path.basename(p))[0]
    if os.path.exists(os.path.join(OUT,obj,name+".szenen.json")): continue  # schon erkannt, nicht neu rechnen
    d=os.path.join(OUT,obj); os.makedirs(d,exist_ok=True)
    work=os.path.expanduser("~/sd/work/"+obj+"__"+re.sub(r'\W+','_',name))
    os.makedirs(work,exist_ok=True)
    D=dur(p); n=int(D//CH)+1
    for i in range(n):
        o=f"{work}/c{i:03d}.json"
        if os.path.exists(o): continue
        if time.time()-t0>BUDGET: todo+=1; continue
        subprocess.run([sys.executable,os.path.expanduser("~/sd/detect.py"),p,str(i*CH),str(min(D,(i+1)*CH)),o],
            env=dict(os.environ,PYTHONPATH=os.path.expanduser("~/.local/lib/python3.10/site-packages")),
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if not os.path.exists(o): todo+=1
print("verbleibende Chunks:",todo,"Zeit",round(time.time()-t0))
