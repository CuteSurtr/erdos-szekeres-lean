#!/usr/bin/env python3
"""Stream-check completed m16 pool exports without retaining large CNFs."""
import audit_pool as audit
import json
import time

started = time.monotonic()
answers = []
for n in (7, 8):
    out = audit.SCRATCH.parent / f'pool/n{n}m16-b128'
    record = json.loads((out / 'result.json').read_text())
    audit.need(record['status'] not in ('STARTED', 'SEARCHING'), 'run not complete')
    source = audit.Path(record['source'])
    info = json.loads(source.read_text())
    original = source.parent / 'case.cnf'
    final = out / 'final.cnf'
    pool_record = json.loads((out / 'pool.json').read_text())
    pool = pool_record['masks']
    selected = set(pool)
    audit.need(len(pool) == len(selected) == record['pool_size'], 'duplicate or miscounted mask')
    audit.need(all(type(s) is int and 0 <= s < (1 << 16) for s in pool), 'mask range')
    old = json.loads((audit.HERE / f'results/input{n}.json').read_text())
    original_hash = audit.sha(original)
    audit.need(original_hash == record['source_cnf_sha256'] == info['hashes']['case.cnf']
               == old['source_cnf_sha256'], 'source differs from independently audited input')
    audit.need(record['source_result_sha256'] == audit.sha(source), 'source record hash')
    audit.need(record['source_script_sha256'] == audit.sha(audit.DRIVER), 'frozen driver hash')
    base_count, nv = record['base_clauses'], record['variables']
    with original.open() as src, (out / 'base.cnf').open() as base, final.open() as target:
        audit.need(src.readline().split() == ['p', 'cnf', str(nv), str(base_count+(1 << 16))], 'source header')
        audit.need(base.readline().split() == ['p', 'cnf', str(nv), str(base_count)], 'base header')
        audit.need(target.readline().split() == ['p', 'cnf', str(nv), str(base_count+len(pool))], 'final header')
        for i in range(base_count):
            a, b, c = src.readline(), base.readline(), target.readline()
            audit.need(a and a == b == c, 'base/prefix/final differ at ' + str(i))
        audit.need(base.read(1) == '', 'extra base content')
        clauses = {}
        for s in range(1 << 16):
            line = src.readline()
            audit.need(line, 'truncated original tail')
            if s in selected:
                clauses[s] = tuple(map(int, line.split()))
        audit.need(src.read(1) == '', 'extra source content')
        for s in pool:
            audit.need(tuple(map(int, target.readline().split())) == clauses[s], 'selected original clause differs')
        audit.need(target.read(1) == '', 'extra final content')
    final_hash = audit.sha(final)
    audit.need(final_hash == record['final_cnf_sha256'], 'final hash')
    audit.need(audit.sha(original) == original_hash, 'source changed during verification')
    entry = dict(status='FINAL_EXPORT_EXACT', m=16, n=n, finder_status=record['status'],
                 base_clauses=base_count, selected_masks=len(pool),
                 final_clauses=base_count+len(pool), final_cnf_sha256=final_hash,
                 source_cnf_sha256=original_hash, parent_result=record,
                 pool_masks=pool, final_cnf=str(final))
    answers.append(entry)
result = dict(label='COMPUTED', status='PASS', cases=answers,
              checker_sha256=audit.sha(__file__), elapsed_seconds=time.monotonic()-started,
              limits=dict(as_mib=400, one_cpu=True, external_seconds=20))
for root in (audit.SCRATCH, audit.HERE / 'results'):
    (root / 'pool_final_audit.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(dict(status='PASS', elapsed_seconds=result['elapsed_seconds'],
                     cases=[{k: c[k] for k in ('n', 'finder_status', 'final_clauses', 'selected_masks', 'final_cnf_sha256')} for c in answers]), sort_keys=True))
