#!/usr/bin/env python3
"""Independent exact audit of the two small fan-exchange obstructions.

Uses all-triple chain tests and monotone hull enumeration, not the endpoint
dynamic program or SAT encoding used during extraction. No solver is invoked.
"""
import itertools
import json
from pathlib import Path


def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def hull(P, ids):
    lower, upper = [], []
    for i in ids:
        while len(lower) > 1 and det(P[lower[-2]], P[lower[-1]], P[i]) < 0:
            lower.pop()
        lower.append(i)
    for i in reversed(ids):
        while len(upper) > 1 and det(P[upper[-2]], P[upper[-1]], P[i]) < 0:
            upper.pop()
        upper.append(i)
    return lower, upper


def verify(path):
    r = json.loads(path.read_text())
    P, n = r['P'], r['n']
    ids = range(len(P))
    assert all(P[i][0] < P[i + 1][0] for i in range(len(P) - 1))
    signs = {t: det(*(P[i] for i in t)) for t in itertools.combinations(ids, 3)}
    assert all(signs.values())
    iscap = lambda t: all(signs[s] < 0 for s in itertools.combinations(t, 3))
    iscup = lambda t: all(signs[s] > 0 for s in itertools.combinations(t, 3))
    caps = [t for t in itertools.combinations(ids, 4) if iscap(t)]
    assert caps == list(map(tuple, r['caps4']))
    assert not any(iscap(t) for t in itertools.combinations(ids, 5))
    assert not any(len(set(sum(hull(P, t), []))) == n for t in itertools.combinations(ids, n))
    lower_sides = {}
    for t in itertools.combinations(ids, n - 1):
        lo, hi = hull(P, t)
        if len(set(lo + hi)) == n - 1:
            lower_sides[tuple(lo)] = len(hi)
    longest_cups = [t for t in itertools.combinations(ids, n - 1) if iscup(t)]
    assert longest_cups == list(map(tuple, r['type2_cups']))
    assert all(lower_sides[d] == 2 for d in longest_cups)
    D, K, A, B = r['D'], r['K'], set(r['A']), set(r['B'])
    assert iscup(D) and iscap(K) and len(K) == 3
    assert (D[0], D[-1]) == (K[0], K[-1])
    assert set(D) & set(K) == {D[0], D[-1]}
    assert lower_sides[tuple(D)] == 3 and not A & set(D)
    v = D[-1]
    H = {k[1] for k in caps if k[0] == v}
    Q = set(ids) - {k[0] for k in caps}
    assert H == set(r['H']) and len(H) == 1
    assert A <= Q and H <= A
    assert B == (A - H) | {v}
    assert not any(set(k) <= A or set(k) <= B for k in caps)
    assert all(A & set(c) for c in longest_cups)
    C = tuple(r['lost_type2_cup'])
    assert C in longest_cups and set(C) & A == H and not set(C) & B
    # These examples obstruct the fan replacement, not E1: adding point 0 works.
    assert 0 in D and 0 in Q
    assert not any(set(k) <= A | {0} for k in caps)
    return {'label': 'COMPUTED', 'file': path.name, 'n': n, 'm': len(P),
            'nonzero_determinants': len(signs), 'five_caps': 0,
            'convex_n_gons': 0, 'four_caps': caps, 'type2_cups': len(longest_cups),
            'H': sorted(H), 'lost_type2_cup': C,
            'fan_exchange_fails_coverage': True, 'E1_repair': {'add': 0, 'remove': []}}


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    rows = [verify(root / f'fan_obstruction_n{n}.json') for n in (7, 8)]
    print(json.dumps(rows, indent=2))
