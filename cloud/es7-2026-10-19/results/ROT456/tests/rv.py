import os
import sys, itertools, math, random, json, time, functools
from decimal import Decimal as D, getcontext
getcontext().prec = 90
sys.path.insert(0, os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'), 'C7UPPER'))
import gen

def zpow(m):
    if m == 4: return [(D(1),D(0)),(D(0),D(1)),(D(-1),D(0)),(D(0),D(-1))]
    if m == 6:
        s = D(3).sqrt()/2; h = D(1)/2
        return [(D(1),D(0)),(h,s),(-h,s),(D(-1),D(0)),(-h,-s),(h,-s)]
    if m == 5:
        r5 = D(5).sqrt(); c1=(r5-1)/4; s1=(10+2*r5).sqrt()/4; c2=-(r5+1)/4; s2=(10-2*r5).sqrt()/4
        return [(D(1),D(0)),(c1,s1),(c2,s2),(c2,-s2),(c1,-s1)]
def wval(w, Z):
    return (sum(D(a)*Z[j][0] for j,a in enumerate(w)), sum(D(a)*Z[j][1] for j,a in enumerate(w)))
def shift(w):  # multiply by zeta
    return tuple([w[-1]]+list(w[:-1]))

MINDET=[None]
def orient(a,b,c,eps):
    d=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    if abs(d) < eps: raise RuntimeError('near-degenerate triple')
    ad=abs(d)
    if MINDET[0] is None or ad<MINDET[0]: MINDET[0]=ad
    return 1 if d>0 else -1

def layered(m, reps):
    """reps: list of weight vectors (one per layer, any order). returns labelled config dict or raises."""
    Z = zpow(m)
    layers=[]
    for w in reps:
        orb=[w]
        for _ in range(m-1): orb.append(shift(orb[-1]))
        P=[wval(x,Z) for x in orb]
        layers.append(P)
    layers.sort(key=lambda P: -(P[0][0]**2+P[0][1]**2))
    M=max(max(abs(x),abs(y)) for P in layers for (x,y) in P)
    eps=M*M*D(10)**-60
    r2=[P[0][0]**2+P[0][1]**2 for P in layers]
    for i in range(len(r2)-1):
        if not r2[i]-r2[i+1] > eps: raise RuntimeError('radii not strictly decreasing')
    t=len(layers)
    ang=lambda p: math.atan2(float(p[1]), float(p[0]))
    a0=ang(layers[0][0])
    u=2*math.pi/m
    pts=[None]*(t*m); theta=[0.0]*t
    for i,P in enumerate(layers):
        lab={}
        for p in P:
            ph=(ang(p)-a0)%(2*math.pi)
            if i==0:
                k=int(round(ph/u))%m; th=0.0
            else:
                k=int(ph//u); th=ph-k*u
            if k in lab: raise RuntimeError('label clash')
            lab[k]=p
            if i>0: theta[i]=th
        for k in range(m): pts[i*m+k]=lab[k]
    psi=[(th % (math.pi/m)) if m%2 else th for th in theta]
    # genericity margins
    sep=min([abs(psi[i]-psi[j]) for i in range(t) for j in range(i+1,t)]+[psi[i] for i in range(1,t)]+([abs(theta[i]-math.pi/m) for i in range(1,t)] if m%2 else [])+[10.0])
    if sep<1e-9: raise RuntimeError('non-generic phases sep=%g'%sep)
    # nesting: every point of layer j>i strictly left of each ccw edge of layer i
    for i in range(t):
        for k in range(m):
            a=pts[i*m+k]; b=pts[i*m+(k+1)%m]
            for x in range(i*m+m, t*m):
                if orient(a,b,pts[x],eps)<0: raise RuntimeError('not nested')
    return dict(m=m,t=t,pts=pts,theta=theta,psi=psi,eps=eps,sep=sep)

def otable(cfg):
    pts=cfg['pts']; n=len(pts); eps=cfg['eps']
    sg={}
    for T in itertools.combinations(range(n),3):
        sg[T]=orient(pts[T[0]],pts[T[1]],pts[T[2]],eps)   # raises on non-GP
    return sg
def osign(sg,a,b,c):
    T,par=gen.Enc.sortpar((a,b,c)); return par*sg[T]

def assign(E, cfg, sg):
    m=E.m; nb=E.ntriplevars+len(E.Y)+len(E.H)
    val={}
    for T,(C,par) in E.canon.items():
        v=E.tvar[C]; b=(par*sg[T]>0)
        if v in val and val[v]!=b: raise RuntimeError('orbit inconsistency (symmetry broken)')
        val[v]=b
    for (i,j),v in E.Y.items(): val[v]=cfg['psi'][i]<cfg['psi'][j]
    for i,v in E.H.items(): val[v]=cfg['theta'][i]<math.pi/m
    return val, nb

def evaluate(clauses, val, nb, nv):
    A=bytearray(nv+1)
    for v,b in val.items(): A[v]=1 if b else 0
    def tr(l): return A[l]==1 if l>0 else A[-l]==0
    for cl in clauses:      # pass 1: least fixpoint (clauses are in dependency order)
        if any(tr(l) for l in cl): continue
        pos=[l for l in cl if l>nb]
        if len(pos)==1: A[pos[0]]=1
    bad=[]
    for idx,cl in enumerate(clauses):
        if not any(tr(l) for l in cl): bad.append(idx)
    return bad

def maxconvex(n, sg, K):
    best=0
    O=lambda a,b,c: osign(sg,a,b,c)
    for p in range(n):
        # p is lowest in the lexicographic order induced by a generic direction: use orientation-free angular sort
        # we need p extreme: take only q with angle in [0,pi) w.r.t. a fixed direction -> use coordinates
        pass
    return best

def maxconvex_xy(cfg, sg, K):
    pts=cfg['pts']; n=len(pts); best=0
    O=lambda a,b,c: osign(sg,a,b,c)
    for p in range(n):
        py,px=pts[p][1],pts[p][0]
        A=[q for q in range(n) if q!=p and (pts[q][1]>py or (pts[q][1]==py and pts[q][0]>px))]
        A.sort(key=functools.cmp_to_key(lambda a,b: -1 if O(p,a,b)>0 else 1))
        L=len(A)
        dp=[[2]*L for _ in range(L)]
        for j in range(L):
            for i in range(j):
                d=dp[i][j]
                for k in range(j+1,L):
                    if O(A[i],A[j],A[k])>0 and dp[j][k]<d+1: dp[j][k]=d+1
        mx=max([max(r) for r in dp]+[1]) if L>=2 else L
        best=max(best,1+mx if L>=2 else 1+L)
    return best
