import sys, json, hashlib, collections, os, random, subprocess, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
root, fpath, man, out = sys.argv[1:5]; files = sys.argv[5:]
CAD, CAKE = "/opt/cadical/build/cadical", "/opt/cake_lpr/cake_lpr"
raw=open(fpath,'rb').read(); assert hashlib.sha256(raw).hexdigest().startswith("69c1dc8f7818cbef")
hdr, body = raw.split(b"\n",1); nv, nc = map(int, hdr.split()[2:4])
cases=[json.loads(l) for l in open(os.path.join(root,"results/Mii-S/cases.jsonl"))]
cubes=[l for l in open(os.path.join(root,"results/Mii-S/cases.icnf")) if l.startswith("a ")]
cube_of={c["case"]:[int(x) for x in l.split()[1:-1]] for c,l in zip(cases,cubes)}
by=collections.defaultdict(list)
for l in open(man):
    r=json.loads(l); by[r["case"]].append(r["lits"])
rec={}; cov={}
for f in files:
    for l in open(os.path.join(root,f)):
        o=json.loads(l)
        if o["verdict"]!="VERIFIED": continue
        if o["kind"]=="leaf": rec.setdefault((o["case"],json.dumps(o["lits"])),o)
        elif "cnf_sha256" in o: cov.setdefault((o["key"],o["leaves_sha256"]),o)
random.seed(777)
def pick(case,n,maxs=90):
    c=[l for l in by[case] if rec[(case,json.dumps(l))]["solve_s"]<maxs]
    return [(case,l) for l in random.sample(c,min(n,len(c)))]
jobs=[]
for c in ("U_L2","U3_L","U_L7"):
    cc=[l for l in by[c] if 90<=rec[(c,json.dumps(l))]["solve_s"]<400]
    jobs+=[(c,l) for l in random.sample(cc,min(6,len(cc)))]
others=[c for c in by if c not in("U_L2","U3_L","U_L7") and by[c]!=[[]]]
for c in random.sample(others,10): jobs+=pick(c,1)
empt=[c for c in by if by[c]==[[]]]
jobs+=[(c,[]) for c in random.sample(empt,4)]
covcases=[c for c in by if by[c]!=[[]]]
covs=["U_L2","U3_L"]+sorted(random.sample(covcases,4))
def run(data,tag):
    w=tempfile.mkdtemp(dir="/opt/work"); cnf=w+"/f.cnf"; prf=w+"/p.lrat"
    open(cnf,"wb").write(data)
    rc=subprocess.run([CAD,"-q","--lrat","--binary=false",cnf,prf],stdout=subprocess.DEVNULL,timeout=1800).returncode
    line=""
    if rc==20:
        o=subprocess.run([CAKE,cnf,prf],capture_output=True,text=True).stdout
        line=[x.strip() for x in o.splitlines() if x.startswith("s ")]
    shutil.rmtree(w); return rc,line
def leaf(j):
    case,l=j; cb=cube_of[case]; cs=set(cb)
    units=sorted(cb,key=abs)+sorted([x for x in l if x not in cs],key=abs)
    d=b"p cnf %d %d\n"%(nv,nc+len(units))+body+b"".join(b"%d 0\n"%x for x in units)
    sha=hashlib.sha256(d).hexdigest(); r=rec[(case,json.dumps(l))]
    rc,line=run(d,"leaf")
    return {"kind":"leaf","case":case,"lits":l,"my_sha":sha,"sha_eq_record":sha==r["cnf_sha256"],"rec_solve_s":r["solve_s"],"rc":rc,"cake":line}
def cover(case):
    lv=by[case]; cb=cube_of[case]
    cl=[[x] for x in cb]+[[-x for x in l] for l in lv]
    d=("p cnf %d %d\n"%(nv,len(cl))+"".join(" ".join(map(str,c))+" 0\n" for c in cl)).encode()
    sha=hashlib.sha256(d).hexdigest(); ls=hashlib.sha256(json.dumps(lv).encode()).hexdigest()
    r=cov.get((case,ls),{})
    rc,line=run(d,"cover")
    return {"kind":"cover","case":case,"nleaves":len(lv),"my_sha":sha,"sha_eq_record":sha==r.get("cnf_sha256"),"rc":rc,"cake":line}
print("jobs",len(jobs),"covers",len(covs),flush=True)
with open(out,"w") as fo, ThreadPoolExecutor(4) as ex:
    for res in ex.map(lambda j: cover(j) if isinstance(j,str) else leaf(j), covs+jobs):
        fo.write(json.dumps(res)+"\n"); fo.flush()
