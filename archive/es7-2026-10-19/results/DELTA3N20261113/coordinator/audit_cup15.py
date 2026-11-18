#!/usr/bin/env python3
"""Independent exact real-coordinate/hull audit of the new cup-side failure.

No encoder, geometry library or SAT import. All subsets are enumerated. Emits
the actual 15-variable coloring CNF for subsequent independent certification.
"""
import itertools
import json
from pathlib import Path


def turn(a, b, c):
    return a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0]


def mask(q):
    return sum(1 << i for i in q)


def hull(P, q):
    chains = []
    for order in (q, tuple(reversed(q))):
        chain = []
        for i in order:
            while len(chain) >= 2 and turn(P[chain[-2]], P[chain[-1]], P[i]) <= 0:
                chain.pop()
            chain.append(i)
        chains.append(chain)
    return chains


def main():
    root = Path('/home/jay/research/data/delta3-codex-20261113/coordinator/cup15')
    source = json.loads((root/'realized.json').read_text())
    P, n = source['P'], source['n']
    m = len(P)
    assert m == 15 and n == 6
    assert all(type(v) is int for p in P for v in p)
    assert all(P[i][0] < P[i+1][0] for i in range(m-1))
    I = range(m)
    comb = itertools.combinations
    orientations = {q: turn(*[P[i] for i in q]) for q in comb(I, 3)}
    assert all(orientations.values())
    assert ''.join('+' if d > 0 else '-' for d in orientations.values()) == source['signs']
    is_cap = lambda q: all(orientations[t] < 0 for t in comb(q, 3))
    caps = [q for q in comb(I, 4) if is_cap(q)]
    assert not any(is_cap(q) for q in comb(I, 5))
    targets = {'weak': {}, 'cup': {}, 'cap': {}}
    for k in (5, 6):
        for q in comb(I, k):
            lo, up = hull(P, q)
            if len(lo)+len(up)-2 != k:
                continue
            assert k == 5, 'Convex hexagon'
            targets['weak'][mask(q)] = q
            targets['cup'][mask(lo)] = q
            targets['cap'][mask(up)] = q
    cap_masks = [mask(q) for q in caps]
    counts = {kind: 0 for kind in targets}
    witnesses = {kind: None for kind in targets}
    for red in range(1 << m):
        if any(red & k == k for k in cap_masks):
            continue
        for kind, edges in targets.items():
            if all(red & e for e in edges):
                counts[kind] += 1
                if witnesses[kind] is None:
                    witnesses[kind] = [i for i in I if red >> i & 1]
    assert counts == {'weak': 353, 'cup': 0, 'cap': 87}
    clauses = [[-i-1 for i in q] for q in caps]
    clauses += [[i+1 for i in I if e >> i & 1] for e in sorted(targets['cup'])]
    cnf = root/'cup15_coloring.cnf'
    cnf.write_text(f'p cnf {m} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    report = dict(label='COMPUTED', method='all-subset integer hull enumeration',
                  m=m, n=n, orientation_count=len(orientations),
                  minimum_absolute_determinant=min(map(abs, orientations.values())),
                  cap5_count=0, hexagon_count=0, cap4_count=len(caps),
                  target_counts={k: len(v) for k,v in targets.items()},
                  working_deltas=counts, first_deltas=witnesses,
                  clauses=len(clauses), cap_clauses=[list(q) for q in caps],
                  lower_clause_witnesses=[{'cup': [i for i in I if e >> i & 1], 'pentagon': list(targets['cup'][e])}
                                          for e in sorted(targets['cup'])])
    (root/'independent_geometry.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k,v in report.items() if k not in ('cap_clauses', 'lower_clause_witnesses')}))


if __name__ == '__main__':
    main()
