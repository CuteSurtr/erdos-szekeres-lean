import math, itertools
from fractions import Fraction
def pts(m,rho,D):
    P=[]
    for k in range(m): P.append(('v%d'%k,(math.cos(2*math.pi*k/m),math.sin(2*math.pi*k/m))))
    for k in range(m): P.append(('w%d'%k,(rho*math.cos(D+2*math.pi*k/m),rho*math.sin(D+2*math.pi*k/m))))
    return P
def convex(S):
    # points in convex position iff each is a vertex of hull: use monotone chain hull size
    Q=sorted(S)
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in Q:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(Q):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return len(lo)+len(up)-2==len(S)
m=8
for Ddeg,g in [(0.375,0.997268),(5,0.960094),(15,0.858719)]:
    D=math.radians(Ddeg)
    for rho in (g*(1+2e-6),):
        P=pts(m,rho,D); found=[]
        for c in itertools.combinations(range(16),9):
            if convex([P[i][1] for i in c]): found.append([P[i][0] for i in c])
        print('D=%g rho=%.7f  convex 9-sets:'%(Ddeg,rho),len(found)); 
        for f in found[:4]: print('   ',f)
