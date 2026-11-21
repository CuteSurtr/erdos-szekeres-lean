# Exact residual states (math.md 2.1-2.2) for an ordered configuration; own code, integer arithmetic only.
import random, itertools
def orient(a,b,c):  # [a,b,c] = det(b-a, c-a)
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def tables(P):
    n=len(P); O={}
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                o=orient(P[i],P[j],P[k]); assert o!=0
                O[(i,j,k)]=o
    # Ecup[u][v]: longest cup ending with (u,v); Ecap: longest cap ending with (u,v); Fcap: longest cap starting with (u,v)
    Ecup=[[0]*n for _ in range(n)]; Ecap=[[0]*n for _ in range(n)]; Fcap=[[0]*n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            bc=2; bk=2
            for t in range(u):
                o=O[(t,u,v)]
                if o>0: bc=max(bc,Ecup[t][u]+1)
                else: bk=max(bk,Ecap[t][u]+1)
            Ecup[u][v]=bc; Ecap[u][v]=bk
    for u in range(n-1,-1,-1):
        for v in range(n-1,u,-1):
            b=2
            for w in range(v+1,n):
                if O[(u,v,w)]<0: b=max(b,Fcap[v][w]+1)
            Fcap[u][v]=b
    return O,Ecup,Ecap,Fcap
def longest(P,O,sign):
    # longest chain (cup if sign>0, cap if sign<0); returns length
    n=len(P)
    if n<=2: return n
    L={}
    best=min(n,2)
    for v in range(n):
        for u in range(v):
            b=2
            for t in range(u):
                if (O[(t,u,v)]>0)==(sign>0): b=max(b,L[(t,u)]+1)
            L[(u,v)]=b; best=max(best,b)
    return best
def chain_in(P,O,idx,sign):
    # longest chain among the points with indices idx (sorted), using precomputed O
    idx=sorted(idx); m=len(idx)
    if m<=2: return m
    L={}; best=2
    for b_ in range(m):
        for a_ in range(b_):
            v=idx[b_]; u=idx[a_]; b=2
            for c_ in range(a_):
                t=idx[c_]
                if (O[(t,u,v)]>0)==(sign>0): b=max(b,L[(c_,a_)]+1)
            L[(a_,b_)]=b; best=max(best,b)
    return best
def junction_free(n,Ecup,Fcap):
    # junction: 6-cup ending at v and 5-cap starting at v
    for v in range(n):
        cupend=max([Ecup[u][v] for u in range(v)]+[1])
        capstart=max([Fcap[v][w] for w in range(v+1,n)]+[1])
        if cupend>=6 and capstart>=5: return False
    return True
def states(P,O=None,Ecup=None,Fcap=None):
    n=len(P)
    if O is None: O,Ecup,Ecap,Fcap=tables(P)
    St=[]
    for v in range(n):
        labs=[(6-Fcap[u][v],Ecup[u][v]-1) for u in range(v)]
        for d1,d2 in labs: assert 1<=d1<=4 and 1<=d2<=6, (d1,d2)
        f=tuple(max([d2 for d1,d2 in labs if d1>=a]+[0]) for a in (1,2,3,4))
        St.append(f)
    return St
