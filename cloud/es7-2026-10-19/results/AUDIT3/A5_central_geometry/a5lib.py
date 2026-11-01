#!/usr/bin/env python3
"""Auditor A5: independent exact-integer helpers for the central 34-point formula (zcnf.py rot 17 7 --m 2 --hull).

Nothing is imported from the repository. Conventions re-derived from zcnf.py by reading it:
  point (o, r) has index 2*o + r, (o, 1) = -(o, 0); the centre c is element Z = 34 (placed at the origin here);
  chi(a, b, c) = sign det[(1,xa,ya),(1,xb,yb),(1,xc,yc)] (counter-clockwise = +);
  base.json 'triples' rows [a, b, c, v, s] (a < b < c) mean chi(a, b, c) = s * X_v (X_v = +1 iff v is true);
  auxiliary 'conv' variables are numbered after the 2856 triple classes, in the order zcnf.py creates them:
  for r = 4, 5, 6, combinations(range(34), r) in lexicographic order, kept iff the set is the lexicographic minimum
  of its orbit under the half-turn i -> i ^ 1.
"""
import functools, itertools, json, math, random

T = 17          # antipodal classes
N = 34          # points
Z = 34          # the centre
ORIGIN = (0, 0)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sgn(x):
    return (x > 0) - (x < 0)


def neg(p):
    return (-p[0], -p[1])


def hull_ccw(P):
    """strict convex hull vertices in counter-clockwise order (Andrew's monotone chain, exact)"""
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
    """no repeated point, the origin not a point, no three points collinear (exact)"""
    if len(set(P)) != len(P) or ORIGIN in P:
        return False
    for a, b, c in itertools.combinations(P, 3):
        if cross(a, b, c) == 0:
            return False
    return True


def sym(pts):
    """the centrally symmetric set {p, -p}"""
    out = []
    for p in pts:
        out += [p, neg(p)]
    return out


def label(P, first):
    """Angular normal form started at `first` (my reading): X[0] = first, X[1] = -first, and for o >= 1, X[2o] is the
    point of class o in the OPEN half-plane left of the ray origin -> first, the classes sorted counter-clockwise
    (by angle in (0, pi)); X[2o+1] = -X[2o]; X[34] = origin. Returns None if the normal form does not exist."""
    assert first in P
    reps = [q for q in P if cross(ORIGIN, first, q) > 0]
    if len(reps) != len(P) // 2 - 1:
        return None
    # angle comparison inside an open half-plane: q before r iff r is left of origin -> q
    reps.sort(key=functools.cmp_to_key(lambda q, r: -1 if cross(ORIGIN, q, r) > 0 else (1 if cross(ORIGIN, q, r) < 0 else 0)))
    for q, r in zip(reps, reps[1:]):
        if cross(ORIGIN, q, r) <= 0:
            return None
    X = [first, neg(first)]
    for q in reps:
        X += [q, neg(q)]
    X.append(ORIGIN)
    return X


