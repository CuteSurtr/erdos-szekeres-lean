"""A7 audit library: exact geometry for the symmetric lower-bound examples (independent re-implementation).

Coordinate systems ("fmt"):
  Z2  : line "x y", ordinary integer coordinates.
  EIS : line "a b" = a + b*w, w = exp(2 pi i/3)  (Eisenstein integer); true plane point (a - b/2, b*sqrt3/2).
  Z5  : line "c0 c1 c2 c3" = c0 + c1 z + c2 z^2 + c3 z^3, z = exp(2 pi i/5) (cyclotomic integer).

Everything decisive is done with Python integers (exact).  Numerical (Decimal, 90 digits) values are used only as an
extra sanity cross-check, never as the basis of a verdict.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations

getcontext().prec = 90

# ------------------------------------------------------------------ parsing
def parse(path, fmt):
    width = {"Z2": 2, "EIS": 2, "Z5": 4}[fmt]
    pts, anomalies = [], []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            toks = s.split()
            try:
                vals = tuple(int(t) for t in toks)
            except ValueError:
                anomalies.append((ln, s))
                continue
            if len(vals) != width:
                anomalies.append((ln, s))
                continue
            pts.append(vals)
    return pts, anomalies

# ------------------------------------------------------------------ Z[sqrt5]
def sgn_r5(a, b):
    """exact sign of a + b*sqrt(5), a, b integers"""
    if a >= 0 and b >= 0:
        return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0:
        return -1
    d = a * a - 5 * b * b          # != 0 because sqrt5 is irrational and (a, b) != (0, 0)
    if a > 0:                       # b < 0: positive iff a > |b| sqrt5
        return 1 if d > 0 else -1
    return -1 if d > 0 else 1       # a < 0 < b: positive iff b sqrt5 > |a|

def r5_mul(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def r5_sub(x, y):
    return (x[0] - y[0], x[1] - y[1])

def r5_cmp(x, y):
    return sgn_r5(x[0] - y[0], x[1] - y[1])

# ------------------------------------------------------------------ affine (orientation-preserving) coordinates
def affine_coords(p, fmt):
    """Coordinates of an orientation-preserving linear image of the TRUE plane point.
    Z2 : identity.  EIS: (a, b) itself, image of the true point under the inverse of
    L(a,b) = (a - b/2, b sqrt3/2), det L = sqrt3/2 > 0.  Z5: (X, Y) = (4 Re w, 2 Im w / sin72) in Z[sqrt5]^2,
    a diagonal positive scaling of (Re w, Im w)."""
    if fmt in ("Z2", "EIS"):
        return p
    c0, c1, c2, c3 = p
    X = (4 * c0 - c1 - c2 - c3, c1 - c2 - c3)
    Y = (2 * c1 - c2 + c3, c2 - c3)
    return (X, Y)

def orient_A(p, q, r, fmt):
    """exact orientation sign, method A: cross product of the affine coordinates"""
    if fmt in ("Z2", "EIS"):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 0) - (v < 0)
    P, Q, Rr = affine_coords(p, fmt), affine_coords(q, fmt), affine_coords(r, fmt)
    ux, uy = r5_sub(Q[0], P[0]), r5_sub(Q[1], P[1])
    vx, vy = r5_sub(Rr[0], P[0]), r5_sub(Rr[1], P[1])
    c = r5_sub(r5_mul(ux, vy), r5_mul(uy, vx))
    return sgn_r5(c[0], c[1])

# --- method B (an independent exact formula for each format)
def _cyc_mul(u, v):
    w = [0] * 5
    for a in range(5):
        for b in range(5):
            w[(a + b) % 5] += u[a] * v[b]
    return w

def orient_B(p, q, r, fmt):
    if fmt == "Z2":
        # 3x3 determinant | 1 x y | expanded along the first column
        (x1, y1), (x2, y2), (x3, y3) = p, q, r
        v = (x2 * y3 - x3 * y2) - (x1 * y3 - x3 * y1) + (x1 * y2 - x2 * y1)
        return (v > 0) - (v < 0)
    if fmt == "EIS":
        # true coordinates x = a - b/2 (rational), y = b*sqrt3/2; cross = (sqrt3/2) * bracket
        def xy(t):
            return (Fraction(t[0]) - Fraction(t[1], 2), Fraction(t[1]))
        (x1, b1), (x2, b2), (x3, b3) = xy(p), xy(q), xy(r)
        v = (x2 - x1) * (b3 - b1) - (b2 - b1) * (x3 - x1)
        return (v > 0) - (v < 0)
    # Z5: cross(u, v) = Im(conj(u) v) computed in Z[zeta5] (5-term vectors), then
    # Im(sum w_j z^j) = (w1 - w4) sin72 + (w2 - w3) sin144, and sin144/sin72 = (sqrt5 - 1)/2
    u = [q[t] - p[t] for t in range(4)] + [0]
    v = [r[t] - p[t] for t in range(4)] + [0]
    cu = [u[(-j) % 5] for j in range(5)]
    w = _cyc_mul(cu, v)
    A = 2 * (w[1] - w[4]) - (w[2] - w[3])
    B = (w[2] - w[3])
    return sgn_r5(A, B)

# --- method C: numerical (sanity only)
_S5 = Decimal(5).sqrt()
_S3 = Decimal(3).sqrt()
COS = [Decimal(1), (_S5 - 1) / 4, -(_S5 + 1) / 4, -(_S5 + 1) / 4, (_S5 - 1) / 4]
SIN = [Decimal(0), (10 + 2 * _S5).sqrt() / 4, (10 - 2 * _S5).sqrt() / 4,
       -(10 - 2 * _S5).sqrt() / 4, -(10 + 2 * _S5).sqrt() / 4]

def true_xy(p, fmt):
    if fmt == "Z2":
        return (Decimal(p[0]), Decimal(p[1]))
    if fmt == "EIS":
        return (Decimal(p[0]) - Decimal(p[1]) / 2, Decimal(p[1]) * _S3 / 2)
    x = sum(Decimal(p[j]) * COS[j] for j in range(4))
    y = sum(Decimal(p[j]) * SIN[j] for j in range(4))
    return (x, y)

def orient_C(p, q, r, fmt):
    P, Q, Rr = true_xy(p, fmt), true_xy(q, fmt), true_xy(r, fmt)
    v = (Q[0] - P[0]) * (Rr[1] - P[1]) - (Q[1] - P[1]) * (Rr[0] - P[0])
    return v

# ------------------------------------------------------------------ symmetry maps (exact, on the native integers)
MAPS = {
    "C2":  lambda p: (-p[0], -p[1]),
    "C4":  lambda p: (-p[1], p[0]),
    "M":   lambda p: (-p[0], p[1]),
    "C3E": lambda p: (-p[1], p[0] - p[1]),          # multiplication by w
    "C6E": lambda p: (p[0] - p[1], p[0]),           # multiplication by 1 + w = exp(i pi/3)
    "C5":  lambda p: (-p[3], p[0] - p[3], p[1] - p[3], p[2] - p[3]),   # multiplication by z
}
ANGLE_DEG = {"C2": 180, "C4": 90, "C3E": 120, "C6E": 60, "C5": 72}
MAP_FMT = {"C2": "Z2", "C4": "Z2", "M": "Z2", "C3E": "EIS", "C6E": "EIS", "C5": "Z5"}

def orbits(pts, g):
    S = set(pts)
    seen, orbs = set(), []
    for p in pts:
        if p in seen:
            continue
        orb, q = [], p
        while True:
            orb.append(q)
            seen.add(q)
            q = g(q)
            if q == p or len(orb) > 100:
                break
        orbs.append(orb)
    return orbs

# ------------------------------------------------------------------ orientation table
def orient_table(pts, fmt, method=orient_A):
    n = len(pts)
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                O[i][j][k] = method(pts[i], pts[j], pts[k], fmt)
    return O

# ------------------------------------------------------------------ generic linear order (lexicographic)
def lex_key_cmp(fmt):
    """returns a comparison function on points: lexicographic on the affine coordinates (exact)"""
    if fmt in ("Z2", "EIS"):
        def cmp(p, q):
            a, b = affine_coords(p, fmt), affine_coords(q, fmt)
            return (a > b) - (a < b)
        return cmp
    def cmp5(p, q):
        A, B = affine_coords(p, fmt), affine_coords(q, fmt)
        c = r5_cmp(A[0], B[0])
        if c:
            return c
        return r5_cmp(A[1], B[1])
    return cmp5

# ------------------------------------------------------------------ the DP: largest subset in convex position
def max_convex_dp(O, order):
    """O: exact orientation table on indices; order: indices sorted by an injective linear functional (lex).
    A set in convex position = lower chain (cup: increasing, all left turns) + upper chain (cap: increasing, all right
    turns), sharing the first and last points.  For each first point l we compute, for every edge (i, j), the longest
    cup / cap starting at l and ending with that edge (O(n^3)), then combine for every last point r.
    Returns (size, witness list of indices)."""
    n = len(order)
    P = order
    if n <= 2:
        return n, list(P)
    best_len, best_wit = 2, [P[0], P[1]]
    for l in range(n):
        cup = [[0] * n for _ in range(n)]
        cap = [[0] * n for _ in range(n)]
        cupp = [[-1] * n for _ in range(n)]
        capp = [[-1] * n for _ in range(n)]
        for j in range(l + 1, n):
            cup[l][j] = 2
            cap[l][j] = 2
        for i in range(l + 1, n):
            Pi = P[i]
            for j in range(i + 1, n):
                Pj = P[j]
                bu, bup, bc, bcp = 0, -1, 0, -1
                for h in range(l, i):
                    s = O[P[h]][Pi][Pj]
                    if s > 0:
                        v = cup[h][i]
                        if v and v + 1 > bu:
                            bu, bup = v + 1, h
                    elif s < 0:
                        v = cap[h][i]
                        if v and v + 1 > bc:
                            bc, bcp = v + 1, h
                cup[i][j], cupp[i][j] = bu, bup
                cap[i][j], capp[i][j] = bc, bcp
        for r in range(l + 1, n):
            bu, bui, bc, bci = 0, -1, 0, -1
            for i in range(l, r):
                if cup[i][r] > bu:
                    bu, bui = cup[i][r], i
                if cap[i][r] > bc:
                    bc, bci = cap[i][r], i
            tot = bu + bc - 2
            if tot > best_len:
                def chain(tab, prv, i, j):
                    c = [j, i]
                    while i != l:
                        h = prv[i][j]
                        c.append(h)
                        i, j = h, i
                    return c[::-1]
                lo = chain(cup, cupp, bui, r)
                up = chain(cap, capp, bci, r)
                assert lo[0] == l and up[0] == l and lo[-1] == r and up[-1] == r
                wit = lo + up[1:-1][::-1]
                best_len, best_wit = tot, [P[t] for t in wit]
                assert len(best_wit) == tot
    return best_len, best_wit

# ------------------------------------------------------------------ convex position by an exact hull (independent)
def hull_is_convex_position(coords, cmpf, crossf):
    """Andrew monotone chain on exact coordinates; returns True iff every point is a hull vertex.
    coords: list of points (any type), cmpf: lexicographic comparison, crossf(o, a, b): exact orientation sign."""
    from functools import cmp_to_key
    pts = sorted(coords, key=cmp_to_key(cmpf))
    if len(pts) <= 2:
        return True
    lower = []
    for p in pts:
        while len(lower) >= 2 and crossf(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and crossf(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return len(hull) == len(pts)

def convex_position_halfplane(idx, O):
    """criterion: every q has some r with all other s strictly left of q->r (gift wrapping)"""
    for q in idx:
        ok = False
        for r in idx:
            if r == q:
                continue
            if all(O[q][r][s] > 0 for s in idx if s != q and s != r):
                ok = True
                break
        if not ok:
            return False
    return True

# ------------------------------------------------------------------ convex layers (exact)
def convex_layers(idx, O):
    """peel hull vertices: q is a hull vertex of the current set iff the half-plane criterion holds"""
    rest = list(idx)
    layers = []
    while rest:
        if len(rest) <= 2:
            layers.append(list(rest))
            break
        hv = []
        for q in rest:
            for r in rest:
                if r != q and all(O[q][r][s] > 0 for s in rest if s != q and s != r):
                    hv.append(q)
                    break
        layers.append(hv)
        rest = [q for q in rest if q not in hv]
    return layers
