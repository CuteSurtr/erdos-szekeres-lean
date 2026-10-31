"""Independent helpers for the Caudit audit (written from scratch; does not import mirlib).

Conventions under test (from tools/etv/gen_etv.py): labels 1..N in x-order, X(i,j,k), i<j<k,
numbered in lexicographic order of triples, true <=> counterclockwise.
All geometry is exact (Python ints / numpy int64 within proven bounds / object arrays).
"""
import itertools, random
import numpy as np
from fractions import Fraction as F


def triples(N):
    return np.array(list(itertools.combinations(range(N), 3)), dtype=np.int64)


_TR = {}
def tri(N):
    if N not in _TR: _TR[N] = triples(N)
    return _TR[N]


def big(P):
    return max(abs(int(c)) for p in P for c in p) > 2**19


def orient_all(P):
    """P: list of (x,y) in label order. Returns int array of orientation signs for all triples
    i<j<k in lex order."""
    N = len(P); T = tri(N)
    dt = object if big(P) else np.int64
    x = np.array([p[0] for p in P], dtype=dt); y = np.array([p[1] for p in P], dtype=dt)
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    d = (x[b] - x[a]) * (y[c] - y[a]) - (y[b] - y[a]) * (x[c] - x[a])
    return np.array([(v > 0) - (v < 0) for v in d], dtype=np.int64) if dt is object else np.sign(d)


def orient_hom(H):
    """H: list of homogeneous (u,v,w) with w>0. Sign of det, which is the orientation of the
    affine points (u/w, v/w) times sign(w_a w_b w_c) = +1."""
    N = len(H); T = tri(N)
    dt = object if max(abs(int(c)) for h in H for c in h) > 2**19 else np.int64
    U = np.array([h[0] for h in H], dtype=dt); V = np.array([h[1] for h in H], dtype=dt); W = np.array([h[2] for h in H], dtype=dt)
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    d = (U[a] * (V[b] * W[c] - V[c] * W[b]) - V[a] * (U[b] * W[c] - U[c] * W[b]) + W[a] * (U[b] * V[c] - U[c] * V[b]))
    return np.array([(v > 0) - (v < 0) for v in d], dtype=np.int64) if dt is object else np.sign(d)


def general_position(P):
    return len(set(P)) == len(P) and not np.any(orient_all(P) == 0)


def hull_vertices(P):
    """Exact monotone-chain convex hull; returns set of indices of strict hull vertices."""
    idx = sorted(range(len(P)), key=lambda i: P[i])
    def cr(o, a, b):
        return (P[a][0] - P[o][0]) * (P[b][1] - P[o][1]) - (P[a][1] - P[o][1]) * (P[b][0] - P[o][0])
    lo, up = [], []
    for i in idx:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], i) <= 0: lo.pop()
        lo.append(i)
    for i in reversed(idx):
        while len(up) >= 2 and cr(up[-2], up[-1], i) <= 0: up.pop()
        up.append(i)
    return set(lo[:-1] + up[:-1])


def is_mirror(P):
    return sorted(P) == sorted((-x, y) for x, y in P)


def bits(signs):
    return "".join("1" if s > 0 else "0" for s in signs)


def sym_perturb(P, rng, M=None):
    """Remove x-ties without breaking the mirror: scale by M and move each pair (a,y),(-a,y)
    to (M a + e, M y), (-(M a + e), M y) with a small e chosen per pair; the axis point stays on
    x = 0. Order of P is kept; the caller checks the order type is unchanged."""
    # each orientation determinant is a nonzero integer; moving x by e/M < 1/(64 C) with
    # C = max |coordinate| + 1 changes it by less than 1/2, so signs are kept.
    C = max(abs(c) for p in P for c in p) + 1
    if M is None: M = 64 * C * 1000
    keys = sorted(set((abs(x), y) for x, y in P if x != 0))
    e = dict(zip(keys, rng.sample(range(1, 1000), len(keys))))
    return [(0, M * y) if x == 0 else ((1 if x > 0 else -1) * (M * abs(x) + e[(abs(x), y)]), M * y) for x, y in P]


def frame_ii(P):
    """Sub-case (ii) frame: x-sort (requires distinct x), y-reflect if X(1,2,3) is false.
    Returns (Q, signs, flipped)."""
    Q = sorted(P)
    assert len(set(q[0] for q in Q)) == len(Q)
    s = orient_all(Q)
    fl = False
    if s[0] < 0:
        Q = sorted((x, -y) for x, y in P); s = orient_all(Q); fl = True
    return Q, s, fl


def frame_i(P):
    """Sub-case (i) frame. P has its unique axis point p as a hull vertex. If p is the bottom
    point, y-reflect. Then apply the projective map with homogeneous image (x, 1, y0 - y)
    (affine (x/d, 1/d)), sort the other points by x/d, put p first; X(1,i,j) := true.
    Returns (labels as homogeneous vectors incl. p=(0,1,0), signs)."""
    p = [q for q in P if q[0] == 0]; assert len(p) == 1; p = p[0]
    if all(q[1] > p[1] for q in P if q != p):
        P = [(x, -y) for x, y in P]; p = (0, -p[1])
    assert all(q[1] < p[1] for q in P if q != p)
    y0 = p[1]
    H = sorted(((x, 1, y0 - y) for x, y in P if (x, y) != p), key=lambda h: F(h[0], h[2]))
    us = [F(h[0], h[2]) for h in H]
    assert len(set(us)) == len(us), "tie in projected x"
    Hall = [(0, 1, 0)] + H
    s = orient_hom(Hall)
    return Hall, s


def realize_hull_frame(Hall):
    """Proof device check: an affine x-sorted realization with the same orientation vector:
    q1 = (min u - 1, Ht) with Ht large, followed by the affine images (u, v)."""
    pts = [(F(h[0], h[2]), F(h[1], h[2])) for h in Hall[1:]]
    x0 = min(u for u, _ in pts) - 1
    Ht = max(abs(v) for _, v in pts) + 1
    while True:
        Q = [(x0, Ht)] + pts
        ok = all(orient_frac(Q[0], Q[i], Q[j]) > 0 for i in range(1, len(Q)) for j in range(i + 1, len(Q)))
        if ok: return Q
        Ht *= 4


def orient_frac(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_pos(pts):
    """Brute force: no point inside (or on) a triangle of three others; pts exact, gen. pos."""
    n = len(pts)
    for d in range(n):
        o = [i for i in range(n) if i != d]
        for a, b, c in itertools.combinations(o, 3):
            s1 = orient_frac(pts[a], pts[b], pts[d]); s2 = orient_frac(pts[b], pts[c], pts[d]); s3 = orient_frac(pts[c], pts[a], pts[d])
            if (s1 > 0) == (s2 > 0) == (s3 > 0): return False
    return True


def has_kgon_brute(P, k):
    """Exhaustive over k-subsets, with a 4-point convexity prefilter (convex position <=> every
    4-subset convex, Caratheodory)."""
    n = len(P)
    bad4 = set()
    for S in itertools.combinations(range(n), 4):
        if not convex_pos([P[i] for i in S]): bad4.add(S)
    for S in itertools.combinations(range(n), k):
        if not any(q in bad4 for q in itertools.combinations(S, 4)): return True
    return False
