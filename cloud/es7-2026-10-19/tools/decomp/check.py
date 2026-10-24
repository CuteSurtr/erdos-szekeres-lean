import math, itertools, sys
from fractions import Fraction as F

def orient(p,q,r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])

def general_position(P):
    m=min(abs(orient(*t)) for t in itertools.combinations(P,3))
    return m

def convex4(P,idx):
    a,b,c,d=[P[i] for i in idx]
    pts=[a,b,c,d]
    for i in range(4):
        o=[pts[j] for j in range(4) if j!=i]
        s=[orient(o[0],o[1],pts[i]),orient(o[1],o[2],pts[i]),orient(o[2],o[0],pts[i])]
        if (s[0]>0 and s[1]>0 and s[2]>0) or (s[0]<0 and s[1]<0 and s[2]<0):
            return False
    return True

def max_convex(P,kmax):
    n=len(P)
    c4={}
    for q in itertools.combinations(range(n),4):
        c4[q]=convex4(P,q)
    best=4 if any(c4.values()) else 3
    for k in range(5,kmax+1):
        found=False
        for S in itertools.combinations(range(n),k):
            if all(c4[q] for q in itertools.combinations(S,4)):
                found=True;break
        if found: best=k
        else: break
    return best

def rot(P,t):
    c,s=math.cos(t),math.sin(t)
    return [(c*x-s*y, s*x+c*y) for x,y in P]

def above(p,a,b):
    # is p strictly above the line through a,b (non-vertical)
    if a[0]>b[0]: a,b=b,a
    return orient(a,b,p)>0

def decomposable(Q, idxs):
    if len(idxs)<=1: return True
    order=sorted(idxs,key=lambda i:Q[i][1])
    for k in range(1,len(order)):
        A=order[:k]; B=order[k:]
        ok=True
        for a1,a2 in itertools.combinations(A,2):
            for b in B:
                if not above(Q[b],Q[a1],Q[a2]): ok=False;break
            if not ok: break
        if not ok: continue
        for b1,b2 in itertools.combinations(B,2):
            for a in A:
                if above(Q[a],Q[b1],Q[b2]): ok=False;break
            if not ok: break
        if not ok: continue
        if decomposable(Q,A) and decomposable(Q,B): return True
    return False

def critical_dirs(P):
    angs=[]
    for p,q in itertools.combinations(P,2):
        a=math.atan2(q[1]-p[1],q[0]-p[0])
        for d in (0,math.pi/2,math.pi,3*math.pi/2):
            angs.append((-a+d)%(2*math.pi))
    angs.sort()
    ded=[angs[0]]
    for a in angs[1:]:
        if a-ded[-1]>1e-9: ded.append(a)
    if 2*math.pi-ded[-1]+ded[0]<1e-9: ded.pop()
    angs=ded
    mids=[(angs[i]+angs[i+1])/2 for i in range(len(angs)-1)]
    mids.append((angs[-1]+angs[0]+2*math.pi)/2 % (2*math.pi))
    return mids

def decomposable_any_direction(P):
    hits=[]
    for t in critical_dirs(P):
        Q=rot(P,t)
        if decomposable(Q,list(range(len(Q)))):
            hits.append(t)
    return hits

def top_split_dirs(P):
    # directions in which at least a top-level deep-below split exists
    cnt=0
    for t in critical_dirs(P):
        Q=rot(P,t)
        order=sorted(range(len(Q)),key=lambda i:Q[i][1])
        for k in range(1,len(order)):
            A=order[:k];B=order[k:]
            if all(above(Q[b],Q[a1],Q[a2]) for a1,a2 in itertools.combinations(A,2) for b in B) and \
               all(not above(Q[a],Q[b1],Q[b2]) for b1,b2 in itertools.combinations(B,2) for a in A):
                cnt+=1;break
    return cnt

def hull_layers(P):
    idx=list(range(len(P)));layers=[]
    while idx:
        pts=sorted(idx,key=lambda i:P[i])
        if len(pts)<=2: layers.append(len(pts));break
        def half(seq):
            h=[]
            for i in seq:
                while len(h)>=2 and orient(P[h[-2]],P[h[-1]],P[i])<=0: h.pop()
                h.append(i)
            return h
        lo=half(pts);up=half(pts[::-1])
        hull=set(lo[:-1]+up[:-1])
        layers.append(len(hull))
        idx=[i for i in idx if i not in hull]
    return layers
