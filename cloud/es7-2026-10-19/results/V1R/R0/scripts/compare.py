import json,glob
base="/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/"
cubes=[tuple(int(x) for x in l.split()[1:-1]) for l in open(base+"verify/hull_leaves.icnf")]
idx={c:k for k,c in enumerate(cubes)}
old={}; notes=set()
for f in sorted(glob.glob(base+"results/V1-[0-3]/leaves_cake.jsonl")):
    src=f.split("/")[-2]
    for l in open(f):
        if not l.strip(): continue
        x=json.loads(l); c=tuple(x["cube"])
        k=x["i"] if "i" in x else x["line"]
        if idx.get(c)!=k: notes.add("%s: index field %s=%s but cube is at 0-based %s"%(src,"i" if "i" in x else "line",k,idx.get(c)))
        old.setdefault(c,[]).append((src,x))
mine=[json.loads(l) for l in open(base+"results/V1R/R0/out.jsonl") if l.strip()]
ver=lambda r: r["solver_exit"]==20 and r["cake_lpr"]=="s VERIFIED UNSAT"
print("records",len(mine),"verified",sum(map(ver,mine)),"of share 300")
print("solve_s total %.1f, check_s total %.1f"%(sum(r["solve_s"] for r in mine),sum(r["check_s"] for r in mine)))
if mine:
    m=max(mine,key=lambda r:r["proof_bytes"]); print("largest proof: i=%d %d bytes, solve %.1fs, check %.1fs"%(m["i"],m["proof_bytes"],m["solve_s"],m["check_s"]))
    m=max(mine,key=lambda r:r["solve_s"]); print("longest solve: i=%d %.1fs"%(m["i"],m["solve_s"]))
print("not verified:",[r["i"] for r in mine if not ver(r)])
d=[]
for r in mine:
    c=tuple(r["cube"])
    if cubes[r["i"]]!=c: d.append("i=%d: my cube differs from the file"%r["i"])
    o=old.get(c)
    if not o: d.append("i=%d: no earlier record with this cube"%r["i"]); continue
    if len(o)>1: d.append("i=%d: %d earlier records (%s)"%(r["i"],len(o),",".join(s for s,_ in o)))
    for s,x in o:
        if x["solver_exit"]!=r["solver_exit"]: d.append("i=%d: solver_exit %s vs %s in %s"%(r["i"],r["solver_exit"],x["solver_exit"],s))
        if x["cake_lpr"].replace("s ","",1)!=r["cake_lpr"].replace("s ","",1): d.append("i=%d: cake_lpr %r vs %r in %s"%(r["i"],r["cake_lpr"],x["cake_lpr"],s))
srcs=sorted({s for r in mine for s,_ in old.get(tuple(r["cube"]),[])}); print("earlier records matched from:",srcs)
print("index-field notes on earlier records (first per source):"); seen=set()
for n in sorted(notes):
    if n.split(":")[0] not in seen: seen.add(n.split(":")[0]); print(" ",n)
print("  total such notes:",len(notes))
print("differences:",len(d)); [print(" ",x) for x in d]
