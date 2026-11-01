#!/usr/bin/env python3
"""Independent re-verification of claim K5-classification (written from scratch; shares no code with k5_exact.py).

Setting: A = {1, i, -1, -i}; B = {b, ib, -b, -ib}, b = x + iy, x > 0, y > 0, x + y < 1 (B strictly inside conv A).
T = open triangle {x > 0, y > 0, x + y < 1}.

All arithmetic is exact (int / Fraction).  Steps:
  1. Every orientation det(p,q,r), p,q,r in S(b), as a polynomial of degree <= 2 in (x,y), computed two ways:
       (M1) symbolic product of affine forms;  (M2) exact interpolation on the unisolvent grid
       {(0,0),(1,0),(2,0),(0,1),(1,1),(0,2)} from numerically evaluated (exact rational) determinants,
     then cross-checked at 50 random rational points.
  2. Sign of each polynomial on the OPEN triangle T, decided by exact min/max over the closed triangle
     (corners, edge vertices of parabolas, interior critical point) plus an interior-zero test.
  3. Representatives of each region (several per region, including far corners of each region):
     chirotope (all 56 triples), convex 5-subsets via (a) Andrew monotone-chain hull and (b) a 4-point
     segment-crossing criterion; largest convex subset.
  4. Degenerate loci: rational points on C1, C2 and on the axis.
  5. Mirror relation I_a <-> I_b, order-type isomorphism classes (brute force over relabelings).
  6. "beyond two edge-lines" reformulation.
  7. Context: the configurations outside the strictly-nested family (convex octagon), the integer example,
     centre never admissible for even m, and a random 3-square sanity check (ES(5) = 9 says never pentagon-free).
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import random, sys

# ------------------------------------------------------------------ points as affine forms in (x, y)
# an affine form is a tuple (c0, cx, cy) meaning c0 + cx*x + cy*y; a point is (Xform, Yform)
Z0 = (0, 0, 0)
def af(c0=0, cx=0, cy=0):
    return (c0, cx, cy)
# rotation by i: (X, Y) -> (-Y, X)
def rot(P):
    X, Y = P
    return (tuple(-c for c in Y), X)

a0 = (af(1), af(0)); a1 = rot(a0); a2 = rot(a1); a3 = rot(a2)
b0 = (af(0, 1, 0), af(0, 0, 1)); b1 = rot(b0); b2 = rot(b1); b3 = rot(b2)
PTS = [a0, a1, a2, a3, b0, b1, b2, b3]
NAMES = ['a0', 'a1', 'a2', 'a3', 'b0', 'b1', 'b2', 'b3']
assert rot(a3) == a0 and rot(b3) == b0

# ------------------------------------------------------------------ M1: symbolic
MONO = ['1', 'x', 'y', 'xx', 'xy', 'yy']
def af_sub(u, v):
    return tuple(p - q for p, q in zip(u, v))
def af_mul(u, v):
    # (u0 + ux x + uy y)(v0 + vx x + vy y)
    r = dict.fromkeys(MONO, 0)
    r['1'] += u[0] * v[0]
    r['x'] += u[0] * v[1] + u[1] * v[0]
    r['y'] += u[0] * v[2] + u[2] * v[0]
    r['xx'] += u[1] * v[1]
    r['xy'] += u[1] * v[2] + u[2] * v[1]
    r['yy'] += u[2] * v[2]
    return r
def q_sub(r, s):
    return {k: r[k] - s[k] for k in MONO}
def det_sym(p, q, r):
    ux, uy = af_sub(q[0], p[0]), af_sub(q[1], p[1])
    vx, vy = af_sub(r[0], p[0]), af_sub(r[1], p[1])
    return q_sub(af_mul(ux, vy), af_mul(uy, vx))

# ------------------------------------------------------------------ numeric (exact) points for given b
def points_at(x, y):
    """exact coordinates of S(b) for b = x + iy, built by complex multiplication by i (independent of affine forms)"""
    P = [(F(1), F(0))]
    for _ in range(3):
        P.append((-P[-1][1], P[-1][0]))
    Q = [(F(x), F(y))]
    for _ in range(3):
        Q.append((-Q[-1][1], Q[-1][0]))
    return P + Q

def det_num(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def sgn(v):
    return (v > 0) - (v < 0)

# ------------------------------------------------------------------ M2: interpolation
GRID = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)]
def det_interp(i, j, k):
    v = {}
    for (gx, gy) in GRID:
        P = points_at(gx, gy)
        v[(gx, gy)] = det_num(P[i], P[j], P[k])
    c1 = v[(0, 0)]
    cxx = (v[(2, 0)] - 2 * v[(1, 0)] + v[(0, 0)]) / 2
    cx = v[(1, 0)] - c1 - cxx
    cyy = (v[(0, 2)] - 2 * v[(0, 1)] + v[(0, 0)]) / 2
    cy = v[(0, 1)] - c1 - cyy
    cxy = v[(1, 1)] - c1 - cx - cy - cxx - cyy
    return {'1': c1, 'x': cx, 'y': cy, 'xx': cxx, 'xy': cxy, 'yy': cyy}

def peval(P, x, y):
    return P['1'] + P['x'] * x + P['y'] * y + P['xx'] * x * x + P['xy'] * x * y + P['yy'] * y * y

def pstr(P):
    terms = []
    for k in MONO:
        c = P[k]
        if c:
            terms.append('%+d%s' % (c, '' if k == '1' else '*' + '*'.join(k)) if c not in (1, -1) or k == '1'
                         else ('+' if c > 0 else '-') + '*'.join(k))
    return ''.join(terms) if terms else '0'

# ------------------------------------------------------------------ exact sign analysis on the open triangle T
CORNERS = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
EDGES = [(CORNERS[0], CORNERS[1]), (CORNERS[1], CORNERS[2]), (CORNERS[2], CORNERS[0])]

def in_open_T(x, y):
    return x > 0 and y > 0 and x + y < 1

def extremes_closed_T(P):
    """exact min and max of the degree-<=2 polynomial P over the closed triangle, with candidate list"""
    cands = list(CORNERS)
    for (p, q) in EDGES:
        # g(t) = P(p + t (q - p)), quadratic in t; vertex t* = -B / (2A)
        dx, dy = q[0] - p[0], q[1] - p[1]
        g0 = peval(P, p[0], p[1]); g1 = peval(P, p[0] + dx, p[1] + dy); gh = peval(P, p[0] + dx / 2, p[1] + dy / 2)
        # g(t) = A t^2 + B t + C with C = g0, A + B + C = g1, A/4 + B/2 + C = gh
        C = g0; A = 2 * g1 - 4 * gh + 2 * g0; Bc = g1 - A - C
        if A != 0:
            t = -Bc / (2 * A)
            if 0 < t < 1:
                cands.append((p[0] + t * dx, p[1] + t * dy))
    # interior critical point: grad = 0:  [2cxx  cxy; cxy 2cyy] (x,y) = (-cx, -cy)
    a, b, c = 2 * F(P['xx']), F(P['xy']), 2 * F(P['yy'])
    D = a * c - b * b
    interior_zero_possible = False
    if D != 0:
        x = (-F(P['x']) * c + b * F(P['y'])) / D
        y = (-a * F(P['y']) + b * F(P['x'])) / D
        if in_open_T(x, y):
            cands.append((x, y))
    else:
        # singular Hessian: critical set is empty or a line; extremes over a compact convex set are then attained
        # on the boundary (P is constant along the critical line, which exits the triangle), so boundary candidates
        # suffice for the min/max values; but an interior zero at an extremum is possible -> flag it
        if any(P[k] for k in ('xx', 'xy', 'yy')):
            interior_zero_possible = True
    vals = [(peval(P, *pt), pt) for pt in cands]
    return min(v for v, _ in vals), max(v for v, _ in vals), vals, interior_zero_possible

def sign_on_open_T(P):
    """returns +1 / -1 if P has that strict sign on all of open T, 0 if P vanishes somewhere in open T"""
    mn, mx, vals, flag = extremes_closed_T(P)
    if mn > 0:
        return +1
    if mx < 0:
        return -1
    if mn < 0 < mx:
        return 0                     # changes sign on the closed triangle => a zero in the open (connected) T
    if mn == 0 and mx == 0:
        return 0                     # identically zero
    # one-sided with value 0 attained somewhere on the closed triangle: a zero in OPEN T would be an interior
    # local extremum, i.e. an interior critical point with value 0
    if flag:
        raise RuntimeError('singular-Hessian one-sided case needs manual treatment: %s' % pstr(P))
    for v, pt in vals:
        if v == 0 and in_open_T(*pt):
            return 0
    return +1 if mn == 0 else -1

C1 = {'1': 0, 'x': -1, 'y': 1, 'xx': 1, 'xy': 0, 'yy': 1}   # x^2+y^2-x+y
C2 = {'1': 0, 'x': 1, 'y': -1, 'xx': 1, 'xy': 0, 'yy': 1}   # x^2+y^2+x-y

def ratio(P, Q):
    """c with P = c*Q (c != 0) or None"""
    c = None
    for k in MONO:
        if Q[k] == 0:
            if P[k] != 0:
                return None
        else:
            r = F(P[k], Q[k]) if isinstance(P[k], int) and isinstance(Q[k], int) else F(P[k]) / F(Q[k])
            if c is None:
                c = r
            elif r != c:
                return None
    return c if c else None

# ------------------------------------------------------------------ convex position tests (exact)
def hull_size(pts):
    """number of strict hull vertices (Andrew monotone chain, collinear points dropped)"""
    P = sorted(set(pts))
    if len(P) <= 2:
        return len(P)
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2

def segs_cross(p, q, r, s):
    d1 = sgn(det_num(p, q, r)); d2 = sgn(det_num(p, q, s)); d3 = sgn(det_num(r, s, p)); d4 = sgn(det_num(r, s, q))
    return d1 * d2 < 0 and d3 * d4 < 0

def convex4_cross(p, q, r, s):
    # 4 points in GP are in convex position iff one of the three pairings gives properly crossing segments
    return segs_cross(p, q, r, s) or segs_cross(p, r, q, s) or segs_cross(p, s, q, r)

def convex_by_4(pts):
    return all(convex4_cross(*c) for c in combinations(pts, 4))

def chirotope(P):
    return tuple(sgn(det_num(P[i], P[j], P[k])) for (i, j, k) in combinations(range(len(P)), 3))

def analyse(x, y, full=True):
    P = points_at(x, y)
    chi = chirotope(P)
    zeros = sum(1 for s in chi if s == 0)
    res = {'chi': chi, 'zeros': zeros}
    if zeros == 0:
        pent_h = [s for s in combinations(range(8), 5) if hull_size([P[i] for i in s]) == 5]
        pent_4 = [s for s in combinations(range(8), 5) if convex_by_4([P[i] for i in s])]
        assert pent_h == pent_4, (x, y)
        res['pent'] = pent_h
        if full:
            best = 0
            for r in range(8, 2, -1):
                if any(hull_size([P[i] for i in s]) == r for s in combinations(range(8), r)):
                    best = r
                    break
            res['maxconvex'] = best
    return res

def region(x, y):
    c1, c2 = peval(C1, x, y), peval(C2, x, y)
    if c1 == 0 or c2 == 0:
        return 'curve'
    return 'I_a' if c1 < 0 else ('I_b' if c2 < 0 else 'II')

# ------------------------------------------------------------------ order-type isomorphism (brute force)
TRIPLES = list(combinations(range(8), 3))
def chi_fun(chi):
    d = {}
    for t, s in zip(TRIPLES, chi):
        i, j, k = t
        for (p, q, r), sg in (((i, j, k), 1), ((j, k, i), 1), ((k, i, j), 1), ((j, i, k), -1), ((i, k, j), -1), ((k, j, i), -1)):
            d[(p, q, r)] = s * sg
    return d

def isomorphic(chiA, chiB, mirror=False):
    dA, dB = chi_fun(chiA), chi_fun(chiB)
    m = -1 if mirror else 1
    for pi in permutations(range(8)):
        if all(dA[(pi[i], pi[j], pi[k])] == m * dB[(i, j, k)] for (i, j, k) in TRIPLES):
            return pi
    return None

# ------------------------------------------------------------------ main
def main():
    log = []
    def pr(*a):
        s = ' '.join(str(t) for t in a)
        print(s); log.append(s)

    pr('== Step 1: 56 determinants, two independent derivations ==')
    rng = random.Random(20261102)
    DET = {}
    for t in TRIPLES:
        Ps = det_sym(*[PTS[i] for i in t])
        Pi = det_interp(*t)
        assert all(F(Ps[k]) == Pi[k] for k in MONO), (t, Ps, Pi)
        for _ in range(50):
            x = F(rng.randint(-10**6, 10**6), rng.randint(1, 10**6)); y = F(rng.randint(-10**6, 10**6), rng.randint(1, 10**6))
            P = points_at(x, y)
            assert peval(Ps, x, y) == det_num(P[t[0]], P[t[1]], P[t[2]])
        DET[t] = Ps
    pr('M1 (symbolic) == M2 (interpolation) for all 56 triples; both agree with direct evaluation at 50 random rational points each')

    pr('== Step 2: sign of each determinant on the open triangle T ==')
    kinds = {}
    for t in TRIPLES:
        P = DET[t]
        deg = max([0] + [{'1': 0, 'x': 1, 'y': 1, 'xx': 2, 'xy': 2, 'yy': 2}[k] for k in MONO if P[k]])
        s = sign_on_open_T(P)
        if s != 0:
            kind = 'const' if deg == 0 else ('linear-definite' if deg == 1 else 'quadratic-definite')
            info = 'sign %+d' % s
        else:
            r1, r2 = ratio(P, C1), ratio(P, C2)
            if r1 is not None:
                kind, info = 'C1-multiple', 'factor %s' % r1
            elif r2 is not None:
                kind, info = 'C2-multiple', 'factor %s' % r2
            else:
                kind, info = 'UNEXPECTED', ''
        kinds.setdefault(kind, []).append(t)
        pr('  %s %s %s: %-28s deg %d  %s  %s' % (NAMES[t[0]], NAMES[t[1]], NAMES[t[2]], pstr(P), deg, kind, info))
    pr('summary:', {k: len(v) for k, v in kinds.items()})
    assert 'UNEXPECTED' not in kinds
    assert len(kinds.get('const', [])) == 4 and len(kinds.get('linear-definite', [])) == 32
    assert len(kinds.get('quadratic-definite', [])) == 12 and len(kinds['C1-multiple']) == 4 and len(kinds['C2-multiple']) == 4
    # identities used in the region topology (hand proof in the report)
    D12 = {k: C1[k] - C2[k] for k in MONO}
    assert D12 == {'1': 0, 'x': -2, 'y': 2, 'xx': 0, 'xy': 0, 'yy': 0}     # C1 - C2 = 2(y - x)
    pr('C1 - C2 = 2(y - x): verified')

    pr('== Step 3: region representatives (exact) ==')
    reps = {
        'I_a': [(F(3, 10), F(1, 10)), (F(1, 2), F(1, 10)), (F(1, 100), F(1, 1000)), (F(9, 10), F(1, 100)), (F(99, 100), F(1, 10**4))],
        'I_b': [(F(1, 10), F(3, 10)), (F(1, 10), F(1, 2)), (F(1, 1000), F(1, 100)), (F(1, 100), F(9, 10))],
        'II':  [(F(3, 10), F(3, 10)), (F(1, 4), F(1, 2)), (F(9, 10), F(9, 100)), (F(1, 100), F(1, 100)), (F(1, 3), F(1, 3)),
                (F(9, 100), F(9, 10)), (F(99, 100), F(99, 10**4)), (F(49, 100), F(1, 2))],
    }
    REF = {}
    for name, L in reps.items():
        for (x, y) in L:
            assert in_open_T(x, y) and region(x, y) == name, (x, y, name, region(x, y))
            r = analyse(x, y)
            assert r['zeros'] == 0
            if name not in REF:
                REF[name] = r
            same = (r['chi'] == REF[name]['chi'])
            pr('  %-4s b=(%s, %s): zero triples %d, convex 5-subsets %d, largest convex subset %d, chirotope = region ref: %s'
               % (name, x, y, r['zeros'], len(r['pent']), r['maxconvex'], same))
            assert same
    pr('  II pentagons at (3/10,3/10):', [' '.join(NAMES[i] for i in s) for s in REF['II']['pent']])
    claimed = ['a0 a1 a2 b2 b3', 'a0 a1 a3 b1 b2', 'a0 a1 b1 b2 b3', 'a0 a2 a3 b0 b1', 'a0 a2 b0 b1 b2', 'a0 a2 b0 b1 b3',
               'a0 a2 b0 b2 b3', 'a0 a2 b1 b2 b3', 'a0 a3 b0 b1 b2', 'a0 b0 b1 b2 b3', 'a1 a2 a3 b0 b3', 'a1 a2 b0 b2 b3',
               'a1 a3 b0 b1 b2', 'a1 a3 b0 b1 b3', 'a1 a3 b0 b2 b3', 'a1 a3 b1 b2 b3', 'a1 b0 b1 b2 b3', 'a2 a3 b0 b1 b3',
               'a2 b0 b1 b2 b3', 'a3 b0 b1 b2 b3']
    mine = [' '.join(NAMES[i] for i in s) for s in REF['II']['pent']]
    pr('  my list of 20 == list printed in k5_exact.out:', mine == claimed)
    assert mine == claimed and len(mine) == 20
    assert REF['I_a']['pent'] == [] and REF['I_b']['pent'] == [] and REF['I_a']['maxconvex'] == 4 and REF['I_b']['maxconvex'] == 4

    # chirotope predicted from the polynomial signs (independent of the representatives)
    pr('  chirotope predicted from Step-2 signs matches each region reference:')
    for name in reps:
        x, y = reps[name][0]
        pred = []
        for t in TRIPLES:
            P = DET[t]
            s = sign_on_open_T(P)
            if s == 0:
                c = ratio(P, C1) or ratio(P, C2)
                base = C1 if ratio(P, C1) else C2
                s = sgn(c) * sgn(peval(base, x, y))
            pred.append(s)
        pr('    %s: %s' % (name, tuple(pred) == REF[name]['chi']))
        assert tuple(pred) == REF[name]['chi']

    pr('== Step 4: degenerate loci ==')
    for s in (F(1, 3), F(1, 2), F(1, 5), F(2, 3), F(9, 10)):
        x = (1 - s) / (1 + s * s); y = s * x                      # second intersection of y = s x with C1
        assert peval(C1, x, y) == 0 and in_open_T(x, y)
        r1 = analyse(x, y, full=False); r2 = analyse(y, x, full=False)   # (y, x) lies on C2
        assert peval(C2, y, x) == 0
        zt1 = [TRIPLES[i] for i, v in enumerate(r1['chi']) if v == 0]
        pr('  on C1 b=(%s,%s): %d collinear triples %s;  mirror point on C2: %d collinear triples'
           % (x, y, r1['zeros'], [' '.join(NAMES[i] for i in t) for t in zt1], r2['zeros']))
        assert r1['zeros'] == 4 and r2['zeros'] == 4
    for x in (F(1, 3), F(1, 2), F(9, 10)):
        r = analyse(x, F(0), full=False)
        pr('  on axis b=(%s,0): %d collinear triples' % (x, r['zeros']))
        assert r['zeros'] > 0

    pr('== Step 5: mirror relation and order-type classes ==')
    # reflection z -> i*conj(z) maps S(x,y) to S(y,x); labels a0<->a1, a2<->a3, b0->b0, b1->b3, b2->b2, b3->b1
    sigma = [1, 0, 3, 2, 4, 7, 6, 5]
    for (x, y) in [(F(3, 10), F(1, 10)), (F(1, 4), F(1, 2)), (F(2, 7), F(3, 11))]:
        P = points_at(x, y); Q = points_at(y, x)
        for i in range(8):
            assert Q[sigma[i]] == (P[i][1], P[i][0]), 'reflection label map wrong'
        dP = chi_fun(chirotope(P)); dQ = chi_fun(chirotope(Q))
        assert all(dQ[(sigma[i], sigma[j], sigma[k])] == -dP[(i, j, k)] for (i, j, k) in TRIPLES)
    pr('  S(y,x) is the mirror image of S(x,y) (exact, with explicit label map): verified')
    chiIa, chiIb, chiII = REF['I_a']['chi'], REF['I_b']['chi'], REF['II']['chi']
    p = isomorphic(chiIa, chiIb, mirror=True)
    pr('  I_a ~ mirror(I_b):', p is not None)
    q = isomorphic(chiIa, chiIb, mirror=False)
    pr('  I_a ~ I_b without reflection (orientation-preserving relabelling):', q is not None, q)
    pr('  I_a ~ II (either way):', isomorphic(chiIa, chiII) is not None or isomorphic(chiIa, chiII, True) is not None)
    # the convex octagon (outside the strictly-nested family) for context
    oc = analyse(F(7, 10), F(7, 10))
    pr('  outside the family: b=(7/10,7/10) (x+y>1): zero triples %d, convex 5-subsets %d, largest convex %d'
       % (oc['zeros'], len(oc['pent']), oc['maxconvex']))

    pr('== Step 6: "each outer vertex lies beyond two edge-lines of the inner square" ==')
    rng2 = random.Random(7)
    count = {'agree': 0}
    for _ in range(3000):
        D = rng2.choice((97, 1000, 65536))
        x = F(rng2.randint(1, D - 1), D); y = F(rng2.randint(1, D - 1), D)
        if not in_open_T(x, y) or region(x, y) == 'curve':
            continue
        P = points_at(x, y)
        A, B = P[:4], P[4:]
        ok = True
        for a in A:
            beyond = 0
            for l in range(4):
                p, q = B[l], B[(l + 1) % 4]
                s_center = sgn(det_num(p, q, (F(0), F(0))))
                s_a = sgn(det_num(p, q, a))
                assert s_center != 0 and s_a != 0
                beyond += (s_a == -s_center)
            ok = ok and (beyond == 2)
        pentfree = (len(analyse(x, y, full=False)['pent']) == 0)
        assert ok == (region(x, y) in ('I_a', 'I_b')) == pentfree, (x, y)
        count['agree'] += 1
    pr('  random exact samples where [all outer vertices beyond exactly 2 edge-lines] == [region I] == [pentagon-free]:',
       count['agree'])

    pr('== Step 7: context checks ==')
    Pint = [(10, 0), (0, 10), (-10, 0), (0, -10), (3, 1), (-1, 3), (-3, -1), (1, -3)]
    assert all(((-p[1], p[0]) in Pint) for p in Pint)
    chi_int = chirotope(Pint)
    assert 0 not in chi_int
    assert not any(hull_size([Pint[i] for i in s]) == 5 for s in combinations(range(8), 5))
    assert chi_int == REF['I_a']['chi']
    pr('  integer example: 4-fold symmetric, general position, no convex pentagon, same chirotope as I_a: verified')
    # centre with an antipodal pair is collinear for even m
    P = points_at(F(3, 10), F(1, 10)) + [(F(0), F(0))]
    assert det_num(P[8], P[4], P[6]) == 0 and det_num(P[8], P[0], P[2]) == 0
    pr('  adding the centre to a 4-fold set always creates collinear triples (centre, p, -p): verified')
    # random three nested squares: by ES(5) = 9 never GP + pentagon-free; tool sanity check only
    rng3 = random.Random(99)
    tried = gp = 0
    N3 =int(sys.argv[1]) if len(sys.argv) > 1 else 300
    for _ in range(N3):
        D = 997
        bx, by = F(rng3.randint(1, D - 1), D), F(rng3.randint(1, D - 1), D)
        cx, cy = F(rng3.randint(1, D - 1), D * 4), F(rng3.randint(1, D - 1), D * 4)
        pts = points_at(bx, by) + points_at(cx, cy)[4:]
        tried += 1
        if 0 in chirotope(pts):
            continue
        gp += 1
        # quick pentagon search
        found = any(hull_size([pts[i] for i in s]) == 5 for s in combinations(range(12), 5))
        assert found, 'pentagon-free 12-point set?! (would contradict ES(5)=9)'
    pr('  random 3-square sets: %d tried, %d in general position, all contain a convex pentagon' % (tried, gp))
    pr('ALL CHECKS PASSED')
    with open(__file__.replace('.py', '.out'), 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
