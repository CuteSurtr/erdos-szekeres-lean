#!/usr/bin/env python3
"""Independent canonical and existential-projection controls for rooted_fast."""
import check_rooted as audit  # This audit's own integer oracle and resource caps.
import argparse
import collections
import hashlib
import itertools
import json
import resource
import subprocess
import time

SRC = audit.SELECTION / 'rooted_fast.cpp'
INCLUDED = audit.RESUME / 'compact/compact_cnf.cpp'
WORK = audit.WORK / 'fast'
BINARY = WORK / 'rooted_fast'
START = time.monotonic()


def execute(command, timeout=5):
    p = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    audit.require(p.returncode == 0, 'command failed: ' + p.stderr)
    return p.stdout


def build():
    command = ['g++', '-std=c++17', '-O1', '-Wall', '-Wextra', str(SRC), '-o', str(BINARY)]
    p = subprocess.run(command, capture_output=True, text=True, timeout=15)
    (WORK / 'compile.stdout').write_text(p.stdout)
    (WORK / 'compile.stderr').write_text(p.stderr)
    audit.require(p.returncode == 0, 'compile failed: ' + p.stderr)
    return dict(status='PASS', command=command, binary_sha256=audit.sha(BINARY))


def prefix_hash(path, end_phase):
    h = hashlib.sha256()
    with path.open('rb') as f:
        f.readline()
        for line in f:
            if line == f'c phase {end_phase}\n'.encode():
                return h.hexdigest()
            h.update(line)
    raise RuntimeError('missing end phase')


def control(points, n, name, project=False):
    ref = audit.reference(points, n)
    m = ref['m']
    audit.require(not ref['fivecaps'] and not ref['ngons'], 'invalid control premises')
    root, old = 1 << (m-1), (1 << (m-1))-1
    amax, bmax = m-n+1, m-3
    cnf = WORK / (name+'.cnf')
    command = [str(BINARY), str(m), str(n), str(cnf)]
    meta = json.loads(execute(command))
    mapping = audit.Path(str(cnf)+'.map')
    flags, values, orient_units = {}, {}, []
    kinds = collections.defaultdict(set)
    for line in mapping.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        sid, kind, subset = line.split()
        v, s = int(sid), int(subset)
        audit.require(v not in values and (kind, s) not in flags, 'duplicate map entry')
        flags[kind, s] = v
        kinds[kind].add(s)
        vertices = [i for i in range(m) if s & (1 << i)]
        if kind == 'orientation':
            audit.require(len(vertices) == 3, 'orientation size')
            truth = audit.det(ref['P'], *vertices) > 0
            orient_units.append(v if truth else -v)
        elif kind == 'convex':
            truth = len(audit.hull(ref['P'], vertices)) == len(vertices)
        elif kind == 'root_bad_contains':
            truth = any(c & (s | root) == c for c in ref['caps'])
        elif kind == 'old_fourcap':
            truth = s in ref['caps']
        elif kind == 'old_target_contains':
            truth = any(t & s == t for t in ref['targets'])
        else:
            raise RuntimeError('unknown kind ' + kind)
        values[v] = truth
    audit.require(set(values) == set(range(1, meta['variables']+1)), 'map coverage')
    expected = {
        'orientation': {audit.mask(s) for s in itertools.combinations(range(m), 3)},
        'convex': {audit.mask(s) for k in range(4, n) for s in itertools.combinations(range(m), k)},
        'root_bad_contains': {audit.mask(s) for k in range(3, amax+1) for s in itertools.combinations(range(m-1), k)},
        'old_fourcap': {audit.mask(s) for s in itertools.combinations(range(m-1), 4)} if amax >= 4 else set(),
        'old_target_contains': {audit.mask(s) for k in range(n, bmax+1) for s in itertools.combinations(range(m-1), k)},
    }
    for kind, domain in expected.items():
        audit.require(kinds[kind] == domain, 'map domain differs for ' + kind)
    pool_masks = sorted(audit.mask(s) for k in range(2, amax+1)
                        for s in itertools.combinations(range(m-1), k))
    working = set(ref['rooted_working'])
    false_masks, phase_counts = [], collections.Counter()
    base, queries = [], []
    index, phase = 0, ''
    with cnf.open() as f:
        header = f.readline().split()
        audit.require(header == ['p', 'cnf', str(meta['variables']), str(meta['clauses'])], 'DIMACS header')
        for line in f:
            if line.startswith('c phase '):
                phase = line.split()[2]
                continue
            if line.startswith('c') or not line.strip():
                continue
            clause = audit.parse_clause(line)
            audit.require(all(abs(v) in values for v in clause), 'unmapped clause variable')
            truth = any(values[abs(v)] == (v > 0) for v in clause)
            phase_counts[phase] += 1
            if phase == 'forall_rooted_delta':
                s = pool_masks[index]
                index += 1
                a = flags.get(('root_bad_contains', s), 0)
                complement = old ^ s
                b = flags.get(('convex', complement), 0) if complement.bit_count() == n-1 else flags.get(('old_target_contains', complement), 0)
                audit.require(clause == tuple(v for v in (a, b) if v), 'pool literal/mask map')
                correct = (s | root) not in working
                audit.require(truth == correct, 'canonical pool semantics')
                if not truth:
                    false_masks.append(s | root)
                if project:
                    queries.append((s | root, clause, correct))
            else:
                audit.require(truth, 'canonical real assignment violates ' + phase)
                if project:
                    base.append(list(clause))
    audit.require(index == len(pool_masks) and sum(phase_counts.values()) == meta['clauses'], 'clause coverage')
    audit.require(false_masks == sorted(d for d in working if 3 <= d.bit_count() <= amax+1), 'rooted false masks')
    projections = 0
    if project:
        from pysat.solvers import Cadical195
        with Cadical195(bootstrap_with=base+[[v] for v in orient_units]) as solver:
            for i, (d, clause, correct) in enumerate(queries):
                guard = meta['variables']+i+1
                solver.add_clause([-guard]+list(clause))
                solver.conf_budget(1500)
                answer = solver.solve_limited(assumptions=[guard])
                audit.require(answer is not None and answer == correct,
                               'auxiliary existential query differs at ' + str(d))
                projections += 1
    moved = []
    for d in working:
        e = d
        if d.bit_count() < 3:
            for i in range(m-1):
                if e.bit_count() == 3:
                    break
                e |= 1 << i
        elif d.bit_count() > amax+1:
            e = root | audit.mask([i for i in range(m-1) if d & (1 << i)][:amax])
        audit.require(e in working and e & root and 3 <= e.bit_count() <= amax+1, 'rooted range repair')
        if d != e:
            moved.append([d, e])
    return dict(status='PASS', name=name, m=m, n=n, root=m-1,
                P=ref['P'], variables=meta['variables'], clauses=meta['clauses'],
                literals=meta['literals'], clauses_by_phase=dict(phase_counts),
                fourcaps=len(ref['caps']), targets=len(ref['targets']),
                old_targets=sum(not (t & root) for t in ref['targets']),
                root_blocker_triples=sum(bool(c & root) for c in ref['caps']),
                old_fourcaps=sum(not (c & root) for c in ref['caps']),
                rooted_working=len(working), rooted_pool_clauses=len(pool_masks),
                false_pool_clauses=len(false_masks), false_rooted_masks=false_masks,
                omitted_working_repairs=moved, existential_projection_queries=projections,
                cnf_sha256=audit.sha(cnf), map_sha256=audit.sha(mapping))


