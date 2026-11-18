#!/usr/bin/env python3
"""Reconstruct the real-point membership CNF and independently replay cake."""
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

from geometry import bits, vertices, digest, geometry

HERE=Path(__file__).resolve().parent
CASE=Path('/home/jay/research/data/delta3-codex-20261113/extension/terminal15')
CAKE=Path('/home/jay/.local/bin/cake_lpr')


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    start=time.monotonic()
    P=json.loads((HERE/'data/real15.coordinates.json').read_text())['P']
    report,truth=geometry(P)
    expected=[]
    for family,sign in (('caps4',-1),('bad',-1),('targets',1)):
        expected.extend(tuple(sorted(sign*(i+1) for i in vertices(s))) for s in truth[family])
    rows=[];nv=nc=None
    cnf=CASE/'witness.terminal.cnf';proof=CASE/'fresh.blrat';compressed=CASE/'fresh.blrat.zst'
    before={str(p):digest(p) for p in (cnf,proof,compressed,CAKE)}
    with cnf.open() as f:
        for line in f:
            fields=line.split()
            if not fields or fields[0]=='c':continue
            if fields[0]=='p':
                assert fields[1]=='cnf' and nv is None;nv,nc=map(int,fields[2:]);continue
            row=tuple(map(int,fields));assert row[-1]==0 and all(1<=abs(x)<=15 for x in row[:-1])
            rows.append(tuple(sorted(row[:-1])))
    assert nv==15 and nc==313 and len(rows)==nc and Counter(rows)==Counter(expected)
    # Exhaustive direct membership assignment evaluation, separate from
    # upward-closure semantics used by the geometry checker.
    satisfied=0
    for s in range(1<<15):
        clause_truth=all(any(bool(s>>(abs(x)-1)&1)==(x>0) for x in row) for row in rows)
        semantic_truth=not truth['D'][s] and not truth['F'][s] and not truth['T'][((1<<15)-1)^s]
        assert clause_truth==semantic_truth
        satisfied+=clause_truth
    assert satisfied==0
    # Check the retained compressed proof independently, without deleting it.
    h=hashlib.sha256()
    process=subprocess.Popen(['/usr/bin/zstd','-q','-d','-c',str(compressed)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for block in iter(lambda:process.stdout.read(1<<16),b''):h.update(block)
    err=process.stderr.read();assert process.wait(timeout=18)==0,err
    assert h.hexdigest()==before[str(proof)]
    cmd=['/usr/bin/timeout','20s','/usr/bin/prlimit','--as=419430400','--cpu=18',str(CAKE),
         '--CML_HEAP_SIZE=128','--CML_STACK_SIZE=32',str(cnf),str(proof)]
    log=HERE/'data/membership-cake.log';timing=HERE/'data/membership-cake.time'
    assert not timing.exists()
    with log.open('x') as f:
        replay=subprocess.run(['/usr/bin/time','-v','-o',str(timing)]+cmd,stdout=f,stderr=subprocess.STDOUT)
    acceptance='s VERIFIED UNSAT' in log.read_text().splitlines()
    after={str(p):digest(p) for p in (cnf,proof,compressed,CAKE)}
    accepted=acceptance and before==after
    result={'label':'CERTIFIED' if accepted else 'NOT CONFIRMED','scope':'Fixed real fifteen-point terminal-safe membership CNF',
            'm':15,'n':7,'variables':nv,'clauses':nc,'family_counts':{'four_caps':48,'bad_triples':78,'six_targets':187},
            'all_clause_families_match':True,'assignments_checked':1<<15,'satisfying_assignments':satisfied,
            'exact_cake_acceptance_line':acceptance,'returncode':replay.returncode,'command':cmd,
            'before':before,'after':after,'stable_inputs':before==after,'compressed_roundtrip_verified':True,
            'proof_bytes':proof.stat().st_size,'compressed_bytes':compressed.stat().st_size,
            'seconds':time.monotonic()-start,'script_sha256':digest(__file__),
            'own_geometry_source_sha256':digest(HERE/'geometry.py'),'coordinate_sha256':digest(HERE/'data/real15.coordinates.json'),
            'log_sha256':digest(log)}
    with (HERE/'data/membership.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result));assert accepted,'Exact acceptance line and stable inputs required.'


if __name__=='__main__':main()
