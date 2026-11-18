#!/usr/bin/env python3
"""Independent endpoint certificate for the whole open parameter interval."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource

from verify import orientation

HERE=Path(__file__).resolve().parent


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    source=HERE/'data/simple11.candidate.json';P=json.loads(source.read_text())['P']
    rows=[];zero_sets=[]
    for label,numerator,denominator,expected in (('lower',-1,1,[(0,5,10)]),('upper',8,61,[(3,5,7)])):
        Q=[[x*denominator,y*denominator] for x,y in P];Q[5][1]+=numerator
        signs=[(t,orientation(P,*t),orientation(Q,*t)) for t in combinations(range(11),3)]
        assert all(a and a*b>=0 for t,a,b in signs)
        zeros=[t for t,a,b in signs if b==0];assert zeros==expected
        zero_sets.append(set(zeros))
        rows.append({'endpoint':label,'parameter':f'{numerator}/{denominator}',
                     'weakly_correct_orientations':len(signs),'zero_triples':zeros})
    assert not zero_sets[0]&zero_sets[1]
    out={'label':'COMPUTED exact endpoint certificate; written interpolation proof in VERIFY_CARDINALITY.md',
         'status':'PASS','checks':rows,'common_zero_triples':[],
         'consequence':'Each oriented determinant is affine in t, nonnegative at both endpoints, and not zero at both; it is strictly positive throughout the open interval.',
         'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'checker_sha256':hashlib.sha256((HERE/'verify.py').read_bytes()).hexdigest()}
    with (HERE/'data/family-endpoints.verify.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps(out))


if __name__=='__main__':main()
