#!/usr/bin/env python3
"""k = 5, m = 4: two nested squares (8 points, no centre).  Exact decision of: is there a 4-fold symmetric 8-point set
in general position with no 5 points in convex position?

Normalisation.  Outer square A = {1, i, -1, -i} (circumradius 1, phase 0).  Inner square B = {b, ib, -b, -ib} with
b = x + iy.  The set S(b) = A u B depends only on b modulo multiplication by i, so b may be taken in the closed first
quadrant; b on an axis puts b, -b, 1, -1 (or i, -i) on one line, so x > 0, y > 0.  B strictly inside conv(A) means
x + y < 1.  (Layer lemma, K = 5 <= 2m = 8: a 4-fold set with no convex pentagon is two nested squares; if B is not
inside conv(A) then either A is inside conv(B) -- swap names -- or all 8 points are hull vertices.)
So the parameter domain is the open triangle T = {x > 0, y > 0, x + y < 1}.

Part 1 (symbolic, exact).  Every orientation det(p, q, r), p, q, r in S(b), is a polynomial of degree <= 2 in (x, y)
with integer coefficients.  We compute all 56 of them and prove that inside T each one either has constant sign or
vanishes exactly on C1 = {x^2 + y^2 = x - y} or C2 = {x^2 + y^2 = y - x}.  Hence the order type of S(b) is constant
on each connected component of T minus (C1 u C2); there are exactly three components (C1 n T and C2 n T are arcs
from the corner (0,0) to (1,0), resp. (0,1)):
   I_a = {x^2 + y^2 < x - y},  I_b = {x^2 + y^2 < y - x} (mirror image of I_a under x <-> y),  II = the rest.
Part 2 (exact brute force).  For a rational representative of each component, list all 5-subsets in convex position
(exact rational orientation signs).  Also: points of C1, C2 themselves are not in general position.
Part 3 (sanity check only, not part of the proof).  Random exact rational samples of T: order type and pentagon
count agree with the component prediction.
"""
from fractions import Fraction as Fr
from itertools import combinations
import random, sys

# ---------- polynomials in x, y: dict {(i, j): int} ----------
def padd(P, Q, s=1):
    R = dict(P)
    for k, v in Q.items():
        R[k] = R.get(k, 0) + s * v
    return {k: v for k, v in R.items() if v}

def pmul(P, Q):
    R = {}
    for (a, b), u in P.items():
        for (c, d), v in Q.items():
            R[(a + c, b + d)] = R.get((a + c, b + d), 0) + u * v
    return {k: v for k, v in R.items() if v}

def const(c):
    return {(0, 0): c} if c else {}

X = {(1, 0): 1}
Y = {(0, 1): 1}
NEG = lambda P: {k: -v for k, v in P.items()}

# points as (xpoly, ypoly)
A = [(const(1), const(0)), (const(0), const(1)), (const(-1), const(0)), (const(0), const(-1))]
B = [(X, Y), (NEG(Y), X), (NEG(X), NEG(Y)), (Y, NEG(X))]      # b, ib, -b, -ib
PTS = A + B
NAMES = ['a0', 'a1', 'a2', 'a3', 'b0', 'b1', 'b2', 'b3']

def det_poly(p, q, r):
    # (q - p) x (r - p)
    qx, qy = padd(q[0], p[0], -1), padd(q[1], p[1], -1)
    rx, ry = padd(r[0], p[0], -1), padd(r[1], p[1], -1)
    return padd(pmul(qx, ry), pmul(qy, rx), -1)

def peval(P, x, y):
    return sum(v * x ** a * y ** b for (a, b), v in P.items())

C1 = {(2, 0): 1, (0, 2): 1, (1, 0): -1, (0, 1): 1}     # x^2 + y^2 - x + y
C2 = {(2, 0): 1, (0, 2): 1, (1, 0): 1, (0, 1): -1}     # x^2 + y^2 + x - y
C3 = {(2, 0): 1, (0, 2): 1, (1, 0): -1, (0, 1): -1}    # x^2 + y^2 - x - y  (< 0 on T: no zero in T)
C4 = {(2, 0): 1, (0, 2): 1, (1, 0): 1, (0, 1): 1}      # x^2 + y^2 + x + y  (> 0 on T)
C5 = {(2, 0): 1, (0, 2): 1}                             # x^2 + y^2  (> 0 for b != 0: three inner points)

