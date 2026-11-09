import json
d=json.load(open('sampled.json')); L=d['LOG']; t0=L['t0']; EX=d['EXinfo']
WIN=60.0
S=[((s['t']-t0)/1000,s) for s in L['samples']]; S=[(t,s) for t,s in S if 0<=t<=WIN]
UP,DOWN=0.43,1.15   # Ansprechzeit des Mockups bei Sprüngen (Anstiegsrate 7/s, Abfallrate 2,6/s)
cues=[]
for fid in EX:
    v=[min(1.0,s['T'][fid]) for t,s in S]; ts=[t for t,s in S]
    if max(v)<0.01: continue
    trans=[];i=1;n=len(v)
    while i<n:
        if abs(v[i]-v[i-1])>0.004:
            a=i-1;j=i;last=i
            while j<n and j-last<=3:
                if abs(v[j]-v[j-1])>0.004: last=j
                j+=1
            b=last;trans.append([a,b]);i=b+1
        else:i+=1
    # merge transitions closer than 0.25 s
    m=[]
    for a,b in trans:
        if m and ts[a]-ts[m[-1][1]]<0.25: m[-1][1]=b
        else: m.append([a,b])
    prev=v[0]
    for a,b in m:
        va,vb=v[a],v[b]
        if abs(vb-va)<0.03: continue
        dur=ts[b]-ts[a]
        step=dur<0.2
        fade=(UP if vb>va else DOWN) if step else dur
        cues.append(dict(t=round(ts[a],2),fid=fid,frm=round(va,2),to=round(vb,2),fade=round(fade,2),step=step,dur=round(dur,2)))
cues.sort(key=lambda c:(c['t'],c['fid']))
for i,c in enumerate(cues,1): c['n']=i
print(len(cues))
for c in cues: print(c)
json.dump(cues,open('cues.json','w'))
