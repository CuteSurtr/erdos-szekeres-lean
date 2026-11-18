#!/usr/bin/env python3
"""Independent compact-encoder review controls; no parent checker imported."""
import audit_pool as audit
import argparse
import collections
import itertools
import json
import math
from pathlib import Path
import resource
import subprocess
import time

ROOT = audit.HERE.parent / 'compact'
SRC = ROOT / 'compact_cnf.cpp'
WORK = audit.SCRATCH / 'compact'
BINARY = WORK / 'compact_cnf'
START = time.monotonic()


def run(command, seconds=8):
    r = subprocess.run(command, capture_output=True, text=True, timeout=seconds)
    audit.need(r.returncode == 0, 'command failed: ' + r.stderr)
    return r.stdout


def build():
    command = ['g++', '-std=c++17', '-O1', '-Wall', '-Wextra', '-pedantic',
               str(SRC), '-o', str(BINARY)]
    output = run(command)
    (WORK / 'compile.log').write_text(output)
    result = dict(status='PASS', command=command, source_sha256=audit.sha(SRC),
                  binary_sha256=audit.sha(BINARY))
    (WORK / 'build.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def require_binary():
    record = json.loads((WORK / 'build.json').read_text())
    audit.need(record['source_sha256'] == audit.sha(SRC), 'source changed since build')
    audit.need(record['binary_sha256'] == audit.sha(BINARY), 'binary changed since build')


def algebra():
    count = 0
    for bits in itertools.product((False, True), repeat=4):
        a, b, c, d = bits
        valid = sum(bits[i] != bits[i+1] for i in range(3)) <= 1
        convex = a == b and c == d
        packet_clauses = []
        for i, j, k in itertools.combinations(range(4), 3):
            packet_clauses.extend((not bits[i] or bits[j] or not bits[k],
                                   bits[i] or not bits[j] or bits[k]))
        for z in (False, True):
            quad_clauses = [not z or not a or b, not z or a or not b,
                            not z or not c or d, not z or c or not d,
                            z or a or d, z or not a or not d,
                            z or b or not c, z or not b or c]
            audit.need(all(packet_clauses + quad_clauses) == (valid and z == convex),
                       'four-point equivalence failed')
            count += 1
    triples = list(itertools.combinations(range(5), 3))
    valid_count = 0
    for bits in itertools.product((False, True), repeat=len(triples)):
        values = dict(zip(triples, bits))
        packets = [[values[t] for t in itertools.combinations(q, 3)]
                   for q in itertools.combinations(range(5), 4)]
        if any(sum(q[i] != q[i+1] for i in range(3)) > 1 for q in packets):
            continue
        valid_count += 1
        all_cap = not any(bits)
        consecutive_cap = not any(values[(i, i+1, i+2)] for i in range(3))
        audit.need(all_cap == consecutive_cap, 'five-cap clause mismatch')
    # Direct cover checks at nonconsecutive masks catch deletion-chain mistakes.
    cover_checks = 0
    for s in range(1 << 9):
        vertices = [i for i in range(9) if s & (1 << i)]
        if len(vertices) < 5:
            continue
        children = [s ^ (1 << i) for i in vertices[:5]]
        for q in itertools.combinations(vertices, 4):
            t = audit.mask(q)
            audit.need(any(t & child == t for child in children), 'five-deletion cover')
            cover_checks += 1
    return dict(status='PASS', q4_assignments=count,
                five_point_orientations_enumerated=1 << 10,
                five_point_signotopes_checked=valid_count, cover_checks=cover_checks)


def encode(m, n, name, convex='recurrence', pool='reduced', containment='witness'):
    cnf, mapping = WORK / (name+'.cnf'), WORK / (name+'.map')
    command = [str(BINARY), '--m', str(m), '--n', str(n), '--out', str(cnf),
               '--map', str(mapping), '--convex', convex, '--pool', pool,
               '--containment', containment]
    stats = json.loads(run(command, 3))
    (WORK / (name+'.encoding.json')).write_text(json.dumps(stats, indent=2)+'\n')
    return cnf, mapping, stats


def evaluate(ref, name, convex='recurrence', pool='reduced', containment='witness', project=False):
    m, n, P = ref['m'], ref['n'], ref['P']
    audit.need(not ref['fivecaps'] and not ref['ngons'], 'positive fixture premises fail')
    cnf, mapping, stats = encode(m, n, name, convex, pool, containment)
    full = (1 << m)-1
    amax = m-n+2 if pool == 'reduced' else m
    bmax = m-3 if pool == 'reduced' else m
    lower = 3 if pool == 'reduced' else 0
    values = [None] * (stats['variables']+1)
    kinds = collections.defaultdict(set)
    orientations = []
    for line in mapping.read_text().splitlines():
        if line.startswith('#'):
            continue
        sid, kind, smask = line.split()
        v, s = int(sid), int(smask)
        audit.need(0 < v < len(values) and values[v] is None, 'duplicate/out-of-range id')
        audit.need(s not in kinds[kind], 'duplicate mapped subset')
        kinds[kind].add(s)
        vertices = [i for i in range(m) if s & (1 << i)]
        if kind == 'orientation':
            audit.need(len(vertices) == 3, 'orientation mask')
            value = audit.determinant(*(P[i] for i in vertices)) > 0
            orientations.append(v if value else -v)
        elif kind == 'convex':
            lo, up = audit.chains(P, vertices)
            value = len(set(lo+up)) == len(vertices)
        elif kind == 'cap_contains':
            value = any(c & s == c for c in ref['fourcaps'])
        elif kind == 'target_contains':
            value = any(t & s == t for t in ref['targets'])
        else:
            raise RuntimeError('unknown kind ' + kind)
        values[v] = value
    audit.need(all(v is not None for v in values[1:]), 'unmapped variable')
    q_sizes = set(range(4, n)) if convex == 'recurrence' else {4, n-1}
    expected_sizes = {'orientation': {3}, 'convex': q_sizes,
                      'cap_contains': set(range(4, amax+1)),
                      'target_contains': set(range(n, bmax+1))}
    for kind, sizes in expected_sizes.items():
        expected = {s for s in range(1 << m) if s.bit_count() in sizes}
        audit.need(kinds[kind] == expected, kind + ': allocated domain mismatch')
    pool_masks = [s for s in range(1 << m) if lower <= s.bit_count() <= amax]
    if amax < lower:
        pool_masks = [None]
    working = set(ref['working_masks'])
    failures = []
    byphase = collections.Counter()
    phase = None
    index = 0
    base = [] if project else None
    queries = [] if project else None
    with cnf.open() as f:
        header = f.readline().split()
        audit.need(header == ['p', 'cnf', str(stats['variables']), str(stats['clauses'])], 'header')
        for line in f:
            if line.startswith('c phase '):
                phase = line.split()[2]
                continue
            ints = list(map(int, line.split()))
            audit.need(ints and ints[-1] == 0 and 0 not in ints[:-1], 'bad clause')
            clause = ints[:-1]
            truth = any(values[abs(v)] == (v > 0) for v in clause)
            byphase[phase] += 1
            if phase == 'forall_delta':
                d = pool_masks[index]
                expected = d is not None and d not in working
                audit.need(truth == expected, 'pool truth mismatch for ' + str(d))
                if not truth:
                    failures.append(d)
                if project:
                    queries.append((d, clause, expected))
                index += 1
            else:
                audit.need(truth, 'canonical real assignment falsifies ' + str(phase))
                if project:
                    base.append(clause)
    audit.need(index == len(pool_masks), 'pool size/order mismatch')
    audit.need(sum(byphase.values()) == stats['clauses'], 'total clause count')
    # Construct a retained working Delta from every omitted working Delta.
    transformed = 0
    if amax >= lower:
        for d in working:
            changed = d
            if d.bit_count() < lower:
                for i in range(m):
                    if changed.bit_count() == lower:
                        break
                    changed |= 1 << i
            elif d.bit_count() > amax:
                changed = audit.mask([i for i in range(m) if d & (1 << i)][:amax])
            audit.need(changed in working and lower <= changed.bit_count() <= amax,
                       'reduced interval failed to retain a working Delta')
            transformed += changed != d
    else:
        audit.need(audit.mask(range(3)) in working, 'empty range witness failed')
    projections = 0
    if project:
        from pysat.solvers import Cadical195
        with Cadical195(bootstrap_with=base + [[v] for v in orientations]) as solver:
            for q, (d, clause, expected) in enumerate(queries):
                guard = stats['variables'] + q + 1
                solver.add_clause([-guard] + clause)
                solver.conf_budget(1000)
                answer = solver.solve_limited(assumptions=[guard])
                audit.need(answer is not None and answer == expected,
                           'existential auxiliary projection differs at ' + str(d))
                projections += 1
    return dict(status='PASS', name=name, m=m, n=n, convex=convex, pool=pool,
                containment=containment, variables=stats['variables'],
                clauses=stats['clauses'], clauses_by_phase=dict(byphase),
                fourcaps=len(ref['fourcaps']), targets=len(ref['targets']),
                working_delta_count=len(working), failed_pool_clauses=len(failures),
                omitted_working_deltas_transformed=transformed,
                existential_projection_queries=projections,
                cnf_sha256=audit.sha(cnf), map_sha256=audit.sha(mapping))


def real(n):
    source = ROOT / ('real_n7m16.json' if n == 7 else 'real_n8m16_targeted.json')
    fixture = json.loads(source.read_text())
    ref = audit.reference(fixture['P'], n)
    name = f'real-n{n}m16'
    result = evaluate(ref, name)
    parent = audit.SCRATCH.parent / f'compact/n{n}m16-final.cnf'
    parent_map = parent.with_suffix('.map')
    audit.need(result['cnf_sha256'] == audit.sha(parent), 'delivered CNF differs from fresh source build')
    audit.need(result['map_sha256'] == audit.sha(parent_map), 'delivered map differs from fresh source build')
    result.update(coordinate_source=str(source), coordinate_sha256=audit.sha(source),
                  delivered_cnf=str(parent), delivered_bytes_confirmed=True,
                  minimum_absolute_determinant=ref['minimum_absolute_determinant'])
    return result


def tiny():
    fixture = json.loads(audit.FIXTURE.read_text())
    ref = audit.reference(fixture['P'][:9], 6)
    cases = []
    for convex, pool, containment in itertools.product(('recurrence', 'direct'), ('reduced', 'all'), ('witness', 'exact')):
        cases.append(evaluate(ref, '-'.join(('tiny', convex, pool, containment)),
                              convex, pool, containment, project=True))
    for m, n in ((4, 5), (4, 8), (5, 8), (6, 7)):
        ref = audit.reference([[i, i*i] for i in range(m)], n)
        cases.append(evaluate(ref, f'edge-m{m}n{n}'))
    return dict(status='PASS', cases=cases,
                total_projection_queries=sum(c['existential_projection_queries'] for c in cases))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['build', 'algebra', 'tiny', 'real7', 'real8', 'real15'])
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    before = audit.sha(SRC)
    if args.mode not in ('build', 'algebra'):
        require_binary()
    result = {'build': build, 'algebra': algebra, 'tiny': tiny,
              'real7': lambda: real(7), 'real8': lambda: real(8),
              'real15': lambda: evaluate(audit.reference(json.loads(audit.FIXTURE.read_text())['P'], 6), 'real15-n6')}[args.mode]()
    audit.need(before == audit.sha(SRC), 'source changed during check')
    result.update(label='COMPUTED', mode=args.mode, source_sha256=before,
                  checker_sha256=audit.sha(__file__), hull_checker_sha256=audit.sha(audit.__file__),
                  elapsed_seconds=time.monotonic()-START,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits=dict(as_mib=400, cpu_seconds=18, external_seconds=20,
                              affinity=list(audit.os.sched_getaffinity(0))),
                  thread_count=len(list(Path('/proc/self/task').iterdir())))
    (WORK / (args.mode+'.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    (audit.HERE / 'results' / ('compact-'+args.mode+'.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
