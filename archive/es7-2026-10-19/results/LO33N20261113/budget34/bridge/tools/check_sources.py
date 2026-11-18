#!/usr/bin/env python3
"""Small exact source identities and inherited receipts; no proof replay or solver."""
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
REPO = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
RESULTS = REPO / 'cloud/es7-2026-10-19/results'
WORK = Path('/home/jay/research/data/es308-20261114')

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

source = REPO / 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
raw = gzip.decompress(source.read_bytes())
raw_sha = hashlib.sha256(raw).hexdigest()
assert raw_sha == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
base = json.loads(raw)
states, rows = base['states'], base['constraints']
F = {i for i, s in enumerate(states) if s[0] >= 5}
Lo = {i for i, s in enumerate(states) if s[0] <= 4}
assert len(states) == 154 and len(rows) == 2650
assert len(F) == 84 and len(Lo) == 70 and F.isdisjoint(Lo) and F | Lo == set(range(154))
assert states[0] == [0, 0, 0, 0, 0] and 0 in Lo
ids = [973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315]
blocks = [set(rows[j]['support']) for j in ids]
assert all(len(b) == 28 and b <= F and rows[j]['rhs'] == 6 for j, b in zip(ids, blocks))
assert all(sum(i in b for b in blocks) == 3 for i in F)
assert blocks[0] == {i for i, s in enumerate(states) if s[0] == 6}

manifest_path = HERE.parent / 'data/input-manifest.json'
manifest = read(manifest_path)
pool_path = WORK / 'inputs/pool812.json'
pool = read(pool_path)
assert len(pool) == 812 and sha(pool_path) == manifest['pool_sha256']
assert sha(source) == manifest['source_sha256']
complement_rows_absent = {}
for t in (19, 20):
    extra_path = WORK / f'inputs/s{t}/extra.json'
    assert sha(extra_path) == manifest['slices'][str(t)]['extra_sha256']
    extra = read(extra_path)
    assert extra == [{'support': sorted(F), 'rhs': t}, {'support': sorted(Lo), 'rhs': 34-t}] + pool
    full = rows + extra
    assert len(full) == 3464
    assert all(not any(set(r['support']) == F-b and r['rhs'] == 48-2*t for r in full) for b in blocks)
    complement_rows_absent[str(t)] = {'count': 9, 'support_size': 56, 'demand': 48-2*t}

s19_path = HERE.parent / 'audit/s19-summary.json'
pool_summary_path = HERE.parent / 'audit/pool_summary.json'
s19, ps = read(s19_path), read(pool_summary_path)
assert s19['label'] == 'EXACT TREE' and s19['budget'] == 34 and s19['capacity_demands'] == [19, 15]
assert s19['contexts_total'] == s19['contexts_replayed'] == 3643 and not s19['contexts_pending']
assert s19['nodes'] == 1658483 and s19['leaves'] == 829242 and s19['minimum_margin'] == 1
assert s19['global_pending'] == 1 and s19['sole_pending_state0_missing'] and not s19['deferred']
assert sha(pool_summary_path) == s19['pool_summary_sha256']
assert ps['status'] == 'CERTIFIED' and ps['rows'] == ps['independently_reconstructed_cnfs'] == ps['accepted_retained_lrats'] == 812
assert ps['all_exact_stdout_acceptances'] and ps['pool_sha256'] == manifest['pool_sha256']

witness_path = WORK / 'runs/s20/bb/WITNESS.refuted-1.json'
witness_validation_path = WORK / 'sat/parent-witness-1/witness.json'
witness_source_path = WORK / 'sat/parent-witness-1/source.json'
w = read(witness_path)
wv, ws = read(witness_validation_path), read(witness_source_path)
assert sha(witness_path) == ws['sha256'] and w['context'] == ws['finder_context'] == 94
holes = set(w['holes'])
assert len(holes) == len(w['holes']) == 34 and 0 not in holes
assert len(holes & F) == 20 and len(holes & Lo) == 14
block_holes = [len(b & holes) for b in blocks]
assert block_holes == [6, 6, 7, 6, 6, 6, 6, 6, 11]
assert wv['valid'] and not wv['violated_rows'] and wv['hole_indices'] == w['holes']
assert wv['holes'] == 34 and wv['F_holes'] == 20 and wv['Lo_holes'] == 14 and wv['h0'] == 0
assert wv['base_sha256'] == manifest['source_sha256'] and wv['pool_sha256'] == manifest['pool_sha256']

