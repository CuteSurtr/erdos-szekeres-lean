#!/usr/bin/env python3
"""Independent integer-polynomial verification of a sixfold linear witness.

This does not import the searcher's dot/determinant coefficient table. In the
positively oriented basis (1,zeta_6), rotation is (u,v)->(-v,u+v). Expand each
triangle determinant directly as an integer polynomial in the orbit seeds.
"""
import argparse, hashlib, itertools, json
from collections import defaultdict
from pathlib import Path

def add(a,b,sign=1):
    d=defaultdict(int,a)
    for key,c in b.items(): d[key]+=sign*c
    return {key:c for key,c in d.items() if c}
def mul(a,b):
    d=defaultdict(int)
    for i,c in a.items():
        for j,e in b.items(): d[tuple(sorted((i,j)))]+=c*e
    return {key:c for key,c in d.items() if c}
def point(i,k):
    u,v={2*i:1},{2*i+1:1}
    for _ in range(k): u,v={j:-c for j,c in v.items()},add(u,v)
    return u,v
def orient(q,m):
    a,b,c=[point(*divmod(x,m)) for x in q]
    return add(mul(add(b[0],a[0],-1),add(c[1],a[1],-1)),
               mul(add(b[1],a[1],-1),add(c[0],a[0],-1)),-1)
def canon(q,m):
    return min(tuple(sorted((x//m)*m+(x%m+s)%m for x in q)) for s in range(m))
def check(witness,model):
    w=json.loads(witness.read_text());raw=model.read_bytes();pos=set(json.loads(raw))
    if w['m']!=6: raise ValueError('sixfold only')
    if hashlib.sha256(raw).hexdigest()!=w['model_sha256']: raise ValueError('model hash')
    m,t=6,w['t'];orbit_to_var={}
    for q in itertools.combinations(range(m*t),3):
        c=canon(q,m)
        if c not in orbit_to_var: orbit_to_var[c]=len(orbit_to_var)+1
    total={};cut=[]
    for row in w['records']:
        q=tuple(row['triple']);v=row['variable'];sign=row['required_sign'];weight=row['weight']
        if q!=canon(q,m) or orbit_to_var[q]!=v: raise ValueError('canonical numbering')
        if sign not in (-1,1) or type(weight) is not int or weight<=0: raise ValueError('positive weights/sign')
        if sign!=(1 if v in pos else -1): raise ValueError('model sign')
        poly={key:coef*sign*weight for key,coef in orient(q,m).items()}
        total=add(total,poly);cut.append(-v*sign)
    if not w['records'] or total: raise ValueError('nonzero symbolic residual')
    if sorted(cut,key=abs)!=w['candidate_clause']: raise ValueError('cut mismatch')
    return {'rigor':'exact computation plus the written cyclotomic-coordinate argument',
            'method':'independent direct polynomial expansion with integer R matrix',
            'model_sha256':hashlib.sha256(raw).hexdigest(),
            'witness_sha256':hashlib.sha256(witness.read_bytes()).hexdigest(),
            'rows':len(cut),'sum_weights':sum(r['weight'] for r in w['records']),
            'integer_polynomial_residual':{},'candidate_clause':w['candidate_clause'],
            'scope':'realizations with the specified geometric sixfold rotation','verified':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--witness',required=True,type=Path);p.add_argument('--model',required=True,type=Path)
    a=p.parse_args();print(json.dumps(check(a.witness,a.model),sort_keys=True))
