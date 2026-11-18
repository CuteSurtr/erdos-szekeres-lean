#!/usr/bin/env python3
"""Standalone integer hull + direct all-Delta audit. No encoder/checker imports.

Ignores all reported counts and optimizer status. Recomputes from P, optionally
matches the original SAT orientation literals, and checks chain-pair families
against geometric hull families. Does not solve, generate a CNF, or certify LRAT.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def ensure(condition, message):
    if not condition:
        raise ValueError(message)


def mask(vertices):
    return sum(1 << p for p in vertices)


def bits(s, m):
    return [p for p in range(m) if s >> p & 1]


def digest(path):
    h = sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def audit(fixture, solver=None):
    started = time.monotonic()
    data = json.loads(fixture.read_text())
    points = data['P']
    ensure(isinstance(points, list) and len(points) == 15, 'expected 15 coordinates')
    ensure(all(isinstance(p, list) and len(p) == 2 and
               all(type(x) is int for x in p) for p in points), 'integer pairs required')
    m, n = 15, 6
    ensure(all(points[i][0] < points[i + 1][0] for i in range(m - 1)), 'x order')

    def det(i, j, k):
        a, b, c = points[i], points[j], points[k]
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    determinants = {t: det(*t) for t in combinations(range(m), 3)}
    ensure(all(determinants.values()), 'collinear triple')
    signs = ''.join('+' if d > 0 else '-' for d in determinants.values())
    ensure(data.get('signs', signs) == signs, 'recorded sign string differs from integers')
    if solver is not None:
        primary = {}
        with solver.open() as f:
            for line in f:
                if line.startswith('v '):
                    for literal in map(int, line.split()[1:]):
                        key = abs(literal)
                        if 1 <= key <= len(signs):
                            value = '+' if literal > 0 else '-'
                            ensure(key not in primary or primary[key] == value,
                                   'contradictory solver orientation literal')
                            primary[key] = value
        ensure(len(primary) == len(signs), 'missing solver orientation')
        ensure(signs == ''.join(primary[i] for i in range(1, len(signs) + 1)),
               'coordinates do not realize the actual SAT signs')
    for q in combinations(range(m), 4):
        seq = [determinants[t] > 0 for t in combinations(q, 3)]
        ensure(sum(a != b for a, b in zip(seq, seq[1:])) <= 1, 'signotope violation')

    def homogeneous(s, positive):
        return all((determinants[t] > 0) == positive for t in combinations(s, 3))

    # Build both hulls directly from integer determinants. This uses no
    # four-subset convexity definition and no endpoint-existence CNF variable.
    def hulls(s):
        lower, upper = [], []
        for p in s:
            while len(lower) >= 2 and det(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
            while len(upper) >= 2 and det(upper[-2], upper[-1], p) >= 0:
                upper.pop()
            upper.append(p)
        return lower, upper

    caps = sorted(mask(s) for s in combinations(range(m), 4) if homogeneous(s, False))
    cap5 = [mask(s) for s in combinations(range(m), 5) if homogeneous(s, False)]
    geometric = {mode: set() for mode in ('cup', 'weak', 'cap')}
    gons6 = []
    for k in (5, 6):
        for s in combinations(range(m), k):
            lower, upper = hulls(s)
            if len(lower) + len(upper) - 2 != k:
                continue
            ensure(homogeneous(lower, True) and homogeneous(upper, False),
                   'hull chains are not homogeneous')
            ensure((mask(lower) & mask(upper)) == mask((s[0], s[-1])),
                   'hull chains intersect internally')
            if k == 6:
                gons6.append(mask(s))
            else:
                geometric['weak'].add(mask(s))
                geometric['cup'].add(mask(lower))
                geometric['cap'].add(mask(upper))
    ensure(not cap5 and not gons6, 'configuration violates no5cap/no6gon')

    # Separate family reconstruction by exact all-triple chains and explicit
    # disjointness. There is no reuse of the hull decisions in this section.
    chains = {False: defaultdict(list), True: defaultdict(list)}
    for positive in (False, True):
        for k in range(2, 7 if positive else 5):
            for s in combinations(range(m), k):
                if homogeneous(s, positive):
                    chains[positive][s[0], s[-1], k].append(mask(s))
    paired = {mode: set() for mode in ('cup', 'weak', 'cap')}
    paired6, pair_count = set(), 0
    for (u, v, c), cap_list in chains[False].items():
        for total in (5, 6):
            d = total + 2 - c
            for cap in cap_list:
                for cup in chains[True].get((u, v, d), []):
                    ensure(cap & cup == (1 << u) | (1 << v),
                           'opposite homogeneous chains share an interior point')
                    if total == 6:
                        paired6.add(cap | cup)
                    else:
                        pair_count += 1
                        paired['weak'].add(cap | cup)
                        paired['cup'].add(cup)
                        paired['cap'].add(cap)
    ensure(not paired6 and paired == geometric, 'chain-pair/hull families differ')

    families = {mode: sorted(s) for mode, s in geometric.items()}
    counts = Counter()
    sizes = {mode: Counter() for mode in families}
    first = {}
    cover = sha256()
    capfree = blocked_by_cap = blocked_by_cup = 0
    # Literal enumeration, no subset transform or bounded-deletion recurrence.
    for delta in range(1 << m):
        witness = next((k for k in caps if delta & k == k), None)
        if witness is not None:
            blocked_by_cap += 1
            cover.update(f'{delta}:cap:{witness}\n'.encode())
            continue
        capfree += 1
        for mode, targets in families.items():
            missed = next((t for t in targets if delta & t == 0), None)
            if missed is None:
                counts[mode] += 1
                sizes[mode][delta.bit_count()] += 1
                first.setdefault(mode, bits(delta, m))
            elif mode == 'cup':
                blocked_by_cup += 1
                cover.update(f'{delta}:cup:{missed}\n'.encode())
    ensure(counts['cup'] == 0 and blocked_by_cap + blocked_by_cup == 1 << m,
           'a cup-side Delta works; no counterexample')
    return dict(
        label='COMPUTED', status='EXACT_REAL_CUP_COUNTEREXAMPLE',
        method='integer hulls and direct enumeration of all Delta; independent chain-pair crosscheck',
        m=m, n=n, P=points, signs=signs, orientation_triples=len(determinants),
        minimum_absolute_determinant=min(map(abs, determinants.values())),
        minimum_x_gap=min(points[i+1][0]-points[i][0] for i in range(m-1)),
        fivecaps=len(cap5), convex_hexagons=len(gons6), fourcaps=len(caps),
        convex_pentagons=len(families['weak']), chain_pairs=pair_count,
        target_counts={mode: len(ts) for mode, ts in families.items()},
        fourcap_masks=caps, target_masks=families,
        all_deltas=1 << m, fourcap_free_deltas=capfree,
        working_deltas={mode: counts[mode] for mode in families}, first_working_delta=first,
        working_delta_sizes={mode: dict(hist) for mode, hist in sizes.items()},
        cup_failure_cover=dict(by_fourcap=blocked_by_cap, by_missed_cup=blocked_by_cup,
                               ordered_witness_sha256=cover.hexdigest()),
        fixture=str(fixture), fixture_sha256=digest(fixture),
        solver=str(solver) if solver else None, solver_sha256=digest(solver) if solver else None,
        signs_sha256=sha256(signs.encode()).hexdigest(),
        wall_seconds=round(time.monotonic() - started, 6))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--solver', type=Path)
    args = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (256 << 20, 256 << 20))
    resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
    print(json.dumps(audit(args.fixture, args.solver), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
