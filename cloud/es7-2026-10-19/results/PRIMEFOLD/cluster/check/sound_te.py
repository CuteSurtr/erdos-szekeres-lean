#!/usr/bin/env python3
"""Soundness test of the relaxation (my encoder enc_te.py), written from scratch.

For a REAL cluster C (points in the OUTWARD radial frame of v_0: x radial outward, y = ccw tangent) and m:
  1. compute Prop. C's g(x) = f_C((0,x)), h(x) = f_C((-x,0)) DIRECTLY from the definition (ccw chains whose edge
     directions, measured from the ccw tangent in units of pi/m, lie in the open arc and increase strictly),
     by exhaustive DFS -- no cups/caps, no frame change;
  2. compute the true values of every variable of enc_te.build(m, n, sig) (inward frame, x-sorted, exact
     orientations, bins from high-precision angles with a genericity margin check), including the encoder's
     notion of g/h (longest cup/cap with last bin in the window) and compare it with step 1;
  3. evaluate every clause; the 'bound' clauses (only negative G/H literals) are expected to hold iff the cluster
     satisfies (i); every other clause must ALWAYS hold.
"""
import sys, random
from fractions import Fraction as Fr
from itertools import combinations
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import enc_te
import hp
from decimal import Decimal
EPS = Decimal(10) ** -40


_ucache = {}
def u_out(k, m):
    """unit vector at angle pi/2 + k*pi/m (k units ccw from the ccw tangent (0,1)) in the OUTWARD frame."""
    key = ('o', k, m)
    if key not in _ucache:
        _ucache[key] = hp.unit_at_pi_multiple(Fr(1, 2) + Fr(k, m))
    return _ucache[key]


def u_in(k, m):
    """unit vector k units ccw from the ccw tangent, which is (0,-1) in the INWARD frame."""
    key = ('i', k, m)
    if key not in _ucache:
        _ucache[key] = hp.unit_at_pi_multiple(Fr(-1, 2) + Fr(k, m))
    return _ucache[key]


def xsgn(u, v):
    """sign of cross(u, v) where u is a Decimal unit vector, v exact rational; raises if within 1e-40."""
    c = u[0] * hp.dec(v[1]) - u[1] * hp.dec(v[0])
    if abs(c) < EPS:
        raise ValueError('non-generic direction (on an arc boundary)')
    return 1 if c > 0 else -1


def cross_exact(a, b):
    return a[0] * b[1] - a[1] * b[0]


def direct_profile(C, m):
    """g(x), h(x) for x = 1..m-1 straight from the definition; also F11 = f_C((-1,1))."""
    n = len(C)
    vec = {(p, q): (C[q][0] - C[p][0], C[q][1] - C[p][1]) for p in range(n) for q in range(n) if p != q}

    def inside(v, lo, hi):            # open arc (lo, hi) in units pi/m from the tangent; hi - lo < m
        return xsgn(u_out(lo, m), v) > 0 and xsgn(u_out(hi, m), v) < 0

    def f(lo, hi):
        best = 1 if n else 0
        stack = [(p, None, 1) for p in range(n)]
        while stack:
            p, vprev, k = stack.pop()
            if k > best:
                best = k
            for q in range(n):
                if q == p:
                    continue
                v = vec[p, q]
                if inside(v, lo, hi) and (vprev is None or cross_exact(vprev, v) > 0):
                    stack.append((q, v, k + 1))
        return best
    g = {x: f(0, x) for x in range(1, m)}
    h = {x: f(-x, 0) for x in range(1, m)}
    F11 = f(-1, 1)
    return g, h, F11


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def true_assignment(C, m, sig):
    n = len(C)
    P = sorted([(-x, -y) for (x, y) in C])          # inward frame (rotation by pi), sorted by x'
    for i in range(n - 1):
        assert P[i][0] < P[i + 1][0], 'equal x'
    b = {}
    for i, j in combinations(range(n), 2):
        v = (P[j][0] - P[i][0], P[j][1] - P[i][1])
        cnt = sum(1 for k in range(1, m) if xsgn(u_in(k, m), v) > 0)
        assert 1 <= cnt <= m - 2, 'direction in the forbidden tangent zone'
        b[i, j] = cnt
    sgn = {}
    for (i, j, k) in combinations(range(n), 3):
        o = orient(P[i], P[j], P[k])
        assert o != 0, 'collinear'
        sgn[i, j, k] = o > 0
    # longest cup/cap ending with edge (i,j)
    cup = {}
    cap = {}
    for j in range(n):
        for i in range(j):
            cu = 2
            ca = 2
            for k in range(i):
                if sgn[k, i, j]:
                    cu = max(cu, cup[k, i] + 1)
                else:
                    ca = max(ca, cap[k, i] + 1)
            cup[i, j] = cu
            cap[i, j] = ca
    genc = {}
    henc = {}
    for x in range(1, m):
        genc[x] = max([1] + [cup[e] for e in cup if b[e] < x])
        henc[x] = max([1] + [cap[e] for e in cap if b[e] >= m - x])
    e, V = enc_te.build(m, n, sig)
    val = {}
    for (i, j, k), var in V['O'].items():
        val[var] = sgn[i, j, k]
    for (i, j, v), var in V['Q'].items():
        val[var] = b[i, j] >= v
    for (l, i, j), var in V['U'].items():
        val[var] = cup[i, j] >= l
    for (l, i, j), var in V['V'].items():
        val[var] = cap[i, j] >= l
    for (x, a), var in V['G'].items():
        val[var] = genc[x] >= a
    for (x, a), var in V['H'].items():
        val[var] = henc[x] >= a
    assert len(val) == e.nv
    GH = set(V['G'].values()) | set(V['H'].values())
    bad_struct = 0
    bad_bound = 0
    for c in e.clauses:
        ok = any((l > 0) == val[abs(l)] for l in c)
        if not ok:
            if all(l < 0 and -l in GH for l in c):
                bad_bound += 1
            else:
                bad_struct += 1
    return genc, henc, bad_struct, bad_bound, len(e.clauses)


