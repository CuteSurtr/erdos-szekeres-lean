# Full-CNF soundness test at N=33, K=8 on the Lean-emitted files: heptagon-free mirror 32-sets
# (results/C/sets) plus one axis point; frame (ii) x-sort (+y-flip) or frame (i) slope order;
# all orientation units appended; CaDiCaL must say SAT for every octagon-free set.
import itertools, random, sys, subprocess, os
from fractions import Fraction as Fr
N=33
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
idx={t:n+1 for n,t in enumerate(itertools.combinations(range(N),3))}
def gp(S): return all(orient(a,b,c)!=0 for a,b,c in itertools.combinations(S,3))
def hullv(S):
    P=sorted(S)
    def half(P):
        h=[]
        for q in P:
            while len(h)>=2 and orient(h[-2],h[-1],q)<=0: h.pop()
            h.append(q)
        return h
    return set(half(P)[:-1]+half(P[::-1])[:-1])
cad, intf, hullf, setsf, per = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
body={}
for name,f in (('int',intf),('hull',hullf)):
    raw=open(f,'rb').read(); h,b=raw.split(b'\n',1); body[name]=(list(map(int,h.split()[2:4])),b)
rnd=random.Random(11); res={}
for line in open(setsf):
    t=line.split(); nm=t[0]; v=list(map(int,t[2:])); pts=list(zip(v[0::2],v[1::2]))
    assert len(pts)==32 and all((-x,y) in pts for x,y in pts)
    ys=sorted(set(y for _,y in pts))
    tries=0; done=0
    while done<per and tries<200:
        tries+=1
        r=rnd.random()
        if r<0.25: y0=ys[-1]+rnd.randint(1,10**8)
        elif r<0.5: y0=ys[0]-rnd.randint(1,10**8)
        else: y0=rnd.randint(ys[0],ys[-1])
        c=(0,y0); S=pts+[c]
        if c in pts or not gp(S): continue
        if c in hullv(S):
            mode='hull'; T=S
            if all(q[1]>y0 for q in pts): T=[(x,-y) for x,y in S]
            p=T[-1]; P=[p]+sorted(T[:-1],key=lambda q:Fr(q[0],p[1]-q[1]))
            sg={t:orient(P[t[0]],P[t[1]],P[t[2]])>0 for t in idx}
        else:
            mode='int'
            P=sorted(S,key=lambda q:(q[0], q[1] if q[0]<0 else -q[1]))
            sg={t:orient(P[t[0]],P[t[1]],P[t[2]])>0 for t in idx}
            if not sg[(0,1,2)]: sg={t:not x for t,x in sg.items()}
        (nv,nc),b=body[mode]
        units=''.join(f"{idx[t] if s else -idx[t]} 0\n" for t,s in sg.items())
        fn=f'/tmp/claude-0/k8/t.cnf'
        open(fn,'wb').write(f"p cnf {nv} {nc+len(sg)}\n".encode()+b+units.encode())
        out=subprocess.run([cad,'-q','-n',fn],capture_output=True,text=True,timeout=600)
        st=out.stdout.strip().splitlines()[0] if out.stdout.strip() else 'rc%d'%out.returncode
        res.setdefault((mode,st),0); res[(mode,st)]+=1
        print(nm,mode,y0,st,flush=True); done+=1
print('SUMMARY',res)
