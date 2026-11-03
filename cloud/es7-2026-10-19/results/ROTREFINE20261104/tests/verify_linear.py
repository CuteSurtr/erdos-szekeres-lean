#!/usr/bin/env python3
"""Exact check of a rotation-specific linear determinant obstruction.

Uses direct symbolic affine determinants under the rational 60-degree matrix,
not the searcher's dot/cross coefficient table. Certified54 checks are exhaustive
over the stated embeddings for at most four source orbits, and deterministic
finite samples for larger supports. No floating point or numerical LP is used.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import random
import time

ROOT=Path(__file__).resolve().parents[2]


def add(a,b,sign=1):
    out=defaultdict(F,a)
    for m,c in b.items():out[m]+=sign*c
    return {m:c for m,c in out.items() if c}


def scale(a,s):return {m:c*s for m,c in a.items() if c*s}


def mul(a,b):
    out=defaultdict(F)
    for x,c in a.items():
        for y,d in b.items():out[tuple(sorted(x+y))]+=c*d
    return {m:c for m,c in out.items() if c}


def symbolic_orbits(t,direction=1):
    ans=[]
    for i in range(t):
        x={(2*i,):F(1)};y={(2*i+1,):F(1)}
        for k in range(6):
            ans.append((x,y))
            x,y=scale(add(x,y,-3*direction),F(1,2)),scale(add(scale(x,direction),y),F(1,2))
    return ans


def determinant(a,b,c):
    return add(mul(add(b[0],a[0],-1),add(c[1],a[1],-1)),mul(add(b[1],a[1],-1),add(c[0],a[0],-1)),-1)


def lift_poly(key):
    kind,i,j=key
    xx={(tuple(sorted((2*i,2*j)))):F(1)}; yy={(tuple(sorted((2*i+1,2*j+1)))):F(3)}
    xy={(tuple(sorted((2*i,2*j+1)))):F(1)}; yx={(tuple(sorted((2*i+1,2*j)))):F(1)}
    return add(xx,yy) if kind=='D' else add(xy,yx,-1)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--witness',required=True,type=Path);ap.add_argument('--model',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();start=time.monotonic()
    raw=args.witness.read_bytes();w=json.loads(raw);model=args.model.read_bytes();pos=set(json.loads(model))
    assert hashlib.sha256(model).hexdigest()==w['model_sha256'];assert w['m']==6
    spec=importlib.util.spec_from_file_location('encoder',ROOT/'C7UPPER/gen.py');G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
    E=G.Enc(6,8,w['t']);points=symbolic_orbits(w['t']);total={}
    for row in w['records']:
        q=tuple(row['triple']);sg=row['required_sign'];weight=row['weight']
        assert sg in (-1,1) and isinstance(weight,int) and weight>0
        assert E.o(*q)==row['variable'] and sg==(1 if row['variable'] in pos else -1)
        p=scale(determinant(*(points[x] for x in q)),2*sg)
        claimed={}
        for key,c in row['signed_coefficients']:claimed=add(claimed,scale(lift_poly(key),c))
        assert p==claimed,'direct determinant differs from advertised lift'
        total=add(total,scale(p,weight))
    assert not total,'nonzero exact polynomial residual'
    reverse=symbolic_orbits(w['t'],-1);reverse_total={}
    for row in w['records']:
        reverse_total=add(reverse_total,scale(determinant(*(reverse[x] for x in row['triple'])),row['required_sign']*row['weight']))
    assert not reverse_total,'direction-reversed identity fails'
    cut=sorted([-row['variable']*row['required_sign'] for row in w['records']],key=abs);assert cut==w['candidate_clause']
    layers=sorted({x//6 for r in w['records'] for x in r['triple']});assert layers==w['source_layers'];assert 2<=len(layers)<=9
    source=ROOT/'ES8SYM/sets/c6_54pts_9layers.pts';sraw=source.read_bytes();pts=[]
    for line in sraw.decode().splitlines():
        if not line or line.startswith('#'):continue
        a,b,c,d,e,f=map(int,line.split());pts.append((2*a+b-c-2*d-e+f,b+c-e-f))
    def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    checked=0;forbidden=0;truehist=defaultdict(int)
    for mirror in ((-1,1) if len(layers)<=4 else ()):
        pp=[(x,mirror*y) for x,y in pts]
        for targets in it.permutations(range(9),len(layers)):
            for offsets in it.product(range(6),repeat=len(layers)-1):
                for direction in (-1,1):
                    mapping=dict(zip(layers,zip(targets,(0,)+offsets)))
                    def p(x):
                        layer,k=divmod(x,6);target,shift=mapping[layer]
                        return pp[6*target+(direction*k+shift)%6]
                    values=[det(*(p(x) for x in r['triple'])) for r in w['records']]
                    assert all(values)
                    assert sum(v*r['required_sign']*r['weight'] for v,r in zip(values,w['records']))==0
                    for flip in (-1,1):
                        truecount=sum((v>0)!=(r['required_sign']*flip>0) for v,r in zip(values,w['records']))
                        forbidden+=truecount==0;truehist[truecount]+=1;checked+=1
    finite_cases=[]
    if len(layers)>4:
        rng=random.Random(20261104)
        for sample in range(100):
            targets=rng.sample(range(9),len(layers));offsets=[rng.randrange(6) for _ in layers]
            mirror=(-1,1)[sample%2];direction=(-1,1)[(sample//2)%2];flip=(-1,1)[(sample//4)%2]
            pp=[(x,mirror*y) for x,y in pts];mapping=dict(zip(layers,zip(targets,offsets)))
            def p(x):
                layer,k=divmod(x,6);target,shift=mapping[layer];return pp[6*target+(direction*k+shift)%6]
            values=[det(*(p(x) for x in r['triple'])) for r in w['records']];assert all(values)
            assert sum(v*r['required_sign']*r['weight'] for v,r in zip(values,w['records']))==0
            truecount=sum((v>0)!=(r['required_sign']*flip>0) for v,r in zip(values,w['records']))
            forbidden+=truecount==0;truehist[truecount]+=1;checked+=1
            finite_cases.append({'targets':targets,'offsets':offsets,'mirror':mirror,'direction':direction,'global_sign':flip,'true_cut_literals':truecount})
    assert forbidden==0
    result={'rigor':'exact computation; soundness is written linear determinant proof','witness_sha256':hashlib.sha256(raw).hexdigest(),
            'model_sha256':w['model_sha256'],'support':len(w['records']),'source_layers':layers,'candidate_clause':cut,
            'direct_symbolic_identity':True,'reverse_direction_identity':True,'positive_integer_weights':True,
            'exact54_sha256':hashlib.sha256(sraw).hexdigest(),'exact54_tests':checked,'exact54_forbidden_matches':forbidden,
            'exact54_test_scope':'exhaustive ordered embeddings' if len(layers)<=4 else '100 deterministic finite injective embeddings, not exhaustive',
            'exact54_true_literal_histogram':dict(truehist),'elapsed_seconds':round(time.monotonic()-start,3),
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'status':'PASS'}
    if finite_cases:result['exact54_cases']=finite_cases
    args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
