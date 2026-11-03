import os
import sys, math, random, time, itertools, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rv, gen
from test_random_lib import read_reps, CERT
K=8
def rand_reps(m, t, rng):
    c,s=math.cos(2*math.pi/m), math.sin(2*math.pi/m); r=1.0; reps=[]
    for i in range(t):
        a0=rng.uniform(0,2*math.pi); x,y=r*math.cos(a0)*1e9, r*math.sin(a0)*1e9
        b=round(y/s); a=round(x-b*c); reps.append(tuple([a,b]+[0]*(m-2)))
        r*=rng.choice([rng.uniform(0.2,0.6), rng.uniform(0.5,0.98)])
    return reps
def convex_poly(cfg, sg):
    """largest convex polygon via DP with parents; returns vertex list"""
    pts=cfg['pts']; n=len(pts); O=lambda a,b,c: rv.osign(sg,a,b,c); best=(0,None)
    for p in range(n):
        py,px=pts[p][1],pts[p][0]
        A=[q for q in range(n) if q!=p and (pts[q][1]>py or (pts[q][1]==py and pts[q][0]>px))]
        A.sort(key=functools.cmp_to_key(lambda a,b: -1 if O(p,a,b)>0 else 1)); L=len(A)
        dp=[[2]*L for _ in range(L)]; par=[[None]*L for _ in range(L)]
        for j in range(L):
            for i in range(j):
                for k in range(j+1,L):
                    if O(A[i],A[j],A[k])>0 and dp[j][k]<dp[i][j]+1: dp[j][k]=dp[i][j]+1; par[j][k]=i
        for j in range(L):
            for k in range(j+1,L):
                if dp[j][k]+1>best[0]:
                    ch=[k,j]; a,b=j,k
                    while par[a][b] is not None: c=par[a][b]; ch.append(c); a,b=c,a
                    best=(dp[j][k]+1,[p]+[A[x] for x in reversed(ch)])
    return best
def in_convex_position(V, sg):
    O=lambda a,b,c: rv.osign(sg,a,b,c)
    for x in V:
        others=[y for y in V if y!=x]
        for a,b,c in itertools.combinations(others,3):
            s=O(a,b,c)
            if O(a,b,x)==s and O(b,c,x)==s and O(c,a,x)==s: return False
    return True
rng=random.Random(int(sys.argv[1])); budget=float(sys.argv[2])
for m in (4,5,6):
    for t in (3,4,5):
        E,_,_=gen.build(m,K,t); tb=time.time(); st=dict(n=0,viol=0,viol_verified=0,viol_unverified=0,dp_vs_exh_mismatch=0,exh=0)
        while time.time()-tb<budget:
            try:
                cfg=rv.layered(m,rand_reps(m,t,rng)); sg=rv.otable(cfg)
            except RuntimeError: continue
            st['n']+=1
            val,nb=rv.assign(E,cfg,sg); bad=rv.evaluate(E.cls,val,nb,E.nv)
            size,V=convex_poly(cfg,sg)
            assert in_convex_position(V,sg), 'DP polygon not convex'
            if bad:
                st['viol']+=1
                if size>=K: st['viol_verified']+=1
                else: st['viol_unverified']+=1; print('UNVERIFIED VIOLATION', m, t, cfg['theta'], flush=True)
            n=len(cfg['pts'])
            if n<=15 and st['exh']<40:
                st['exh']+=1
                ex=any(in_convex_position(S,sg) for S in itertools.combinations(range(n),K))
                if ex!=(size>=K): st['dp_vs_exh_mismatch']+=1
        print('m=%d t=%d'%(m,t), st, flush=True)
print('DONE', flush=True)
