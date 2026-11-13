#!/usr/bin/env python3
"""Embed an exact linear determinant obstruction into all sixfold orbit slots.

Every candidate embedding receives an exact coefficient-cancellation check.
The source witness must already pass tests/verify_linear.py, including the
independent direct polynomial identity and certified54 embedding tests.
"""
import argparse
from collections import defaultdict
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import random
import time

ROOT=Path(__file__).resolve().parent.parent


def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--witness',required=True,type=Path);ap.add_argument('--verified',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--order-preserving',action='store_true');ap.add_argument('--shift-limit',type=int);ap.add_argument('--independent',type=Path)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    raw=args.witness.read_bytes();w=json.loads(raw);v=json.loads(args.verified.read_text());wh=hashlib.sha256(raw).hexdigest()
    assert v['status']=='PASS' and v['witness_sha256']==wh and v['direct_symbolic_identity'] and v['reverse_direction_identity']
    assert v['exact54_forbidden_matches']==0
    M=load('linear_forms',Path(__file__).with_name('math_linear.py'));G=load('encoder',ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,w['t'])
    vs=M.variables(w['t']);ix={v:j for j,v in enumerate(vs)};forms={var:M.form(q,ix) for q,var in E.tvar.items()}
    layers=w['source_layers'];assert 2<=len(layers)<=9
    if len(layers)>4:
        assert args.order_preserving and args.shift_limit and v['exact54_tests']>=100 and args.independent
        independent=json.loads(args.independent.read_text());assert independent['verified'] and independent['witness_sha256']==wh and independent['model_sha256']==w['model_sha256']
    V=load('exact_known_set',Path(__file__).parent/'tests/verify_sdp.py');known_path,known=V.known54();reverse={var:q for q,var in E.tvar.items()}
    clauses={};verified=0;conflicts=0;exact_tests=0
    shift_patterns=None
    if args.shift_limit:
        rng=random.Random(20261104);shift_patterns={(0,)*(len(layers)-1)}
        while len(shift_patterns)<min(args.shift_limit,6**(len(layers)-1)):shift_patterns.add(tuple(rng.randrange(6) for _ in range(len(layers)-1)))
        shift_patterns=sorted(shift_patterns)
    stream=(args.out/'family.clauses').open('wb') if args.order_preserving else None
    records=(args.out/'family_witnesses.jsonl').open('w') if args.order_preserving else None
    targets_iter=it.combinations(range(w['t']),len(layers)) if args.order_preserving else it.permutations(range(w['t']),len(layers))
    for targets in targets_iter:
        for offsets in (shift_patterns if shift_patterns is not None else it.product(range(6),repeat=len(layers)-1)):
            for direction,flip in it.product((-1,1),repeat=2):
                mapping=dict(zip(layers,zip(targets,(0,)+offsets)))
                def f(x):
                    layer,k=divmod(x,6);target,shift=mapping[layer]
                    return 6*target+(direction*k+shift)%6
                required={};balance=defaultdict(int);weights=defaultdict(int);conflict=False
                for row in w['records']:
                    q=tuple(f(x) for x in row['triple']);lit=E.o(*q)
                    sg=row['required_sign']*flip*(1 if lit>0 else -1);var=abs(lit)
                    if var in required and required[var]!=sg:conflict=True
                    required[var]=sg
                    weights[var]+=row['weight']
                    for j,c in forms[var].items():balance[j]+=row['weight']*sg*c
                assert not any(balance.values()),'mapped identity fails'
                if conflict:conflicts+=1;continue
                clause=tuple(-var*sg for var,sg in sorted(required.items()))
                embedding={'orbits':targets,'relative_phase_shifts':offsets,'direction':direction,'global_sign':flip}
                if args.order_preserving:
                    if clause not in clauses:
                        if len(layers)>4:
                            target_to_known=dict(zip(targets,range(len(layers))))
                            for mirror in (1,-1):
                                pp=V.mirrored_ccw(known,mirror)
                                def point(x):return pp[6*target_to_known[x//6]+x%6]
                                values={var:V.det(*(point(x) for x in reverse[var])) for var in required};assert all(values.values())
                                assert sum(values[var]*required[var]*weights[var] for var in required)==0
                                assert any((values[var]>0)!=(required[var]>0) for var in required);exact_tests+=1
                        clauses[clause]=None
                        stream.write((' '.join(map(str,clause))+' 0\n').encode())
                        records.write(json.dumps({'clause':clause,'embedding':embedding})+'\n')
                else:clauses.setdefault(clause,embedding)
                verified+=1
    if args.order_preserving:
        stream.close();records.close();payload=(args.out/'family.clauses').read_bytes()
    else:
        ordered=sorted(clauses);payload=''.join(' '.join(map(str,c))+' 0\n' for c in ordered).encode()
        (args.out/'family.clauses').write_bytes(payload)
        (args.out/'family_witnesses.json').write_text(json.dumps([{'clause':c,'embedding':clauses[c]} for c in ordered],indent=2)+'\n')
    result={'rigor':'exact computation; soundness uses written rotation-specific linear identity proof',
            'source_witness_sha256':wh,'source_model_sha256':w['model_sha256'],'source_verified_sha256':hashlib.sha256(args.verified.read_bytes()).hexdigest(),
            'embeddings_verified':verified,'inconsistent_premises':conflicts,'source_layers':layers,'unique_clauses':len(clauses),'orbit_injections':'order-preserving only' if args.order_preserving else 'all injections',
            'family_sha256':hashlib.sha256(payload).hexdigest(),'source_exact54_tests':v['exact54_tests'],
            'source_exact54_forbidden_matches':v['exact54_forbidden_matches'],'elapsed_seconds':round(time.monotonic()-start,3),
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'status':'PASS'}
    if args.shift_limit:result.update({'relative_shift_patterns':len(shift_patterns),'coverage':'bounded partial family, not exhaustive'})
    if exact_tests:result.update({'exact54_tests':exact_tests,'exact54_test_scope':'each emitted clause on original and mirrored CCW injective embeddings','exact54_forbidden_matches':0,'exact54_sha256':hashlib.sha256(known_path.read_bytes()).hexdigest()})
    if args.independent:result['independent_verification_sha256']=hashlib.sha256(args.independent.read_bytes()).hexdigest()
    (args.out/'family_verified.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
