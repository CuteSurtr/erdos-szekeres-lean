#!/usr/bin/env python3
"""Model-free exact checker for clause certificates (JSONL: {"clause": [...], "records": [...]}).
Records as in facial-cert-v1 (triple / phase_sign / phase_plus / phase_minus / radius), positive integer weights.
Checks, in OBLIQUE seed coordinates z_i = a_i + b_i w (independent of the (D,E) code that produced the weights):
  (1) the weighted sum P of the record forms is negative semidefinite (complete exact test; P = 0 allowed:
      sum of strictly positive terms cannot vanish);
  (2) the clause is exactly the set of negated record literals (triple: -(sign*var); phase_sign(i,j), i >= 1:
      -Y(i,j) if sign = +1 else +Y(i,j); i = 0 requires sign = +1 and adds no literal; plus/minus/radius: none).
Soundness: if every record literal held in a real normal-form configuration, every record form would be > 0, so
P > 0 there, contradicting P <= 0.  Hence every real configuration satisfies the clause."""
import sys, json, importlib.util
from fractions import Fraction as F
import os, pathlib
R=os.environ.get('ES_RESULTS', str(pathlib.Path(__file__).resolve().parents[2]))
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E=G.Enc(6,8,10); NV=20
def point(x):
    i,k=divmod(x,6); a={i:1}; b={10+i:1}
    for _ in range(k): a,b={j:-c for j,c in b.items()},{j:a.get(j,0)+b.get(j,0) for j in set(a)|set(b)}
    return a,b
def add(S,f,g,c):
    for i,x in f.items():
        for j,y in g.items():
            S[i][j]+=F(c)*x*y/2; S[j][i]+=F(c)*x*y/2
def check(cert):
    S=[[F(0)]*NV for _ in range(NV)]; clause=set(); recs=cert['records']; assert recs
    for r in recs:
        w=r['weight']; assert type(w) is int and w>0
        k=r['kind']
        if k=='triple':
            t=tuple(r['triple']); assert list(t)==sorted(t) and len(set(t))==3 and E.tvar[t]==r['var']; sg=r['sign']; assert sg in (1,-1)
            P=[point(x) for x in t]
            for p,q in zip(P,P[1:]+P[:1]): add(S,p[0],q[1],w*sg); add(S,p[1],q[0],-w*sg)
            clause.add(-sg*r['var'])
        elif k=='phase_sign':
            i,j=r['pair']; sg=r['sign']; assert 0<=i<j<10 and sg in (1,-1)
            if i==0: assert sg==1
            else: y=E.Y[(i,j)]; clause.add(-y if sg==1 else y)
            add(S,{i:1},{10+j:1},F(w*sg,2)); add(S,{10+i:1},{j:1},F(-w*sg,2))
        elif k in ('phase_plus','phase_minus'):
            i,j=r['pair']; assert 0<=i<j<10; e=1 if k=='phase_plus' else -1
            add(S,{i:1},{j:1},w); add(S,{i:1},{10+j:1},F(w,2)); add(S,{10+i:1},{j:1},F(w,2)); add(S,{10+i:1},{10+j:1},w)
            add(S,{i:1},{10+j:1},F(w*e,2)); add(S,{10+i:1},{j:1},F(-w*e,2))
        elif k=='radius':
            a_,b_=r['pair']; assert 0<=a_<b_<10
            for l,c in ((a_,w),(b_,-w)): add(S,{l:1},{l:1},c); add(S,{l:1},{10+l:1},c); add(S,{10+l:1},{10+l:1},c)
        else: raise AssertionError(k)
    A=[[-x for x in row] for row in S]; idx=list(range(NV))
    while idx:
        for i in idx:
            if A[i][i]<0 or (A[i][i]==0 and any(A[i][j] for j in idx)): return False,'not NSD'
        idx=[i for i in idx if A[i][i]!=0]
        if not idx: break
        p=idx.pop(0)
        for i in idx:
            f=A[i][p]/A[p][p]
            if f:
                for j in idx: A[i][j]-=f*A[p][j]
    if sorted(clause,key=abs)!=sorted(cert['clause'],key=abs): return False,'clause mismatch'
    return True,'ok'
if __name__=='__main__':
    n=bad=0
    for line in open(sys.argv[1]):
        c=json.loads(line); ok,why=check(c); n+=1
        if not ok: bad+=1; print('FAIL', why, c['clause'])
    print(json.dumps({'certificates':n,'failed':bad}))
    # corruption tests: flip a record sign / perturb a weight / swap a clause literal
    import random; random.seed(7); certs=[json.loads(l) for l in open(sys.argv[1])]; rej=0; tot=0
    for c in random.sample(certs,200):
        c2=json.loads(json.dumps(c)); r=random.choice([r for r in c2['records'] if r['kind'] in ('triple','phase_sign')] or c2['records'])
        if 'sign' in r: r['sign']*=-1
        else: r['weight']+=7
        tot+=1
        try: rej+= (not check(c2)[0])
        except AssertionError: rej+=1
    print('corrupted copies rejected', rej, 'of', tot)
