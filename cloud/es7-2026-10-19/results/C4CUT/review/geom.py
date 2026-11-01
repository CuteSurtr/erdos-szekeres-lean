"""Independent exact geometry for the C4 review (Fractions / ints only)."""
from fractions import Fraction as F
from itertools import combinations
import numpy as np


def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(x):
    return (x > 0) - (x < 0)


def rot90(p, c):
    """counter-clockwise quarter turn about c"""
    return (c[0] - (p[1] - c[1]), c[1] + (p[0] - c[0]))


def in_gp(P):
    return all(det(a, b, c) != 0 for a, b, c in combinations(P, 3))


def hull(P):
    """vertices of conv(P) (exact, Andrew monotone chain, strict turns)"""
    pts = sorted(set(P))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and det(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and det(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def layers(P):
    rest, out = list(P), []
    while rest:
        V = hull(rest)
        out.append(V)
        Vs = set(V)
        rest = [p for p in rest if p not in Vs]
    return out


def orbit(p, c):
    o = [p]
    for _ in range(3):
        o.append(rot90(o[-1], c))
    return o


def is_c4(P, c):
    S = set(P)
    return all(rot90(p, c) in S for p in P)


def label_normal_form(P, c, first=0):
    """Label a fourfold set per the layer normal form; returns list lab[0..N-1] of points.
    Asserts every convex layer is exactly one rotation orbit. first in 0..3 picks (0,0) among O_0."""
    L = layers(P)
    for V in L:
        assert len(V) == 4 and set(V) == set(orbit(V[0], c)), ("layer is not one orbit", len(V))
    p00 = orbit(L[0][0], c)[first]
    r00 = rot90(p00, c)
    lab = []
    for o, V in enumerate(L):
        if o == 0:
            q = p00
        else:
            cand = [q for q in V if det(c, p00, q) > 0 and det(c, q, r00) > 0]
            assert len(cand) == 1, cand
            q = cand[0]
        for r in range(4):
            lab.append(q)
            q = rot90(q, c)
    return lab


def conv4_table(P):
    """boolean array T[a,b,c,d] (any order) : 4 points in convex position"""
    n = len(P)
    inside = np.zeros((n, n, n, n), dtype=bool)  # inside[a,b,c,d]: d strictly inside triangle abc
    S = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if len({a, b, c}) == 3:
                    S[a][b][c] = sgn(det(P[a], P[b], P[c]))
    conv = np.zeros((n, n, n, n), dtype=bool)
    for q in combinations(range(n), 4):
        nin = 0
        for d in q:
            a, b, c = [x for x in q if x != d]
            if S[a][b][d] == S[b][c][d] == S[c][a][d]:
                nin += 1
        assert nin in (0, 1)
        if nin == 0:
            for perm in __import__("itertools").permutations(q):
                conv[perm] = True
    return conv


def convex_ksets(P, k):
    """list of all k-subsets (sorted index tuples) in convex position (4-point criterion, vectorised)"""
    n = len(P)
    conv = conv4_table(P)
    combs = np.array(list(combinations(range(n), k)), dtype=np.int16)
    ok = np.ones(len(combs), dtype=bool)
    for q in combinations(range(k), 4):
        ok &= conv[combs[:, q[0]], combs[:, q[1]], combs[:, q[2]], combs[:, q[3]]]
    return [tuple(map(int, r)) for r in combs[ok]]


def convex_brute(pts):
    """direct definition: no point of pts in the closed convex hull of the others (via hull vertex count)"""
    return len(hull(pts)) == len(pts)
