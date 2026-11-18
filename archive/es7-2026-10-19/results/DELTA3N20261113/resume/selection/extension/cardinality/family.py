#!/usr/bin/env python3
"""Exact one-parameter, non-affine deformation of the eleven-point example."""
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource

HERE=Path(__file__).resolve().parent


def determinant(P,a,b,c):
    return sum(P[i][0]*P[j][1]-P[i][1]*P[j][0] for i,j in ((a,b),(b,c),(c,a)))


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    path=HERE/'data/simple11.candidate.json';raw=json.loads(path.read_text());P=raw['P']
    # Replace only p5=(48,1) by (48,1+t). All other points stay fixed.
    changed=[p[:] for p in P];changed[5][1]+=1
    inequalities=[];lower=[];upper=[]
    for triple in combinations(range(11),3):
        d=determinant(P,*triple);s=1 if d>0 else -1
        coefficient=s*(determinant(changed,*triple)-d)
        intercept=s*d
        assert intercept>0
        inequalities.append({'triple':triple,'positive_intercept':intercept,'coefficient':coefficient})
        if coefficient>0:lower.append((Fraction(-intercept,coefficient),triple))
        if coefficient<0:upper.append((Fraction(-intercept,coefficient),triple))
    lo=max(lower)[0];hi=min(upper)[0]
    assert lo<0<hi
    samples=[]
    for tag,t in (('family-low',lo/2),('family-high',hi/2)):
        den=t.denominator
        Q=[[x*den,y*den] for x,y in P];Q[5][1]+=t.numerator
        assert all(determinant(Q,*triple)*determinant(P,*triple)>0 for triple in combinations(range(11),3))
        out={**raw,'P':Q,'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'finder':'Exact one-point parameter family','parameter':str(t)}
        with (HERE/f'data/{tag}.candidate.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
        samples.append({'tag':tag,'parameter':str(t)})
    for endpoint in (lo,hi):
        assert any(row['positive_intercept']+row['coefficient']*endpoint==0 for row in inequalities)
    out={'label':'PROVED exact affine-in-parameter sign inequalities',
         'statement':'Replace p5=(48,1) by (48,1+t), fixing all ten other points.',
         'open_parameter_interval':[str(lo),str(hi)],
         'lower_active_triples':[t for q,t in lower if q==lo],
         'upper_active_triples':[t for q,t in upper if q==hi],
         'inequalities':inequalities,'samples':samples,
         'scope':'Same eleven labels and oriented order type, not a family with growing n or m.',
         'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with (HERE/'data/family.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='inequalities'}))


if __name__=='__main__':main()
