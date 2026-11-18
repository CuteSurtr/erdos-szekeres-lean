#!/usr/bin/env python3
"""Independent all-gap selector controls and source-to-certificate CNF binding."""
import audit_pool as audit
import itertools
import json
import math
import subprocess
import time

START = time.monotonic()
ROOT = audit.HERE.parent / 'lift'
SRC = ROOT / 'extension_cnf.cpp'
OLD = audit.RECORD / 'encoder/delta_cnf.cpp'
WORK = audit.SCRATCH / 'embedding'
WORK.mkdir(exist_ok=True)
source_hash, old_hash = audit.sha(SRC), audit.sha(OLD)
binary, old_binary = WORK / 'extension_cnf', WORK / 'old_cnf'

def run(command, timeout=5):
    p = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    audit.need(p.returncode == 0, 'command failed: ' + p.stderr)
    return p.stdout

for source, executable in ((SRC, binary), (OLD, old_binary)):
    run(['g++', '-std=c++17', '-O1', str(source), '-o', str(executable)], 8)

def signs(P):
    dets = [audit.determinant(*(P[i] for i in t)) for t in itertools.combinations(range(len(P)), 3)]
    audit.need(all(dets), 'collinear positive control')
    return ''.join('+' if d > 0 else '-' for d in dets)

def extend(P, positions, k):
    m = len(P)+k
    result = [None]*m
    for p, i in zip(P, positions):
        result[i] = p[:]
    endpoints = [(-1, P[0][0]-6000)] + [(i, result[i][0]) for i in positions] + [(m, P[-1][0]+6000)]
    for (a, x), (b, y) in zip(endpoints, endpoints[1:]):
        for i in range(a+1, b):
            xx = x + (y-x)*(i-a)//(b-a)
            yy = 1234567*(i+1)
            while any(audit.determinant(u, v, [xx, yy]) == 0
                      for u, v in itertools.combinations([p for p in result if p is not None], 2)):
                yy += 1
            result[i] = [xx, yy]
    audit.need(all(result[i][0] < result[i+1][0] for i in range(m-1)), 'extension x order')
    return result

def satisfied(c, values):
    return any(values[abs(x)] == (x > 0) for x in c)

def control(P, k, name, enumerate_bad):
    r, m = len(P), len(P)+k
    old_signs = signs(P)
    signfile = WORK / (name+'.signs')
    signfile.write_text(old_signs+'\n')
    cnf = WORK / (name+'.cnf')
    metadata = json.loads(run([str(binary), '--old-signs', str(signfile), '--old-size', str(r),
                               '--add', str(k), '--n', '7', '--mode', 'cup', '--embedding-only',
                               '--out', str(cnf)]))
    nv, clauses = audit.parse_cnf(cnf)
    triples = list(itertools.combinations(range(m), 3))
    indices = {t: i+1 for i, t in enumerate(triples)}
    selector = metadata['selector_ids']
    audit.need(selector == [[len(triples)+i*(k+1)+d+1 for d in range(k+1)] for i in range(r)],
               'selector allocation differs')
    structural_count = metadata['phases']['embedding_one_hot']['clauses']
    structural_count += metadata['phases'].get('embedding_order', {}).get('clauses', 0)
    structural = clauses[:structural_count]
    shift_tests = 0
    if enumerate_bad:
        for shift in itertools.product(range(k+1), repeat=r):
            values = [False]*(nv+1)
            for i, d in enumerate(shift):
                values[selector[i][d]] = True
            expected = all(shift[i] <= shift[i+1] for i in range(r-1))
            audit.need(all(satisfied(c, values) for c in structural) == expected,
                       'monotone selector acceptance mismatch')
            shift_tests += 1
    patterns, flipped = 0, 0
    for positions in itertools.combinations(range(m), r):
        Q = extend(P, positions, k)
        new_signs = signs(Q)
        values = [False] + [c == '+' for c in new_signs] + [False]*(r*(k+1))
        for i, p in enumerate(positions):
            values[selector[i][p-i]] = True
        audit.need(all(satisfied(c, values) for c in clauses), 'real canonical embedding rejected')
        for t in itertools.combinations(range(r), 3):
            v = indices[tuple(positions[i] for i in t)]
            values[v] = not values[v]
            audit.need(not all(satisfied(c, values) for c in clauses), 'old triple not enforced')
            values[v] = not values[v]
            flipped += 1
        patterns += 1
    audit.need(patterns == math.comb(m, r), 'missing insertion patterns')
    return dict(old_m=r, added=k, insertion_patterns=patterns,
                shift_vectors=shift_tests, flipped_old_triples_rejected=flipped,
                cnf_sha256=audit.sha(cnf), clauses=len(clauses))

