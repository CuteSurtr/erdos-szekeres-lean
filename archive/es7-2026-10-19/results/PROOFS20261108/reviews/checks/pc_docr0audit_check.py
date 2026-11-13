# Exact check of the opening claim of pc.tex (hunk 1), angles in units of pi (Fractions).
# For alpha<beta<delta<alpha+2: the six points alpha,beta,delta,alpha+1,beta+1,delta+1 (mod 2) are
# distinct  <=>  no gap (beta-alpha, delta-beta, alpha+2-delta) equals 1;
# some gap equals 1 <=> some direction coincides with some antipode (mod 2).
from fractions import Fraction as F
from itertools import product
def mod2(x):
    q = x - 2*(x//2)
    return q
N=24
mism=0; tot=0; gapcases=0
for a0 in [F(0),F(1,7),F(-5,3)]:
    for j,k in product(range(1,2*N),range(1,2*N)):
        b=a0+F(j,N); d=a0+F(k,N)
        if not (a0<b<d<a0+2): continue
        tot+=1
        dirs=[a0,b,d]; anti=[x+1 for x in dirs]
        pts=[mod2(x) for x in dirs+anti]
        distinct = len(set(pts))==6
        gaps=[b-a0,d-b,a0+2-d]
        nogap = all(g!=1 for g in gaps)
        coincide = any(mod2(x)==mod2(y) for x in dirs for y in anti)
        if nogap: pass
        else: gapcases+=1
        if distinct!=nogap: mism+=1
        if (not nogap)!=coincide: mism+=1
print("triples",tot,"gap=pi cases",gapcases,"mismatches",mism)
