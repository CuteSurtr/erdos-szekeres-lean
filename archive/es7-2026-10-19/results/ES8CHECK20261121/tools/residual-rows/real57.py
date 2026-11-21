import json
from fractions import Fraction
from resstate import *
D=json.load(open('<repo>/archive/es7-2026-10-19/results/THEORY310N20261113/data/residual57_points.json'))
pts=D['R_chart_points']
def toF(z):
    if isinstance(z,str): return Fraction(z)
    if isinstance(z,list) and len(z)==2: return Fraction(int(z[0]),int(z[1]))
    return Fraction(z)
P=[(toF(p[0]),toF(p[1])) for p in pts]
# scale to integers (exact)
import math
den=1
for x,y in P: den=den*x.denominator//math.gcd(den,x.denominator); den=den*y.denominator//math.gcd(den,y.denominator)
P=sorted((int(x*den),int(y*den)) for x,y in P)
assert len(set(p[0] for p in P))==len(P)
O,Ecup,Ecap,Fcap=tables(P); n=len(P)
print('n',n,'longest cap',longest(P,O,-1),'longest cup',longest(P,O,+1),'junction-free',junction_free(n,Ecup,Fcap))
St=states(P,O,Ecup,Fcap); print('injective',len(set(St))==n)
fam={'F':lambda s:s[0]>=5,'Lo':lambda s:s[0]<=4,'F&A2':lambda s:s[0]>=5 and s[3]>=2,'A2':lambda s:s[3]>=2,'f4=0':lambda s:s[3]==0,
     'F&f4=0':lambda s:s[0]>=5 and s[3]==0,'Lo&f4=0':lambda s:s[0]<=4 and s[3]==0,'f1=6':lambda s:s[0]==6,'flat':lambda s:s[0]==s[1]==s[2]==s[3]>=1}
import gzip
d=json.load(gzip.open('<repo>/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
CAT=[tuple(s[:4]) for s in d['states']]
for k,f in fam.items():
    tot=sum(1 for s in CAT if f(s)); occ=sum(1 for s in St if f(s))
    print(f'{k:8s} states {tot:3d} occupied {occ:3d} holes {tot-occ:3d}')
idx={s:i for i,s in enumerate(CAT)}
assert all(s in idx for s in St)
occ=set(idx[s] for s in St)
viol=[c for c in d['constraints'] if sum(1 for i in c['support'] if i not in occ)<c['rhs']]
print('2650 rows violated by this real set:',len(viol))
json.dump({'n':n,'states':St},open('real57_states.json','w'))
