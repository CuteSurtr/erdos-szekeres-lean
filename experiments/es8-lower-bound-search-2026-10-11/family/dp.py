#!/usr/bin/env python3
"""DP over the stacking bound recursion.

A stacking tree has leaves = single points and internal nodes Up(A,B) / Down(A,B).
Bound vector of a node: (n, p, q, c) = (size, cup bound, cap bound, convex bound).
  leaf:      (1, 1, 1, 1)
  Up(A,B):   p = max(pA+1, pB), q = max(qA, qB+1), c = max(cA, cB, pA+qB)
  Down(A,B): p = max(pA, pB+1), q = max(qA+1, qB), c = max(cA, cB, qA+pB)
  and, for n >= 2, c = min(c, p+q-2)  (a convex polygon = cup + cap sharing 2 ends).
All of these are valid upper bounds on the true values for any realization in
which B is placed to the right of A and the A-A-B / A-B-B triple signs are as
required (this is what stack() in scripts/es_lower_bound_witness.py enforces).

This script counts trees with n = 64 and c <= 7 and reports the state graph.
"""
import json, sys
from collections import defaultdict

NMAX, CMAX = 64, 7


def combine(sa, sb, d):
    na, pa, qa, ca = sa
    nb, pb, qb, cb = sb
    if d == 'U':
        p, q, c = max(pa + 1, pb), max(qa, qb + 1), max(ca, cb, pa + qb)
    else:
        p, q, c = max(pa, pb + 1), max(qa + 1, qb), max(ca, cb, qa + pb)
    c = min(c, p + q - 2)
    return (na + nb, p, q, c)


def build():
    count = defaultdict(int)          # state -> number of trees
    count[(1, 1, 1, 1)] = 1
    by_n = defaultdict(list)
    by_n[1].append((1, 1, 1, 1))
    for n in range(2, NMAX + 1):
        for na in range(1, n):
            nb = n - na
            for sa in by_n[na]:
                for sb in by_n[nb]:
                    for d in 'UD':
                        s = combine(sa, sb, d)
                        if s[3] > CMAX:
                            continue
                        if s not in count:
                            by_n[n].append(s)
                        count[s] += count[sa] * count[sb]
    return count, by_n


if __name__ == '__main__':
    count, by_n = build()
    tops = {s: v for s, v in count.items() if s[0] == NMAX}
    print('states per n (n: #states):', {n: len(by_n[n]) for n in (8, 16, 32, 48, 63, 64)})
    print('top states (n=64, c<=7):')
    for s, v in sorted(tops.items()):
        print('  ', s, 'trees =', v, f'(~2^{v.bit_length()-1})')
    # max n for each (p,q,c)
    best = {}
    for s in count:
        k = s[1:]
        best[k] = max(best.get(k, 0), s[0])
    print('max size by c bound:', {c: max(v for k, v in best.items() if k[2] == c) for c in range(1, CMAX + 1)})
