#!/usr/bin/env python3
"""CATALAN20261110: independent check of the cup/cap bounds and Proposition C (i)-(iii) for the explicit F-trees (odd m = 2h+1).
F-tree T(h, a, c): leaf if h == 1 or a == 1; else a MIN node of class c with L = T(h, a-1, c), R = T(h-1, min(a,h), c+1).
Angle of a node of class c at depth j of its same-class chain: c + 0.45*(j+1)/(J+1)  (in (c, c+0.45): never an integer
or half-integer, and < h + 1/2 for c = h).  Leaves in in-order (L before R) = x-order; direction t(p,q) of a pair
= angle of its lowest common node.  Then the longest cups (t increasing) / caps (t decreasing) are computed directly."""
import sys, bisect
from math import comb
from fractions import Fraction as Fr
sys.setrecursionlimit(100000)
def cat(n): return comb(2*n, n)//(n+1)
def build(h, a, c, j, J):
    if h == 1 or a == 1: return None
    return ('min', c, Fr(c) + Fr(45, 100) * Fr(j + 1, J + 1),
            build(h, a - 1, c, j + 1, J), build(h - 1, min(a, h), c + 1, 0, J))
def check(h):
    m = 2*h + 1; J = h + 2
    T = build(h, h + 1, 1, 0, J)
    leaves = []        # each leaf: list of (node angle, side) from root, to get LCA angle by common prefix
    def walk(t, path):
        if t is None: leaves.append(path); return
        walk(t[3], path + [(id(t), t[2], 'L')]); walk(t[4], path + [(id(t), t[2], 'R')])
    walk(T, [])
    n = len(leaves)
    # heap property: every min node's angle < all descendant angles
    def heap(t):
        if t is None: return []
        below = heap(t[3]) + heap(t[4])
        assert all(t[2] < x for x in below), 'heap violated'
        return below + [t[2]]
    heap(T)
    def lca(p, q):
        for (a, b) in zip(leaves[p], leaves[q]):
            if a[2] != b[2]: return a[1]
        raise AssertionError
    t = [[None]*n for _ in range(n)]
    for p in range(n):
        for q in range(p+1, n): t[p][q] = lca(p, q)
    # D[p][q]: longest cup with last edge (p,q); E[p][q]: longest cap with last edge (p,q)
    D = [[0]*n for _ in range(n)]; E = [[0]*n for _ in range(n)]
    for p in range(n):
        ins = sorted((t[o][p], D[o][p], E[o][p]) for o in range(p))
        ts = [x[0] for x in ins]
        pre = []; mx = 0
        for x in ins: mx = max(mx, x[1]); pre.append(mx)          # prefix max of D over increasing t
        suf = [0]*len(ins); mx = 0
        for i in range(len(ins)-1, -1, -1): mx = max(mx, ins[i][2]); suf[i] = mx   # suffix max of E
        for q in range(p+1, n):
            x = t[p][q]
            i = bisect.bisect_left(ts, x)            # o with t(o,p) < x
            D[p][q] = 1 + max(1, pre[i-1] if i > 0 else 0)
            i2 = bisect.bisect_right(ts, x)          # o with t(o,p) > x
            E[p][q] = 1 + max(1, suf[i2] if i2 < len(ins) else 0)
    def cup_below(e):   # longest cup with all t < e  (cup: last edge is the largest)
        return max([1] + [D[p][q] for p in range(n) for q in range(p+1, n) if t[p][q] < e])
    def cap_above(s, strict):   # longest cap with all t > s (or >= s)  (cap: last edge is the smallest)
        return max([1] + [E[p][q] for p in range(n) for q in range(p+1, n) if (t[p][q] > s if strict else t[p][q] >= s)])
    ok = n == cat(h+1) - cat(h)
    for e in range(2, h+2): ok &= cup_below(e) <= min(e, h)
    for s in range(1, h+1): ok &= cap_above(s, False) <= h + 2 - s
    for x in range(1, m):                                         # Prop C (i)
        ok &= cup_below(x) + cap_above(m - x, True) <= x + 1
    half = Fr(m, 2)
    ok &= cup_below(half) + cap_above(half, True) <= h + 1        # sufficient condition for (ii)
    # (iii): a convex polygon with >= 3 vertices is a cup plus a cap sharing 2 end points; at most 2 points otherwise
    mc_bound = max(min(n, 2), cup_below(m) + cap_above(0, True) - 2)
    ok &= mc_bound <= m
    print(f'h={h} m={m} n={n} (Cat(h+1)-Cat(h)={cat(h+1)-cat(h)}) max cup={cup_below(m)} max cap={cap_above(0, True)} '
          f'g={[cup_below(x) for x in range(1, m)]} hh={[cap_above(m-x, True) for x in range(1, m)]} mc<= {mc_bound}  ->', 'OK' if ok else 'FAIL')
    return ok
H = int(sys.argv[1]) if len(sys.argv) > 1 else 6
res = [check(h) for h in range(1, H+1)]
print('ALL OK' if all(res) else 'SOME FAIL'); sys.exit(0 if all(res) else 1)
