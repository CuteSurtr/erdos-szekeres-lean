#!/usr/bin/env python3
"""Chord lemma clauses for C7UPPER/gen.py Enc(m, K, t), any m >= 3 (exact rational-degree interval logic).
Lemma (see writeup/CHORD_LEMMA.md): for vertices q1=(j,k), q2=(j,k+d) of one layer (ccw separation phi = 360d/m <= 180)
and any other point p: if phi < 180 and angle(p, n) in [90,270] (n = outward chord normal) then orient(q1,q2,p) = +;
if phi = 180 then orient(q1,-q1,p) = sign(p.n) with n = q1 rotated by -90 degrees.
Phases (gen.py): vertex (i,k) has angle theta_i + 360k/m, theta_0 = 0;  even m: theta_i = psi_i in (0, 360/m);
odd m: theta_i = psi_i + (0 if H_i else 180/m), psi_i in (0, 180/m); Y(i,j) = [psi_i < psi_j]; H(0) = true.
Each emitted clause is (orientation literal) OR (negation of a prime implicant over the condition literals
{Y(i,j) (or Y(j,i)), H(i), H(j)} of the region of phase cases in which the conclusion holds).
Usage: chord_rules_m.py m t OUT.clauses"""
import sys, itertools, importlib.util
from fractions import Fraction as Fr
import os, pathlib
R=os.environ.get('ES_RESULTS', str(pathlib.Path(__file__).resolve().parents[2]))
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
def build(m, t):
    E=G.Enc(m,8,t); odd=(m%2==1); u=Fr(180,m); U=u if odd else 2*u
    def cases(i,j):
        """list of (assignment dict {literal-var: bool}, (lo,hi) for delta=theta_i-theta_j)  [open interval; lo==hi exact]"""
        if i==j: return [({}, (Fr(0),Fr(0)))]
        out=[]
        Hs=[None,None]
        hv=[[True] if (x==0 or not odd) else [True,False] for x in (i,j)]
        for Hi in hv[0]:
            for Hj in hv[1]:
                for sgn in (+1,-1):
                    # psi_i - psi_j in (0,U) if sgn>0 else (-U,0)
                    if i==0 and sgn>0: continue          # psi_0 = 0 is the least
                    if j==0 and sgn<0: continue
                    asg={}
                    if i!=0 and j!=0:
                        y=E.ylit(i,j)                    # literal for psi_i < psi_j
                        asg[abs(y)]=((sgn<0)==(y>0))      # var value making 'psi_i<psi_j' == (sgn<0)
                    if odd:
                        if i!=0: asg[E.H[i]]=Hi
                        if j!=0: asg[E.H[j]]=Hj
                    hi_=0 if Hi else 1; hj_=0 if Hj else 1
                    base=u*(hi_-hj_) if odd else Fr(0)
                    lo,hi=(base, base+U) if sgn>0 else (base-U, base)
                    out.append((asg,(lo,hi)))
        return out
    def within(lo,hi,a,b):   # [lo,hi] subset of [a,b] modulo 360
        for sh in range(-3,4):
            if a<=lo+360*sh and hi+360*sh<=b: return True
        return False
    rules={}   # (orientation literal) -> {frozenset(condition vars)-> set of satisfied assignments tuples}, plus all cases
    for j in range(t):
        for d in range(1, m//2+1):
            phi=Fr(360*d,m); diam=(2*d==m)
            for k1 in range(m):
                q1=m*j+k1; q2=m*j+(k1+d)%m
                for i in range(t):
                    for l in range(m):
                        p=m*i+l
                        if p in (q1,q2): continue
                        base=Fr(360*(l-k1),m)+(Fr(90) if diam else -phi/2)
                        cs=cases(i,j); key=(q1,q2,p)
                        for asg,(lo,hi) in cs:
                            a_lo,a_hi=base+lo,base+hi
                            concl=None
                            if not diam:
                                if within(a_lo,a_hi,90,270): concl=+1
                            else:
                                if within(a_lo,a_hi,-90,90) and not (lo==hi and (within(a_lo,a_hi,90,90) or within(a_lo,a_hi,-90,-90))): concl=+1
                                elif within(a_lo,a_hi,90,270): concl=-1
                            if concl is None: continue
                            L=E.o(q1,q2,p)*(1 if concl>0 else -1)
                            vars_=tuple(sorted(asg)); allc=rules.setdefault((L,vars_,i,j),[set(),len(cs)])
                            allc[0].add(tuple(asg[v] for v in vars_))
    clauses=set()
    for (L,vars_,i,j),(holds,ncases) in rules.items():
        n=len(vars_)
        # prime implicants: subcubes (partial assignments) fully inside 'holds'; holds is a set of full tuples over vars_
        full=set(itertools.product([True,False],repeat=n))
        # only cases that exist (feasible combos) count; infeasible combos (e.g. psi_0 constraints) are absent from cases()
        feasible=set(tuple(a[v] for v in vars_) for a,_ in cases(i,j)) if n else {()}
        imps=[]
        for r in range(0,n+1):
            for idx in itertools.combinations(range(n),r):
                for vals in itertools.product([True,False],repeat=r):
                    cube=[f for f in feasible if all(f[q]==v for q,v in zip(idx,vals))]
                    if cube and all(f in holds for f in cube):
                        if not any(set(zip(i2,v2))<=set(zip(idx,vals)) for i2,v2 in imps):
                            imps.append((idx,vals))
        for idx,vals in imps:
            c=[L]+[(-vars_[q] if v else vars_[q]) for q,v in zip(idx,vals)]
            clauses.add(tuple(sorted(c,key=abs)))
    # drop clauses subsumed by units
    units={c[0] for c in clauses if len(c)==1}
    clauses={c for c in clauses if len(c)==1 or not any(x in units for x in c)}
    return E, sorted(clauses,key=lambda c:[abs(x) for x in c])
if __name__=='__main__':
    m,t=int(sys.argv[1]),int(sys.argv[2]); E,C=build(m,t)
    with open(sys.argv[3],'w') as f:
        for c in C: f.write(' '.join(map(str,c))+' 0\n')
    from collections import Counter
    print('m=%d t=%d clauses %d by length %s' % (m,t,len(C),dict(Counter(len(c) for c in C))))
