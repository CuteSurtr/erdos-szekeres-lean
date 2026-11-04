#!/usr/bin/env python3
"""Independent check of the GP cuts (written by the coordinator, not the altcert agent).
For each clause with its quintuple (a,b,c,d,e):
  * the 3-term Grassmann-Pluecker identity [abc][ade] - [abd][ace] + [abe][acd] = 0 (anchor a)
    holds for all points (checked symbolically on random integer points below);
  * the clause forbids exactly one assignment of its variables; under that assignment the three
    terms T0=[abc][ade], T1=-[abd][ace], T2=[abe][acd] must all have the same sign -> impossible
    in general position, so the clause holds for every real configuration;
  * every variable of the clause is the orbit variable of one of the six brackets (no extra literal).
Literal semantics are taken from gen.py Enc(6,8,10).o(x,y,z) = literal for orient(x,y,z) = +.
Also: random real sixfold configurations (generic) must satisfy every clause."""
import sys, json, importlib.util, random, math
from fractions import Fraction
import os, pathlib
R=os.environ.get('ES_RESULTS', str(pathlib.Path(__file__).resolve().parents[2]))
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E=G.Enc(6,8,10)
clauses=[list(map(int,l.split()))[:-1] for l in open(sys.argv[1]) if l.strip()]
wits=[json.loads(l) for l in open(sys.argv[2])]
assert len(clauses)==len(wits)
# 1. the identity with this anchor/sign convention, on random integer points (exact)
def det(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
for _ in range(2000):
    P=[(random.randint(-99,99),random.randint(-99,99)) for _ in range(5)]
    a,b,c,d,e=P
    assert det(a,b,c)*det(a,d,e)-det(a,b,d)*det(a,c,e)+det(a,b,e)*det(a,c,d)==0
bad=0
for cl,w in zip(clauses,wits):
    assert cl==w['clause'], 'clause/witness mismatch'
    a,b,c,d,e=w['quintuple']; assert len({a,b,c,d,e})==5 and all(0<=x<60 for x in (a,b,c,d,e))
    forb={abs(l):(l<0) for l in cl}   # forbidden assignment: every literal false
    assert len(forb)==len(cl), 'repeated variable'
    def sg(x,y,z):
        lit=E.o(x,y,z); v=abs(lit); assert v in forb, 'bracket var not in clause'
        val=forb[v] if lit>0 else (not forb[v]); return 1 if val else -1
    br=[(a,b,c),(a,d,e),(a,b,d),(a,c,e),(a,b,e),(a,c,d)]
    used={abs(E.o(*t)) for t in br}
    if used!=set(forb): bad+=1; print('extra/missing var', cl, used); continue
    T0=sg(a,b,c)*sg(a,d,e); T1=-sg(a,b,d)*sg(a,c,e); T2=sg(a,b,e)*sg(a,c,d)
    if not (T0==T1==T2): bad+=1; print('NOT a GP-forbidden pattern', cl)
print('clauses', len(clauses), 'bad', bad)
# 2. random generic sixfold configurations, nested radii, phases in (0,60): every clause must hold
def config():
    rs=sorted([math.exp(random.uniform(-9,0)) for _ in range(10)], reverse=True); rs[0]=1.0
    th=[0.0]+[random.uniform(0.001,math.pi/3-0.001) for _ in range(9)]
    pts=[]
    for i in range(10):
        for k in range(6):
            ang=th[i]+k*math.pi/3; pts.append((rs[i]*math.cos(ang), rs[i]*math.sin(ang)))
    return pts
viol=0; tested=0
for _ in range(300):
    P=config(); val={}
    for T,v in E.tvar.items():
        dd=det(P[T[0]],P[T[1]],P[T[2]]); val[v]=dd>0
    for cl in clauses:
        if not any((val[abs(l)] if l>0 else not val[abs(l)]) for l in cl): viol+=1
    tested+=1
print('random configs', tested, 'clause violations', viol)
