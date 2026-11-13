#!/usr/bin/env python3
"""Check of the strict radial-needle limit for 3-fold sets (Proposition N of the record).

Arm orbit j: p_j = r_j * 1 + eps * r_j e_j * omega (oblique Z[omega] coordinates), r_j = L / u_j; the three rotated
copies form three needles.  Claim: the configuration (3n points) has no convex octagon iff the planar set
A = {(u_j, e_j)} satisfies cup(A) + cap(A) <= 7 (cup/cap w.r.t. the u-order).  Tested exactly on random A and on an
Erdos-Szekeres extremal A with cup <= 3, cap <= 4 (|A| = 10).
"""
import sys, os, random, math
from functools import reduce
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval, rot


def cupcap(A):
    A = sorted(A)
    n = len(A)
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    cup = [[2] * n for _ in range(n)]; cap = [[2] * n for _ in range(n)]
    best_cup = min(n, 1); best_cap = min(n, 1)
    if n >= 2:
        best_cup = best_cap = 2
    for j in range(n):
        for i in range(j):
            for k in range(j + 1, n):
                c = cr(A[i], A[j], A[k])
                if c > 0 and cup[i][j] + 1 > cup[j][k]:
                    cup[j][k] = cup[i][j] + 1
                if c < 0 and cap[i][j] + 1 > cap[j][k]:
                    cap[j][k] = cap[i][j] + 1
    for i in range(n):
        for j in range(i + 1, n):
            best_cup = max(best_cup, cup[i][j]); best_cap = max(best_cap, cap[i][j])
    return best_cup, best_cap


def arm_config(A):
    """A = planar set B = {(r_j, y_j)} (r_j > 0 distinct): arm point j = r_j + eps * y_j * omega.  Its (u, e) picture
    {(1/r_j, y_j/r_j)} has the same cup and cap numbers as B (projective map (x, y) -> (1/x, y/x) reverses both the
    x-order and the orientation)."""
    pts = []
    for (r, y) in A:
        rep = [(0, r, 0), (1, 0, y)]
        cur = rep
        for _ in range(3):
            pts.append(cur)
            cur = [(ee,) + rot(3, (x, y)) for (ee, x, y) in cur]
    return pts


def es_set(k, l):
    """planar set with no k-cup and no l-cap, size C(k+l-4, k-2) (Erdos-Szekeres recursion): Rgt is placed to the
    right of Lft and so high that every L-R connecting slope exceeds every internal slope; then a cup has at most one
    point in Rgt and a cap at most one point in Lft."""
    if k <= 2 or l <= 2:
        return [(0, 0)]
    Lft = es_set(k - 1, l)
    Rgt = es_set(k, l - 1)
    pts = Lft + Rgt
    W = 1 + max(max(abs(x), abs(y)) for x, y in pts)
    def maxslope(P):
        s = 0
        for i in range(len(P)):
            for j in range(len(P)):
                if P[i][0] != P[j][0]:
                    s = max(s, abs(P[i][1] - P[j][1]) / abs(P[i][0] - P[j][0]))
        return s
    S = max(maxslope(Lft), maxslope(Rgt), 1)
    dx = 4 * W
    dy = int(S * (dx + 4 * W) + 8 * W) + 1
    return Lft + [(x + dx, y + dy) for (x, y) in Rgt]


def check(A):
    cu, ca = cupcap(A)
    ml, cnt, nz = peval(arm_config(A), 8)
    return cu, ca, cnt[8], nz


if __name__ == '__main__':
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    E = es_set(4, 5)
    E = [(x + 1, y) for (x, y) in E]  # r > 0
    E = sorted(E)
    print('ES set size', len(E), 'cup/cap', cupcap(E))
    print('ES arm: cup, cap, n8, zero =', check(E))
    agree = 0; tot = 0; bad = []
    for trial in range(300):
        n = random.randint(5, 11)
        us = random.sample(range(1, 60), n)
        A = [(u, random.randint(-60, 60)) for u in us]
        cu, ca, n8, nz = check(A)
        if nz:
            continue
        tot += 1
        pred = (cu + ca <= 7)
        if pred == (n8 == 0):
            agree += 1
        else:
            bad.append((A, cu, ca, n8))
    print('random tests: %d/%d agree with "octagon-free iff cup + cap <= 7"' % (agree, tot))
    for b in bad[:5]:
        print('  MISMATCH', b)
    # every 11-point extension of the ES set has an octagon (sample)
    hits = 0
    for trial in range(50):
        u = random.randint(1, 2 * max(x for x, y in E))
        if u in [x for x, y in E]:
            continue
        A = sorted(E + [(u, random.randint(-10 ** 6, 10 ** 6))])
        cu, ca, n8, nz = check(A)
        hits += (n8 > 0)
    print('11-point extensions of the ES set with an octagon: %d (of those tested)' % hits)
