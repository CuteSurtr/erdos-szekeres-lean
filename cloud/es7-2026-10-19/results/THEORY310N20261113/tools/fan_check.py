"""Empirical check of fan monotonicity on random real point sets (exact ints)."""
import random, itertools
def orient(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
def labels(P):
    n=len(P); Ep={}; Em={}; Fm={}; Fp={}
    for v in range(n):
        for u in range(v):
            Ep[u,v]=1+max([Ep[x,u] for x in range(u) if orient(P[x],P[u],P[v])>0]+[1])
            Em[u,v]=1+max([Em[x,u] for x in range(u) if orient(P[x],P[u],P[v])<0]+[1])
    for u in range(n-1,-1,-1):
        for v in range(n-1,u,-1):
            Fm[u,v]=1+max([Fm[v,y] for y in range(v+1,n) if orient(P[u],P[v],P[y])<0]+[1])
            Fp[u,v]=1+max([Fp[v,y] for y in range(v+1,n) if orient(P[u],P[v],P[y])>0]+[1])
    return Ep,Em,Fm,Fp
rng=random.Random(13)
bad=0; tot=0
for trial in range(60):
    n=rng.randint(8,22)
    xs=sorted(rng.sample(range(10**6),n)); P=[(x,rng.randint(-10**6,10**6)) for x in xs]
    Ep,Em,Fm,Fp=labels(P)
    for p,q,r in itertools.combinations(range(n),3):
        o=orient(P[p],P[q],P[r]); tot+=1
        if o==0: continue
        cup=o>0
        ok = (Ep[p,r]>=Ep[p,q] and Em[p,r]<=Em[p,q] and Fm[p,r]<=Fm[q,r] and Fp[p,r]>=Fp[q,r]) if cup else \
             (Ep[p,r]<=Ep[p,q] and Em[p,r]>=Em[p,q] and Fm[p,r]>=Fm[q,r] and Fp[p,r]<=Fp[q,r])
        bad+= not ok
print('triples',tot,'violations',bad)
