#!/usr/bin/env python3
"""Independent, short controls for batch_pool.py; writes only assigned audit paths.

Run each mode with an external 20-second SIGKILL timeout. The reference uses
integer monotone hulls and direct subset tests, never the pool zeta transform
or any previous checker. Importing Geometry is solely the implementation under
test. Solver outcomes here are COMPUTED, never certificates.
"""
import os
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
                  PYTHONDONTWRITEBYTECODE='1')
import resource
resource.setrlimit(resource.RLIMIT_AS, (400 << 20, 400 << 20))
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RECORD = HERE.parent.parent
DRIVER = HERE.parent / 'pool/batch_pool.py'
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/resume/audit')
DATA = SCRATCH.parent.parent
FIXTURE = RECORD / 'coordinator/data/cup15/realized.json'
SOURCE = DATA / 'encoder/resume-pool-control-n6m8/result.json'
START = time.monotonic()


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_driver():
    spec = importlib.util.spec_from_file_location('pool_under_test', DRIVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def determinant(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def chains(points, indices):
    # Andrew monotone hull; every arithmetic operation is a Python integer.
    def half(seq):
        ans = []
        for v in seq:
            while len(ans) > 1 and determinant(points[ans[-2]], points[ans[-1]], points[v]) <= 0:
                ans.pop()
            ans.append(v)
        return ans
    return half(indices), half(reversed(indices))


def mask(indices):
    return sum(1 << i for i in indices)


def reference(points, n):
    m = len(points)
    need(all(type(x) is int for p in points for x in p), 'noninteger coordinate')
    need(all(points[i][0] < points[i+1][0] for i in range(m-1)), 'x order')
    determinants = [determinant(*(points[i] for i in t))
                    for t in itertools.combinations(range(m), 3)]
    need(all(determinants), 'collinear triple')
    signs = ''.join('+' if d > 0 else '-' for d in determinants)
    caps = []
    cap5 = []
    convex = {k: [] for k in (n-1, n)}
    for k in sorted({4, 5, n-1, n}):
        for s in itertools.combinations(range(m), k):
            lo, up = chains(points, s)
            if len(lo) == 2 and len(up) == k:
                if k == 4:
                    caps.append(mask(s))
                if k == 5:
                    cap5.append(mask(s))
            if k in convex and len(set(lo + up)) == k:
                convex[k].append(mask(s))
    targets = convex[n-1]
    # No subset DP, no four-sign convexity shortcut, no auxiliary variables.
    working = [d for d in range(1 << m)
               if not any((d & c) == c for c in caps)
               and not any((d & t) == 0 for t in targets)]
    return dict(P=points, m=m, n=n, signs=signs, fourcaps=caps, fivecaps=cap5,
                targets=targets, ngons=convex[n], working_masks=working,
                minimum_absolute_determinant=min(map(abs, determinants)))


def compare(module, name, ref):
    need(not ref['fivecaps'] and not ref['ngons'], 'invalid positive control')
    g = module.Geometry(ref['m'], ref['n'])
    found, stats = g.analyze(ref['signs'])
    need(list(map(int, found)) == ref['working_masks'], name + ': Delta mask mismatch')
    need(stats == dict(fourcaps=len(ref['fourcaps']), targets=len(ref['targets']),
                       working_deltas=len(ref['working_masks'])), name + ': count mismatch')
    # Check both families' containment at every mask independently of final AND.
    for family in ('fourcaps', 'targets'):
        a = g.upward(module.np.array(ref[family], dtype=module.np.int32))
        full = (1 << ref['m'])-1
        for d in range(full+1):
            need(int(a[d]) == int(any(d & s == s for s in ref[family])),
                 name + ': containment mismatch')
            need(a[::-1][d] == a[full ^ d], name + ': complement mismatch')
    return dict(name=name, status='PASS', **ref, stats=stats)


def geometry():
    module = load_driver()
    fixture = json.loads(FIXTURE.read_text())
    results = []
    for n in (6, 7, 8):
        ref = reference(fixture['P'], n)
        need(ref['signs'] == fixture['signs'], 'real15 recorded signs mismatch')
        results.append(compare(module, 'real15-n' + str(n), ref))
    # Deterministic small integer fixtures, selected only for the geometric
    # premises. Counts and working masks are never used to select a fixture.
    rng = random.Random(20261114)
    for n in (5, 6, 7, 8):
        accepted = 0
        for attempt in range(1000):
            points = [[i, rng.randrange(-100, 101)] for i in range(n+1)]
            try:
                ref = reference(points, n)
            except RuntimeError as exc:
                if str(exc) == 'collinear triple':
                    continue
                raise
            if ref['fivecaps'] or ref['ngons']:
                continue
            results.append(compare(module, f'integer-n{n}-{accepted}', ref))
            accepted += 1
            if accepted == 3:
                break
        need(accepted == 3, 'too few valid small fixtures')
    reversal_tests = 0
    for m in range(4, 17):
        for d in range(1 << m):
            expected = sum(1 << (m-1-i) for i in range(m) if d & (1 << i))
            need(int(f'{d:0{m}b}'[::-1], 2) == expected, 'mask reversal mismatch')
            reversal_tests += 1
    return dict(status='PASS', fixture_sha256=sha(FIXTURE), cases=results,
                compared_delta_masks=sum(1 << r['m'] for r in results),
                reversal_masks_compared=reversal_tests)


def edges():
    module = load_driver()
    observed = []
    for m, n in ((4, 5), (4, 8), (5, 6), (5, 8), (6, 7), (7, 8)):
        ref = reference([[i, i*i] for i in range(m)], n)
        need(not ref['fivecaps'] and not ref['ngons'], 'invalid edge fixture')
        try:
            found, stats = module.Geometry(m, n).analyze(ref['signs'])
        except Exception as exc:
            observed.append(dict(m=m, n=n, status='BUG_REPRODUCED',
                                 exception=type(exc).__name__, message=str(exc),
                                 reference_working=len(ref['working_masks'])))
        else:
            need(list(map(int, found)) == ref['working_masks'], 'edge mismatch')
            observed.append(dict(m=m, n=n, status='PASS', stats=stats))
    return dict(status='COMPLETED', cases=observed)


def parse_cnf(path):
    with path.open() as f:
        head = f.readline().split()
        need(head[:2] == ['p', 'cnf'], 'bad header')
        clauses = []
        for line in f:
            values = tuple(map(int, line.split()))
            need(values and values[-1] == 0 and 0 not in values[:-1], 'bad clause')
            need(all(abs(v) <= int(head[2]) for v in values[:-1]), 'bad literal')
            clauses.append(values[:-1])
        need(len(clauses) == int(head[3]), 'clause count mismatch')
    return int(head[2]), clauses


def expected_tail(m, n):
    # Reconstruct only the audited old encoder's variable allocation, not
    # geometry. This verifies the numerical mask order independently of
    # batch_pool's last-2**m assumption, including compile-time false nodes.
    nv = math.comb(m, 3)
    cap = [0] * (1 << m)
    for s in range(1 << m):
        if s.bit_count() >= 4:
            nv += 1
            cap[s] = nv
    nv += math.comb(m, 4)  # convex-four indicators
    seed = [0] * (1 << m)
    for t in itertools.combinations(range(m), n-1):
        nv += 1
        seed[mask(t)] = nv
    target = [0] * (1 << m)
    for s in range(1 << m):
        if s.bit_count() < n-1:
            continue
        rhs = ([seed[s]] if seed[s] else [])
        vertices = [i for i in range(m) if s & (1 << i)]
        rhs += [target[s ^ (1 << i)] for i in vertices[:n]
                if target[s ^ (1 << i)]]
        if len(rhs) == 1:
            target[s] = rhs[0]
        elif rhs:
            nv += 1
            target[s] = nv
    full = (1 << m)-1
    return nv, [tuple(v for v in (cap[d], target[full ^ d]) if v)
                for d in range(1 << m)]


def verify_export(out, source):
    info = json.loads(source.read_text())
    p = info['parameters']
    m, n = p['m'], p['n']
    source_cnf = source.parent / 'case.cnf'
    nv, original = parse_cnf(source_cnf)
    base_count = len(original)-(1 << m)
    expected_nv, tail = expected_tail(m, n)
    need(nv == expected_nv and original[base_count:] == tail, 'source tail mismatch')
    bnv, base = parse_cnf(out / 'base.cnf')
    fnv, final = parse_cnf(out / 'final.cnf')
    pool = json.loads((out / 'pool.json').read_text())['masks']
    result = json.loads((out / 'result.json').read_text())
    need(bnv == fnv == nv, 'variable count mismatch')
    need(base == original[:base_count], 'base is not exact prefix')
    need(len(pool) == len(set(pool)), 'duplicate pool mask')
    need(all(type(d) is int and 0 <= d < (1 << m) for d in pool), 'invalid mask')
    need(final == base + [original[base_count+d] for d in pool], 'final clauses differ')
    need(result['final_cnf_sha256'] == sha(out / 'final.cnf'), 'final hash mismatch')
    need(info['hashes']['case.cnf'] == sha(source_cnf), 'source hash mismatch')
    need(result['source_cnf_sha256'] == sha(source_cnf), 'provenance mismatch')
    need(result['source_result_sha256'] == sha(source), 'source record mismatch')
    need(result['pool_size'] == len(pool) and result['base_clauses'] == base_count,
         'export metadata mismatch')
    return dict(status='PASS', directory=str(out), finder_status=result['status'],
                variables=nv, base_clauses=base_count, selected_masks=pool,
                final_clauses=len(final), full_subset_clauses_checked=1 << m,
                source_cnf_sha256=sha(source_cnf), final_cnf_sha256=sha(out / 'final.cnf'),
                empty_subset_clauses=sum(not c for c in tail))


def run_driver(name, batch, seconds):
    out = SCRATCH / name
    command = [sys.executable, '-B', str(DRIVER), '--source', str(SOURCE),
               '--out', str(out), '--seconds', str(seconds), '--batch', str(batch),
               '--seed', '1', '--as-mib', '400']
    before = time.monotonic()
    p = subprocess.run(command, capture_output=True, text=True, timeout=10)
    (SCRATCH / (name + '.stdout')).write_text(p.stdout)
    (SCRATCH / (name + '.stderr')).write_text(p.stderr)
    need(p.returncode == 0, 'driver failed: ' + p.stderr)
    checked = verify_export(out, SOURCE)
    checked.update(command=command, measured_seconds=time.monotonic()-before)
    return checked


def exports():
    own = run_driver('tiny-n6m8', 16, 4)
    zero = run_driver('zero-batch-n6m8', 0, 1)
    zero_result = json.loads((SCRATCH / 'zero-batch-n6m8/result.json').read_text())
    zero_events = [json.loads(s) for s in (SCRATCH / 'zero-batch-n6m8/events.jsonl').read_text().splitlines()]
    need(zero_result['iterations'] > 1 and not zero['selected_masks'], 'zero-batch changed behavior')
    need(all(e['added'] == 0 and e['working_deltas'] > 0 for e in zero_events), 'zero-batch events')
    zero.update(status='BUG_REPRODUCED', iterations=zero_result['iterations'],
                distinct_models=len({e['signs_sha256'] for e in zero_events}))
    parent = verify_export(SCRATCH.parent / 'pool/control-n6m8', SOURCE)
    return dict(status='COMPLETED', own_tiny=own, parent_tiny=parent, zero_batch=zero)


def input_snapshot(n):
    source = DATA / f'encoder/direct-weak-n{n}-m16/result.json'
    info = json.loads(source.read_text())
    source_cnf = source.parent / 'case.cnf'
    h = sha(source_cnf)
    need(h == info['hashes']['case.cnf'], 'source hash mismatch')
    need(info['parameters']['pool'] == 'lattice', 'unexpected pool kind')
    nv, tail = expected_tail(16, n)
    need(nv == info['encoding']['variables'], 'source variable count mismatch')
    base_count = info['encoding']['clauses'] - (1 << 16)
    out = SCRATCH.parent / f'pool/n{n}m16-b128'
    # Capture the two independently written status files with their own hashes;
    # do not assume they form an atomic, final snapshot.
    snapshots = {}
    for name in ('pool.json', 'result.json'):
        raw = (out / name).read_bytes()
        (SCRATCH / f'n{n}m16-{name}').write_bytes(raw)
        snapshots[name] = hashlib.sha256(raw).hexdigest()
    pool = json.loads((SCRATCH / f'n{n}m16-pool.json').read_text())['masks']
    need(len(pool) == len(set(pool)) and all(type(d) is int and 0 <= d < (1 << 16) for d in pool), 'pool mask error')
    with source_cnf.open() as src, (out / 'base.cnf').open() as base:
        header = src.readline().split()
        base_header = base.readline().split()
        need(header == ['p', 'cnf', str(nv), str(base_count+(1 << 16))], 'source header')
        need(base_header == ['p', 'cnf', str(nv), str(base_count)], 'base header')
        for i in range(base_count):
            a, b = src.readline(), base.readline()
            need(a and a == b, 'base prefix mismatch at ' + str(i))
        need(base.read(1) == '', 'base has extra content')
        for d, clause in enumerate(tail):
            actual = tuple(map(int, src.readline().split()))
            need(actual == clause + (0,), 'tail differs at mask ' + str(d))
        need(src.read(1) == '', 'source has extra content')
    need(sha(source_cnf) == h, 'source changed during audit')
    return dict(status='PASS_INTERIM', n=n, m=16, source=str(source),
                source_cnf_sha256=h, base_clauses=base_count,
                subset_clauses_checked=len(tail), selected_masks_at_read=len(pool),
                snapshot_hashes=snapshots, final_cnf_present=(out / 'final.cnf').exists(),
                final_cnf_checked=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['geometry', 'edges', 'exports', 'input7', 'input8'])
    args = parser.parse_args()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    driver_hash = sha(DRIVER)
    result = {'geometry': geometry, 'edges': edges, 'exports': exports,
              'input7': lambda: input_snapshot(7), 'input8': lambda: input_snapshot(8)}[args.mode]()
    need(sha(DRIVER) == driver_hash, 'driver changed during control')
    result.update(label='COMPUTED', mode=args.mode, driver_sha256=driver_hash,
                  checker_sha256=sha(__file__), elapsed_seconds=time.monotonic()-START,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits=dict(as_mib=400, cpu_seconds=18, external_seconds=20,
                              affinity=list(os.sched_getaffinity(0))),
                  thread_count=len(list(Path('/proc/self/task').iterdir())))
    (SCRATCH / (args.mode + '.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('cases', 'own_tiny', 'parent_tiny', 'zero_batch')}, sort_keys=True))


if __name__ == '__main__':
    main()
