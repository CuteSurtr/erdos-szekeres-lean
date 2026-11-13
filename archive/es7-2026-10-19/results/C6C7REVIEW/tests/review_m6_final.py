#!/usr/bin/env python3
"""Independent exact review of a retained rotation-specific GP cycle.

Usage: python3 -I review_m6_final.py --run RUN_DIR --witness WITNESS.json
Checks model archive binding, formal GP identity, every signed bracket and
rotation magnitude equality, and product-exponent cancellation. No solver,
full GP scan, or large point-set embedding test is run.
"""
import argparse
from collections import Counter
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import time

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('independent_first_review',HERE/'review_m6_witness.py')
R=importlib.util.module_from_spec(sp);sp.loader.exec_module(R)


def main():
    start=time.monotonic()
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True,type=Path);ap.add_argument('--witness',required=True,type=Path);args=ap.parse_args()
    wraw=args.witness.read_bytes();w=json.loads(wraw)
    raw=(args.run/'model.json').read_bytes();zraw=(args.run/'model.json.zst').read_bytes()
    manifest=json.loads((args.run/'archive_manifest.json').read_text())
    rec=next(r for r in manifest if r['file'].endswith('/model.json'))
    assert R.h(raw)==rec['raw_sha256']==w['model_sha256'] and R.h(zraw)==rec['zstd_sha256']
    assert subprocess.run(['zstd','-dc',str(args.run/'model.json.zst')],capture_output=True,check=True).stdout==raw
    pos=set(json.loads(raw));assert w['m']==6 and w['t']==10
    canonical={q:R.canonical(q) for q in it.combinations(range(60),3)}
    reps=sorted({c for c,s in canonical.values()});ids={c:i+1 for i,c in enumerate(reps)}
    assert len(ids)==5710
    sp=importlib.util.spec_from_file_location('actual_encoder_a',R.O.ROOT/'C7UPPER/gen.py')
    G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G);E=G.Enc(6,8,10);assert E.tvar==ids
    def literal(q):
        a,b,c=q;par=1 if (b-a)*(c-a)*(c-b)>0 else -1
        rep,sg=canonical[tuple(sorted(q))]
        return par*sg*ids[rep]
    def model_sign(l):return (1 if abs(l) in pos else -1)*(1 if l>0 else -1)
    pattern={};balance=Counter();edges=[]
    print(json.dumps({'event':'input','witness_sha256':R.h(wraw),'model_sha256':R.h(raw),'compressed_model_sha256':R.h(zraw),
                      'archive_model_bound':True,'triple_ids_cross_checked':len(ids),'formal_GP_monomials_cancelled':R.gp_symbolic_check()}),flush=True)
    for row in w['comparisons']:
        q=tuple(row['anchor_quintuple']);assert len(set(q))==5
        terms=R.products(q);signs=[];pairs=[];lits=[]
        for x,y,co in terms:
            lx,ly=literal(x),literal(y);assert lx==E.o(*x) and ly==E.o(*y)
            lits.append((lx,ly));signs.append(co*model_sign(lx)*model_sign(ly));pairs.append(tuple(sorted((abs(lx),abs(ly)))))
            for v in (abs(lx),abs(ly)):pattern[reps[v-1]]=1 if v in pos else -1
        mi,lo=row['minority_term'],row['other_term']
        assert signs==row['term_signs'] and signs.count(signs[mi])==1 and lo!=mi
        assert pairs[mi]==tuple(sorted(ids[tuple(x)] for x in row['greater_orbits']))
        assert pairs[lo]==tuple(sorted(ids[tuple(x)] for x in row['lesser_orbits']))
        assert row['weight']==1
        for v in pairs[mi]:balance[v]+=1
        for v in pairs[lo]:balance[v]-=1
        edges.append((pairs[mi],pairs[lo]))
        print(json.dumps({'event':'comparison','quintuple':q,'term_signs':signs,'orientation_literals':lits,
                          'greater_ids':pairs[mi],'lesser_ids':pairs[lo]}),flush=True)
    assert all(v==0 for v in balance.values())
    assert all(edges[i][1]==edges[(i+1)%len(edges)][0] for i in range(len(edges)))
    cut=tuple(-ids[q]*sg for q,sg in sorted(pattern.items(),key=lambda kv:ids[kv[0]]))
    assert all((lit>0)!=(abs(lit) in pos) for lit in cut)
    source_layers=sorted({x//6 for q in pattern for x in q})
    print(json.dumps({'event':'PASS','comparisons':len(edges),'candidate_clause':cut,'source_layers':source_layers,
                      'exponent_balance':dict(balance),'strict_cycle':True,'model_violates_cut':True,
                      'elapsed_seconds':round(time.monotonic()-start,3),'maximum_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'scope':'realizations invariant under the specified Euclidean sixfold rotation'}),flush=True)


if __name__=='__main__':main()
