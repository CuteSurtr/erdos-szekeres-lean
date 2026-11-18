#!/usr/bin/env python3
"""Independent short rooted-filter/finder audit; no parent checker imports."""
import os
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
                  PYTHONDONTWRITEBYTECODE='1')
import sys
import resource
AS_MIB = 500 if len(sys.argv) > 1 and sys.argv[1] == 'build' else 400
resource.setrlimit(resource.RLIMIT_AS, (AS_MIB << 20, AS_MIB << 20))
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
SELECTION = HERE.parent
RESUME = SELECTION.parent
RECORD = RESUME.parent
WORK = Path('/home/jay/research/data/delta3-codex-20261113/selection/audit')
OLD_WORK = Path('/home/jay/research/data/delta3-codex-20261113/resume/compact')
PYTHON = Path('/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python')
FILTER = SELECTION / 'rooted_formula.py'
FINDER = SELECTION / 'rooted.cpp'
INCLUDED = RECORD / 'search/delta_search.cpp'
START = time.monotonic()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def mask(vertices):
    return sum(1 << i for i in vertices)


def det(P, a, b, c):
    ax, ay = P[a]
    bx, by = P[b]
    cx, cy = P[c]
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)


def hull(P, indices):
    # Ordinary monotone hull, independent of any sign-packet/chain recurrence.
    def part(order):
        out = []
        for i in order:
            while len(out) >= 2 and det(P, out[-2], out[-1], i) <= 0:
                out.pop()
            out.append(i)
        return out
    lo, up = part(indices), part(reversed(indices))
    return set(lo+up)


def reference(points, n):
    require(all(len(p) == 2 and all(type(x) is int for x in p) for p in points), 'noninteger points')
    P = sorted(points)
    m = len(P)
    require(m > 0 and all(P[i][0] < P[i+1][0] for i in range(m-1)), 'x order')
    determinants = [det(P, *t) for t in itertools.combinations(range(m), 3)]
    require(all(determinants), 'collinear triple')
    caps = {k: [] for k in (4, 5)}
    convex = {k: [] for k in (n-1, n)}
    for k in sorted(set(caps) | set(convex)):
        for s in itertools.combinations(range(m), k):
            if k in caps and all(det(P, *t) < 0 for t in itertools.combinations(s, 3)):
                caps[k].append(mask(s))
            if k in convex and len(hull(P, s)) == k:
                convex[k].append(mask(s))
    root = 1 << (m-1)
    working = [d for d in range(1 << m)
               if not any(d & c == c for c in caps[4])
               and all(d & h for h in convex[n-1])]
    return dict(P=P, m=m, n=n, caps=caps[4], fivecaps=caps[5],
                targets=convex[n-1], ngons=convex[n],
                all_working=working, rooted_working=[d for d in working if d & root],
                signs=''.join('+' if d > 0 else '-' for d in determinants),
                min_abs_det=min(map(abs, determinants)) if determinants else None)


def parse_clause(line):
    v = tuple(map(int, line.split()))
    require(v and v[-1] == 0 and 0 not in v[:-1], 'invalid DIMACS clause')
    return v[:-1]


