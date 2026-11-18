#!/usr/bin/env python3
"""Deliberate corruptions must fail semantic translation audit, not just hashes."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

MIB = 1024**2
resource.setrlimit(resource.RLIMIT_AS, (64*MIB, 120*MIB))
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
source, target = map(Path, sys.argv[1:])
target.mkdir(exist_ok=False)
meta = json.loads((source/'encoding.json').read_text())
mapping = json.loads((source/'row-clauses.json').read_text())
nontrivial = next(r for r in mapping if r['origin'] == 'base' and r['last_clause'] > r['first_clause'])
poolrow = next(r for r in mapping if r['origin'] == 'pool')
gate_line = None
with (source/'system.cnf').open() as f:
    for line_no, line in enumerate(f):
        if line_no and len(line.split()) == 3:
            gate_line = line_no
            break
assert gate_line is not None
cases = [('h0_sign', 1), ('row_support_index', 2), ('gate_sign', gate_line),
         ('demand_off_by_one', nontrivial['last_clause']),
         ('budget33_instead34', meta['clauses']),
         ('missing_pool_row', poolrow['first_clause'])]
summary = []


def hash_file(p):
    d = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(MIB), b''):
            d.update(block)
    return d.hexdigest()


def child_limits():
    resource.setrlimit(resource.RLIMIT_AS, (120*MIB, 120*MIB))


before = hash_file(source/'system.cnf')
for name, line_index in cases:
    out = target/name
    out.mkdir()
    (out/'encoding.json').write_bytes((source/'encoding.json').read_bytes())
    with (source/'system.cnf').open() as inp, (out/'system.cnf').open('w') as dst:
        for number, line in enumerate(inp):
            if number == line_index:
                vals = list(map(int, line.split()))
                old = vals[:]
                if name in ('h0_sign', 'gate_sign'):
                    vals[0] = -vals[0]
                elif name == 'row_support_index':
                    vals[0] = next(i for i in range(1, 155) if i not in vals)
                elif name == 'demand_off_by_one':
                    vals[0] -= 1
                elif name == 'budget33_instead34':
                    vals[0] += 1
                elif name == 'missing_pool_row':
                    vals = [1, -1, 0]
                assert vals != old
                line = ' '.join(map(str, vals))+'\n'
            dst.write(line)
    with (out/'audit.log').open('w') as log:
        r = subprocess.run([sys.executable, str(Path(__file__).with_name('audit_translation.py')), str(out)],
                           stdout=log, stderr=subprocess.STDOUT, timeout=40, preexec_fn=child_limits)
    log = (out/'audit.log').read_text()
    assert r.returncode != 0 and 'AssertionError' in log
    assert 'MemoryError' not in log and 'Traceback' in log
    summary.append({'corruption': name, 'changed_DIMACS_line_index': line_index,
                    'rejected': True, 'returncode': r.returncode,
                    'mutated_cnf_sha256': hash_file(out/'system.cnf')})
assert before == hash_file(source/'system.cnf')
result = {'label': 'COMPUTED adversarial encoding controls PASS',
          'source_cnf_sha256': before, 'original_unchanged': True,
          'note': 'Audit never compares stored CNF hash; rejection comes from semantic/structural checks',
          'cases': summary}
(target/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
