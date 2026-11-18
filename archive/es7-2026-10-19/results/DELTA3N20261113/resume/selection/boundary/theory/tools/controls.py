#!/usr/bin/env python3
"""Tiny exact controls of the written family; no solver or random search.

Run with the research venv, external timeout20s and RLIMIT_AS400MiB.
The stdout report is deterministic. It uses only Python's standard library.
"""

import hashlib
import itertools
import json
from pathlib import Path


def family(n):
    k = n - 2
    q = 100 * k
    a = [(4*q*i, q*i + 4*i*i) for i in range(k-1)]
    b = [(4*q*q + 4*q*j, 4*q*q + 4*j*j) for j in range(3)]
    d = [(8*q*q + 4*q*i, -q*i + 4*i*i) for i in range(k-1)]
    return a + b + d, "A"*(k-1) + "B"*3 + "D"*(k-1)


def determinant(p, q, r):
    return ((q[0]-p[0])*(r[1]-p[1])
            - (q[1]-p[1])*(r[0]-p[0]))


def hull(points, ids):
    order = sorted(ids, key=points.__getitem__)
    chains = []
    for seq in (order, list(reversed(order))):
        chain = []
        for v in seq:
            while len(chain) >= 2 and determinant(
                    points[chain[-2]], points[chain[-1]], points[v]) <= 0:
                chain.pop()
            chain.append(v)
        chains.append(chain[:-1])
    return chains[0] + chains[1]


def control(n):
    points, blocks = family(n)
    k, m = n-2, len(points)
    ids = tuple(range(m))
    a, b, d = [tuple(i for i in ids if blocks[i] == name)
               for name in "ABD"]
    dets = {t: determinant(*(points[i] for i in t))
            for t in itertools.combinations(ids, 3)}
    expected = {"AAA": 1, "BBB": 1, "DDD": 1, "AAB": 1,
                "ABB": -1, "AAD": -1, "ADD": -1, "BBD": -1,
                "BDD": 1, "ABD": -1}
    assert all(points[i][0] < points[i+1][0] for i in range(m-1))
    assert all(value * expected[''.join(blocks[i] for i in t)] > 0
               for t, value in dets.items())

    def cup(vertices):
        return all(dets[t] > 0 for t in itertools.combinations(vertices, 3))

    def cap(vertices):
        return all(dets[t] < 0 for t in itertools.combinations(vertices, 3))

    def convex(vertices):
        return len(hull(points, vertices)) == len(vertices)

    cups = [c for c in itertools.combinations(ids, k) if cup(c)]
    expected_cups = sorted([a+(j,) for j in b] + [(j,)+d for j in b])
    assert cups == expected_cups
    assert not any(cup(c) for c in itertools.combinations(ids, k+1))
    assert not any(cap(c) for c in itertools.combinations(ids, 5))
    assert not any(convex(c) for c in itertools.combinations(ids, n))
    targets = [c for c in itertools.combinations(ids, n-1) if convex(c)]
    expected_targets = sorted(
        [a+pair for pair in itertools.combinations(b, 2)]
        + [pair+d for pair in itertools.combinations(b, 2)])
    assert targets == expected_targets
    complements = [tuple(i for i in ids if i not in c) for c in cups]
    assert all(convex(c) for c in complements)
    assert all(not set(pair).isdisjoint(t)
               for pair in itertools.combinations(b, 2) for t in targets)
    assert all(any(v not in t for t in targets) for v in ids)
    edges = [(i, j) for i, j in itertools.combinations(range(6), 2)
             if len(set(cups[i]) & set(cups[j])) == k-1]
    assert edges == [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)]
    return {"n": n, "k": k, "points": points,
            "minimum_absolute_determinant": min(map(abs, dets.values())),
            "maximum_cups": cups, "convex_complements": complements,
            "target_polygons": targets, "cup_exchange_edges": edges,
            "terminal_safe_pair": b[:2], "minimum_delta_size": 2,
            "status": "PASS"}


if __name__ == '__main__':
    result = {"label": "COMPUTED exact integer controls; proof is in theory.md",
              "scope": "fixed formula at n=6,7,8; no search",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "controls": [control(n) for n in (6, 7, 8)]}
    print(json.dumps(result, indent=2))
