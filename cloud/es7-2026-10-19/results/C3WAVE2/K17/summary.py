import json, sys, os
T="/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools"
sys.path.insert(0, os.path.join(T,"..","..","C3a")); sys.path.insert(0,T)
from hullcase import tree_children, parse_layers, layers_name
recs=[json.loads(l) for l in open("/opt/work/out.jsonl")]
cert={r["node"] for r in recs if r.get("certified")}
split={r["node"] for r in recs if r.get("split")}
started=set(l.split()[2] for l in open("/opt/work/driver.log") if l.startswith("=== ROOT") and " start " in l)
def closed(n):
    if n in cert: return True
    if n in split: return all(closed(layers_name(c)) for c in tree_children(11,7,parse_layers(n)))
    return False
roots=[l.split("\t")[1] for l in open("/opt/work/roots.tsv").read().splitlines()[1:]]
out=[]
for k,R in enumerate(roots,1):
    rs=[r for r in recs if r["node"]==R or r["node"].startswith(R+"_")]
    d=lambda n: len(parse_layers(n))
    cb={}; sp={}; unk=0
    for r in rs:
        if r.get("certified"): cb[d(r["node"])]=cb.get(d(r["node"]),0)+1
        if r.get("split"): sp[d(r["node"])]=sp.get(d(r["node"]),0)+1
        if r.get("status")=="UNKNOWN": unk+=1
    st="closed" if closed(R) else ("partial" if R in started else "not reached")
    s=dict(idx=k,root=R,status=st,certified_by_depth=cb,splits_by_depth=sp,unknown=unk,
           solve_s=round(sum(r.get("solve_s",0) for r in rs)),check_s=round(sum(r.get("check_s",0) for r in rs)))
    out.append(s); print(json.dumps(s))
