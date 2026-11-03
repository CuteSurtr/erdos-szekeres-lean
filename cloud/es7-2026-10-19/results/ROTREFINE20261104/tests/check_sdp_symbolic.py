#!/usr/bin/env python3
"""Independent exact seed-polynomial and definiteness check; no SDP imports."""
import argparse, hashlib, importlib.util, itertools, json
from fractions import Fraction as F
from pathlib import Path
def check(witness,model):
    w=json.loads(witness.read_text());raw=model.read_bytes();positive=set(json.loads(raw))
    if w['m']!=6 or hashlib.sha256(raw).hexdigest()!=w['model_sha256']:raise ValueError('model binding')
    s=importlib.util.spec_from_file_location('polynomial',Path(__file__).with_name('check_linear_symbolic.py'))
    p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
    mapping={}
    for q in itertools.combinations(range(6*w['t']),3):
        c=p.canon(q,6)
        if c not in mapping:mapping[c]=len(mapping)+1
    poly={};clause=[];layers=sorted({x//6 for row in w['records'] for x in row['triple']})
    if layers!=w['source_layers']:raise ValueError('source support')
    for row in w['records']:
        q=tuple(row['triple']);v=row['variable'];sign=row['required_sign'];weight=row['weight']
        if q!=p.canon(q,6) or mapping[q]!=v:raise ValueError('canonical variable')
        if sign not in (-1,1) or sign!=(1 if v in positive else -1):raise ValueError('model sign')
        if type(weight) is not int or weight<=0:raise ValueError('positive integer weight')
        poly=p.add(poly,{key:c*weight*sign for key,c in p.orient(q,6).items()});clause.append(-sign*v)
    if not clause or sorted(clause,key=abs)!=w['candidate_clause']:raise ValueError('clause')
    n=2*len(layers);index={2*layer+k:2*i+k for i,layer in enumerate(layers) for k in (0,1)}
    twice=[[F(0) for _ in range(n)] for _ in range(n)]
    for (i,j),c in poly.items():
        i,j=index[i],index[j]
        if i==j:twice[i][i]+=2*c
        else:twice[i][j]+=c;twice[j][i]+=c
    # Search coordinates: (x_i,sqrt(3)*y_i), ordered x block then y block.
    # Oblique (u_i,v_i) gives x_i=u_i+v_i/2, y_i=v_i/2.
    advertised=[[F(x) for x in row] for row in w['quadratic_matrix_twice']]
    if len(advertised)!=n or any(len(row)!=n for row in advertised):raise ValueError('matrix shape')
    if any(advertised[i][j]!=advertised[j][i] for i in range(n) for j in range(n)):raise ValueError('matrix symmetry')
    transform=[];half=n//2
    for i in range(n):
        orbit,coord=divmod(i,2)
        transform.append({orbit:F(1)} if coord==0 else {orbit:F(1,2),half+orbit:F(1,2)})
    for i in range(n):
        for j in range(n):
            actual=sum(x*advertised[a][b]*y for a,x in transform[i].items() for b,y in transform[j].items())
            if actual!=twice[i][j]:raise ValueError('advertised matrix is not the seed polynomial')
    schur=[[-x for x in row] for row in twice];pivots=[]
    for k in range(n):
        pivot=schur[k][k]
        if pivot<=0:raise ValueError('not negative definite')
        pivots.append(pivot)
        for i in range(k+1,n):
            for j in range(i,n):
                schur[i][j]-=schur[i][k]*schur[k][j]/pivot;schur[j][i]=schur[i][j]
    return {'model_sha256':w['model_sha256'],'witness_sha256':hashlib.sha256(witness.read_bytes()).hexdigest(),
        'method':'independent direct seed expansion, exact matrix congruence and rational Schur complements',
        'rows':len(clause),'source_layers':layers,'matrix_dimension':n,'all_weights_positive':True,
        'negative_definite':True,'exact_oblique_negative_matrix_ldl_pivots':list(map(str,pivots)),
        'candidate_clause':w['candidate_clause'],'scope':'excludes the prescribed geometric sixfold realization',
        'rigor':'exact computation plus the quadratic-form soundness argument'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--witness',type=Path,required=True);p.add_argument('--model',type=Path,required=True)
    a=p.parse_args();print(json.dumps(check(a.witness,a.model),sort_keys=True))