def proportional(P, Q):
    """P = c Q for a nonzero rational c? return c or None"""
    if set(P) != set(Q):
        return None
    k0 = next(iter(Q))
    c = Fr(P[k0], Q[k0])
    return c if all(Fr(P[k], Q[k]) == c for k in Q) else None

def classify(P):
    """returns a description of the zero set of P inside T, raising if it is not one of the proven cases"""
    if not P:
        raise ValueError('identically zero determinant')
    deg = max(a + b for a, b in P)
    if deg == 0:
        return 'const', None
    if deg == 1:
        # linear: constant sign on open T iff its values at the closed-triangle corners are all >= 0 or all <= 0
        vals = [peval(P, *v) for v in ((0, 0), (1, 0), (0, 1))]
        if all(v >= 0 for v in vals) or all(v <= 0 for v in vals):
            # and it is not identically zero on T (deg 1), so it is nonzero on the open triangle
            return 'lin-const', vals
        raise ValueError('a line crosses T: %r' % P)
    for name, Q in (('C1', C1), ('C2', C2), ('C3', C3), ('C4', C4), ('C5', C5)):
        c = proportional(P, Q)
        if c is not None:
            return name, c
    raise ValueError('unclassified quadratic %r' % P)

# Proofs that C3 and C4 have no zero in T (written out, checked here only numerically as a reminder):
#  C4 = x^2+y^2+x+y > 0 for x, y > 0.   C3: x^2 + y^2 <= (x+y)^2 < x+y for 0 < x+y < 1, so C3 < 0 on T.
#  C1 n T, C2 n T are curves (arcs), on which the configuration is degenerate (zero orientation).


def orient_exact(P, x, y):
    s = peval(P, x, y)
    return (s > 0) - (s < 0)

def convex_position(idx, O):
    # a set is in convex position iff no point lies inside a triangle of three others
    for t in combinations(idx, 4):
        for d in t:
            a, b, c = [e for e in t if e != d]
            o1, o2, o3 = O[(a, b, d)], O[(b, c, d)], O[(c, a, d)]
            if o1 == o2 == o3:
                return False
    return True

def orient_table(x, y):
    O = {}
    for a in range(8):
        for b in range(8):
            for c in range(8):
                if len({a, b, c}) == 3:
                    O[(a, b, c)] = orient_exact(DET[(a, b, c)], x, y)
    return O

def pentagons(x, y):
    O = orient_table(x, y)
    zero = sum(1 for v in O.values() if v == 0)
    pent = [s for s in combinations(range(8), 5) if convex_position(s, O)] if zero == 0 else None
    return O, zero, pent

def region(x, y):
    c1, c2 = peval(C1, x, y), peval(C2, x, y)
    if c1 == 0 or c2 == 0:
        return 'curve'
    if c1 < 0:
        return 'I_a'
    if c2 < 0:
        return 'I_b'
    return 'II'


DET = {}
for a in range(8):
    for b in range(8):
        for c in range(8):
            if len({a, b, c}) == 3:
                DET[(a, b, c)] = det_poly(PTS[a], PTS[b], PTS[c])