def formula_control(n):
    m = 16
    parent = OLD_WORK / f'n{n}m16-final.cnf'
    mapping = OLD_WORK / f'n{n}m16-final.map'
    coordinates = RESUME / 'compact' / ('real_n7m16.json' if n == 7 else 'real_n8m16_targeted.json')
    ref = reference(json.loads(coordinates.read_text())['P'], n)
    require(ref['m'] == m and not ref['fivecaps'] and not ref['ngons'], 'invalid real control')
    parent_hash, map_hash, filter_hash = sha(parent), sha(mapping), sha(FILTER)
    root = 1 << (m-1)
    lo, hi = 3, m-n+2

    # Build the expected mask family by combinations, not the production
    # integer loop or a copied list from its report.
    by_size = {k: sorted(mask(s) for s in itertools.combinations(range(m), k))
               for k in range(lo, hi+1)}
    all_masks = sorted(s for family in by_size.values() for s in family)
    rooted_masks = sorted(mask(s) | root
                          for k in range(lo, hi+1)
                          for s in itertools.combinations(range(m-1), k-1))
    require(len(rooted_masks) == sum(math.comb(m-1, k-1) for k in range(lo, hi+1)), 'rooted mask count')
    desired = set(rooted_masks)
    flags = {}
    values = {}
    by_id = {}
    for line in mapping.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        v, kind, s = line.split()
        v, s = int(v), int(s)
        require(v not in values and (kind, s) not in flags, 'duplicate mapped flag')
        flags[kind, s] = v
        by_id[v] = (kind, s)
        vertices = [i for i in range(m) if s & (1 << i)]
        if kind == 'orientation':
            require(len(vertices) == 3, 'orientation mask size')
            value = det(ref['P'], *vertices) > 0
        elif kind == 'convex':
            value = len(hull(ref['P'], vertices)) == len(vertices)
        elif kind == 'cap_contains':
            value = any(c & s == c for c in ref['caps'])
        elif kind == 'target_contains':
            value = any(t & s == t for t in ref['targets'])
        else:
            raise RuntimeError('unknown map kind ' + kind)
        values[v] = value

    independent = WORK / f'n{n}m16-independent.cnf'
    actual = WORK / f'n{n}m16-filter.cnf'
    retained = []
    false_masks = []
    total_in = total_out = nonpool = pool_index = 0
    phase = ''
    all_working = set(ref['all_working'])
    with parent.open('rb') as src, independent.open('wb+') as out:
        header = src.readline().split()
        require(header[:2] == [b'p', b'cnf'], 'parent header')
        nv, nc = map(int, header[2:])
        require(set(values) == set(range(1, nv+1)), 'map not complete')
        out.write(b' '*95+b'\n')
        for raw in src:
            if raw.startswith(b'c phase '):
                phase = raw.split()[2].decode()
                out.write(raw)
                continue
            if raw.startswith(b'c') or not raw.strip():
                out.write(raw)
                continue
            clause = parse_clause(raw)
            require(all(0 < abs(v) <= nv for v in clause), 'literal range')
            total_in += 1
            truth = any(values[abs(v)] == (v > 0) for v in clause)
            if phase == 'forall_delta':
                d = all_masks[pool_index]
                pool_index += 1
                # Verify the parent index-to-clause contract through map IDs.
                a = flags.get(('cap_contains', d), 0)
                rest = ((1 << m)-1) ^ d
                b = flags.get(('convex', rest), 0) if rest.bit_count() == n-1 else flags.get(('target_contains', rest), 0)
                require(clause == tuple(v for v in (a, b) if v), 'parent mask/clause contract differs')
                require(truth == (d not in all_working), 'source failure clause semantics')
                if d not in desired:
                    continue
                retained.append(d)
                if not truth:
                    false_masks.append(d)
            else:
                require(truth, 'false nonpool clause: ' + phase)
                nonpool += 1
            # Copy exact bytes: no literal, sign, order or whitespace rewrite.
            out.write(raw)
            total_out += 1
        require(total_in == nc and pool_index == len(all_masks), 'source counts')
        out.seek(0)
        out.write(f'p cnf {nv} {total_out}'.encode().ljust(95)+b'\n')
    require(retained == rooted_masks, 'mask coverage/order mismatch')
    expected_false = sorted(desired & set(ref['rooted_working']))
    require(false_masks == expected_false, 'false clauses differ from rooted working masks')

    # Check both forms of range repair while retaining the root explicitly.
    moved = []
    for d in ref['rooted_working']:
        e = d
        if d.bit_count() < lo:
            for i in range(m):
                if e.bit_count() >= lo:
                    break
                e |= 1 << i
        elif d.bit_count() > hi:
            e = root | mask([i for i in range(m-1) if d & (1 << i)][:hi-1])
        require(e & root and e in desired and e in all_working, 'root lost during range repair')
        if e != d:
            moved.append([d, e])

    command = [str(PYTHON), '-B', str(FILTER), '--m', str(m), '--n', str(n),
               '--input', str(parent), '--output', str(actual)]
    p = subprocess.run(command, capture_output=True, text=True, timeout=5)
    (WORK / f'n{n}m16-filter.stdout').write_text(p.stdout)
    (WORK / f'n{n}m16-filter.stderr').write_text(p.stderr)
    require(p.returncode == 0, 'production filter failed: ' + p.stderr)
    require(sha(actual) == sha(independent), 'independent/production child differs')
    report = json.loads(actual.with_suffix('.generation.json').read_text())
    require(report['clauses'] == total_out and report['rooted_pool_size'] == len(rooted_masks), 'generation counts')
    require(report['input_sha256'] == parent_hash and report['output_sha256'] == sha(actual), 'generation hashes')
    require(report['source_sha256'] == filter_hash, 'filter provenance')
    require(sha(parent) == parent_hash and sha(mapping) == map_hash and sha(FILTER) == filter_hash, 'input changed')
    # Copies here are small source/control data; large CNFs stay in scratch.
    (HERE / 'results' / f'n{n}m16-fixture.json').write_text(json.dumps(dict(P=ref['P'], n=n), indent=2)+'\n')
    return dict(status='PASS', n=n, m=m, root=m-1, root_policy='rightmost',
                variables=nv, input_clauses=nc, nonpool_clauses=nonpool,
                source_pool_clauses=len(all_masks), rooted_pool_clauses=len(rooted_masks),
                child_clauses=total_out, child_sha256=sha(actual),
                source_cnf=str(parent), source_cnf_sha256=parent_hash, map_sha256=map_hash,
                coordinate_source=str(coordinates), coordinate_sha256=sha(coordinates),
                filter_sha256=filter_hash, filter_command=command,
                fourcaps=len(ref['caps']), targets=len(ref['targets']),
                fivecaps=0, ngons=0, minimum_absolute_determinant=ref['min_abs_det'],
                all_working_count=len(ref['all_working']), rooted_working_count=len(ref['rooted_working']),
                false_rooted_pool_clauses=len(false_masks), false_rooted_masks=false_masks,
                omitted_rooted_repairs=moved, generation=report,
                future_solver_outcome='PENDING_NOT_AUDITED')


