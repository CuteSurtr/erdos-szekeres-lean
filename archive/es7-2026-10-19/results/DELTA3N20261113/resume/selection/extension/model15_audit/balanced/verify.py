#!/usr/bin/env python3
"""Independent exact equivalence of balanced and discovery coordinates."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import sys
import time
import traceback

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
sys.path.insert(0,str(AUDIT))
from geometry import geometry, digest, vertices

ROOT=Path('/home/jay/research/data/delta3-codex-20261113/extension')
EXPECTED=[[0,0],[37,-35],[38,-248],[84,-270],[202,-640],[472,-427],[653,-757],
          [665,-793],[666,-717],[683,-718],[736,-567],[737,-827],[926,-895],[999,-926],[1000,0]]


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    start=time.monotonic()
    result={'label':'COMPUTED independent exact coordinate equivalence','status':'IN_PROGRESS',
            'script_sha256':digest(__file__),'independent_geometry_source_sha256':digest(AUDIT/'geometry.py')}
    data=HERE/'data';data.mkdir(exist_ok=True)
    try:
        prior_manifest=AUDIT/'SHA256SUMS';prior_count=0
        for line in prior_manifest.read_text().splitlines():
            expected,relative=line.split('  ',1)
            assert digest(AUDIT/relative)==expected,(relative,'frozen original changed')
            prior_count+=1
        source=ROOT/'balance15-a/witness.json';pointfile=ROOT/'balance15-a/witness.points'
        balanced_cnf=ROOT/'terminal15/balanced.terminal.cnf'
        original_coords=AUDIT/'data/real15.coordinates.json'
        original_cnf=AUDIT/'data/certificate/witness.terminal.cnf'
        proof=AUDIT/'data/certificate/fresh.blrat'
        paths=[source,pointfile,balanced_cnf,original_coords,original_cnf,proof]
        before={str(p):digest(p) for p in paths}
        raw=json.loads(source.read_text());P=raw['P']
        assert P==EXPECTED and raw['m']==15 and raw['n']==7
        text=[tuple(map(int,line.split())) for line in pointfile.read_text().splitlines() if line.strip()]
        assert text[0]==(15,7) and [list(p) for p in text[1:]]==P
        original=json.loads(original_coords.read_text())['P']
        own,truth=geometry(P)
        discovery,oldtruth=geometry(original)
        assert own['signs']==discovery['signs'] and len(own['signs'])==455
        assert own['signs']==raw['orientation_signs']
        for family in ('signs','caps4','bad','targets','D','F','T','nonconvex'):
            assert truth[family]==oldtruth[family],family
        for key in ('four_caps','five_caps','bad_triples','convex_six_subsets','convex_seven_subsets',
                    'maximum_cap_cup_convex','all_subsets_checked','terminal_safe_deltas','failure_reasons',
                    'weak_deltas','weak_delta_size_counts','rooted_weak_deltas'):
            assert own[key]==discovery[key],key
        expected=[]
        for family,sign in (('caps4',-1),('bad',-1),('targets',1)):
            expected.extend(tuple(sorted(sign*(i+1) for i in vertices(s))) for s in truth[family])
        actual=[];nv=nc=None
        for line in balanced_cnf.read_text().splitlines():
            parts=line.split()
            if not parts or parts[0]=='c':continue
            if parts[0]=='p':
                assert parts[1]=='cnf' and nv is None;nv,nc=map(int,parts[2:]);continue
            row=tuple(map(int,parts));assert row[-1]==0 and 0 not in row[:-1]
            actual.append(tuple(sorted(row[:-1])))
        assert nv==15 and nc==313 and len(actual)==313
        assert Counter(actual)==Counter(expected)
        assert balanced_cnf.read_bytes()==original_cnf.read_bytes()
        cert=json.loads((AUDIT/'data/membership.json').read_text())
        assert cert['label']=='CERTIFIED' and cert['exact_cake_acceptance_line'] and cert['stable_inputs']
        assert 's VERIFIED UNSAT' in (AUDIT/'data/membership-cake.log').read_text().splitlines()
        assert digest(original_cnf)==cert['before'][str(ROOT/'terminal15/witness.terminal.cnf')]
        assert digest(proof)==cert['before'][str(ROOT/'terminal15/fresh.blrat')]
        after={str(p):digest(p) for p in paths};assert before==after
        for file,target in ((source,data/'coordinates.json'),(pointfile,data/'coordinates.points'),
                            (balanced_cnf,data/'membership.cnf')):
            with target.open('xb') as f:f.write(file.read_bytes())
        result.update(status='PASS',result=own,all_455_signs_match=True,all_semantic_families_identical=True,
            all_32768_selection_semantics_identical=True,
            membership_clauses_reconstructed=313,membership_cnf_byte_identical=True,
            certificate_applicability='Existing independently accepted binary LRAT applies to the identical balanced membership CNF; no additional replay needed.',
            before=before,after=after,stable_inputs=True,
            original_audit_manifest={'sha256':digest(prior_manifest),'files_checked':prior_count,'unchanged':True})
    except BaseException:
        result.update(status='FAIL',error=traceback.format_exc());raise
    finally:
        result.update(seconds=time.monotonic()-start,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      checked_utc=datetime.now(timezone.utc).isoformat())
        with (data/'equivalence.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
        small={k:v for k,v in result.items() if k not in ('result','before','after')}
        if 'result' in result:small['minimum_absolute_determinant']=result['result']['minimum_absolute_determinant']
        print(json.dumps(small))


if __name__=='__main__':main()
