import json,sys,os,hashlib,subprocess,time,random
sys.path.insert(0,"/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3a")
from c3cnf import C3Enc
M=11;N=33;E=C3Enc(M,7)
# independent layer order / units (own code, using only E.ccw and E.sig literals)
def parse(name):
    out=[]
    for lay in name.split("_"):
        L=[]
        for t in lay.split("-"):
            if "s" in t: r,s=t.split("s"); L.append((int(r),int(s)))
            else: L.append((int(t),None))
        out.append(L)
    return out
def sig(i,L):  # sigma of label i given layer spec residue sigmas
    r=i%M; w=i//M; s=dict(L)[r]
    return s if w!=1 else 1-s
def units(name):
    us=[];used=set()
    for L in parse(name):
        for r,s in L:
            if s is not None and r!=0: us.append(E.sig(r) if s else -E.sig(r))
        pts=[r+w*M for r,_ in L for w in range(3)]
        if len(L)==1: order=[pts[0],pts[2],pts[1]]
        else: order=sorted(pts,key=lambda i:(sig(i,L),i))
        rest=[w for w in range(N) if w not in used]
        for t in range(len(order)):
            u,v=order[t],order[(t+1)%len(order)]
            us+=[E.ccw(u,v,w) for w in rest if w not in (u,v)]
        used|=set(order)
    return us
base=open("/opt/audit/base.cnf","rb").read()
hdr,body=base.split(b"\n",1)
h=hdr.split()
def run(f,r):
    node=r["node"];us=units(node)
    cnf=f"/opt/audit/work/{node}.cnf";prf=cnf[:-4]+".lrat"
    data=f"p cnf {int(h[2])} {int(h[3])+len(us)}\n".encode()+body+"".join(f"{u} 0\n" for u in us).encode()
    open(cnf,"wb").write(data)
    rec={"src":f,"node":node,"units":len(us),"units_rec":r["units"],"sha":hashlib.sha256(data).hexdigest()}
    rec["sha_match"]=rec["sha"]==r["cnf_sha256"]
    t=time.time()
    o=subprocess.run(["/opt/build/cadical/build/cadical","-q","--lrat","--binary=false",cnf,prf],capture_output=True,text=True).stdout
    rec["status"]=next((l[2:] for l in o.splitlines() if l.startswith("s ")),"UNKNOWN");rec["solve_s"]=round(time.time()-t,1)
    if rec["status"]=="UNSATISFIABLE":
        t=time.time()
        o=subprocess.run(["/opt/build/cake_lpr/cake_lpr","--CML_HEAP_SIZE=5000","--CML_STACK_SIZE=1000",cnf,prf],capture_output=True,text=True)
        rec["cake_lpr"]=(o.stdout.strip().splitlines() or ["none"])[0];rec["check_s"]=round(time.time()-t,1)
        rec["proof_bytes"]=os.path.getsize(prf)
    for x in (cnf,prf):
        if os.path.exists(x): os.remove(x)
    return rec
if __name__=="__main__":
    import concurrent.futures as cf
    pick=json.load(open(sys.argv[1]))
    with cf.ProcessPoolExecutor(int(sys.argv[3])) as ex, open(sys.argv[2],"a") as fo:
        for rec in ex.map(lambda x: None, []): pass
        futs=[ex.submit(run,f,r) for f,r in pick]
        for fu in cf.as_completed(futs):
            fo.write(json.dumps(fu.result())+"\n");fo.flush()
