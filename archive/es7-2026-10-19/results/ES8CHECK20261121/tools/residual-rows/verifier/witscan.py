"""Scan residual hole-vector witnesses in git: does any violate the endpoint rows? (verify-residual-row)"""
import json, sys, os, gzip
REPO=sys.argv[1]
FLAT=[7,35,80,120,144,153]; SECOND=[1,2,4,7]
def vectors(obj, path=""):
    # yield (path, missing set) for any dict having a 'missing' list or 'holes' list of ints within 0..153 or 'occupied'
    if isinstance(obj, dict):
        for key in ("missing","holes","missing_states","hole_states"):
            v=obj.get(key)
            if isinstance(v,list) and v and all(isinstance(x,int) for x in v) and max(v)<154 and len(v)<154:
                yield path+"/"+key, set(v)
        v=obj.get("occupied")
        if isinstance(v,list) and v and all(isinstance(x,int) for x in v) and max(v)<154 and len(v)>60:
            yield path+"/occupied->missing", set(range(154))-set(v)
        v=obj.get("h") or obj.get("vector") or obj.get("x")
        if isinstance(v,list) and len(v)==154 and all(x in (0,1) for x in v):
            yield path+"/h", {i for i,x in enumerate(v) if x==1}
        for k,val in obj.items():
            if isinstance(val,(dict,list)): yield from vectors(val, path+"/"+str(k))
    elif isinstance(obj, list):
        for i,val in enumerate(obj[:5000]):
            if isinstance(val,(dict,list)): yield from vectors(val, path+f"[{i}]")
files=[l.strip() for l in open(sys.argv[2]) if l.strip()]
tot=0; vf=0; vs=0; seen=set(); per={}
for f in files:
    p=os.path.join(REPO,f)
    try:
        if f.endswith(".jsonl"):
            objs=[json.loads(l) for l in open(p) if l.strip()]
        else:
            objs=[json.load(open(p))]
    except Exception as e:
        continue
    for o in objs:
        for path,M in vectors(o):
            key=(f,tuple(sorted(M)))
            if key in seen: continue
            seen.add(key)
            if 0 in M:  # state 0 missing: not a residual-zero witness
                continue
            tot+=1; per.setdefault("_sizes",{}); per["_sizes"][len(M)]=per["_sizes"].get(len(M),0)+1; per.setdefault("_fs",{}); k=sum(1 for i in FLAT if i in M); per["_fs"][k]=per["_fs"].get(k,0)+1
            a=all(i in M for i in FLAT); b=all(i in M for i in SECOND)
            vf+=a; vs+=b
            d=per.setdefault(f,[0,0,0]); d[0]+=1; d[1]+=a; d[2]+=b
print("witness vectors scanned (state 0 occupied):", tot, "violating flat row:", vf, "violating second row:", vs)
for f,d in per.items(): print(f, d)
