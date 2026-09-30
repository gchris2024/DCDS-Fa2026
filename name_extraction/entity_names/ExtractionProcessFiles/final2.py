import glob, os, re, json
import numpy as np
from PIL import Image
os.makedirs("/home/claude/read",exist_ok=True); os.makedirs("/home/claude/cols",exist_ok=True)
G={int(k):v for k,v in json.load(open("gutters.json")).items()}
def pn(f): return int(re.search(r"\((\d+)\)", f).group(1))
for f in sorted(glob.glob("/home/claude/Plumer Biographies Index/*.jpg"), key=pn):
    n=pn(f)
    a=np.asarray(Image.open(f).convert("L"),dtype=np.int16)
    thr=int(np.percentile(a,25))-25
    H,W=a.shape
    a=a[int(H*0.03):int(H*0.97), int(W*0.03):int(W*0.97)]
    d=a<thr
    r=np.where(d.sum(axis=1)>max(3,a.shape[1]*0.005))[0]
    c=np.where(d.sum(axis=0)>max(3,a.shape[0]*0.005))[0]
    sub=a[r[0]:r[-1], c[0]:c[-1]]
    gut=G[n]
    for side,(x0,x1) in (("L",(0,gut+8)),("R",(max(0,gut-8),sub.shape[1]))):
        col=sub[:,x0:x1]
        dd=col<thr
        rr=np.where(dd.sum(axis=1)>max(2,col.shape[1]*0.004))[0]
        cc=np.where(dd.sum(axis=0)>max(2,col.shape[0]*0.004))[0]
        col=col[max(0,rr[0]-12):rr[-1]+12, max(0,cc[0]-12):cc[-1]+12]
        img=Image.fromarray(col.astype(np.uint8))
        img.resize((img.size[0]*2,img.size[1]*2),Image.LANCZOS).save(f"/home/claude/cols/p{n:02d}{side}.png")
        cw,ch=img.size
        if ch < cw*1.3: canvas=img
        else:
            mid=ch//2
            top=img.crop((0,0,cw,mid+25)); bot=img.crop((0,mid-25,cw,ch))
            Hc=max(top.size[1],bot.size[1])
            canvas=Image.new("L",(cw*2+40,Hc),255)
            canvas.paste(top,(0,0)); canvas.paste(bot,(cw+40,0))
        s=1560/max(canvas.size)
        canvas=canvas.resize((max(1,int(canvas.size[0]*s)),max(1,int(canvas.size[1]*s))),Image.LANCZOS)
        canvas.save(f"/home/claude/read/p{n:02d}{side}.png")
    print(n,end=" ",flush=True)