def hull_classes(X, pts_idx=None):
    """classes of the strict hull vertices of the labelled points with the given indices (default: all 34)"""
    if pts_idx is None:
        pts_idx = list(range(N))
    pts = [X[i] for i in pts_idx]
    H = set(hull_ccw(pts))
    return sorted({i // 2 for i in pts_idx if X[i] in H}), [i for i in pts_idx if X[i] in H]


class Map:
    def __init__(self, path):
        info = json.load(open(path))
        assert info["kind"] == "rot" and info["m"] == 2 and info["t"] == T and info["N"] == N and info["Z"] == Z
        self.info = info
        self.nX = info["X_vars"]
        self.nv = info["vars"]
        self.tv = {}
        for a, b, c, v, s in info["triples"]:
            assert a < b < c
            self.tv[(a, b, c)] = (v, s)

    def lit(self, a, b, c):
        """literal that is true iff chi(a, b, c) = +; 0 for a zero triple"""
        S = tuple(sorted((a, b, c)))
        if S not in self.tv:
            return 0
        inv = (a > b) + (a > c) + (b > c)
        ps = -1 if inv & 1 else 1
        v, s = self.tv[S]
        return ps * s * v


def canon(S):
    img = tuple(sorted(i ^ 1 for i in S))
    return min(tuple(S), img)


def conv_numbering(nX):
    """dict frozen-tuple -> var for the canonical 4-, 5-, 6-sets, in zcnf.py's creation order"""
    num = {}
    v = nX
    for r in (4, 5, 6):
        for S in itertools.combinations(range(N), r):
            if canon(S) == S:
                v += 1
                num[S] = v
    return num, v


def assignment(mp, X, convnum):
    """full assignment (list index var -> +1/-1) of the base variables for labelled coordinates X (X[34] = centre).
    Checks that every triple class is consistent and that exactly the triples {c, p, -p} are zero."""
    val = [0] * (mp.nv + 1)
    for (a, b, c), (v, s) in mp.tv.items():
        ch = sgn(cross(X[a], X[b], X[c]))
        if ch == 0:
            raise AssertionError(f"mapped triple {(a, b, c)} has chi = 0")
        x = s * ch
        if val[v] == 0:
            val[v] = x
        elif val[v] != x:
            raise AssertionError(f"triple class {v} inconsistent at {(a, b, c)}")
    for Tr in itertools.combinations(range(N + 1), 3):
        if Tr not in mp.tv:
            assert Tr[2] == Z and Tr[1] == Tr[0] ^ 1, Tr
            assert cross(X[Tr[0]], X[Tr[1]], X[Tr[2]]) == 0
    assert all(val[v] != 0 for v in range(1, mp.nX + 1))
    # convexity of 4-sets from orientations (no point inside the triangle of the other three)
    conv4 = {}
    for S in itertools.combinations(range(N), 4):
        ok = True
        for d in range(4):
            a, b, c = [S[i] for i in range(4) if i != d]
            o1 = sgn(cross(X[a], X[b], X[S[d]]))
            o2 = sgn(cross(X[b], X[c], X[S[d]]))
            o3 = sgn(cross(X[c], X[a], X[S[d]]))
            if o1 == o2 == o3:
                ok = False
                break
        conv4[S] = ok
    conv = dict(conv4)
    for r in (5, 6):
        for S in itertools.combinations(range(N), r):
            conv[S] = all(conv[S[:i] + S[i + 1:]] for i in range(r))
    for S, v in convnum.items():
        val[v] = 1 if conv[S] else -1
    return val, conv


def convex_7sets_canonical(conv):
    """canonical 7-sets in convex position (all 6-subsets convex)"""
    out = []
    six = [S for S, c in conv.items() if len(S) == 6 and c]
    six_set = set(six)
    for S in six:
        for x in range(S[-1] + 1, N):
            U = S + (x,)
            if all((U[:i] + U[i + 1:]) in six_set for i in range(6)):
                if canon(U) == U:
                    out.append(U)
    return out


def write_masks(path, vals, nv):
    """binary file: for var 1..nv one little-endian uint64 whose bit j is the value of the var in labelling j"""
    import struct
    L = len(vals)
    assert L <= 64
    buf = bytearray(8 * (nv + 1))
    for v in range(1, nv + 1):
        m = 0
        for j, val in enumerate(vals):
            if val[v] > 0:
                m |= 1 << j
        struct.pack_into("<Q", buf, 8 * v, m)
    open(path, "wb").write(bytes(buf))


def load_cubes(path):
    out = {}
    order = []
    for line in open(path):
        if line.strip():
            name, *ls = line.split()
            out[name] = [int(x) for x in ls]
            order.append(name)
    return out, order


def lit_true(val, l):
    return val[abs(l)] == (1 if l > 0 else -1)


def cube_true(val, lits):
    return all(lit_true(val, l) for l in lits)


# ---------------- configuration generators (only steer; every test re-derives the geometry exactly) -------------

def gen_parallelogram(rng, scale=10 ** 7, inner_kind=None):
    """random centrally symmetric 34-point set with a parallelogram hull; inner_kind 2/3 steers the second layer to a
    quadrilateral/hexagon, None leaves the inner 15 classes uniformly random in a shrunken parallelogram."""
    while True:
        A = (rng.randint(-scale, scale), rng.randint(-scale, scale))
        B = (rng.randint(-scale, scale), rng.randint(-scale, scale))
        if abs(cross(ORIGIN, A, B)) > scale * scale // 3:
            break
    pts = [A, B]
    if inner_kind is None:
        while len(pts) < T:
            u, w = rng.uniform(-1, 1), rng.uniform(-1, 1)
            if abs(u) + abs(w) < 0.98:
                pts.append((round(u * A[0] + w * B[0]), round(u * A[1] + w * B[1])))
    else:
        # second layer: inner_kind classes on an affine image of a circle inside the parallelogram, rest deeper
        k = inner_kind
        r2 = rng.uniform(0.35, 0.48)
        phis = sorted(rng.uniform(0, math.pi) for _ in range(k))
        for ph in phis:
            u, w = r2 * math.cos(ph), r2 * math.sin(ph)
            pts.append((round(u * A[0] + w * B[0]), round(u * A[1] + w * B[1])))
        while len(pts) < T:
            rr = r2 * rng.uniform(0.0, 0.45)
            ph = rng.uniform(0, 2 * math.pi)
            u, w = rr * math.cos(ph), rr * math.sin(ph)
            pts.append((round(u * A[0] + w * B[0]), round(u * A[1] + w * B[1])))
    return sym(pts)


def gen_random_disc(rng, scale=10 ** 7):
    pts = []
    while len(pts) < T:
        x, y = rng.randint(-scale, scale), rng.randint(-scale, scale)
        if x * x + y * y < scale * scale:
            pts.append((x, y))
    return sym(pts)


def gen_hexagon(rng, scale=10 ** 7):
    """three hull classes (hexagonal hull), rest inside"""
    phis = sorted(rng.uniform(0, math.pi) for _ in range(3))
    hull = [(round(scale * math.cos(p)), round(scale * math.sin(p))) for p in phis]
    pts = list(hull)
    while len(pts) < T:
        rr = scale * rng.uniform(0, 0.45)
        ph = rng.uniform(0, 2 * math.pi)
        pts.append((round(rr * math.cos(ph)), round(rr * math.sin(ph))))
    return sym(pts)


def reflect(P, kind):
    if kind == 0:
        return [(-x, y) for x, y in P]
    if kind == 1:
        return [(x, -y) for x, y in P]
    if kind == 2:
        return [(y, x) for x, y in P]
    return [(-y, -x) for x, y in P]
