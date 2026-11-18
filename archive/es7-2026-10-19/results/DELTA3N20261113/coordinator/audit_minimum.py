#!/usr/bin/env python3
"""Independent full-subset hull audit of the minimum-transversal obstruction.

No imports from the search program, esgeo, or a SAT library. All integers are
Python arbitrary-precision integers. Enumerates all 2^16 candidate subsets.
"""
import itertools
import json
from pathlib import Path
import time
from collections import Counter


def determinant(p, q, r):
    return p[0]*(q[1]-r[1])+q[0]*(r[1]-p[1])+r[0]*(p[1]-q[1])


def mask(vertices):
    return sum(1 << i for i in vertices)


def hull(points, indices):
    lo, up = [], []
    for chain, seq in ((lo, indices), (up, list(reversed(indices)))):
        for i in seq:
            while len(chain) > 1 and determinant(points[chain[-2]], points[chain[-1]], points[i]) < 0:
                chain.pop()
            chain.append(i)
    return lo, up


def audit(path):
    start = time.monotonic()
    source = json.loads(path.read_text())
    P, n = source['P'], source['n']
    m = len(P)
    assert m <= 20
    assert all(P[i][0] < P[i+1][0] for i in range(m-1))
    I = list(range(m))
    comb = itertools.combinations
    assert all(determinant(*[P[i] for i in t]) for t in comb(I, 3))
    cap = lambda q: all(determinant(*[P[i] for i in t]) < 0 for t in comb(q, 3))
    assert not any(cap(q) for q in comb(I, 5))
    caps = [mask(q) for q in comb(I, 4) if cap(q)]
    cups, supports = set(), {}
    gon_count = 0
    for k in (n-1, n):
        for q in comb(I, k):
            lo, up = hull(P, q)
            if len(lo)+len(up)-2 == k:
                assert k != n, 'Forbidden convex polygon'
                gon_count += 1
                c = mask(lo)
                cups.add(c)
                supports[c] = q
    cups = sorted(cups, key=lambda c: (c.bit_count(), c))
    # Independently justify every dynamic positive clause used by the search.
    for q in source['cup_constraints']:
        assert mask(q) in cups
    # Check the actual saved formulas as well, rather than trust their builder.
    threshold = lambda i, j: m+i*(i-1)//2+j
    expected_counter = []
    for i in range(1, m+1):
        expected_counter.append((-i, threshold(i, 1)))
        for j in range(2, i+1):
            expected_counter.append((-i, -threshold(i-1, j-1), threshold(i, j)))
        for j in range(1, i):
            expected_counter.append((-threshold(i-1, j), threshold(i, j)))
    formula_audits = {}
    for filename, bound, with_caps in [('unconstrained_lower.cnf', 3, False),
                                        ('cap_free_same_size.cnf', 4, True)]:
        lines = (path.parent/filename).read_text().splitlines()
        header = lines[0].split()
        assert header[:2] == ['p', 'cnf'] and int(header[2]) == threshold(m, m)
        clauses = [tuple(map(int, s.split()[:-1])) for s in lines[1:]]
        assert len(clauses) == int(header[3])
        fixed = Counter(expected_counter+[(-threshold(m, bound+1),)])
        seen_caps, positive_count = set(), 0
        for c in clauses:
            if fixed[c]:
                fixed[c] -= 1
            elif c and all(0 < x <= m for x in c):
                assert mask([x-1 for x in c]) in cups
                positive_count += 1
            else:
                assert with_caps and len(c) == 4 and all(-m <= x < 0 for x in c)
                capmask = mask([-x-1 for x in c])
                assert capmask in caps
                seen_caps.add(capmask)
        assert not any(fixed.values())
        assert seen_caps == (set(caps) if with_caps else set())
        formula_audits[filename] = dict(clauses=len(clauses),
                                       necessary_lower_clauses=positive_count,
                                       fourcap_clauses=len(seen_caps), bound=bound,
                                       counter_and_bound_exact=True)
    counts, safe_counts = [0]*(m+1), [0]*(m+1)
    first, first_safe = {}, {}
    minimum_covers = []
    for red in range(1 << m):
        if not all(red & c for c in cups):
            continue
        size = red.bit_count()
        counts[size] += 1
        first.setdefault(size, red)
        if not any(red & c == c for c in caps):
            safe_counts[size] += 1
            first_safe.setdefault(size, red)
    tau = next(k for k, c in enumerate(counts) if c)
    safe_tau = next(k for k, c in enumerate(safe_counts) if c)
    for red in range(1 << m):
        if red.bit_count() == tau and all(red & c for c in cups):
            minimum_covers.append([i for i in I if red >> i & 1])
    assert tau < safe_tau
    assert tau == source['minimum']
    bare = mask(source['bare'])
    assert bare.bit_count() == tau and all(bare & c for c in cups)
    safe = [i for i in I if first_safe[safe_tau] >> i & 1]
    # A small disjoint family, if one exists, is an elementary lower-bound proof.
    def packing(chosen, covered, offset):
        if len(chosen) == tau:
            return chosen
        for j in range(offset, len(cups)):
            if not cups[j] & covered:
                found = packing(chosen+[cups[j]], covered | cups[j], j+1)
                if found:
                    return found
        return None
    packed = packing([], 0, 0)
    result = dict(label='COMPUTED', independent_full_hull_enumeration=True,
                  m=m, n=n, cap4_count=len(caps), cap5_count=0,
                  gon_n_count=0, gon_n_minus_1_count=gon_count,
                  distinct_lower_parts=len(cups), tau=tau, cap_free_tau=safe_tau,
                  counts_by_size=counts, cap_free_counts_by_size=safe_counts,
                  all_minimum_transversals=minimum_covers,
                  cap_free_witness=safe,
                  disjoint_cups=None if packed is None else [[i for i in I if c >> i & 1] for c in packed],
                  formula_audits=formula_audits,
                  seconds=round(time.monotonic()-start, 6))
    (path.parent/'independent_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('counts_by_size', 'cap_free_counts_by_size', 'all_minimum_transversals')}))


if __name__ == '__main__':
    audit(Path('/home/jay/research/data/delta3-codex-20261113/coordinator/minimized/counterexample/witness.json'))
