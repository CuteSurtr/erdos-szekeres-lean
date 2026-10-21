import json,glob,sys
base="/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/"
old={}
for f in glob.glob(base+"V1-[0-3]/leaves_cake.jsonl"):
    for l in open(f):
        if l.strip(): r=json.loads(l); old.setdefault(r["i"],[]).append((f.split("/")[-2],r))
mine=[json.loads(l) for l in open(base+"V1R/R0/out.jsonl") if l.strip()]
ok=sum(1 for r in mine if r["solver_exit"]==20 and r["cake_lpr"]=="s VERIFIED UNSAT")
print("records",len(mine),"verified",ok)
print("solve_s total %.1f check_s total %.1f"%(sum(r["solve_s"] for r in mine),sum(r["check_s"] for r in mine)))
if mine:
    m=max(mine,key=lambda r:r["proof_bytes"]); print("largest proof: i=%d %d bytes solve %.1fs"%(m["i"],m["proof_bytes"],m["solve_s"]))
    m=max(mine,key=lambda r:r["solve_s"]); print("longest solve: i=%d %.1fs"%(m["i"],m["solve_s"]))
diffs=[]
for r in mine:
    o=old.get(r["i"])
    if not o: diffs.append("i=%d: no earlier record"%r["i"]); continue
    for src,x in o:
        if x["cube"]!=r["cube"]: diffs.append("i=%d: cube differs from %s"%(r["i"],src))
        if x["solver_exit"]!=r["solver_exit"]: diffs.append("i=%d: solver_exit %s vs %s in %s"%(r["i"],r["solver_exit"],x["solver_exit"],src))
        if x["cake_lpr"]!=r["cake_lpr"]: diffs.append("i=%d: cake_lpr differs from %s"%(r["i"],src))
    if len(o)>1: diffs.append("i=%d: %d earlier records"%(r["i"],len(o)))
bad=[r["i"] for r in mine if not (r["solver_exit"]==20 and r["cake_lpr"]=="s VERIFIED UNSAT")]
print("not verified:",bad)
print("differences (cube/solver_exit/cake_lpr):",len(diffs)); [print(" ",d) for d in diffs]
