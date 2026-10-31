#!/usr/bin/env python3
"""Independent exact-integer helpers for reviewing the C2C34 relabelling arguments (A) and (B).
Nothing here is imported from the code under test."""
import functools, itertools, json, math, random

O = (0, 0)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sgn(x):
    return (x > 0) - (x < 0)


def neg(p):
    return (-p[0], -p[1])


def hull_ccw(P):
    pts = sorted(set(P))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def general_position(P):
    if len(set(P)) != len(P) or O in P:
        return False
    return all(cross(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def in_convex_position(S):
    return len(hull_ccw(S)) == len(S)


def has_convex_k(P, K):
    return any(in_convex_position(S) for S in itertools.combinations(P, K))


def normal_form(P, first):
    """My reading of the angular normal form: (0,0) = first, (0,1) = -first; for o >= 1, (o,0) is the point of pair o
    in the open half-plane LEFT of the ray O -> first, sorted counter-clockwise (increasing angle) from that ray;
    (o,1) = -(o,0). Returns X with X[2o+r] = point (o,r) and X[2t] = O (the centre Z)."""
    assert first in P
    t = len(P) // 2
    reps = [q for q in P if cross(O, first, q) > 0]
    assert len(reps) == t - 1, (len(reps), t)
    reps.sort(key=functools.cmp_to_key(lambda q, r: -1 if cross(O, q, r) > 0 else 1))
    for q, r in zip(reps, reps[1:]):
        assert cross(O, q, r) > 0
    X = [first, neg(first)]
    for q in reps:
        X += [q, neg(q)]
    X.append(O)
    return X


def classes_of(X, pts):
    idx = {p: i for i, p in enumerate(X[:-1])}
    return sorted({idx[p] // 2 for p in pts})


def geometry_case(X):
    """(hull classes, second-layer classes, hull ccw labels) computed from the coordinates alone."""
    pts = X[:-1]
    H = hull_ccw(pts)
    inner = [p for p in pts if p not in set(H)]
    H2 = hull_ccw(inner)
    return classes_of(X, H), classes_of(X, H2), H, H2


class Map:
    """The triple-variable map written by zcnf.py --map: chi(a,b,c) = s * X_v for sorted triples (a,b,c)."""

    def __init__(self, path):
        info = json.load(open(path))
        self.info = info
        self.t, self.N, self.Z, self.nX = info["t"], info["N"], info["Z"], info["X_vars"]
        self.triples = [tuple(x) for x in info["triples"]]
        self.tv = {(a, b, c): (v, s) for a, b, c, v, s in self.triples}
        self.rep = {}
        for a, b, c, v, s in self.triples:
            self.rep.setdefault(v, ((a, b, c), s))

    def lit(self, a, b, c):
        T = (a, b, c)
        S = tuple(sorted(T))
        inv = (a > b) + (a > c) + (b > c)
        ps = -1 if inv & 1 else 1
        if S not in self.tv:
            return 0
        v, s = self.tv[S]
        return ps * s * v

    def assign(self, X):
        """values val[v] in {+1,-1} of the triple variables for labelled coordinates X; checks that every class is
        consistent and that exactly the unmapped triples are zero."""
        val = [0] * (self.nX + 1)
        for a, b, c, v, s in self.triples:
            ch = sgn(cross(X[a], X[b], X[c]))
            if ch == 0:
                raise AssertionError(f"mapped triple {(a, b, c)} is zero")
            x = s * ch
            if val[v] == 0:
                val[v] = x
            elif val[v] != x:
                raise AssertionError(f"class {v} inconsistent at {(a, b, c)}")
        P = self.N + 1
        nz = 0
        for T in itertools.combinations(range(P), 3):
            if T not in self.tv:
                nz += 1
                if cross(X[T[0]], X[T[1]], X[T[2]]) != 0:
                    raise AssertionError(f"unmapped triple {T} nonzero")
        assert nz == self.t * (1 if self.info["m"] == 2 else 0), nz
        assert all(val[v] != 0 for v in range(1, self.nX + 1))
        return val


def lit_true(val, l):
    v = abs(l)
    return val[v] == (1 if l > 0 else -1)


def cube_true(val, lits):
    for l in lits:
        if not lit_true(val, l):
            return False
    return True


def load_cubes(path):
    out = {}
    for line in open(path):
        if line.strip():
            name, *ls = line.split()
            out[name] = [int(x) for x in ls]
    return out


# ---------- configuration generator ----------

def design(t, a, V, rng, scale=10 ** 9, jitter=True):
    """A centrally symmetric set of 2t points designed so that, in the normal form started at the point of class 0,
    the hull classes are {0, a} and the second-layer classes are V (the result is re-derived from the integer
    coordinates by the tests; this only steers the generator). Random rotation of the whole picture."""
    # angles of the class representatives (class 0 at angle 0), strictly increasing in (0, pi)
    while True:
        ang = sorted(rng.uniform(0.02, math.pi - 0.02) for _ in range(t - 1))
        if all(y - x > 1e-3 for x, y in zip(ang, ang[1:])):
            break
    ang = [0.0] + ang
    th = ang[a]
    r1 = 1.0
    inr1 = r1 * min(math.cos(th / 2), math.sin(th / 2))
    Vs = sorted(V)
    va = [ang[v] for v in Vs]
    gaps = [y - x for x, y in zip(va, va[1:])] + [va[0] + math.pi - va[-1]]
    r2 = 0.97 * inr1 * (rng.uniform(0.6, 1.0) if jitter else 1.0)
    inr2 = r2 * math.cos(max(gaps) / 2)
    rot = rng.uniform(0, 2 * math.pi)
    pts = []
    for o in range(t):
        if o in (0, a):
            r = r1          # both hull classes on the unit circle; the parallelogram contains the r2-disc
        elif o in V:
            r = r2          # second-layer classes on one circle: convex position
        else:
            r = inr2 * rng.uniform(0.15, 0.95)
        phi = ang[o] + rot
        p = (round(scale * r * math.cos(phi)), round(scale * r * math.sin(phi)))
        pts.append(p)
    P = []
    for p in pts:
        P += [p, neg(p)]
    return P, pts[0]


def random_set(t, rng, scale=10 ** 6):
    """undesigned: a random parallelogram and 2(t-2) random points inside it (symmetric)."""
    while True:
        A = (rng.randint(-scale, scale), rng.randint(-scale, scale))
        B = (rng.randint(-scale, scale), rng.randint(-scale, scale))
        if abs(cross(O, A, B)) > scale * scale // 4:
            break
    pts = [A, B]
    while len(pts) < t:
        u, w = rng.uniform(-0.97, 0.97), rng.uniform(-0.97, 0.97)
        if abs(u) + abs(w) >= 0.97:          # strictly inside the parallelogram A, B, -A, -B
            continue
        p = (round(u * A[0] + w * B[0]), round(u * A[1] + w * B[1]))
        pts.append(p)
    P = []
    for p in pts:
        P += [p, neg(p)]
    return P


def reflect(P, kind):
    if kind == 0:
        return [(-x, y) for x, y in P]
    if kind == 1:
        return [(x, -y) for x, y in P]
    return [(y, x) for x, y in P]
