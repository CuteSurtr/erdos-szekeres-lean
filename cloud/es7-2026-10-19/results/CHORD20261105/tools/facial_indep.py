#!/usr/bin/env python3
"""Coordinator's independent exact re-check of facial-cert-v1 witnesses, in OBLIQUE coordinates
z_i = a_i + b_i*w (w = e^{i pi/3}), a different basis from the agent's checker (congruent, so the NSD verdict must agree).
  (2/sqrt3)*orient(p,q,r) = sum_cyc (p_a q_b - p_b q_a);  E_ij = det(z_i,z_j)/sqrt3 = (a_i b_j - b_i a_j)/2;
  D_ij = dot(z_i,z_j) = a_i a_j + (a_i b_j + b_i a_j)/2 + b_i b_j.
Signs and clause are bound to the ORIGINAL cluster file (representative + flips), not to the agent's model file.
NSD test: Bareiss-free rational symmetric elimination, complete (zero pivot => zero row)."""
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
            S[i][j]+=F(c*x*y,2); S[j][i]+=F(c*x*y,2)
def check(wit, cluster, corrupt=None):
    base=set(cluster['representative_true_vars']); members=[]
    for m in cluster['members']:
        t=set(base)
        for v in m['flips']: t^={v}
        members.append(t)
    rep=members[0] if not cluster['members'][0]['flips'] else base
    S=[[F(0)]*NV for _ in range(NV)]; clause=set()
    recs=json.loads(json.dumps(wit['records']))
    if corrupt: corrupt(recs)
    for r in recs:
        w=r['weight']; assert type(w) is int and w>0
        if r['kind']=='triple':
            t=tuple(r['triple']); assert list(t)==sorted(t) and len(set(t))==3
            v=E.tvar[t]; assert v==r['var']; sg=r['sign']; assert sg in (1,-1)
            P=[point(x) for x in t]
            for p,q in zip(P,P[1:]+P[:1]):
                add(S,p[0],q[1],w*sg); add(S,p[1],q[0],-w*sg)
            clause.add(-sg*v)
        elif r['kind']=='phase_sign':
            i,j=r['pair']; sg=r['sign']; assert 0<=i<j<10 and sg in (1,-1)
            if i==0: assert sg==1
            else: y=E.Y[(i,j)]; clause.add(-y if sg==1 else y)
            add(S,{i:1},{10+j:1},F(w*sg,2)); add(S,{10+i:1},{j:1},F(-w*sg,2))
        elif r['kind'] in ('phase_plus','phase_minus'):
            i,j=r['pair']; e=1 if r['kind']=='phase_plus' else -1
            add(S,{i:1},{j:1},w); add(S,{i:1},{10+j:1},F(w,2)); add(S,{10+i:1},{j:1},F(w,2)); add(S,{10+i:1},{10+j:1},w)
            add(S,{i:1},{10+j:1},F(w*e,2)); add(S,{10+i:1},{j:1},F(-w*e,2))
        elif r['kind']=='radius':
            a_,b_=r['pair']; assert 0<=a_<b_<10
            for l,c in ((a_,w),(b_,-w)):
                add(S,{l:1},{l:1},c); add(S,{l:1},{10+l:1},c); add(S,{10+l:1},{10+l:1},c)
        else: raise AssertionError('kind')
    # complete NSD test on -S
    A=[[-x for x in row] for row in S]; idx=list(range(NV)); rank=0
    while idx:
        for i in idx:
            if A[i][i]<0: return ('not NSD', None)
            if A[i][i]==0 and any(A[i][j] for j in idx): return ('not NSD', None)
        idx=[i for i in idx if A[i][i]!=0]
        if not idx: break
        p=idx.pop(0); rank+=1
        for i in idx:
            f=A[i][p]/A[p][p]
            if f:
                for j in idx: A[i][j]-=f*A[p][j]
    assert any(any(x for x in row) for row in S), 'zero form'
    # clause literal falsified by every member?  (literal l false in member m)
    killed=sum(all(((abs(l) in m)!=(l>0)) for l in clause) for m in members)
    return ('NSD rank %d' % rank, killed, len(members), len(clause), sorted(clause,key=abs)==sorted(wit['clause'],key=abs))
W=os.environ.get('SIX10_WORK','<six10-work-dir>')
import glob, os, copy, random
for d in sorted(glob.glob(W+'/facial/certs/*/witness.json')):
    cube=d.split('/')[-2]; wit=json.load(open(d)); cl=json.load(open(R+'/SIX10CEGAR/hard_models/cluster_%s.json'%cube))
    res=check(wit,cl)
    def flip(recs): recs[random.randrange(len(recs))]['sign']*=-1
    def bump(recs): r=recs[random.randrange(len(recs))]; r['weight']=r['weight']*3+1
    def drop(recs): del recs[random.randrange(len(recs))]
    rej=[]
    for name,fn in (('flip',flip),('bump',bump),('drop',drop)):
        n=0
        for _ in range(5):
            try: r=check(wit,cl,fn); n+= (r[0]=='not NSD' or r[1]==0)
            except AssertionError: n+=1
        rej.append('%s %d/5'%(name,n))
    print(cube, res, 'kinds', {k:sum(1 for r in wit['records'] if r['kind']==k) for k in set(r['kind'] for r in wit['records'])}, 'corruptions rejected:', ', '.join(rej))