def main():
    out = []
    pr = lambda *s: (print(*s), out.append(' '.join(map(str, s))))
    pr('# Part 1: the 56 orientation determinants (sorted triples) as polynomials in b = x + iy')
    kinds = {}
    for t in combinations(range(8), 3):
        P = DET[t]
        k, info = classify(P)
        kinds.setdefault(k, []).append(t)
        pr('  ', ' '.join(NAMES[i] for i in t), ':', k, info if k != 'const' else P.get((0, 0)))
    pr('# summary:', {k: len(v) for k, v in kinds.items()})
    assert set(kinds) <= {'const', 'lin-const', 'C1', 'C2', 'C3', 'C4', 'C5'}
    # C1 and C2 really meet T (so they are genuine walls): points (1/2 - ..., ...) on C1 inside T
    # C1: (x - 1/2)^2 + (y + 1/2)^2 = 1/2 ; the point (1/2, (sqrt2-1)/2) lies on it; use the rational point
    # (x, y) = (1/5, 2/... ) check: we just exhibit rational points of C1 n T: x = 2/5, y = ? -> solve y^2 + y + (x^2 - x) = 0
    pr('# rational points on C1 inside T (zero orientation there => not general position):')
    for (x, y) in ((Fr(1, 2), Fr(1, 2) * 0 + Fr(0)),):
        pass
    # parametrise C1 through the origin: line y = s x meets C1 again at x = (1 - s)/(1 + s^2), y = s x
    for s in (Fr(1, 3), Fr(1, 2), Fr(1, 5)):
        x = (1 - s) / (1 + s * s); y = s * x
        assert peval(C1, x, y) == 0 and x > 0 and y > 0 and x + y < 1
        O, zero, pent = pentagons(x, y)
        pr('   s=%s: b=(%s, %s), zero orientations: %d' % (s, x, y, zero))
        assert zero > 0
    pr('# Part 2: representatives of the three components')
    reps = {'I_a': (Fr(3, 10), Fr(1, 10)), 'I_b': (Fr(1, 10), Fr(3, 10)), 'II': (Fr(3, 10), Fr(3, 10))}
    res = {}
    for name, (x, y) in reps.items():
        assert region(x, y) == name
        O, zero, pent = pentagons(x, y)
        res[name] = (zero, pent)
        pr('  %s: b = (%s, %s): zero orientations %d, convex 5-subsets: %d %s' % (
            name, x, y, zero, len(pent), [' '.join(NAMES[i] for i in s) for s in pent]))
    assert res['I_a'][0] == 0 and res['I_a'][1] == [] and res['I_b'][1] == [] and len(res['II'][1]) > 0
    # integer version of the I_a representative (scale 10): A = {+-10, +-10i}, B = {3+i, -1+3i, -3-i, 1-3i}
    pr('# integer realisation (scale 10): A = (10,0),(0,10),(-10,0),(0,-10); B = (3,1),(-1,3),(-3,-1),(1,-3)')
    P = [(10, 0), (0, 10), (-10, 0), (0, -10), (3, 1), (-1, 3), (-3, -1), (1, -3)]
    def o(p, q, r):
        d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (d > 0) - (d < 0)
    O = {(a, b, c): o(P[a], P[b], P[c]) for a in range(8) for b in range(8) for c in range(8) if len({a, b, c}) == 3}
    zero = sum(1 for v in O.values() if v == 0)
    pent = [s for s in combinations(range(8), 5) if convex_position(s, O)]
    # largest convex subset by brute force over all subsets
    best = max(len(s) for r in range(3, 9) for s in combinations(range(8), r) if convex_position(s, O))
    pr('   zero orientations %d, convex 5-subsets %d, largest convex subset %d' % (zero, len(pent), best))
    assert zero == 0 and not pent and best == 4
    # same order type as the rational representative of I_a (the integer set is S(b) scaled by 10 with b = (3+i)/10)
    O2, _, _ = pentagons(Fr(3, 10), Fr(1, 10))
    assert all(O[k] == O2[k] for k in O)
    pr('   order type identical to the I_a representative: True')
    # Part 3: random exact sampling (sanity check only)
    random.seed(12345)
    cnt = {'I_a': [0, 0], 'I_b': [0, 0], 'II': [0, 0], 'curve': [0, 0]}
    ref = {name: pentagons(*reps[name])[0] for name in reps}
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    for _ in range(N):
        D = random.choice((50, 1000, 10 ** 6))
        x = Fr(random.randint(1, D - 1), D); y = Fr(random.randint(1, D - 1), D)
        if x + y >= 1:
            continue
        rg = region(x, y)
        O, zero, pent = pentagons(x, y)
        cnt[rg][0] += 1
        if rg != 'curve':
            assert zero == 0
            assert all(O[k] == ref[rg][k] for k in O), (x, y, rg)
            cnt[rg][1] += (len(pent) == 0)
    pr('# Part 3 (sanity): random rational samples per component [samples, pentagon-free]:', cnt)
    assert cnt['I_a'][0] == cnt['I_a'][1] and cnt['I_b'][0] == cnt['I_b'][1] and cnt['II'][1] == 0
    pr('RESULT: component I (x^2+y^2 < |x-y|, i.e. rho < |cos(phi) - sin(phi)|) is pentagon-free; component II and '
       'the curves are not.')
    with open(__file__.replace('.py', '.out'), 'w') as f:
        f.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
