#!/usr/bin/env python3
"""Pin parent accepted proof artifacts without launching a proof checker."""
import hashlib
import json
import os
from pathlib import Path
import resource

resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
R=Path(__file__).resolve().parents[1]
E=R.parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')

def sha(p):
    h=hashlib.sha256();a=p.stat()
    with p.open('rb') as f:
        offset=0;pending=0
        for b in iter(lambda:f.read(1 << 20),b''):
            h.update(b);pending+=len(b)
            if pending>=64 << 20:
                os.posix_fadvise(f.fileno(),offset,pending,os.POSIX_FADV_DONTNEED)
                offset+=pending;pending=0
        if pending:os.posix_fadvise(f.fileno(),offset,pending,os.POSIX_FADV_DONTNEED)
    b=p.stat();assert (a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns)
    return h.hexdigest()

cases={}
for m in (11,12,13,14):
    tag=f'low{m}-n7-'+('b' if m==14 else 'a')
    case=W/tag
    parent=json.loads((case/'result.json').read_text())
    source=W/f'low{m}-n7{"-compact" if m==14 else ""}.cnf'
    assert sha(source)==sha(case/'input.cnf')==parent['hashes']['input.cnf']
    hashes={name:sha(case/name) for name in ('input.cnf','proof.blrat','proof.blrat.zst','cake.log')}
    assert all(hashes[name]==parent['hashes'][name] for name in hashes)
    assert (case/'proof.blrat').stat().st_size==parent['proof_bytes']
    if m<14:
        assert parent['finished'] and parent['status']=='UNSAT_CERTIFIED'
        assert 's VERIFIED UNSAT' in (case/'cake.log').read_text().splitlines()
        acceptance=case/'result.json';accept_log=case/'cake.log'
    else:
        assert parent['status']=='UNSAT_UNCERTIFIED'
        assert 'CakeML heap space exhausted.' in (case/'cake.log').read_text()
        replay=W/'low14-replay-a'
        accepted=json.loads((replay/'result.json').read_text())
        assert accepted['status']=='UNSAT_CERTIFIED' and accepted['hashes_before']==accepted['hashes_after']
        assert hashes['input.cnf']==accepted['hashes_before']['input.cnf']
        assert hashes['proof.blrat']==accepted['hashes_before']['proof.blrat']
        assert 's VERIFIED UNSAT' in (replay/'cake.log').read_text().splitlines()
        acceptance=replay/'result.json';accept_log=replay/'cake.log'
    cases[str(m)]={'parent_label':'CERTIFIED','source_run':str(case),'source_cnf':str(source),
        'hashes_recomputed_streaming':hashes,'raw_proof_bytes':parent['proof_bytes'],
        'acceptance_receipt':str(acceptance),'acceptance_receipt_sha256':sha(acceptance),
        'accepted_log':str(accept_log),'accepted_log_sha256':sha(accept_log),
        'parent_exact_acceptance_line_seen':True,'fresh_independent_replay_here':False,
        'original_heap128_failure_preserved':m==14}
sources={str(p):sha(p) for p in (E/'low_split_cnf.cpp',E/'low_split_compact.cpp',E.parents[1]/'compact/compact_cnf.cpp')}
result={'status':'PASS','label':'Parent CERTIFIED artifacts pinned; no fresh replay in this audit',
        'cases':cases,'sources':sources,'stream_cache_release':'every64MiB and remainder',
        'limits':{'AS_MiB':300,'CPUs':1,'wall_seconds':20,'CPU_seconds':19}}
with (R/'data/parent-certificate-provenance.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','parent_accepted_sizes':list(cases),'fresh_replays':0}))