def real(n):
    fixture = audit.RESUME / 'compact' / ('real_n7m16.json' if n == 7 else 'real_n8m16_targeted.json')
    P = json.loads(fixture.read_text())['P']
    name = f'n{n}m16'
    result = control(P, n, name)
    original = json.loads((audit.HERE / f'results/formula{n}.json').read_text())
    audit.require(result['false_rooted_masks'] == original['false_rooted_masks'], 'fast/filter projection differs')
    fast_prefix = prefix_hash(WORK / (name+'.cnf'), 'root_blocker3')
    audit.require(fast_prefix == prefix_hash(audit.OLD_WORK / f'n{n}m16-final.cnf', 'fourcap'), 'geometric base changed')
    result.update(coordinate_sha256=audit.sha(fixture), same_geometric_prefix=True,
                  geometry_prefix_sha256=fast_prefix, same_false_masks_as_filtered_formula=True)
    return result


def tiny():
    source15 = json.loads((audit.RECORD / 'coordinator/data/cup15/realized.json').read_text())['P']
    source7 = json.loads((audit.RESUME / 'compact/real_n7m16.json').read_text())['P']
    source8 = json.loads((audit.RESUME / 'compact/real_n8m16_targeted.json').read_text())['P']
    ref8 = audit.reference(source8, 8)
    target = next(t for t in ref8['targets'] if not t & (1 << 15))
    chosen = {15} | {i for i in range(16) if target & (1 << i)}
    for i in range(16):
        if len(chosen) == 12:
            break
        chosen.add(i)
    P8 = [source8[i] for i in sorted(chosen)]
    fixtures = [('n6-m10', source15[:10], 6), ('n7-m12', source7[:12], 7),
                ('n8-m12-old-target', P8, 8), ('n7-m8-boundary', source7[:8], 7),
                ('n8-m9-boundary', source8[:9], 8)]
    cases = [control(P, n, name, project=True) for name, P, n in fixtures]
    audit.require(cases[2]['old_targets'] > 0, 'n8 control missed old targets')
    audit.require(any(c['root_blocker_triples'] and c['old_fourcaps'] for c in cases), 'missing blocker types')
    return dict(status='PASS', cases=cases,
                total_projection_queries=sum(c['existential_projection_queries'] for c in cases))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['build', 'real7', 'real8', 'tiny'])
    args = parser.parse_args()
    WORK.mkdir(exist_ok=True)
    initial = {str(p): audit.sha(p) for p in (SRC, INCLUDED)}
    if args.mode != 'build':
        built = json.loads((WORK / 'build.json').read_text())
        audit.require(built['source_sha256'] == initial[str(SRC)] and
                      built['included_sha256'] == initial[str(INCLUDED)] and
                      built['binary_sha256'] == audit.sha(BINARY), 'build provenance')
    result = {'build': build, 'real7': lambda: real(7), 'real8': lambda: real(8), 'tiny': tiny}[args.mode]()
    audit.require(initial == {p: audit.sha(p) for p in initial}, 'source changed during control')
    result.update(label='COMPUTED', mode=args.mode, source_sha256=initial[str(SRC)],
                  included_sha256=initial[str(INCLUDED)], checker_sha256=audit.sha(__file__),
                  oracle_sha256=audit.sha(audit.__file__), elapsed_seconds=time.monotonic()-START,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  limits=dict(as_mib=audit.AS_MIB, cpu_seconds=18, external_seconds=20,
                              affinity=list(audit.os.sched_getaffinity(0))),
                  threads=len(list(audit.Path('/proc/self/task').iterdir())),
                  future_solver_outcome='PENDING_NOT_AUDITED')
    (WORK / (args.mode+'.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    (audit.HERE / 'results' / ('fast-'+args.mode+'.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'P', 'false_rooted_masks', 'omitted_working_repairs')}, sort_keys=True))


if __name__ == '__main__':
    main()
