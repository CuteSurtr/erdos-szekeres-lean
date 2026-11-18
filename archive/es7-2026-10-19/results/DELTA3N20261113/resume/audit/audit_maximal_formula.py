#!/usr/bin/env python3
"""Canonical real-coordinate positive control for the maximal-set CNF."""
import audit_pool as audit
import itertools
import json
import subprocess
import time

started = time.monotonic()
src = audit.HERE.parent / 'pool/maximal_cnf.cpp'
source_hash = audit.sha(src)
included = audit.RECORD / 'encoder/delta_cnf.cpp'
included_hash = audit.sha(included)
binary = audit.SCRATCH / 'maximal_cnf_audit'
compile_command = ['g++', '-std=c++17', '-O1', str(src), '-o', str(binary)]
compiled = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)
(audit.SCRATCH / 'maximal_compile.log').write_text(compiled.stdout+compiled.stderr)
audit.need(compiled.returncode == 0, 'compile failed')
fixture = json.loads((audit.HERE / 'results/real_star_audit.json').read_text())
m, n, P = fixture['m'], fixture['n'], fixture['P']
R = set(fixture['red'])
cnf = audit.SCRATCH / 'maximal-real12.cnf'
encoded = subprocess.run([str(binary), str(m), str(n), str(cnf)],
                         capture_output=True, text=True, timeout=3)
audit.need(encoded.returncode == 0, 'encode failed')
metadata = json.loads(encoded.stdout)
caps = {audit.mask(s) for s in fixture['fourcaps']}
targets = {audit.mask(s) for s in fixture['targets']}
values = [None]
def add(value):
    values.append(bool(value))
for t in itertools.combinations(range(m), 3):
    add(audit.determinant(*(P[i] for i in t)) > 0)
for i in range(m):
    add(i in R)
for q in itertools.combinations(range(m), 4):
    add(audit.mask(q) in caps)
for p in range(m):
    for q in itertools.combinations([i for i in range(m) if i != p], 3):
        add(set(q) <= R and audit.mask((*q, p)) in caps)
for q in itertools.combinations(range(m), 4):
    lo, up = audit.chains(P, q)
    add(len(set(lo+up)) == 4)
for q in itertools.combinations(range(m), n-1):
    add(set(q).isdisjoint(R) and audit.mask(q) in targets)
nv, clauses = audit.parse_cnf(cnf)
audit.need(nv == len(values)-1 == metadata['variables'], 'variable allocation mismatch')
for i, c in enumerate(clauses):
    audit.need(any(values[abs(v)] == (v > 0) for v in c), f'canonical assignment falsifies clause {i}')
audit.need(audit.sha(src) == source_hash and audit.sha(included) == included_hash, 'source changed')
result = dict(label='COMPUTED', status='CANONICAL_REAL_POSITIVE_CONTROL_PASS',
              source_sha256=source_hash, included_source_sha256=included_hash,
              checker_sha256=audit.sha(__file__), compile_command=compile_command,
              binary_sha256=audit.sha(binary), cnf_sha256=audit.sha(cnf),
              variables=nv, clauses_checked=len(clauses), m=m, n=n,
              orientation_fixed_by_canonical_assignment=True,
              actual_solver_used=False, elapsed_seconds=time.monotonic()-started)
for root in (audit.SCRATCH, audit.HERE / 'results'):
    (root / 'maximal_formula_audit.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, sort_keys=True))
