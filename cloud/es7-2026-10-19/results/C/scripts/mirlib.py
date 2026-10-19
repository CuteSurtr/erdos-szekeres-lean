"""Exact helpers for mirror-symmetric point sets (vertical axis x = 0).

Conventions match tools/etv/gen_etv.py and tools/trackB/gen_cnf.py:
points are sorted by x and numbered 1..N; X(i,j,k) (i<j<k) is the variable
index of the triple in lexicographic order; X true <=> counterclockwise <=> cup.
Everything here is exact (Python ints and Fractions).
"""
import itertools, random
from fractions import Fraction as F


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def triple_index(N):
    return {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}


def general_position(P):
    if len(set(P)) != len(P):
        return False
    return all(orient(*t) != 0 for t in itertools.combinations(P, 3))


def mirror_set(npairs, axis, rng, R=10**6, where=None):
    """Random exactly mirror-symmetric integer set: npairs pairs (x,y),(-x,y), x>0,
    plus `axis` points (0, y) (axis in {0,1,2}).  where in {None,'top','bottom','interior'}
    places the single axis point above all pairs, below all, or strictly between.
    All x distinct, general position checked exactly."""
    while True:
        xs = rng.sample(range(1, R), npairs)
        ys = rng.sample(range(-R, R), npairs + axis)
        pairs = list(zip(xs, ys[:npairs]))
        ay = ys[npairs:]
        if axis == 1 and where is not None:
            lo, hi = min(ys[:npairs]), max(ys[:npairs])
            if where == 'top':
                ay = [hi + rng.randrange(1, R)]
            elif where == 'bottom':
                ay = [lo - rng.randrange(1, R)]
            elif where == 'interior':
                if hi - lo < 2:
                    continue
                ay = [rng.randrange(lo + 1, hi)]
        P = [(x, y) for x, y in pairs] + [(-x, y) for x, y in pairs] + [(0, y) for y in ay]
        if len(set(y for _, y in P)) != npairs + len(ay):
            continue  # a horizontal line through two pairs would be collinear-prone; resample
        if general_position(P):
            return P


def xsorted(P):
    Q = sorted(P)
    assert len(set(p[0] for p in Q)) == len(Q), "repeated x-coordinate"
    return Q


def orientations(Q):
    """Q sorted by x.  Returns dict (i,j,k) 1-based -> bool (ccw)."""
    X = {}
    for i, j, k in itertools.combinations(range(len(Q)), 3):
        v = orient(Q[i], Q[j], Q[k])
        assert v != 0
        X[(i + 1, j + 1, k + 1)] = v > 0
    return X


def hull_frame(P):
    """P symmetric with exactly one axis point p = (0, y0), p strictly above every other point.
    Projective map (x,y) -> (x/d, 1/d), d = y0 - y > 0, homogeneous matrix [[1,0,0],[0,0,1],[0,-1,y0]]
    of determinant +1, so orientations of the other points are preserved; lines through p become
    vertical, and p goes to vertical infinity (upwards), i.e. index 1 with X(1,i,j) = true.
    Returns (Q, X) with Q[0] = None (p) and Q[1:] the transformed points sorted by u."""
    ax = [q for q in P if q[0] == 0]
    assert len(ax) == 1
    p = ax[0]
    y0 = p[1]
    rest = [q for q in P if q != p]
    assert all(q[1] < y0 for q in rest)
    T = sorted((F(x, y0 - y), F(1, y0 - y)) for x, y in rest)
    assert len(set(t[0] for t in T)) == len(T)
    N = len(P)
    X = {}
    for i, j, k in itertools.combinations(range(1, N + 1), 3):
        if i == 1:
            X[(i, j, k)] = True
        else:
            v = orient(T[i - 2], T[j - 2], T[k - 2])
            assert v != 0
            X[(i, j, k)] = v > 0
    # sanity: the map preserves orientation of triples not containing p
    return [None] + T, X


def read_cnf(path):
    cls = []
    nv = 0
    with open(path) as f:
        for line in f:
            if line.startswith('p'):
                nv = int(line.split()[2])
                continue
            if line.startswith('c') or not line.strip():
                continue
            c = list(map(int, line.split()))
            assert c[-1] == 0
            cls.append(c[:-1])
    return nv, cls


def eval_x_clauses(cls, nX, X, idx):
    """Evaluate every clause whose variables are all orientation variables (<= nX)
    under the orientation assignment X.  Returns (#checked, #violated, first violated)."""
    val = {idx[t]: v for t, v in X.items()}
    checked = bad = 0
    first = None
    for c in cls:
        if all(abs(l) <= nX for l in c):
            checked += 1
            if not any((l > 0) == val[abs(l)] for l in c):
                bad += 1
                if first is None:
                    first = c
    return checked, bad, first


def convex_position(pts):
    """pts: list of points (exact).  True iff no point is inside a triangle of three others."""
    n = len(pts)
    for d in range(n):
        for a, b, c in itertools.combinations([i for i in range(n) if i != d], 3):
            s1 = orient(pts[a], pts[b], pts[d]) > 0
            s2 = orient(pts[b], pts[c], pts[d]) > 0
            s3 = orient(pts[c], pts[a], pts[d]) > 0
            if s1 == s2 == s3:
                return False
    return True


def has_kgon(P, k):
    return any(convex_position(S) for S in itertools.combinations(P, k))
