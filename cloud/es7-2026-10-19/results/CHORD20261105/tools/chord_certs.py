#!/usr/bin/env python3
"""Exact degree-2 certificate for every chord-lemma clause, in the linear-lift (D,E) coordinates of
ROTREFINE20261104/math_linear.py (D_ij = dot(z_i,z_j), E_ij = det(z_i,z_j)/sqrt3; (2/sqrt3)*orient is an integer
combination of D, E).  For clause  (orientation literal L) or (not cond):  the record set is
  R_triple : -L as a signed triple (the orientation opposite to the rule),
  phase rows: phase_sign(i,j) bound to cond (or unconditional when a layer is 0), phase_plus(i,j), phase_minus(i,j).
Weights: triple weight 1; phase weights lambda >= 0 solved exactly so that every mixed (i,j) coefficient cancels.
The remaining form is c * D_jj with c <= 0 (chords) or 0 (diameters): negative semidefinite.  Output: JSONL, one
certificate per clause."""
import importlib.util, json, sys
from fractions import Fraction as F
import os, pathlib
R=os.environ.get('ES_RESULTS', str(pathlib.Path(__file__).resolve().parents[2]))
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ML=load('ml', R+'/ROTREFINE20261104/math_linear.py'); G=load('g', R+'/C7UPPER/gen.py')
E=G.Enc(6,8,10); vs=ML.variables(10); ix={v:j for j,v in enumerate(vs)}
inv={v:t for t,v in E.tvar.items()}; Yinv={v:k for k,v in E.Y.items()}
out=open(sys.argv[2],'w'); n=0; fail=0
for line in open(sys.argv[1]):
    cl=list(map(int,line.split()))[:-1]
    tl=[l for l in cl if abs(l)<=E.ntriplevars]; yl=[l for l in cl if abs(l)>E.ntriplevars]
    assert len(tl)==1 and len(yl)<=1
    L=tl[0]; t=inv[abs(L)]; s=-1 if L>0 else 1          # record: orientation opposite to the clause literal
    row={vs[j]:c*s for j,c in ML.form(t,ix).items()}       # s * (2/sqrt3) * orient(t)
    layers=sorted({x//6 for x in t}); assert len(layers) in (1,2), (t,layers)
    if len(layers)==1:   # same-layer triple: the form is c*D_jj only; certificate = the record alone if c <= 0
        assert not yl and set(k[0] for k in row)=={'D'} and len(row)==1, row
        if list(row.values())[0] < 0:
            out.write(json.dumps({'clause':cl,'records':[{'kind':'triple','triple':list(t),'var':abs(L),'sign':s,'weight':1}]})+'\n'); n+=1
        else: fail+=1; print('same-layer rule not certified', cl, row)
        continue
    i,jj=layers
    # phase literal: clause contains -cond; record phase_sign with sign from cond
    recs=[{'kind':'triple','triple':list(t),'var':abs(L),'sign':s,'weight':1}]
    cD=row.get(('D',i,jj),0); cE=row.get(('E',i,jj),0)
    if yl:
        y=yl[0]; a,b=Yinv[abs(y)]; assert (a,b)==(i,jj)
        # clause has -cond; cond = Y(a,b) if y<0 else not Y(a,b);  Y(a,b) = [theta_a < theta_b] -> E_ab > 0
        ssign=1 if y<0 else -1
    elif i==0: ssign=1      # theta_0 = 0 < theta_jj
    else: ssign=None        # unconditional rule (no phase literal): sign row not available
    # unknowns: l1 (sign row, if available), l2 (D+E), l3 (D-E) >= 0 with cD + l2 + l3 = 0, cE + ssign*l1 + l2 - l3 = 0
    sol=None
    cands=[]
    if ssign is not None:
        # try l3=0 or l2=0 or l1=0 vertices
        for fix in ('l1','l2','l3'):
            if fix=='l1': l1=F(0); l2=F(-cD-cE,2) if True else 0; l3=F(-cD,1)-l2
            elif fix=='l2': l2=F(0); l3=F(-cD); l1=F(-cE+l3,1)/ssign
            else: l3=F(0); l2=F(-cD); l1=F(-cE-l2,1)/ssign
            if l1>=0 and l2>=0 and l3>=0: cands.append((l1,l2,l3))
    else:
        l2=F(-cD-cE,2); l3=F(-cD)-l2
        if l2>=0 and l3>=0: cands.append((F(0),l2,l3))
    if not cands: fail+=1; print('no certificate for', cl, t, row); continue
    l1,l2,l3=cands[0]; den=1
    for x in (l1,l2,l3): den=den*x.denominator//__import__('math').gcd(den,x.denominator)
    if den!=1:
        recs[0]['weight']=den
    for kind,val,extra in (('phase_sign',l1,{'sign':ssign}),('phase_plus',l2,{}),('phase_minus',l3,{})):
        if val>0:
            r={'kind':kind,'pair':[i,jj],'weight':int(val*den)}; r.update(extra); recs.append(r)
    out.write(json.dumps({'clause':cl,'records':recs})+'\n'); n+=1
print('certificates', n, 'failures', fail)