assembly_path = REPO / 'experiments/omission-compact-checker-2026-11-05/logs/es310/final310-compact.json'
assembly_source = REPO / 'experiments/omission-compact-checker-2026-11-05/assembly/Final310Compact.lean'
assembly = read(assembly_path)
assert assembly['verified'] and assembly['mode'] == 'real' and not assembly['test_only'] and not assembly['problems']
assert assembly['axioms'] == assembly['audit_axioms'] == 'propext, Classical.choice, Quot.sound'
assert sha(assembly_source) == assembly['final_source_sha256'] == assembly['final_source_pin']

paths = [
    source, manifest_path, pool_path, s19_path, pool_summary_path, witness_path,
    witness_validation_path, witness_source_path,
    WORK / 'inputs/s19/extra.json', WORK / 'inputs/s20/extra.json',
    assembly_path, assembly_source,
    REPO / 'AGENTS.md', REPO / '.claude/skills/es-research/SKILL.md',
    REPO / 'ErdosSzekeres/Omission/PopulationBounds.lean',
    REPO / 'ErdosSzekeres/Omission/ResidualStates.lean',
    REPO / 'ErdosSzekeres/Omission/ResidualRanks.lean',
    REPO / 'experiments/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Rows.lean',
    REPO / 'experiments/omission-residual32-context-certificates-2026-10-10/ZeroState.lean',
    RESULTS / 'STATUS20261114_0840/README.md',
    RESULTS / 'ES309N20261113/README.md',
    RESULTS / 'THEORY310N20261113/README.md',
    RESULTS / 'LO33N20261113/VERIFY_LO.md',
    RESULTS / 'ETV5N20261113/README.md',
    RESULTS / 'ETV5N20261113/VERIFY_N5.md',
    RESULTS / 'VERIFY309N20261113/README.md',
    RESULTS / 'VERIFY309N20261113/followup56/README.md',
    RESULTS / 'VERIFY309N20261113/followup56/VERIFY_N66_56.md',
]
vm_kib = {line.split(':', 1)[0]: int(line.split()[1])
          for line in Path('/proc/self/status').read_text().splitlines()
          if line.split(':', 1)[0] in {'VmPeak', 'VmSize', 'VmHWM', 'VmRSS'}}
assert vm_kib['VmPeak'] <= 150 * 1024 and vm_kib['VmRSS'] <= 150 * 1024
out = {
    'scope': 'Exact small source identities and inherited receipt inspection only; no solver, Lean build, CNF/proof audit or tree replay.',
    'finished_kst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
    'decompressed_source_sha256': raw_sha,
    'catalog': {'states': len(states), 'F': len(F), 'Lo': len(Lo), 'first_height_counts': dict(sorted(Counter(s[0] for s in states).items()))},
    'nine_blocks': {'row_indices': ids, 'each_support_size': 28, 'each_demand': 6, 'each_F_state_multiplicity': 3, 'row973_exact_f1_6': True},
    'explicit_complement_rows_absent': complement_rows_absent,
    'inherited_s19_receipt': {k: s19[k] for k in ('label', 'budget', 'capacity_demands', 'contexts_total', 'contexts_replayed', 'nodes', 'leaves', 'minimum_margin', 'global_pending', 'sole_pending_state0_missing', 'coupled_rows_used', 'finished_local')},
    'inherited_pool_receipt': ps,
    's20_witness_small_counts': {'total': 34, 'F': 20, 'Lo': 14, 'nine_block_holes': block_holes, 'full_row_validation_here': False, 'full_row_validation_source': str(witness_validation_path), 'snapshot': 'data/s20-v1-witness.json'},
    'inherited_witness_validation': {k: wv[k] for k in ('valid', 'holes', 'F_holes', 'Lo_holes', 'h0', 'violated_rows', 'label', 'cnf_clauses_checked', 'cnf_sha256', 'base_sha256', 'pool_sha256', 'scope')},
    'witness_path_note': 'Live WITNESS.json changed during this sidecar. V1 is pinned by the archived context-94 file and the independent source receipt; the local snapshot preserves its exact bytes.',
    'inherited_assembly': {k: assembly[k] for k in ('verified', 'mode', 'statement', 'axioms', 'audit_axioms', 'final_source_sha256')},
    'files_sha256': {str(p): sha(p) for p in paths},
    'resources': {'AS_limit_bytes': 150 << 20, 'CPU_time_limit_seconds': 10, 'affinity': sorted(os.sched_getaffinity(0)), 'proc_status_kib': vm_kib, 'reported_ru_maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
}
(HERE / 'data').mkdir(exist_ok=True)
(HERE / 'data/s20-v1-witness.json').write_bytes(witness_path.read_bytes())
(HERE / 'data/source-audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'finished_kst': out['finished_kst'], 'source_identities': 'passed', 'inherited_receipts': 'consistent', 'proc_status_kib': vm_kib, 'files_hashed': len(paths)}))
