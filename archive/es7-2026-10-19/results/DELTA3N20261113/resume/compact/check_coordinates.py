#!/usr/bin/env python3
"""Independent exact-integer geometry + canonical emitted-clause audit.

No imports from either encoder, their audits, or SAT libraries. Convexity
comes from hulls; containment from a full zeta transform, not five deletions.
This does not verify an LRAT proof or certify a universal theorem.
"""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def analyze(points, n):
    require(4 <= len(points) <= 16, 'point count outside checker scope')
    require(all(len(p) == 2 and all(type(x) is int for x in p) for p in points),
            'integer pairs required')
    m, full = len(points), (1 << len(points)) - 1
    require(all(points[i][0] < points[i+1][0] for i in range(m-1)), 'x order')

    def det(i, j, k):
        a, b, c = points[i], points[j], points[k]
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

    triples = list(combinations(range(m), 3))
    ds = {t: det(*t) for t in triples}
    require(all(ds.values()), 'collinear triple')
    signs = {t: ds[t] > 0 for t in triples}
    mask = lambda s: sum(1 << x for x in s)

    def convex(s):
        lower, upper = [], []
        for p in s:
            while len(lower) >= 2 and det(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        for p in reversed(s):
            while len(upper) >= 2 and det(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        return len(lower)+len(upper)-2 == len(s)

    q = {}
    criterion_checks = 0
    for k in range(4, min(n, m)+1):
        for s in combinations(range(m), k):
            q[mask(s)] = convex(s)
            criterion = all(signs[a,b,c] == signs[a,b,d] and signs[a,c,d] == signs[b,c,d]
                            for a,b,c,d in combinations(s, 4))
            require(q[mask(s)] == criterion, 'hull/4-subset criterion mismatch')
            criterion_checks += 1
    caps = [mask(s) for s in combinations(range(m), 4)
            if all(ds[t] < 0 for t in combinations(s, 3))]
    cap5 = [mask(s) for s in combinations(range(m), 5)
            if all(ds[t] < 0 for t in combinations(s, 3))]
    targets = [s for s, val in q.items() if s.bit_count() == n-1 and val]
    ngons = [s for s, val in q.items() if s.bit_count() == n and val]

    def closure(seeds):
        a = bytearray(full+1)
        for s in seeds:
            a[s] = 1
        for i in range(m):
            bit = 1 << i
            for s in range(full+1):
                if s & bit:
                    a[s] |= a[s ^ bit]
        return a

    ca, tg = closure(caps), closure(targets)
    working = [d for d in range(full+1) if not ca[d] and not tg[full ^ d]]
    first = working[0] if working else None
    # Explicitly check the first witness using the raw families as well.
    if first is not None:
        require(not any(k & first == k for k in caps), 'bad cap-free witness')
        require(all(k & first for k in targets), 'bad transversal witness')
    report = dict(label='COMPUTED', m=m, n=n, valid=not cap5 and not ngons,
                  triples=len(triples), min_abs_determinant=min(map(abs, ds.values())),
                  fourcaps=len(caps), fivecaps=len(cap5), targets=len(targets), ngons=len(ngons),
                  hull_criterion_comparisons=criterion_checks, working_deltas=len(working),
                  first_delta=[i for i in range(m) if first is not None and first >> i & 1],
                  signs=''.join('+' if signs[t] else '-' for t in triples),
                  caps=caps, target_masks=targets,
                  reduced_pool_working=sum(3 <= d.bit_count() <= m-n+2 for d in working))
    return report, q, ca, tg, signs


def audit(points, n, cnf, mapfile):
    started = time.monotonic()
    report, q, ca, tg, signs = analyze(points, n)
    values = [False]
    kinds = Counter()
    for line in Path(mapfile).read_text().splitlines():
        if line.startswith('#') or not line.strip():
            continue
        ident, kind, sm = line.split()
        ident, s = int(ident), int(sm)
        require(ident == len(values), 'nonconsecutive variable identifiers')
        require(0 < s < 1 << len(points), 'bad variable mask')
        if kind == 'orientation':
            v = signs[tuple(i for i in range(len(points)) if s >> i & 1)]
        elif kind == 'convex':
            v = q[s]
        elif kind == 'cap_contains':
            v = ca[s]
        elif kind == 'target_contains':
            v = tg[s]
        else:
            raise ValueError('unknown map kind: '+kind)
        values.append(bool(v))
        kinds[kind] += 1
    counts, failures, first_failure = Counter(), Counter(), {}
    phase, declared, literals = None, None, 0
    with open(cnf) as f:
        for line in f:
            words = line.split()
            if not words:
                continue
            if words[0] == 'p':
                require(declared is None and words[1] == 'cnf', 'bad DIMACS header')
                declared = tuple(map(int, words[2:]))
                continue
            if words[0] == 'c':
                if words[1:2] == ['phase']:
                    phase = words[2]
                continue
            row = list(map(int, words))
            require(phase is not None and row[-1] == 0 and 0 not in row[:-1], 'bad clause')
            c = row[:-1]
            require(all(0 < abs(x) < len(values) for x in c), 'out-of-range variable')
            counts[phase] += 1
            literals += len(c)
            if not any(values[abs(x)] == (x > 0) for x in c):
                failures[phase] += 1
                first_failure.setdefault(phase, c)
    require(declared == (len(values)-1, sum(counts.values())), 'header/map/count mismatch')
    require(not any(v for k, v in failures.items()
                    if k not in ('forall_delta', 'no5cap', 'no_ngon')), 'false definition clause')
    require(bool(failures['no5cap']) == bool(report['fivecaps']), 'cap-premise mismatch')
    require(bool(failures['no_ngon']) == bool(report['ngons']), 'convex-premise mismatch')
    if counts['forall_delta']:
        expected = (report['working_deltas'] if counts['forall_delta'] == 1 << len(points)
                    else report['reduced_pool_working'])
        if len(points)-n+2 < 3:
            expected = 1  # Explicit trivial-obstruction empty clause.
        require(failures['forall_delta'] == expected, 'pool truth/count mismatch')
    report.update(canonical=dict(variables=len(values)-1, clauses=sum(counts.values()),
                                literals=literals, phases=dict(counts), false_clauses=dict(failures),
                                first_false_clauses=first_failure, variable_kinds=dict(kinds)),
                  hashes=dict(cnf=sha(cnf), variable_map=sha(mapfile)),
                  seconds=round(time.monotonic()-started, 6))
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--points', required=True)
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--cnf')
    ap.add_argument('--map')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.points).read_text())
    points = data['P'] if isinstance(data, dict) else data
    require(bool(args.cnf) == bool(args.map), 'supply CNF and map together')
    if args.cnf:
        report = audit(points, args.n, args.cnf, args.map)
    else:
        report = analyze(points, args.n)[0]
    report['coordinate_input_sha256'] = sha(args.points)
    Path(args.out).write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: report[k] for k in ('label','m','n','valid','fourcaps','targets','working_deltas')}))


if __name__ == '__main__':
    main()