small = [[0, 0], [6000, 3000], [12000, -2000], [18000, 0]]
cases = [control(small, k, f'small-add{k}', True) for k in range(6)]
fixture = json.loads(audit.FIXTURE.read_text())
cases.append(control(fixture['P'], 1, 'real15-all16gaps', False))

# Rebuild the exact full formula used by the parent's successful certificate.
old_signs = WORK / 'real15-all16gaps.signs'
full = WORK / 'full-cup-n7-add1.cnf'
meta = json.loads(run([str(binary), '--old-signs', str(old_signs), '--old-size', '15',
                       '--add', '1', '--n', '7', '--mode', 'cup', '--out', str(full)]))
base = WORK / 'standalone-universal-cup-n7m16.cnf'
base_meta = json.loads(run([str(old_binary), '--m', '16', '--n', '7', '--mode', 'cup',
                            '--pool', 'lattice', '--sym', 'none', '--out', str(base)]))
with base.open() as f, full.open() as g:
    f.readline(); g.readline()
    for i, line in enumerate(f):
        audit.need(g.readline() == line, 'inherited universal prefix differs')
    audit.need(i+1 == base_meta['clauses'], 'standalone clause count')
    tail = [tuple(map(int, line.split()))[:-1] for line in g]
_, embedding = audit.parse_cnf(WORK / 'real15-all16gaps.cnf')
offset = meta['universal_variables']-math.comb(16, 3)
shifted = [tuple((1 if x > 0 else -1)*(abs(x)+offset if abs(x)>math.comb(16, 3) else abs(x))
                 for x in c) for c in embedding]
audit.need(tail == shifted, 'full appended embedding family differs')

cert = audit.SCRATCH.parent / 'lift/cert-n7-add1-all-gaps'
certificate = json.loads((cert / 'result.json').read_text())
cert_cnf = audit.Path(certificate['cnf'])
audit.need(audit.sha(full) == audit.sha(cert_cnf) == certificate['hashes']['input.cnf'],
           'certificate input differs from independent full build')
audit.need(audit.sha(cert / 'proof.lrat') == certificate['hashes']['proof.lrat'], 'proof hash')
audit.need(audit.sha(cert / 'proof.lrat.zst') == certificate['hashes']['proof.lrat.zst'], 'compressed proof hash')
audit.need(audit.sha(cert / 'cake.log') == certificate['hashes']['cake.log'], 'checker log hash')
audit.need('s VERIFIED UNSAT' in (cert / 'cake.log').read_text().splitlines(), 'no exact cake acceptance')
audit.need(audit.sha(SRC) == source_hash and audit.sha(OLD) == old_hash, 'source changed')
for name in ('result.json', 'cake.log'):
    (audit.HERE / 'results' / ('lift-parent-'+name)).write_bytes((cert / name).read_bytes())
result = dict(label='COMPUTED', status='EMBEDDING_REVIEW_CONTROLS_PASS',
              source_sha256=source_hash, included_source_sha256=old_hash,
              checker_sha256=audit.sha(__file__), binary_sha256=audit.sha(binary),
              cases=cases, total_insertion_patterns=sum(c['insertion_patterns'] for c in cases),
              full_cnf_sha256=audit.sha(full), full_variables=meta['variables'],
              full_clauses=meta['clauses'], inherited_clauses=base_meta['clauses'],
              embedding_clauses=len(tail), parent_certificate_log_hashes_checked=True,
              independently_replayed_cake=False,
              elapsed_seconds=time.monotonic()-START,
              limits=dict(as_mib=400, one_cpu=True, external_seconds=20))
for root in (audit.SCRATCH, audit.HERE / 'results'):
    (root / 'embedding_audit.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))
