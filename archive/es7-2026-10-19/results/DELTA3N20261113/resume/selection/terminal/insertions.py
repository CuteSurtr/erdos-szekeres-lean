"""Six fixed insertion controls, not a rightmost cell search."""
from fractions import Fraction as Q
import itertools as it
import json
from pathlib import Path
from check import cap,convex,cross

here=Path(__file__).resolve().parent;data=here/'data'
w=json.loads((data/'witness.json').read_text());p=w['P'];A=w['ordinary_weak_Delta']
g=json.loads((data/'witness.geometry.json').read_text());xmax=p[-1][0];span=xmax-p[0][0]
def height(pair,x):
    a,b=pair;return Q(p[a][1])+Q(p[b][1]-p[a][1],p[b][0]-p[a][0])*(x-p[a][0])
def ceil(q):return -(-q.numerator//q.denominator)
result=[]
for X in (xmax+1,xmax+span,xmax+100*span):
    f4=max(height(t[-2:],X) for t in g['fourcaps'])
    for offset in (1,span):
        Y=ceil(f4)+offset
        while any(cross(p+[[X,Y]],a,b,len(p))==0 for a,b in it.combinations(range(len(p)),2)):Y+=1
        pp=p+[[X,Y]];r=len(p);newcap5=[t+(r,) for t in it.combinations(range(len(p)),4) if cap(pp,t+(r,))]
        newgons=[t+(r,) for t in it.combinations(range(len(p)),6) if convex(pp,t+(r,))]
        enlarged=A+[r]
        assert not newcap5 and not any(cap(pp,t) for t in it.combinations(enlarged,4))
        assert not any(convex(pp,t) for t in it.combinations([i for i in range(len(pp)) if i not in enlarged],6))
        result.append(dict(label='COMPUTED',r=[X,Y],F4=str(f4),Y_minus_F4=str(Q(Y)-f4),
                           no_fivecap=True,no_heptagon=not newgons,new_heptagons=len(newgons),
                           first_new_heptagon=newgons[0] if newgons else None,rooted_weak_Delta=enlarged))
record=dict(scope='Six fixed controls only; universal rooted success for this U already follows from the written all-X domination proof.',
            controls=result)
(data/'insertion_controls.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
