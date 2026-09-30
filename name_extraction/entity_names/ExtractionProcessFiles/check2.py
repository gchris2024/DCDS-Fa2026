import glob, os, re, subprocess
for p in sorted(glob.glob("/home/claude/cols/*.png")):
    txt=subprocess.run(["tesseract",p,"-","--psm","6"],capture_output=True,text=True).stdout
    lines=[l.strip() for l in txt.splitlines() if len(l.strip())>8]
    full=[l for l in lines if re.search(r"\d{3,4}\s*[,.]?\s*\d\s+\d{1,3}\W{0,3}$",l)]
    print(f"{os.path.basename(p)}: lines={len(lines)} wellformed={len(full)}")