def build():
    binary = WORK / 'rooted'
    command = ['g++', '-std=c++17', '-O1', '-Wall', '-Wextra', str(FINDER), '-o', str(binary)]
    p = subprocess.run(command, capture_output=True, text=True, timeout=15)
    (WORK / 'compile.stdout').write_text(p.stdout)
    (WORK / 'compile.stderr').write_text(p.stderr)
    require(p.returncode == 0, 'build failed: ' + p.stderr)
    return dict(status='PASS', command=command, binary_sha256=sha(binary),
                finder_sha256=sha(FINDER), included_geometry_sha256=sha(INCLUDED))


def finder_control():
    build_info = json.loads((WORK / 'build.json').read_text())
    require(build_info['binary_sha256'] == sha(WORK / 'rooted') and
            build_info['finder_sha256'] == sha(FINDER) and
            build_info['included_geometry_sha256'] == sha(INCLUDED), 'build provenance changed')
    fixtures = []
    source7 = json.loads((RESUME / 'compact/real_n7m16.json').read_text())['P']
    source8 = json.loads((RESUME / 'compact/real_n8m16_targeted.json').read_text())['P']
    real15 = json.loads((RECORD / 'coordinator/data/cup15/realized.json').read_text())['P']
    star = json.loads((RESUME / 'pool/maximal/real-star.json').read_text())['P'] if (RESUME / 'pool/maximal/real-star.json').exists() else json.loads((RESUME / 'audit/results/real-star-input.json').read_text())['P']
    for n, source in ((7, source7), (8, source8)):
        fixtures.extend((f'prefix-{size}-n{n}', n, source[:size], 'valid') for size in (4, 8, 10, 12))
        fixtures.append((f'reversed-input-n{n}', n, list(reversed(source[:10])), 'valid'))
        fixtures.append((f'cup15-prefix-n{n}', n, real15[:10], 'valid'))
        fixtures.append((f'real-star-n{n}', n, star, 'valid'))
        fixtures.append((f'fivecap-n{n}', n, [[i, -i*i] for i in range(5)], 'invalid_premise'))
        fixtures.append((f'convex-ngon-n{n}', n, [[i, i*i] for i in range(n)], 'invalid_premise'))
    refs = {}
    for name, n, P, expectation in fixtures:
        ref = reference(P, n)
        require((not ref['fivecaps'] and not ref['ngons']) == (expectation == 'valid'), 'fixture classification')
        refs[name] = ref
    results = []
    for n in (7, 8):
        selected = [f for f in fixtures if f[1] == n]
        input_path, outdir = WORK / f'finder-n{n}.pool', WORK / f'finder-n{n}'
        text = [f'D3POOL 1 {len(selected)}']
        for _, _, P, _ in selected:
            text.append(str(len(P)))
            text.extend(f'{x} {y}' for x, y in P)
        input_path.write_text('\n'.join(text)+'\n')
        command = [str(WORK / 'rooted'), str(n), str(input_path), str(outdir), '300']
        p = subprocess.run(command, capture_output=True, text=True, timeout=5)
        (WORK / f'finder-n{n}.stdout.jsonl').write_text(p.stdout)
        (WORK / f'finder-n{n}.stderr').write_text(p.stderr)
        require(p.returncode == 0, 'finder process failed: ' + p.stderr)
        lines = [json.loads(line) for line in p.stdout.splitlines()]
        require(len(lines) == len(selected), 'finder output length')
        for index, (item, (name, _, P, expectation)) in enumerate(zip(lines, selected)):
            require(item['pool_index'] == index, 'finder pool order')
            result, ref = item['result'], refs[name]
            require(result['n'] == n and result['m'] == len(P) and result['mode'] == 'weak', 'finder metadata')
            if expectation == 'invalid_premise':
                require(result['status'] == 'INVALID', 'invalid premise not rejected')
            elif ref['rooted_working']:
                require(result['status'] == 'OK' and result['forward_verified'], 'existing rooted Delta not returned')
                d = result['Delta']
                require(len(d) == len(set(d)) and all(type(i) is int and 0 <= i < len(P) for i in d), 'invalid Delta labels')
                require(mask(d) in ref['rooted_working'], 'returned Delta fails independent hull/root check')
                require(result['negative_clauses'] == len(ref['caps']), 'four-cap count mismatch')
                require(result['positive_clauses'] >= 1, 'missing root membership clause')
            else:
                require(result['status'] == 'NO_ROOTED_DELTA_COMPUTED', 'expected no rooted Delta')
            results.append(dict(name=name, expectation=expectation, finder=result,
                                sorted_P=ref['P'], input_was_x_sorted=P == ref['P'],
                                fourcaps=len(ref['caps']), targets=len(ref['targets']),
                                rooted_working_count=len(ref['rooted_working']),
                                rooted_working_masks=ref['rooted_working'],
                                fivecaps=len(ref['fivecaps']), ngons=len(ref['ngons'])))
    return dict(status='PASS', cases=results, binary_sha256=sha(WORK / 'rooted'),
                finder_sha256=sha(FINDER), inherited_geometry_sha256=sha(INCLUDED),
                valid_cases=sum(c['expectation'] == 'valid' for c in results),
                invalid_premise_cases=sum(c['expectation'] != 'valid' for c in results),
                future_negative_finder_outcomes='PENDING_NOT_AUDITED')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['formula7', 'formula8', 'build', 'finder'])
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    (HERE / 'results').mkdir(exist_ok=True)
    before = {str(p): sha(p) for p in (FILTER, FINDER, INCLUDED)}
    result = {'formula7': lambda: formula_control(7), 'formula8': lambda: formula_control(8),
              'build': build, 'finder': finder_control}[args.mode]()
    require(before == {p: sha(p) for p in before}, 'reviewed sources changed during control')
    result.update(label='COMPUTED', mode=args.mode, checker_sha256=sha(__file__),
                  elapsed_seconds=time.monotonic()-START,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  limits=dict(as_mib=AS_MIB, cpu_seconds=18, external_seconds=20,
                              affinity=list(os.sched_getaffinity(0))),
                  threads=len(list(Path('/proc/self/task').iterdir())))
    for directory in (WORK, HERE / 'results'):
        (directory / (args.mode+'.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    excluded = {'cases', 'false_rooted_masks', 'omitted_rooted_repairs', 'generation'}
    print(json.dumps({k: v for k, v in result.items() if k not in excluded}, sort_keys=True))


if __name__ == '__main__':
    main()
