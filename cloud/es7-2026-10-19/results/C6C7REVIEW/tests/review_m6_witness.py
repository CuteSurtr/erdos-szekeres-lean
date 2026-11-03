#!/usr/bin/env python3
"""Independent exact check of a rotation-specific product-cycle witness.

Usage: python3 -I review_m6_witness.py --witness WITNESS.json --model MODEL.json
       --archive ARCHIVE_DIR
Checks GP algebra by formal integer polynomial expansion, reconstructs encoder A
IDs independently, and tests the cut on all ordered pairs and relative shifts
of the exact 54-point set and its mirror. No candidate verifier is imported.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exact54_helpers',HERE/'certified54.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
O=C.O


def h(raw): return hashlib.sha256(raw).hexdigest()


def gp_symbolic_check():
    # Translate anchor a to zero. Other vectors have eight independent symbols.
    def bracket(i,j):
        return {tuple(sorted((2*i,2*j+1))):1,tuple(sorted((2*i+1,2*j))):-1}
    def multiply(p,q):
        out=Counter()
        for x,c in p.items():
            for y,d in q.items():out[tuple(sorted(x+y))]+=c*d
        return out
    terms=[multiply(bracket(0,1),bracket(2,3)),multiply(bracket(0,2),bracket(1,3)),multiply(bracket(0,3),bracket(1,2))]
    total=Counter()
    for sign,p in zip((1,-1,1),terms):
        for x,c in p.items():total[x]+=sign*c
    assert all(v==0 for v in total.values())
    return len(total)


def canonical(q):
    best=None; sg=None
    for shift in range(6):
        moved=tuple((x//6)*6+(x%6+shift)%6 for x in q)
        rep=tuple(sorted(moved))
        a,b,c=moved
        sign=1 if (b-a)*(c-a)*(c-b)>0 else -1
        if best is None or rep<best: best,sg=rep,sign
        elif rep==best:assert sign==sg
    return best,sg


def products(q):
    a,b,c,d,e=q
    return [((a,b,c),(a,d,e),1),((a,b,d),(a,c,e),-1),((a,b,e),(a,c,d),1)]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--witness',type=Path,required=True);ap.add_argument('--model',type=Path,required=True);ap.add_argument('--archive',type=Path,required=True)
    args=ap.parse_args();wraw=args.witness.read_bytes();w=json.loads(wraw);raw=args.model.read_bytes()
    assert w['m']==6 and w['t']==10
    archive_name='gp_m6K8t10.cnf.model.json.zst';zraw=(args.archive/archive_name).read_bytes()
    recorded={line.split()[1]:line.split()[0] for line in (args.archive/'SHA256SUMS').read_text().splitlines()}
    assert h(zraw)==recorded[archive_name]
    archived_raw=subprocess.run(['zstd','-dc',str(args.archive/archive_name)],capture_output=True,check=True).stdout
    assert archived_raw==raw and h(raw)==w['model_sha256']
    positive=set(json.loads(raw));assert all(isinstance(x,int) and x>0 for x in positive)
    reps=sorted({canonical(q)[0] for q in it.combinations(range(60),3)})
    ids={q:i+1 for i,q in enumerate(reps)};assert len(ids)==5710
    # Independently reconstructed numbering is cross-checked with the actual encoder.
    sp=importlib.util.spec_from_file_location('actual_encoder_a',O.ROOT/'C7UPPER/gen.py')
    G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G);E=G.Enc(6,8,10)
    assert ids==E.tvar
    print(json.dumps({'event':'inputs','witness_sha256':h(wraw),'model_sha256':h(raw),'compressed_model_sha256':h(zraw),
                      'archive_match':True,'triple_ids_cross_checked':len(ids),'formal_GP_monomials_cancelled':gp_symbolic_check()}),flush=True)
    used=set();exponents=Counter();records=[]
    for comp in w['comparisons']:
        q=tuple(comp['anchor_quintuple']);assert len(set(q))==5
        terms=[];signs=[];pairs=[]
        for left,right,coefficient in products(q):
            rc,sc=canonical(left);rd,sd=canonical(right);vi,vj=ids[rc],ids[rd]
            assert E.o(*left)==sc*vi and E.o(*right)==sd*vj
            used.update((vi,vj))
            sl=sc*(1 if vi in positive else -1);sr=sd*(1 if vj in positive else -1)
            signs.append(coefficient*sl*sr);pairs.append(tuple(sorted((rc,rd))))
            terms.append({'triples':[left,right],'orientation_literals':[sc*vi,sd*vj],
                          'bracket_signs':[sl,sr],'coefficient':coefficient,'term_sign':signs[-1]})
        assert signs==comp['term_signs']
        mi=comp['minority_term'];other=comp['other_term']
        assert signs.count(signs[mi])==1 and other!=mi
        assert pairs[mi]==tuple(sorted(map(tuple,comp['greater_orbits'])))
        assert pairs[other]==tuple(sorted(map(tuple,comp['lesser_orbits'])))
        assert comp['weight']==1
        for triple in pairs[mi]:exponents[triple]+=1
        for triple in pairs[other]:exponents[triple]-=1
        record={'anchor_quintuple':q,'terms':terms,'greater_product_ids':sorted(ids[x] for x in pairs[mi]),
                'lesser_product_ids':sorted(ids[x] for x in pairs[other])}
        records.append(record);print(json.dumps({'event':'verified_comparison',**record}),flush=True)
    assert all(v==0 for v in exponents.values())
    cut=[-v if v in positive else v for v in sorted(used)]
    assert cut==[-58,-71,-72,-73,-74,-75,-76,-712,751,-868]
    assert all((v>0)!=(abs(v) in positive) for v in cut)
    # Translate every cut literal back to its canonical triple; only layers 0,3 occur.
    patterns=[]
    for lit in cut:
        triple=reps[abs(lit)-1]
        assert set(x//6 for x in triple)<={0,3}
        patterns.append((lit,triple))
    rows=[list(map(int,line.split())) for line in C.SOURCE.read_text().splitlines() if line and not line.startswith('#')]
    original=list(map(C.convert,rows));trial_count=0;minimum_satisfied=10;hist=Counter()
    for mirror in (False,True):
        seeds,_=C.normalized_layers(original,mirror)
        points=O.points6(seeds)
        for first,second in it.permutations(range(9),2):
            for relative_shift in range(6):
                truths=[]
                for lit,triple in patterns:
                    actual=[]
                    for x in triple:
                        layer,k=divmod(x,6)
                        actual.append(first*6+k if layer==0 else second*6+(k+relative_shift)%6)
                    value=O.turn(*(points[x] for x in actual))
                    assert value!=0
                    truths.append((value>0)==(lit>0))
                assert any(truths),(mirror,first,second,relative_shift)
                cnt=sum(truths);minimum_satisfied=min(minimum_satisfied,cnt);hist[cnt]+=1;trial_count+=1
    assert trial_count==864
    print(json.dumps({'event':'verified_cut','cut':cut,'exponent_balance':{str(k):v for k,v in exponents.items()},
                      'model_violates_cut':True,'exact54_embeddings':trial_count,'minimum_true_literals':minimum_satisfied,
                      'true_literal_count_histogram':dict(hist),'mirrors':True,
                      'scope':'realizations invariant under the specified Euclidean sixfold rotation',
                      'status':'PASS'}),flush=True)


if __name__=='__main__': main()
