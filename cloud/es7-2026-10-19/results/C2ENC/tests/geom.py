"""Exact-integer plane geometry for testing the zcnf.py rot (m = 2) encoding.

Written for this audit; it imports nothing from the repository.  All predicates use Python integers, so every sign is
exact.  A configuration is a list of integer points; the centre c is an integer point; the half-turn is h(p) = 2c - p.
"""
import functools
import itertools
import random


def orient(a, b, c):
    """twice the signed area of (a, b, c); > 0 iff counter-clockwise (same formula as ErdosSzekeres.orient)"""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def det3(u, v, w):
    """3x3 determinant of the homogeneous vectors (1, x, y); equals orient(u, v, w)"""
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0])
            + u[2] * (v[0] * w[1] - v[1] * w[0]))


def sgn(x):
    return (x > 0) - (x < 0)


def half_turn(c, p):
    return (2 * c[0] - p[0], 2 * c[1] - p[1])


def general_position(P):
    """no three of the points collinear (distinctness checked too)"""
    if len(set(P)) != len(P):
        return False
    return all(orient(a, b, d) != 0 for a, b, d in itertools.combinations(P, 3))


def hull_ccw(P):
    """vertices of conv(P) in counter-clockwise order (Andrew's monotone chain, strict turns)"""
    pts = sorted(set(P))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def in_convex_position(Q):
    """every point of Q is a vertex of conv(Q) (Q in general position)"""
    return len(Q) <= 3 or len(hull_ccw(Q)) == len(Q)


def inside_triangle(q, a, b, d):
    """q strictly inside triangle abd (general position assumed)"""
    s1, s2, s3 = sgn(orient(a, b, q)), sgn(orient(b, d, q)), sgn(orient(d, a, q))
    return s1 == s2 == s3 != 0


def convex4(Q):
    """4 points in general position are in convex position iff none is inside the triangle of the other three"""
    for i in range(4):
        others = [Q[j] for j in range(4) if j != i]
        if inside_triangle(Q[i], *others):
            return False
    return True


def max_convex_bruteforce(P, cap=None):
    """largest subset in convex position, by exhaustive search (small P only)"""
    n = len(P)
    best = min(n, 3)
    hi = n if cap is None else min(n, cap)
    for k in range(4, hi + 1):
        if any(in_convex_position([P[i] for i in S]) for S in itertools.combinations(range(n), k)):
            best = k
        else:
            break
    return best


# ---------------------------------------------------------------- configurations
def random_central(t, rng, box=10 ** 6, centre=(0, 0), shape="box", tries=10000):
    """t random antipodal pairs about an integer centre, in general position, centre not in the set.
    Returns the list [q_1, h(q_1), ..., q_t, h(q_t)] (pair order random)."""
    import math
    for _ in range(tries):
        P = []
        for i in range(t):
            if shape == "box":
                q = (rng.randint(-box, box), rng.randint(-box, box))
            elif shape == "ring":
                a = rng.uniform(0, 2 * math.pi)
                r = box * rng.uniform(0.9, 1.0)
                q = (int(r * math.cos(a)), int(r * math.sin(a)))
            elif shape == "radial":      # many radii scales: deep layer structure, tiny angular gaps
                a = rng.uniform(0, 2 * math.pi)
                r = box * (0.5 ** rng.randint(0, 12)) * rng.uniform(0.5, 1.0)
                q = (int(r * math.cos(a)), int(r * math.sin(a)))
            elif shape == "nearline":    # pairs almost collinear with the centre: near-degenerate angular order
                a = rng.choice([0.3, 1.1]) + rng.uniform(-1e-4, 1e-4)
                r = box * rng.uniform(0.05, 1.0)
                q = (int(r * math.cos(a)), int(r * math.sin(a)))
            else:
                raise ValueError(shape)
            q = (q[0] + centre[0], q[1] + centre[1])
            P += [q, half_turn(centre, q)]
        if centre in P:
            continue
        if general_position(P):
            return P
    raise RuntimeError("no configuration found")


# ---------------------------------------------------------------- the normal-form labelling
def normal_form(P, c, p0):
    """Label the centrally symmetric set P (centre c, c not in P) in the angular normal form of zcnf.py rot m=2:
    X[0] = p0, X[1] = h(p0); for o = 1..t-1, X[2o] is the point of pair o in the open half-plane left of the
    directed line c -> p0, sorted by angle; X[2o+1] = h(X[2o]); X[2t] = c.  Returns X (2t+1 points)."""
    assert p0 in P and c not in P
    S = set(P)
    assert all(half_turn(c, q) in S for q in P), "not centrally symmetric about c"
    t = len(P) // 2
    hp0 = half_turn(c, p0)
    reps = []
    for q in P:
        if q in (p0, hp0):
            continue
        o = orient(c, p0, q)
        assert o != 0, "c, p0, q collinear: contradicts general position"
        if o > 0:
            reps.append(q)
    assert len(reps) == t - 1
    reps.sort(key=functools.cmp_to_key(lambda a, b: -1 if orient(c, a, b) > 0 else 1))
    X = [p0, hp0]
    for q in reps:
        X += [q, half_turn(c, q)]
    X.append(c)
    # the normal-form facts, checked exactly
    for o in range(1, t):
        assert orient(c, X[0], X[2 * o]) > 0
        for o2 in range(o + 1, t):
            assert orient(c, X[2 * o], X[2 * o2]) > 0
    return X


def hull_vertices(P):
    return hull_ccw(P)


def read_points(path):
    pts = []
    with open(path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            x, y = line.replace(",", " ").split()[:2]
            pts.append((int(x), int(y)))
    return pts
