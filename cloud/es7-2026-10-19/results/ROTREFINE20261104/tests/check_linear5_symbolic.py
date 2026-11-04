#!/usr/bin/env python3
"""Independent exact fivefold identity verification in Q(sqrt(5)).
In the positive basis (1,zeta5), R(u,v)=(-v,u+s*v), s=(sqrt(5)-1)/2.
Expand actual triangle determinants in independent seed coordinates, without
using the searcher's dot/cross table or trusting any floating LP computation.
"""
import argparse, hashlib, importlib.util, itertools, json
from fractions import Fraction as F
from pathlib import Path
ZERO=(F(0),F(0));ONE=(F(1),F(0));S=(F(-1,2),F(1,2))
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def times(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def sign(a):
    x,y=a
    if x>=0 and y>=0:return int(x>0 or y>0)
    if x<=0 and y<=0:return -int(x<0 or y<0)
    q=x*x-5*y*y
    return (1 if q>0 else -1 if q<0 else 0)*(1 if x>0 else -1)
def add(a,b,scale=ONE):
    d=dict(a)
    for key,c in b.items():d[key]=plus(d.get(key,ZERO),times(c,scale))
    return {key:c for key,c in d.items() if c!=ZERO}
def multiply(a,b):
    d={}
    for i,c in a.items():
        for j,e in b.items():
            key=tuple(sorted((i,j)));d[key]=plus(d.get(key,ZERO),times(c,e))
    return {key:c for key,c in d.items() if c!=ZERO}
def point(i,k):
    u,v={2*i:ONE},{2*i+1:ONE}
    for _ in range(k):u,v={j:neg(c) for j,c in v.items()},add(u,v,S)
    return u,v
def orient(q):
    a,b,c=[point(*divmod(x,5)) for x in q]
    return add(multiply(add(b[0],a[0],neg(ONE)),add(c[1],a[1],neg(ONE))),
               multiply(add(b[1],a[1],neg(ONE)),add(c[0],a[0],neg(ONE))),neg(ONE))
def check(witness,model):
    if point(0,5)!=point(0,0):raise ValueError('rotation normalization')
    w=json.loads(witness.read_text());raw=model.read_bytes();pos=set(json.loads(raw))
    if w['m']!=5 or hashlib.sha256(raw).hexdigest()!=w['model_sha256']:raise ValueError('model binding')
    p=Path(__file__).with_name('check_product_symbolic.py');spec=importlib.util.spec_from_file_location('orbits',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    numbering={}
    for q in itertools.combinations(range(5*w['t']),3):
        c,_=mod.cs(q,5)
        if c not in numbering:numbering[c]=len(numbering)+1
    residual={};clause=[]
    for row in w['records']:
        q=tuple(row['triple']);v=row['variable'];sg=row['required_sign'];weight=row['weight']
        weight=(F(weight),F(0)) if isinstance(weight,int) else tuple(F(x) for x in weight)
        if len(weight)!=2 or sign(weight)<=0:raise ValueError('nonpositive exact weight')
        if q!=mod.cs(q,5)[0] or numbering[q]!=v or sg!=(1 if v in pos else -1):raise ValueError('canonical sign')
        residual=add(residual,orient(q),times((F(sg),F(0)),weight));clause.append(-sg*v)
    if not w['records'] or residual:raise ValueError('nonzero seed polynomial')
    if sorted(clause,key=abs)!=w['candidate_clause']:raise ValueError('cut')
    return {'rigor':'exact computation plus the written positive-basis rotation argument','verified':True,'m':5,
        'model_sha256':hashlib.sha256(raw).hexdigest(),'witness_sha256':hashlib.sha256(witness.read_bytes()).hexdigest(),
        'records':len(w['records']),'exact_field':'Q(sqrt(5))','positive_weights':True,'polynomial_residual':{},
        'source_layers':w['source_layers'],'candidate_clause':w['candidate_clause'],
        'scope':'realizations carrying the specified geometric fivefold rotation'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--witness',required=True,type=Path);p.add_argument('--model',required=True,type=Path);a=p.parse_args()
    print(json.dumps(check(a.witness,a.model),sort_keys=True))
