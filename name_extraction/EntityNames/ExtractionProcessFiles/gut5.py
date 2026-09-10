import glob, re, json
import numpy as np
from PIL import Image
def pn(f): return int(re.search(r"\((\d+)\)", f).group(1))
files=sorted(glob.glob("/home/claude/Plumer Biographies Index/*.jpg"), key=pn)
ROWFRAC={4:(0.10,1.0), 23:(0.0,0.30)}
def runs_of(mask, merge):
    rs=[];st=None
    for i,v in enumerate(mask):
        if v and st is None: st=i
        elif not v and st is not None: rs.append([st,i-1]); st=None
    if st is not None: rs.append([st,len(mask)-1])
    m=[]
    for x in rs:
        if m and x[0]-m[-1][1]<merge: m[-1][1]=x[1]
        else: m.append(list(x))
    return m
G={}
for f in files:
    n=pn(f)
    a=np.asarray(Image.open(f).convert("L"),dtype=np.int16)
    thr=int(np.percentile(a,25))-25
    H,W=a.shape
    a=a[int(H*0.03):int(H*0.97), int(W*0.03):int(W*0.97)]
    d=a<thr
    r=np.where(d.sum(axis=1)>max(3,a.shape[1]*0.005))[0]
    c=np.where(d.sum(axis=0)>max(3,a.shape[0]*0.005))[0]
    sub=a[r[0]:r[-1], c[0]:c[-1]]
    h,w=sub.shape
    lo,hi=ROWFRAC.get(n,(0.45,1.0))
    tbl=(sub[int(h*lo):int(h*hi)]<thr)
    prof=tbl.sum(axis=0); nrow=tbl.shape[0]
    on=prof>max(2,nrow*0.02)
    m=runs_of(on,6)
    wide=[x for x in m if x[1]-x[0]>0.15*w]
    ok = len(wide)>=2
    b2 = wide[1][0] if ok else None
    # gap immediately before block2
    prev = [x for x in m if x[1] < b2] if ok else []
    gut = (prev[-1][1]+b2)//2 if prev else (b2-10 if ok else w//2)
    # validate: between end of names1 and gutter there should be >=2 narrow runs (vol, page)
    n1end = wide[0][1]
    between=[x for x in m if x[0]>n1end and x[1]<gut]
    G[n]=int(gut)
    print(f"p{n:02d} w={w} nwide={len(wide)} gutter={gut} ({gut/w:.0%}) numcols_left={len(between)}")
json.dump(G, open("gutters.json","w"))
