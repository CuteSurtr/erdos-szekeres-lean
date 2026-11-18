#!/usr/bin/env python3
"""Inspect the finite row statement and prior receipts, without proof replay."""
import os
import resource
resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})

import datetime
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
B = HERE.parent
WORK = Path('/home/jay/research/data/es308-20261114')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text())

mp = B / 'data/input-manifest.json'
source = WORK / 'inputs/source-2650.json.gz'
extra_path = WORK / 'inputs/s19/extra.json'
pool_path = WORK / 'inputs/pool812.json'
tree_path = B / 'audit/s19-summary.json'
cert_path = B / 'audit/pool_summary.json'
m = read(mp)
raw = gzip.decompress(source.read_bytes())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
base, extra, pool = json.loads(raw), read(extra_path), read(pool_path)
assert sha(source) == m['source_sha256']
assert sha(extra_path) == m['slices']['19']['extra_sha256']
assert sha(pool_path) == m['pool_sha256']
F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
Lo = [i for i, s in enumerate(base['states']) if s[0] <= 4]
assert len(base['states']) == 154 and len(F) == 84 and len(Lo) == 70
assert sorted(F + Lo) == list(range(154)) and set(F).isdisjoint(Lo)
assert base['states'][0] == [0, 0, 0, 0, 0] and 0 in Lo and 0 not in F
assert extra == [{'support': F, 'rhs': 19}, {'support': Lo, 'rhs': 15}] + pool
assert len(pool) == 812 and all(r['rhs'] == 1 for r in pool)
rows = base['constraints'] + extra
assert len(base['constraints']) == 2650 and len(rows) == 3464
for r in rows:
    assert type(r['rhs']) is int and 0 <= r['rhs'] <= len(r['support'])
    assert len(set(r['support'])) == len(r['support'])
    assert all(type(i) is int and 0 <= i < 154 for i in r['support'])

# Independently compare the simple positive-unit lower-row serialization.
rowfile = WORK / 'inputs/s19/rows.txt'
assert sha(rowfile) == m['slices']['19']['rows_sha256']
serialized = rowfile.read_text().splitlines()
assert serialized[0] == 'FASTBB-ROWS 1' and serialized[7] == 'rows 3464'
assert len(serialized[8:]) == len(rows)
for line, r in zip(serialized[8:], rows):
    demand, count, *support = map(int, line.split())
    assert demand == r['rhs'] and count == len(support) and support == r['support']

tree, cert = read(tree_path), read(cert_path)
assert tree['label'] == 'EXACT TREE' and tree['budget'] == 34 and tree['capacity_demands'] == [19, 15]
assert tree['contexts_total'] == tree['contexts_replayed'] == 3643
assert not tree['contexts_pending'] and not tree['deferred']
assert tree['nodes'] == 1658483 and tree['leaves'] == 829242 and tree['minimum_margin'] == 1
assert tree['global_pending'] == 1 and tree['sole_pending_state0_missing']
assert tree['input_sha256'][str(extra_path)] == sha(extra_path)
assert tree['input_sha256'][str(source)] == sha(source)
assert tree['input_sha256'][str(rowfile)] == sha(rowfile)
assert tree['pool_summary_sha256'] == sha(cert_path)
assert cert['status'] == 'CERTIFIED' and cert['pool_sha256'] == sha(pool_path)
assert cert['rows'] == cert['independently_reconstructed_cnfs'] == cert['accepted_retained_lrats'] == 812
assert cert['all_exact_stdout_acceptances']

preserved = {}
for line in (B / 'bridge/SHA256SUMS').read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    actual = sha(B / 'bridge' / name)
    assert actual == expected
    preserved[name] = actual
vm = {line.split(':')[0]: int(line.split()[1])
      for line in Path('/proc/self/status').read_text().splitlines()
      if line.split(':')[0] in {'VmPeak', 'VmHWM', 'VmRSS'}}
assert vm['VmPeak'] <= 150 * 1024 and vm['VmRSS'] <= 150 * 1024
paths = [mp, source, extra_path, pool_path, rowfile, tree_path, cert_path]
out = {
    'finished_kst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
    'scope': 'Source statement and inherited receipt check only; no certificate audit, tree replay, solver or Lean build.',
    'verdict': 'Padding hypotheses confirmed; written structural deduction PROVED from stated dependencies.',
    'states': 154, 'F': 84, 'Lo': 70, 'state0_in_Lo': True,
    'eligible_Lo_indices_excluding_state0': 69,
    'rows': 3464, 'base_rows': 2650, 'coupled_rows': 812,
    'all_rows': 'positive-unit support sums bounded below by nonnegative integer demands',
    'demand_histogram': dict(sorted(Counter(r['rhs'] for r in rows).items())),
    'capacity_demands': [19, 15],
    'inherited_tree': {k: tree[k] for k in ('label', 'budget', 'contexts_total', 'contexts_replayed', 'nodes', 'leaves', 'minimum_margin', 'global_pending', 'sole_pending_state0_missing')},
    'inherited_pool': {k: cert[k] for k in ('status', 'rows', 'independently_reconstructed_cnfs', 'accepted_retained_lrats', 'all_exact_stdout_acceptances')},
    'inputs_sha256': {str(p): sha(p) for p in paths},
    'preserved_bridge_sha256': preserved,
    'resources': {'AS_limit_bytes': 150 << 20, 'affinity': sorted(os.sched_getaffinity(0)), 'proc_status_kib': vm},
}
(HERE / 'data').mkdir(exist_ok=True)
(HERE / 'data/input-check.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'finished_kst': out['finished_kst'], 'row_checks': 'passed', 'original_bridge': 'unchanged, 4 hashes match', 'proc_status_kib': vm}))
