#!/usr/bin/env python3
"""Independently check the sixfold GP cycle through encoder A and exact points.

The witness is valid only for realizations with the specified rotational
symmetry: geometric rotation preserves determinant magnitude. This checker
also evaluates the forbidden sign pattern on every ordered selection of distinct
orbits of the certified 54-point set, with all cyclic labels and both mirrors.
No generated clause is inserted into a CNF by this script.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


def load_module(path):
    spec=importlib.util.spec_from_file_location('reference_encoder',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def triples(q):
    a,b,c,d,e=q
    return (((a,b,c),(a,d,e),1),((a,b,d),(a,c,e),-1),((a,b,e),(a,c,d),1))


import sys
sys.dont_write_bytecode = True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    results=Path(__file__).resolve().parents[1]
    mod=load_module(results/'C7UPPER/gen.py')
    e=mod.Enc(6,8,10)
    positive=set(json.loads(args.model.read_text()))
    witness=json.loads(args.witness.read_text())
    assert witness['model_sha256']==hashlib.sha256(args.model.read_bytes()).hexdigest()
    assert all(e.tvar[q]==i+1 for i,q in enumerate(sorted(e.tvar)))
    used={};exponents=Counter();comparisons=[]; products=[]
    def sign(q):
        l=e.o(*q);v=abs(l)
        used[v]=v in positive
        return (1 if l>0 else -1)*(1 if v in positive else -1)
    def orbit(q):
        return e.canon[tuple(sorted(q))][0]
    for row in witness['comparisons']:
        q=tuple(row['anchor_quintuple']);tt=triples(q)
        signs=[co*sign(x)*sign(y) for x,y,co in tt]
        assert signs==row['term_signs']
        mi,j=row['minority_term'],row['other_term']
        assert mi!=j and signs.count(signs[mi])==1
        plus=tuple(sorted((orbit(tt[mi][0]),orbit(tt[mi][1]))))
        minus=tuple(sorted((orbit(tt[j][0]),orbit(tt[j][1]))))
        assert plus==tuple(sorted(map(tuple,row['greater_orbits'])))
        assert minus==tuple(sorted(map(tuple,row['lesser_orbits'])))
        w=row['weight'];assert w==1
        for x in plus:exponents[x]+=w
        for x in minus:exponents[x]-=w
        products.append((plus,minus))
        comparisons.append({'quintuple':q,'gp_signs':signs,'literals':[[e.o(*x),e.o(*y)] for x,y,_ in tt]})
    assert products and all(products[i][1]==products[(i+1)%len(products)][0] for i in range(len(products)))
    assert all(v==0 for v in exponents.values())
    clause=[-v if b else v for v,b in sorted(used.items())]
    assert all((l>0)!=(abs(l) in positive) for l in clause)
    # Z[zeta_6] -> (2*Re(z), 2*Im(z)/sqrt(3)); orientation is a
    # positive scalar multiple of the ordinary integer determinant.
    raw=(results/'ES8SYM/sets/c6_54pts_9layers.pts').read_bytes()
    points=[]
    for line in raw.decode().splitlines():
        if not line.strip() or line.startswith('#'):continue
        a,b,c,d,f,g=map(int,line.split())
        points.append((2*a+b-c-2*d-f+g,b+c-f-g))
    assert len(points)==54
    determinant=lambda a,b,c: (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for q in itertools.combinations(points,3):assert determinant(*q)!=0
    expected={q:1 if v in positive else -1 for q,v in e.tvar.items() if v in used}
    actual_layers=sorted({x//6 for q in expected for x in q})
    assert 2 <= len(actual_layers) <= 3, actual_layers
    checks=0;matching=0;gp_checks=0;rotation_checks=0
    for mirror in (False,True):
        pts=[(x,-y if mirror else y) for x,y in points]
        for target_orbits in itertools.permutations(range(9),len(actual_layers)):
            for shifts in itertools.product(range(6),repeat=len(actual_layers)):
                mapping=dict(zip(actual_layers,zip(target_orbits,shifts)))
                def p(x):
                    layer,k=divmod(x,6)
                    assert layer in actual_layers
                    o,s=mapping[layer]
                    return pts[6*o+(k+s)%6]
                is_match=all((1 if determinant(*(p(x) for x in q))>0 else -1)==sg for q,sg in expected.items())
                checks+=1;matching+=is_match
                for row in witness['comparisons']:
                    vals=[]
                    for x,y,co in triples(row['anchor_quintuple']):
                        dx,dy=determinant(*(p(v) for v in x)),determinant(*(p(v) for v in y))
                        vals.append(co*dx*dy)
                        for q,dq in ((x,dx),(y,dy)):
                            rep=orbit(q)
                            assert abs(dq)==abs(determinant(*(p(v) for v in rep)))
                            rotation_checks+=1
                    assert sum(vals)==0 and all(vals)
                    gp_checks+=1
    assert matching==0
    result={'rigor':'exact computation; soundness uses written GP and rotation proof',
            'model_sha256':witness['model_sha256'],
            'generator_sha256':hashlib.sha256((results/'C7UPPER/gen.py').read_bytes()).hexdigest(),
            'witness_sha256':hashlib.sha256(args.witness.read_bytes()).hexdigest(),
            'verified_all_triple_ids':len(e.tvar),'comparisons':comparisons,
            'exponents':{','.join(map(str,k)):v for k,v in sorted(exponents.items())},
            'candidate_clause':clause,'candidate_added_to_cnf':False,
            'exact54_sha256':hashlib.sha256(raw).hexdigest(),'exact54_all_triples_nonzero':True,
            'source_layers':actual_layers,'exact54_labelled_pair_tests':checks,'exact54_forbidden_pattern_matches':matching,
            'exact54_gp_identities_checked':gp_checks,'exact54_rotation_equalities_checked':rotation_checks}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
