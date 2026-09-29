import csv, glob, os, re

# Notes for pages 1-5, which were transcribed before the Notes column was added.
PATCH = {
 ("Allison Francis","1777","2","565"):"printed without comma after surname",
 ("Atlee, Wm. Augustus","","3","555"):"no year printed",
 ("Baldwin Loammi","1807","4","400"):"printed without comma after surname",
 ("Baxter Samuel","1804","4","302"):"printed without comma after surname",
 ("Bartine, John","1815","5","45"):"printed out of alphabetical order, among the Barnards",
 ("Belknap, Hannah","1779","2","28"):"handwritten 3 written over the printed volume 2",
 ("Bellomont, Richard Earl of","","1","525"):"no year printed",
 ("Berry; Thomas","1750","2","290"):"1756 written beside the year in pencil",
 ("Blanchard, Jonathan","1788","3","307"):"page 307 struck through in pencil; 290 written beside it",
 ("Boylston, Ward Nicholas","","5","438"):"no year printed",
 ("Brattle William","1776","2","554"):"printed without comma after surname",
 ("Buss, John","1736","2","147"):"printed without comma before year",
 ("Carey, Thomas","1730","2","110"):"page 110 struck through in pencil; 116 written beside it",
 ("Currier, Thomas","1735","2","143"):"printed out of alphabetical order, among the Carters",
 ("Berkley Warborne","1770","2","431"):"printed without comma after surname",
 ("Dame John","1818","5","188"):"printed without comma after surname",
}

rows=[]
for f in sorted(glob.glob("data2/p*.txt")):
    page=int(re.search(r"p(\d+)",os.path.basename(f)).group(1))
    for ln in open(f, encoding="utf-8"):
        ln=ln.rstrip("\n")
        if not ln.strip(): continue
        parts=ln.split("|")
        while len(parts)<5: parts.append("")
        name,year,vol,pg,note = [p.strip() for p in parts[:5]]
        if not note:
            note = PATCH.get((name,year,vol,pg),"")
        rows.append({"Name":name,"Year":year,"Volume":vol,"Page":pg,
                     "Notes":note,"Index Page":page})

out="/mnt/user-data/outputs/Plumer_Biographies_Index.csv"
os.makedirs(os.path.dirname(out),exist_ok=True)
with open(out,"w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=["Name","Year","Volume","Page","Notes","Index Page"])
    w.writeheader(); w.writerows(rows)

print("total rows:", len(rows))
bad_vol=[r for r in rows if r["Volume"] not in {"1","2","3","4","5"}]
no_year=[r for r in rows if not r["Year"]]
no_page=[r for r in rows if not r["Page"]]
odd_year=[r for r in rows if r["Year"] and not (1500<=int(r["Year"])<=1860)]
big_page=[r for r in rows if r["Page"] and int(r["Page"])>700]
noted=[r for r in rows if r["Notes"]]
print("volume not 1-5:", [(r['Name'],r['Volume']) for r in bad_vol])
print("missing year:", len(no_year), " missing page:", len(no_page))
print("year out of range:", [(r['Name'],r['Year']) for r in odd_year])
print("page > 700:", [(r['Name'],r['Page']) for r in big_page])
print("rows with notes:", len(noted))
print("volume distribution:", {v:sum(1 for r in rows if r['Volume']==v) for v in ['1','2','3','4','5','6']})
