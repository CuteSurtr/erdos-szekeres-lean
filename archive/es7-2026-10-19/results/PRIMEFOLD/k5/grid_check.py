#!/usr/bin/env python3
"""Exhaustive exact integer grid over T (sanity layer on top of the symbolic proof in verify_k5.py), plus exact
polynomial identities behind the hand proofs of the sign / topology steps.

Grid: scale N; A = (+-N,0),(0,+-N); b = (i, j) with i, j >= 0, i + j < N (this includes the axis points).
For each grid point: full chirotope (56 sorted triples, integer arithmetic).  Prediction:
  on axis (i == 0 or j == 0)  -> some zero triple
  C1 = i^2+j^2-iN+jN == 0 or C2 = i^2+j^2+iN-jN == 0 -> exactly 4 zero triples
  else region by signs of C1, C2 -> chirotope equals that region's reference chirotope.
"""
from itertools import combinations
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
TR = list(combinations(range(8), 3))

def pts(i, j):
    A = [(N, 0), (0, N), (-N, 0), (0, -N)]
    B = [(i, j)]
    for _ in range(3):
        B.append((-B[-1][1], B[-1][0]))
    return A + B

def chi(P):
    out = []
    for a, b, c in TR:
        d = (P[b][0] - P[a][0]) * (P[c][1] - P[a][1]) - (P[b][1] - P[a][1]) * (P[c][0] - P[a][0])
        out.append((d > 0) - (d < 0))
    return tuple(out)

def reg(i, j):
    c1 = i * i + j * j - i * N + j * N
    c2 = i * i + j * j + i * N - j * N
    if i == 0 or j == 0:
        return 'axis'
    if c1 == 0 or c2 == 0:
        return 'curve'
    return 'I_a' if c1 < 0 else ('I_b' if c2 < 0 else 'II')

# references at scale N from the same points used in verify_k5.py (scaled): (3/10,1/10), (1/10,3/10), (3/10,3/10)
assert N % 10 == 0
REF = {'I_a': chi(pts(3 * N // 10, N // 10)), 'I_b': chi(pts(N // 10, 3 * N // 10)), 'II': chi(pts(3 * N // 10, 3 * N // 10))}
cnt = {}
for i in range(0, N):
    for j in range(0, N - i):
        if i == 0 and j == 0:
            continue
        r = reg(i, j)
        c = chi(pts(i, j))
        z = c.count(0)
        if r == 'axis':
            assert z > 0, (i, j)
        elif r == 'curve':
            assert z == 4, (i, j, z)
        else:
            assert z == 0 and c == REF[r], (i, j, r)
        cnt[r] = cnt.get(r, 0) + 1
print('grid N=%d: all %d points agree with prediction; per class: %s' % (N, sum(cnt.values()), cnt))

# ---- exact polynomial identities (polynomials as dicts {(a,b): coeff}) behind the hand proofs
def mul(P, Q):
    R = {}
    for (a, b), u in P.items():
        for (c, d), v in Q.items():
            R[(a + c, b + d)] = R.get((a + c, b + d), 0) + u * v
    return {k: v for k, v in R.items() if v}
def add(*Ps):
    R = {}
    for P in Ps:
        for k, v in P.items():
            R[k] = R.get(k, 0) + v
    return {k: v for k, v in R.items() if v}
def sc(c, P):
    return {k: c * v for k, v in P.items() if c * v}
x = {(1, 0): 1}; y = {(0, 1): 1}; one = {(0, 0): 1}
s = add(x, y)
C1 = add(mul(x, x), mul(y, y), sc(-1, x), y)
C2 = add(mul(x, x), mul(y, y), x, sc(-1, y))
C3 = add(mul(x, x), mul(y, y), sc(-1, x), sc(-1, y))
# C3 = (x+y)(x+y-1) - 2xy  -> < 0 on T since 0 < x+y < 1 and xy > 0
assert C3 == add(mul(s, add(s, sc(-1, one))), sc(-2, mul(x, y)))
# C1 - C2 = 2(y - x)
assert add(C1, sc(-1, C2)) == add(sc(2, y), sc(-2, x))
# C1 = (x - 1/2)^2 + (y + 1/2)^2 - 1/2, checked as 4*C1 = (2x-1)^2 + (2y+1)^2 - 2
assert sc(4, C1) == add(mul(add(sc(2, x), sc(-1, one)), add(sc(2, x), sc(-1, one))),
                        mul(add(sc(2, y), one), add(sc(2, y), one)), sc(-2, one))
# restriction of C1 to the line x + y = c (substitute y = c - x): 2x^2 - (2c+2)x + c^2 + c ; values at x=0, x=c, x=c/2
def C1v(X, Y):
    return X * X + Y * Y - X + Y
from fractions import Fraction as F
for c in (F(1, 7), F(1, 2), F(9, 10), F(999, 1000)):
    assert C1v(0, c) == c * c + c > 0 and C1v(c, 0) == c * c - c < 0 and C1v(c / 2, c / 2) == c * c / 2 > 0
print('identities: C3 = (x+y)(x+y-1) - 2xy;  C1 - C2 = 2(y-x);  4*C1 = (2x-1)^2 + (2y+1)^2 - 2;  line-restriction values: OK')
