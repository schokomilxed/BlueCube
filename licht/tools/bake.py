import json, csv, sys, numpy as np
START_BEAT=int(sys.argv[1]) if len(sys.argv)>1 else 1
WAVE_MODE=sys.argv[2] if len(sys.argv)>2 else 'mean'     # mean | max
WAVE_GAIN=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
EPS=0.012; FPS=25
d=json.load(open('sampled_full.json')); film=json.load(open('film_data.json'))
ids=d['ids']; N=len(ids); info=d['info']
A=np.array(d['samples'],dtype=float); t=A[:,0]/1000.0
lv=A[:,1::3]; wmax=A[:,2::3]; wmean=A[:,3::3]
wave=wmean if WAVE_MODE=='mean' else wmax
wave=np.where(wave<0.03,0,wave)*WAVE_GAIN
tot=np.maximum(lv,np.minimum(1,wave))
bt=[(b['bi'],b['t']/1000.0) for b in d['beats']]
starts=[x for x in bt if x[0]==START_BEAT]
t_start=starts[0][1]
durs=[b['dur']/1000.0 for b in film['beats']]
loop_s=sum(durs[START_BEAT:])
t_end=t_start+loop_s
print('start',t_start,'loop_s',round(loop_s,3),'measured next start',starts[1][1] if len(starts)>1 else None)
grid=np.arange(0,loop_s,1/FPS)
S=np.stack([np.interp(grid+t_start,t,tot[:,k]) for k in range(N)],axis=1)
# Loop-Naht: Anfang an Endwert angleichen, falls nötig
endv=np.stack([np.interp(t_end,t,tot[:,k]) for k in range(N)])
gap=np.abs(S[0]-endv).max(); print('Loop-Naht max Abweichung',round(gap,3))
blend=int(0.6*FPS)
for i in range(blend):
    w=i/blend; S[i]=endv*(1-w)+S[i]*w
def rdp(x,y,eps):
    keep=[0,len(x)-1]; stack=[(0,len(x)-1)]
    while stack:
        a,b=stack.pop()
        if b<=a+1: continue
        yc=y[a]+(y[b]-y[a])*(x[a+1:b]-x[a])/(x[b]-x[a])
        dd=np.abs(y[a+1:b]-yc); k=int(dd.argmax())
        if dd[k]>eps:
            m=a+1+k; keep.append(m); stack+= [(a,m),(m,b)]
    return sorted(keep)
rows=[]; stats={}
for k,fid in enumerate(ids):
    y=S[:,k]
    if y.max()<0.02: continue
    idx=rdp(grid,y,EPS)
    stats[fid]=len(idx)
    for i in idx: rows.append((round(float(grid[i]),2),fid,round(float(y[i]),3)))
    # Wertekurve am Loopende exakt schließen
    rows.append((round(loop_s,2),fid,round(float(S[0,k]),3)))
rows.sort(key=lambda r:(r[1],r[0]))
# doppelte Endzeiten vermeiden
seen=set();out=[]
for r in rows:
    if (r[0],r[1]) in seen: continue
    seen.add((r[0],r[1])); out.append(r)
with open('cues.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['time_s','fach_id','level'])
    for r in sorted(out,key=lambda r:(r[0],r[1])): w.writerow(r)
print('Fächer mit Licht',len(stats),'Keyframes',len(out))
print(sorted(stats.items(),key=lambda kv:-kv[1])[:8])
# Patch: nach Wandposition sortiert
order=sorted(ids,key=lambda i:(info[i]['rect']['x'],info[i]['rect']['y']))
with open('patch.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['fach_id','exponat','universe','channel','mode','color','max_level'])
    for n,fid in enumerate(order,1): w.writerow([fid,info[fid]['name'],0,n,'dim','ffffff',1])
json.dump(dict(loop_s=round(loop_s,3),start_beat=START_BEAT,ids=ids,info=info),open('bake_meta.json','w'),ensure_ascii=False)