def check(C, m, sig=1, verbose=False):
    g, h, F11 = direct_profile(C, m)
    if F11 != 1:
        return None
    genc, henc, bs, bb, nc = true_assignment(C, m, sig)
    sat_i = all(g[x] + h[x] <= x + 1 for x in range(1, m))
    same = all(g[x] == genc[x] and h[x] == henc[x] for x in range(1, m))
    if verbose or not same or bs or (sat_i and bb) or ((not sat_i) and bb == 0):
        print('m=%d n=%d  direct g=%s h=%s | enc g=%s h=%s | (i)=%s  struct_viol=%d bound_viol=%d of %d' % (
            m, len(C), [g[x] for x in range(1, m)], [h[x] for x in range(1, m)], [genc[x] for x in range(1, m)],
            [henc[x] for x in range(1, m)], sat_i, bs, bb, nc))
    return same, bs, bb, sat_i


if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    stats = dict(tested=0, mismatch=0, struct_viol=0, sat_i=0, sat_i_bound_viol=0, unsat_i_no_bound_viol=0)
    for tr in range(trials):
        m = rng.choice([4, 5, 6, 7, 8])
        n = rng.randint(2, int(sys.argv[3]) if len(sys.argv) > 3 else 8)
        # random cluster: rational coordinates, small vertical spread (so most segments avoid the tangent zone),
        # occasionally a two-scale / rotated cluster
        mode = rng.random()
        C = []
        for _ in range(n):
            if mode < 0.5:
                C.append((Fr(rng.randint(-10**6, 10**6), 10**6), Fr(rng.randint(-10**5, 10**5), 10**6)))
            else:
                ang = rng.uniform(-1.2, 1.2)
                r = rng.uniform(-1, 1)
                s = rng.uniform(-0.05, 0.05)
                import math
                xx = r * math.cos(ang) - s * math.sin(ang)
                yy = r * math.sin(ang) + s * math.cos(ang)
                C.append((Fr(int(xx * 10**9), 10**9), Fr(int(yy * 10**9), 10**9)))
        if len(set(C)) < n:
            continue
        try:
            r = check(C, m)
        except (AssertionError, ValueError) as ex:
            continue
        if r is None:
            continue
        same, bs, bb, sat_i = r
        stats['tested'] += 1
        stats['mismatch'] += (not same)
        stats['struct_viol'] += (bs > 0)
        stats['sat_i'] += sat_i
        stats['sat_i_bound_viol'] += (sat_i and bb > 0)
        stats['unsat_i_no_bound_viol'] += ((not sat_i) and bb == 0)
    print(stats)
