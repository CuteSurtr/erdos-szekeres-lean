#!/usr/bin/env python3
"""Embed a verified two- or three-orbit GP cycle in every choice of ten sixfold orbits.

Point maps send (i,k) to (f(i), direction*k+offset_i) mod 6, with f
injective on the source orbits. They commute with a common rotation or
its inverse, so determinant magnitudes retain the equalities in the cycle.
A simultaneous sign reversal of all brackets preserves GP product signs.
Every output clause is the negation of one impossible sign pattern. The
script verifies exponent cancellation and premises for every embedding.
"""
import argparse
from collections import Counter
import hashlib, importlib.util, itertools, json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',required=True,type=Path)
    ap.add_argument('--witness',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    results=Path(__file__).resolve().parent.parent
    spec=importlib.util.spec_from_file_location('reference',results/'C7UPPER/gen.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    e=mod.Enc(6,8,10)
    pos=set(json.loads(a.model.read_text()));w=json.loads(a.witness.read_text())
    assert w['model_sha256']==hashlib.sha256(a.model.read_bytes()).hexdigest()
    def terms(q):
        p,b,c,d,f=q
        return (((p,b,c),(p,d,f),1),((p,b,d),(p,c,f),-1),((p,b,f),(p,c,d),1))
    used=set()
    for row in w['comparisons']:
        for x,y,co in terms(row['anchor_quintuple']):used.update((abs(e.o(*x)),abs(e.o(*y))))
    pattern={q:1 if v in pos else -1 for q,v in e.tvar.items() if v in used}
    layers=sorted({x//6 for q in pattern for x in q});assert 2 <= len(layers) <= 3
    clauses={};verified=0;tautologies=0
    for target_orbits in itertools.permutations(range(10),len(layers)):
        for relative_shifts in itertools.product(range(6),repeat=len(layers)-1):
         for direction,flip in itertools.product((-1,1),(-1,1)):
            mapping=dict(zip(layers,zip(target_orbits,(0,)+relative_shifts)))
            def f(x):
                layer,k=divmod(x,6)
                orbit,shift=mapping[layer]
                return 6*orbit+(direction*k+shift)%6
            required={};conflict=False
            for q,sg in pattern.items():
                lit=e.o(*(f(x) for x in q));sg*=flip
                val=sg*(1 if lit>0 else -1)
                if abs(lit) in required and required[abs(lit)]!=val:conflict=True;break
                required[abs(lit)]=val
            if conflict:tautologies+=1;continue
            expo=Counter()
            for row in w['comparisons']:
                tt=terms(tuple(map(f,row['anchor_quintuple'])))
                def sgn(q):
                    lit=e.o(*q);return required[abs(lit)]*(1 if lit>0 else -1)
                ss=[co*sgn(x)*sgn(y) for x,y,co in tt]
                mi,o=row['minority_term'],row['other_term']
                assert ss.count(ss[mi])==1 and o!=mi
                for k,sg in ((mi,1),(o,-1)):
                    for q in tt[k][:2]:expo[e.canon[tuple(sorted(q))][0]]+=sg
            assert all(x==0 for x in expo.values());verified+=1
            clause=tuple(-v if s>0 else v for v,s in sorted(required.items()))
            clauses.setdefault(clause,{'orbits':target_orbits,'relative_phase_shifts':relative_shifts,'direction':direction,'sign_flip':flip})
    ordered=sorted(clauses)
    (a.out/'family.clauses').write_text(''.join(' '.join(map(str,c))+' 0\n' for c in ordered))
    (a.out/'family_witnesses.json').write_text(json.dumps([{'clause':c,'embedding':clauses[c]} for c in ordered],indent=2)+'\n')
    raw=(results/'ES8SYM/sets/c6_54pts_9layers.pts').read_bytes();pts=[]
    for line in raw.decode().splitlines():
        if not line.strip() or line.startswith('#'):continue
        x,y,z,u,v,w0=map(int,line.split());pts.append((2*x+y-z-2*u-v+w0,y+z-v-w0))
    det=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    checks=0;matches=0
    for mirror in (-1,1):
        pp=[(x,mirror*y) for x,y in pts]
        for target_orbits in itertools.permutations(range(9),len(layers)):
            for shifts in itertools.product(range(6),repeat=len(layers)):
             for direction,flip in itertools.product((-1,1),(-1,1)):
                mapping=dict(zip(layers,zip(target_orbits,shifts)))
                def p(x):
                    layer,k=divmod(x,6);o,s=mapping[layer]
                    return pp[6*o+(direction*k+s)%6]
                matches+=all((1 if det(*(p(x) for x in q))>0 else -1)==sg*flip for q,sg in pattern.items())
                checks+=1
    assert matches==0
    summary={'source_model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),
             'source_witness_sha256':hashlib.sha256(a.witness.read_bytes()).hexdigest(),
             'source_layers':layers,'embeddings_verified':verified,'tautological_premises':tautologies,
             'unique_clauses':len(ordered),'exact54_tests':checks,'exact54_forbidden_matches':matches,
             'exact54_sha256':hashlib.sha256(raw).hexdigest(),
             'family_sha256':hashlib.sha256((a.out/'family.clauses').read_bytes()).hexdigest(),
             'scope':'Euclidean sixfold realizations with the specified orbit action'}
    (a.out/'family_verified.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
