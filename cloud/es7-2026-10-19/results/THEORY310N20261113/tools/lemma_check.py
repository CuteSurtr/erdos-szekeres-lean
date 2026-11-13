"""Empirical check of Lemmas A and B on random point sets (exact integers).
Generates random sets, keeps those that are residual / balanced, verifies the claims."""
import random, itertools
def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
def chains(P):
    n=len(P); cupE={}; capE={}; cupS={}; capS={}
    for v in range(n):
        for u in range(v):
            cupE[u,v]=1+max([cupE[x,u] for x in range(u) if o(P[x],P[u],P[v])>0]+[1])
            capE[u,v]=1+max([capE[x,u] for x in range(u) if o(P[x],P[u],P[v])<0]+[1])
    for u in range(n-1,-1,-1):
        for v in range(n-1,u,-1):
            cupS[u,v]=1+max([cupS[v,y] for y in range(v+1,n) if o(P[u],P[v],P[y])>0]+[1])
            capS[u,v]=1+max([capS[v,y] for y in range(v+1,n) if o(P[u],P[v],P[y])<0]+[1])
    return cupE,capE,cupS,capS
def convex8(P):
    n=len(P)
    for S in itertools.combinations(range(n),8):
        ok=True
        for a,b,c,d in itertools.combinations(S,4):
            pts=[P[a],P[b],P[c],P[d]]
            # point-in-triangle test for each point
            for k in range(4):
                t=[pts[j] for j in range(4) if j!=k]; x=pts[k]
                s1=o(t[0],t[1],x); s2=o(t[1],t[2],x); s3=o(t[2],t[0],x)
                if (s1>0 and s2>0 and s3>0) or (s1<0 and s2<0 and s3<0): ok=False; break
            if not ok: break
        if ok: return True
    return False
def longest(P, sub, kind):
    # longest cup (kind=+1) or cap (-1) inside index subset sub, and per-vertex end lengths
    sub=sorted(sub); m=len(sub); E={}
    best=1 if m else 0; endlen={v:1 for v in sub}; startlen={v:1 for v in sub}
    for j in range(m):
        for i in range(j):
            u,v=sub[i],sub[j]
            E[u,v]=1+max([E[x,u] for x in sub[:i] if (o(P[x],P[u],P[v])>0)==(kind>0)]+[1])
            best=max(best,E[u,v]); endlen[v]=max(endlen[v],E[u,v])
    # start lengths via reversal
    S={}
    for i in range(m-1,-1,-1):
        for j in range(m-1,i,-1):
            u,v=sub[i],sub[j]
            S[u,v]=1+max([S[v,y] for y in sub[j+1:] if (o(P[u],P[v],P[y])>0)==(kind>0)]+[1])
            startlen[u]=max(startlen[u],S[u,v])
    return best,endlen,startlen
rng=random.Random(2026)
cnt={'res':0,'bal':0}; bad=0
for trial in range(4000):
    n=rng.randint(9,14); xs=sorted(rng.sample(range(10**4),n)); P=[(x,rng.randint(-10**4,10**4)) for x in xs]
    if any(o(*t)==0 for t in itertools.combinations(P,3)): continue
    allidx=range(n)
    cupmax,cupend,cupstart=longest(P,allidx,+1); capmax,capend,capstart=longest(P,allidx,-1)
    junction=any(cupend[v]>=6 and capstart[v]>=5 for v in allidx)
    if capmax<=5 and not junction and cupmax<=7:
        if convex8(P): continue
        cnt['res']+=1
        R6=[v for v in allidx if cupend[v]>=6]; Rlow=[v for v in allidx if cupend[v]<6]; R7=[v for v in allidx if cupend[v]>=7]
        if longest(P,R6,-1)[0]>=5: bad+=1; print('A(i) fails',P)
        if longest(P,Rlow,+1)[0]>=6: bad+=1; print('A(ii) fails',P)
        if any(capstart[v]>=4 for v in R7): bad+=1; print('A(iii) fails',P)
    if capmax<=6 and cupmax<=6:
        if convex8(P): continue
        cnt['bal']+=1
        H6=[v for v in allidx if cupend[v]>=6]; Hl=[v for v in allidx if cupend[v]<6]; Hc=[v for v in allidx if capend[v]>=6]
        if longest(P,H6,-1)[0]>=6: bad+=1; print('B H6 fails',P)
        if longest(P,Hl,+1)[0]>=6: bad+=1; print('B low fails',P)
        if longest(P,Hc,+1)[0]>=6: bad+=1; print('B H^6 fails',P)
print('residual sets',cnt['res'],'balanced sets',cnt['bal'],'violations',bad)
