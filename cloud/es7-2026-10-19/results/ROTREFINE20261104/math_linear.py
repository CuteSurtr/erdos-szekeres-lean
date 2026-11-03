#!/usr/bin/env python3
"""Farkas obstruction for prescribed Euclidean sixfold point configurations.

D_ij = dot(z_i,z_j), E_ij = det(z_i,z_j)/sqrt(3). D is symmetric and E
antisymmetric. (2/sqrt(3))*det(z_i,R^k z_j) has integer (D,E) coefficients
(0,2),(1,1),(1,-1),(0,-2),(-1,-1),(-1,1), for k=0,...,5.
Every triangle determinant is a linear form in t*t lift variables. Any
nonzero nonnegative dependency of the signed forms is an exact obstruction.
LP values only select support; retained integer weights are checked exactly.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
import resource
import time
import warnings

ROOT=Path(__file__).resolve().parent.parent
DCO=(0,1,1,0,-1,-1)
ECO=(2,1,-1,-2,-1,1)


def variables(t):
    return [('D',i,j) for i in range(t) for j in range(i,t)]+[('E',i,j) for i in range(t) for j in range(i+1,t)]


def form(triple,index):
    row=defaultdict(int)
    for a,b in zip(triple,triple[1:]+triple[:1]):
        i,ka=divmod(a,6);j,kb=divmod(b,6);k=(kb-ka)%6
        row[index[('D',min(i,j),max(i,j))]]+=DCO[k]
        if i!=j:row[index[('E',min(i,j),max(i,j))]]+=ECO[k]*(1 if i<j else -1)
    return {j:c for j,c in row.items() if c}


def exact_weights(rows,approx,nvars):
    """Solve [A_support^T; ones] w = [0;1] by rational elimination."""
    count=len(rows)
    matrix=[[Fraction(row.get(j,0)) for row in rows]+[Fraction(0)] for j in range(nvars)]
    matrix.append([Fraction(1)]*count+[Fraction(1)])
    pivotrow=0;pivots=[]
    for col in range(count):
        pr=next((r for r in range(pivotrow,len(matrix)) if matrix[r][col]),None)
        if pr is None:continue
        matrix[pivotrow],matrix[pr]=matrix[pr],matrix[pivotrow]
        fac=matrix[pivotrow][col];matrix[pivotrow]=[x/fac for x in matrix[pivotrow]]
        for r in range(len(matrix)):
            if r!=pivotrow and matrix[r][col]:
                fac=matrix[r][col];matrix[r]=[a-fac*b for a,b in zip(matrix[r],matrix[pivotrow])]
        pivots.append(col);pivotrow+=1
    assert all(any(row[:-1]) or not row[-1] for row in matrix),'inconsistent rational support'
    if len(pivots)<count:
        # A degenerate floating solution may include free columns. Fix them
        # to rational approximants and solve pivot variables exactly.
        w=[Fraction(float(x)).limit_denominator(10**8) for x in approx]
        free=set(range(count))-set(pivots)
        for r,col in enumerate(pivots):w[col]=matrix[r][-1]-sum(matrix[r][j]*w[j] for j in free)
    else:w=[Fraction(0)]*count
    for r,col in enumerate(pivots):
        if len(pivots)==count:w[col]=matrix[r][-1]
    assert all(x>0 for x in w),'nonpositive exact dependency'
    den=math.lcm(*(x.denominator for x in w));ints=[int(x*den) for x in w]
    g=math.gcd(*ints);ints=[x//g for x in ints]
    total=defaultdict(int)
    for row,weight in zip(rows,ints):
        for j,c in row.items():total[j]+=weight*c
    assert not any(total.values()),'nonzero exact residual'
    return ints


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--layers',help='comma-separated restriction, or all');ap.add_argument('--seconds',type=float,default=45)
    ap.add_argument('--seed',type=int,default=0);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();raw=args.model.read_bytes();pos=set(json.loads(raw))
    spec=importlib.util.spec_from_file_location('encoder',ROOT/'C7UPPER/gen.py');G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
    E=G.Enc(6,8,10);vs=variables(10);ix={v:j for j,v in enumerate(vs)}
    layers=set(map(int,args.layers.split(','))) if args.layers and args.layers!='all' else set(range(10))
    reps=[(q,v) for q,v in E.tvar.items() if {x//6 for x in q}<=layers]
    rows=[{j:c*(1 if v in pos else -1) for j,c in form(q,ix).items()} for q,v in reps]
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,vstack
    import numpy as np
    rr=[];cc=[];dd=[]
    for k,row in enumerate(rows):
        for j,c in row.items():rr.append(j);cc.append(k);dd.append(c)
    A=coo_matrix((dd,(rr,cc)),shape=(len(vs),len(rows))).tocsr()
    eq=vstack((A,coo_matrix(np.ones((1,len(rows)))))).tocsr();rhs=np.r_[np.zeros(len(vs)),1.0]
    rng=np.random.default_rng(args.seed)
    # Random positive objective chooses sparse extreme points; one equality fixes scale.
    objective=rng.uniform(0.5,1.5,len(rows))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sol=linprog(objective,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs',
                    options={'time_limit':args.seconds,'threads':1,'presolve':True})
    result={'model_sha256':hashlib.sha256(raw).hexdigest(),'layers':sorted(layers),'constraints':len(rows),'lift_variables':len(vs),
            'lp_status':int(sol.status),'lp_message':sol.message,'lp_elapsed_seconds':round(time.monotonic()-start,3)}
    if sol.success:
        support=np.flatnonzero(sol.x>1e-9).tolist();selected=[rows[i] for i in support]
        weights=exact_weights(selected,[sol.x[i] for i in support],len(vs))
        records=[]
        for k,weight in zip(support,weights):
            triple,var=reps[k];sg=1 if var in pos else -1
            records.append({'triple':triple,'variable':var,'required_sign':sg,'weight':weight,
                            'signed_coefficients':[[vs[j],c] for j,c in sorted(rows[k].items())]})
        cut=sorted([-r['variable']*r['required_sign'] for r in records],key=abs)
        witness={'m':6,'t':10,'scope':'realizations with the specified Euclidean sixfold rotation','model_sha256':result['model_sha256'],
                 'method':'positive exact linear dependency of rotation-specific determinant forms',
                 'lift_variables':vs,'records':records,'candidate_clause':cut,'exact_residual_zero':True,
                 'source_layers':sorted({x//6 for r in records for x in r['triple']})}
        payload=(json.dumps(witness,indent=2)+'\n').encode();(args.out/'linear_witness.json').write_bytes(payload)
        result.update({'exact_dependency':True,'support':len(records),'source_layers':witness['source_layers'],
                       'maximum_weight':max(weights),'witness_sha256':hashlib.sha256(payload).hexdigest(),'candidate_clause':cut})
    else:result['conclusion']='no exact obstruction obtained; no realizability conclusion'
    result['elapsed_seconds']=round(time.monotonic()-start,3);result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (args.out/'linear_search.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
