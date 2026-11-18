#!/usr/bin/env python3
"""Read parent outcomes, independently reconstruct filters and check raw hashes.

No solver or proof checker is invoked. UNKNOWN traces are not hashed here.
"""
import check_rooted as audit
import hashlib
import itertools
import json
import math
import sys
import time

started = time.monotonic()
n = int(sys.argv[1])
audit.require(n in (7, 8), 'n')
root = audit.WORK.parent / f'rooted/sweep{n}'
destination = audit.HERE / 'results' / f'sweep{n}'
destination.mkdir(exist_ok=True)
outcomes = json.loads((root / 'status.json').read_text())
audit.require([x['m'] for x in outcomes] == list(range(n+2, 17)), 'incomplete sweep')
frozen_filter = audit.sha(root / 'source/rooted_formula.py')
frozen_encoder = audit.sha(root / 'source/compact_cnf.cpp')
audit.require(frozen_filter == audit.sha(audit.FILTER), 'frozen filter differs')
audit.require(frozen_encoder == audit.sha(audit.RESUME / 'compact/compact_cnf.cpp'), 'frozen compact source differs')
cases = []
for outcome in outcomes:
    m = outcome['m']
    case = root / f'm{m}'
    record_path = case / 'solve/result.json'
    raw = record_path.read_bytes()
    record = json.loads(raw)
    generation = json.loads((case / 'rooted.generation.json').read_text())
    full, child = case / 'full.cnf', case / 'rooted.cnf'
    audit.require(record['cnf'] == str(child), 'solver input path differs')
    masks = sorted(audit.mask(s) for k in range(3, m-n+3)
                   for s in itertools.combinations(range(m), k))
    rootbit = 1 << (m-1)
    kept_count = sum(math.comb(m-1, k-1) for k in range(3, m-n+3))
    phase, index, count = '', 0, 0
    independent_hash = hashlib.sha256()
    with full.open('rb') as stream:
        header = stream.readline().split()
        audit.require(header[:2] == [b'p', b'cnf'], 'full CNF header')
        nv, nc = map(int, header[2:])
        child_count = nc-len(masks)+kept_count
        independent_hash.update(f'p cnf {nv} {child_count}'.encode().ljust(95)+b'\n')
        for line in stream:
            if line.startswith(b'c phase '):
                phase = line.split()[2].decode()
            elif line.startswith(b'c') or not line.strip():
                pass
            else:
                count += 1
                if phase == 'forall_delta':
                    d = masks[index]
                    index += 1
                    if not d & rootbit:
                        continue
            independent_hash.update(line)
    audit.require(count == nc and index == len(masks), 'source clause/mask count')
    cnf_hash = audit.sha(child)
    audit.require(independent_hash.hexdigest() == cnf_hash == record['hashes']['input.cnf']
                   == generation['output_sha256'], 'derived CNF hash mismatch')
    audit.require(audit.sha(full) == generation['input_sha256'], 'source CNF hash mismatch')
    audit.require(generation['source_sha256'] == frozen_filter, 'generation source hash mismatch')
    audit.require(record['status'] == outcome['status'], 'status mismatch')
    audit.require(audit.sha(case / 'solve/cadical.log') == record['hashes']['cadical.log'], 'solver log hash')
    checked = {'input.cnf': cnf_hash, 'cadical.log': record['hashes']['cadical.log']}
    if record['status'] == 'UNSAT_CERTIFIED':
        log = case / 'solve/cake.log'
        audit.require('s VERIFIED UNSAT' in log.read_text().splitlines(), 'missing exact acceptance line')
        for name in ('cake.log', 'proof.lrat', 'proof.lrat.zst'):
            h = audit.sha(case / 'solve' / name)
            audit.require(h == record['hashes'][name], name + ' hash mismatch')
            checked[name] = h
        (destination / f'm{m}-cake.log').write_bytes(log.read_bytes())
    else:
        audit.require(record['status'] == 'UNKNOWN', 'new outcome needs separate audit')
    (destination / f'm{m}-result.json').write_bytes(raw)
    cases.append(dict(n=n, m=m, parent_status=record['status'],
                      clauses=child_count, rooted_masks=kept_count,
                      independently_reconstructed_child=True, checked_hashes=checked,
                      proof_bytes=record.get('proof_bytes'),
                      independently_replayed_cake=False,
                      unknown_trace_hashes_checked=False if record['status'] == 'UNKNOWN' else None))
    audit.require(record_path.read_bytes() == raw, 'result changed during read')
if n in (7, 8):
    controlled = json.loads((audit.HERE / f'results/formula{n}.json').read_text())
    audit.require(cases[-1]['checked_hashes']['input.cnf'] == controlled['child_sha256'], 'actual m16 child differs from canonical control')
report = dict(label='COMPUTED', status='PARENT_LOGS_HASHES_FILTERS_CONFIRMED', n=n,
              frozen_filter_sha256=frozen_filter, frozen_compact_sha256=frozen_encoder,
              cases=cases, checker_sha256=audit.sha(__file__),
              elapsed_seconds=time.monotonic()-started,
              limits=dict(as_mib=400, one_cpu=True, external_seconds=20),
              cake_replay_performed=False)
for directory in (audit.WORK, audit.HERE / 'results'):
    (directory / f'sweep{n}.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
print(json.dumps(dict(status=report['status'], n=n,
                     certified_logs_checked=sum(c['parent_status'] == 'UNSAT_CERTIFIED' for c in cases),
                     unknowns=sum(c['parent_status'] == 'UNKNOWN' for c in cases),
                     elapsed_seconds=report['elapsed_seconds'], cake_replay_performed=False)))
