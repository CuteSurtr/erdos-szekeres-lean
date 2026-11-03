#!/usr/bin/env python3
"""Independent second-witness and complete embedding-family check; no solver.

Usage: python3 -I review_m6_second.py --run FAMILY_RUN_DIR --family FAMILY_DIR
No candidate search or embedding implementation is imported. The independent
first-witness review supplies only formal GP expansion and rotation canonicals.
"""
import argparse
from collections import Counter
import hashlib
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
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True,type=Path);ap.add_argument('--family',required=True,type=Path);args=ap.parse_args()
    wraw=(args.run/'search/m6_cycle_witness.json').read_bytes();w=json.loads(wraw)
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
    pattern={};balance=Counter()
    print(json.dumps({'event':'input','witness_sha256':R.h(wraw),'model_sha256':R.h(raw),'compressed_model_sha256':R.h(zraw),
                      'archive_model_bound':True,'triple_ids_cross_checked':len(ids),'formal_GP_monomials_cancelled':R.gp_symbolic_check()}),flush=True)
    for row in w['comparisons']:
        q=tuple(row['anchor_quintuple']);terms=R.products(q);signs=[];pairs=[];lits=[]
        for x,y,co in terms:
            lx,ly=literal(x),literal(y);assert lx==E.o(*x) and ly==E.o(*y)
            lits.append((lx,ly));signs.append(co*model_sign(lx)*model_sign(ly));pairs.append(tuple(sorted((abs(lx),abs(ly)))))
            for v in (abs(lx),abs(ly)):pattern[reps[v-1]]=1 if v in pos else -1
        mi,lo=row['minority_term'],row['other_term']
        assert signs==row['term_signs'] and signs.count(signs[mi])==1 and lo!=mi
        assert pairs[mi]==tuple(sorted(ids[tuple(x)] for x in row['greater_orbits']))
        assert pairs[lo]==tuple(sorted(ids[tuple(x)] for x in row['lesser_orbits']))
        for v in pairs[mi]:balance[v]+=1
        for v in pairs[lo]:balance[v]-=1
        print(json.dumps({'event':'comparison','quintuple':q,'term_signs':signs,'orientation_literals':lits,
                          'greater_ids':pairs[mi],'lesser_ids':pairs[lo]}),flush=True)
    assert all(v==0 for v in balance.values())
    cut=tuple(-ids[q]*sg for q,sg in sorted(pattern.items(),key=lambda kv:ids[kv[0]]))
    assert cut==(-58,-59,-61,-63,-72,-74,-76,-154,-255,-358)
    source_layers=sorted({x//6 for q in pattern for x in q});assert source_layers==[0,1,3]
    # Enumerate every target injection, independent relative shifts, common
    # direction +/- and global bracket-sign reversal. No geometry resampling.
    seen=set();checked=0;conflicts=0
    for targets in it.permutations(range(10),3):
        for offsets in it.product(range(6),repeat=2):
            for direction,flip in it.product((-1,1),repeat=2):
                image={old:(target,offset) for old,target,offset in zip(source_layers,targets,(0,)+offsets)}
                def f(x):
                    layer,k=divmod(x,6);dest,offset=image[layer]
                    return 6*dest+(direction*k+offset)%6
                req={};conflict=False
                for q,sg in pattern.items():
                    l=literal(tuple(f(x) for x in q));value=sg*flip*(1 if l>0 else -1)
                    if abs(l) in req and req[abs(l)]!=value:conflict=True;break
                    req[abs(l)]=value
                if conflict:conflicts+=1;continue
                expo=Counter()
                for row in w['comparisons']:
                    terms=R.products(tuple(f(x) for x in row['anchor_quintuple']))
                    signs=[];pairs=[]
                    for x,y,co in terms:
                        lx,ly=literal(x),literal(y)
                        signs.append(co*req[abs(lx)]*req[abs(ly)]*(1 if lx*ly>0 else -1))
                        pairs.append((abs(lx),abs(ly)))
                    mi,lo=row['minority_term'],row['other_term']
                    assert signs==row['term_signs'] and signs.count(signs[mi])==1
                    for v in pairs[mi]:expo[v]+=1
                    for v in pairs[lo]:expo[v]-=1
                assert all(v==0 for v in expo.values())
                seen.add(tuple(-v*sg for v,sg in sorted(req.items())));checked+=1
                if checked%1024==0:assert time.monotonic()-start<60,'60-second limit'
    assert checked+conflicts==720*36*4
    family_bytes=''.join(' '.join(map(str,c))+' 0\n' for c in sorted(seen)).encode()
    retained=(args.family/'family.clauses').read_bytes();assert retained==family_bytes
    print(json.dumps({'event':'PASS','candidate_clause':cut,'exponent_balance':dict(balance),
                      'family_embeddings_checked':checked,'inconsistent_premises':conflicts,'unique_clauses':len(seen),
                      'family_sha256':R.h(family_bytes),'candidate_family_byte_match':True,
                      'elapsed_seconds':round(time.monotonic()-start,3),'maximum_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'scope':'realizations invariant under the specified Euclidean sixfold rotation'}),flush=True)


if __name__=='__main__':main()
