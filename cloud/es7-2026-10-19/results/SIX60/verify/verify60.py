#!/usr/bin/env python3
"""Coordinator's independent exact verifier for a sixfold point set given as rows w_0..w_5 (point = sum w_j zeta^j,
zeta = e^{2 pi i/6}).  Uses oblique integer coordinates z = a + b*zeta (affine image of the plane with positive
determinant, so orientation signs and convex position are preserved).  Checks:
  (1) 60 distinct points, origin absent, set closed under z -> zeta*z;
  (2) general position: all C(60,3) orientations nonzero;
  (3) largest subset in convex position, by two independently anchored O(n^4) dynamic programs
      (anchor = lowest point in (b,a)-order, and anchor = leftmost point in (a,b)-order).
Standard library only; exact integers."""
import sys, itertools, hashlib
from functools import cmp_to_key
raw=open(sys.argv[1],'rb').read(); print('sha256', hashlib.sha256(raw).hexdigest())
P=[]
for line in raw.decode().splitlines():
    line=line.split('#')[0].strip()
    if not line: continue
    w=list(map(int,line.split())); assert len(w)==6
    a=w[0]-w[2]-w[3]+w[5]; b=w[1]+w[2]-w[4]-w[5]   # 1,z,z^2=z-1,z^3=-1,z^4=-z,z^5=1-z
    P.append((a,b))
n=len(P); print('points', n)
assert len(set(P))==n, 'duplicate points'
assert (0,0) not in P, 'origin present'
S=set(P); rot=lambda p:(-p[1],p[0]+p[1])
assert all(rot(p) in S for p in P), 'not closed under 60-degree rotation'
print('distinct, origin absent, rotation-closed: OK')
def cr(o,p,q): return (p[0]-o[0])*(q[1]-o[1])-(p[1]-o[1])*(q[0]-o[0])
zero=sum(1 for x,y,z in itertools.combinations(P,3) if cr(x,y,z)==0)
print('collinear triples', zero); assert zero==0
def largest(key):
    best=0; bestset=None
    for p in P:
        Q=[q for q in P if key(q)>key(p)]
        Q.sort(key=cmp_to_key(lambda u,v: -1 if cr(p,u,v)>0 else 1))
        m=len(Q); L={}
        for j in range(m):
            for i in range(j):
                v=3; 
                for h in range(i):
                    if (h,i) in L and cr(Q[h],Q[i],Q[j])>0 and L[(h,i)]+1>v: v=L[(h,i)]+1
                L[(i,j)]=v
                if cr(Q[i],Q[j],p)>0 and v>best: best=v
    return best
k1=largest(lambda q:(q[1],q[0])); print('largest convex subset (anchor lowest):', k1)
k2=largest(lambda q:(q[0],q[1])); print('largest convex subset (anchor leftmost):', k2)
print('RESULT', 'NO 8 POINTS IN CONVEX POSITION' if max(k1,k2)<=7 else 'CONTAINS A CONVEX OCTAGON', 'max', max(k1,k2))
