#!/usr/bin/env python3
"""A1 audit: the lower-example files cited in the size table exist and have the claimed size; in addition (cheap,
exact integer arithmetic, own code): distinct points, invariance under the stated symmetry, the fixed points (centre /
axis points), no three collinear, and -- for the integer-coordinate files -- the FULL affine symmetry group, with a check
that every affine symmetry fixes the centroid and that the averaged Gram matrix B = sum L^T L is invariant
(L^T B L = B), i.e. the group is orthogonal for the inner product B.  The 7-gon-freeness of the files is NOT checked
here (another auditor does that).

usage: examples_check.py RESULTS_DIR
"""
import itertools, json, os, sys
from fractions import Fraction

R = sys.argv[1]
FILES = {
    # name: (path, claimed size, kind, map description)
    "C3": ("SYMMAX/c3_31points.txt", 31, "eis3"),
    "C4": ("SYMMAX/c4_28points.txt", 28, "c4"),
    "C5": ("SYMMAX/c5_31points.txt", 31, "z5"),
    "C6": ("SYMMAX/c6_30points.txt", 30, "eis6"),
    "mirror": ("SYMMAX/mirror_32points.txt", 32, "mirror"),
    "C2": ("SYM2/sym7_32points.txt", 32, "c2"),
}
MAPS = {
    "eis3": lambda p: (-p[1], p[0] - p[1]),          # rotation by 120 deg in Eisenstein coordinates a + b w
    "eis6": lambda p: (p[0] - p[1], p[0]),           # rotation by 60 deg in Eisenstein coordinates
    "c4": lambda p: (-p[1], p[0]),
    "c2": lambda p: (-p[0], -p[1]),
    "mirror": lambda p: (-p[0], p[1]),
    # Z[zeta5], basis 1, z, z^2, z^3, z^4 = -1-z-z^2-z^3; multiplication by z
    "z5": lambda c: (-c[3], c[0] - c[3], c[1] - c[3], c[2] - c[3]),
}


def read(path):
    pts = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith(("#", "FOUND")):
            continue
        pts.append(tuple(int(x) for x in line.split()))
    return pts


def orient2(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


# ---- Q(zeta5) arithmetic: element = list of 5 coefficients in basis z^0..z^4 (not reduced); conj(z^i) = z^(5-i)
def z5_vec(c):
    return [c[0], c[1], c[2], c[3], 0]


def z5_sub(u, v):
    return [a - b for a, b in zip(u, v)]


def z5_mul(u, v):
    w = [0] * 5
    for i in range(5):
        for j in range(5):
            w[(i + j) % 5] += u[i] * v[j]
    return w


def z5_conj(u):
    return [u[0]] + [u[5 - i] for i in range(1, 5)]


def sign_a_plus_b_sqrt5(a, b):
    """sign of a + b*sqrt5 for integers a, b (exact)"""
    if a >= 0 and b >= 0:
        return (a > 0 or b > 0) and 1 or 0
    if a <= 0 and b <= 0:
        return -1 if (a < 0 or b < 0) else 0
    # opposite signs: compare a^2 with 5 b^2
    d = a * a - 5 * b * b
    if d == 0:
        return 0  # impossible for integers unless a = b = 0
    return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)


def z5_orient(p, q, r):
    """sign of Im((q-p) * conj(r-p)) * (-1): orientation of p, q, r as plane points (ccw = +).
    Im(w) for w = sum w_i z^i equals sin72 * ((w1-w4) + (w2-w3)(sqrt5-1)/2) (sin144/sin72 = (sqrt5-1)/2)."""
    u = z5_sub(z5_vec(q), z5_vec(p))
    v = z5_sub(z5_vec(r), z5_vec(p))
    w = z5_mul(z5_conj(u), v)        # conj(q-p) * (r-p): Im > 0 iff r-p is ccw from q-p
    a2 = 2 * (w[1] - w[4]) - (w[2] - w[3])
    b2 = (w[2] - w[3])
    return sign_a_plus_b_sqrt5(a2, b2)


def affine_group(P):
    """all affine maps g of the plane (rational) with g(P) = P; P integer points, general position assumed."""
    S = set(P)
    p0, p1, p2 = P[0], P[1], None
    for c in P[2:]:
        if orient2(p0, p1, c) != 0:
            p2 = c
            break
    M = ((p1[0] - p0[0], p2[0] - p0[0]), (p1[1] - p0[1], p2[1] - p0[1]))
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    adj = ((M[1][1], -M[0][1]), (-M[1][0], M[0][0]))
    rel = [(x[0] - p0[0], x[1] - p0[1]) for x in P]
    group = []
    for q0, q1, q2 in itertools.permutations(P, 3):
        Q = ((q1[0] - q0[0], q2[0] - q0[0]), (q1[1] - q0[1], q2[1] - q0[1]))
        # N = Q adj(M); g(x) = q0 + N (x - p0) / det
        N = ((Q[0][0] * adj[0][0] + Q[0][1] * adj[1][0], Q[0][0] * adj[0][1] + Q[0][1] * adj[1][1]),
             (Q[1][0] * adj[0][0] + Q[1][1] * adj[1][0], Q[1][0] * adj[0][1] + Q[1][1] * adj[1][1]))
        ok = True
        for (dx, dy) in rel:
            vx = N[0][0] * dx + N[0][1] * dy
            vy = N[1][0] * dx + N[1][1] * dy
            if vx % det or vy % det or (q0[0] + vx // det, q0[1] + vy // det) not in S:
                ok = False
                break
        if ok:
            L = tuple(tuple(Fraction(N[i][j], det) for j in range(2)) for i in range(2))
            t = (Fraction(q0[0]) - L[0][0] * p0[0] - L[0][1] * p0[1], Fraction(q0[1]) - L[1][0] * p0[0] - L[1][1] * p0[1])
            group.append((L, t))
    return group


def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def transpose(A):
    return ((A[0][0], A[1][0]), (A[0][1], A[1][1]))


def analyse_group(P, group):
    n = len(P)
    cx = Fraction(sum(p[0] for p in P), n)
    cy = Fraction(sum(p[1] for p in P), n)
    fixes_centroid = all(L[0][0] * cx + L[0][1] * cy + t[0] == cx and L[1][0] * cx + L[1][1] * cy + t[1] == cy
                         for L, t in group)
    Ls = [L for L, t in group]
    B = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    for L in Ls:
        LtL = matmul(transpose(L), L)
        B = tuple(tuple(B[i][j] + LtL[i][j] for j in range(2)) for i in range(2))
    invariant = all(matmul(matmul(transpose(L), B), L) == B for L in Ls)
    # element orders and determinants
    I = ((1, 0), (0, 1))
    info = []
    for L in Ls:
        d = L[0][0] * L[1][1] - L[0][1] * L[1][0]
        X, k = L, 1
        while X != I and k <= 2 * len(Ls):
            X, k = matmul(X, L), k + 1
        info.append((int(d), k))
    rot_orders = sorted(k for d, k in info if d == 1)
    refl = sum(1 for d, k in info if d == -1)
    max_rot = max(rot_orders)
    if refl == 0:
        gtype = "C%d" % len(Ls)
    else:
        gtype = "D%d" % (len(Ls) // 2)
    return {"order": len(Ls), "type": gtype, "rotation_orders": rot_orders, "reflections": refl,
            "max_rotation_order": max_rot, "all_fix_centroid": fixes_centroid,
            "centroid": [str(cx), str(cy)], "averaged_form_invariant": invariant,
            "averaged_form_B": [[str(x) for x in row] for row in B]}


out = {}
allok = True
for name, (rel, size, kind) in FILES.items():
    path = os.path.join(R, rel)
    rec = {"file": rel, "exists": os.path.isfile(path)}
    if not rec["exists"]:
        out[name] = rec
        allok = False
        continue
    P = read(path)
    S = set(P)
    f = MAPS[kind]
    rec["points"] = len(P)
    rec["claimed"] = size
    rec["size_ok"] = len(P) == size
    rec["distinct"] = len(S) == len(P)
    rec["invariant"] = all(f(p) in S for p in P)
    # orbit structure under the stated generator
    seen, orbit_sizes = set(), []
    for p in P:
        if p in seen:
            continue
        o, q = [p], f(p)
        while q != p:
            o.append(q)
            q = f(q)
        seen.update(o)
        orbit_sizes.append(len(o))
    rec["orbit_sizes"] = {str(k): orbit_sizes.count(k) for k in sorted(set(orbit_sizes))}
    rec["fixed_points"] = [list(p) for p in P if f(p) == p]
    if kind == "z5":
        col = sum(1 for a, b, c in itertools.combinations(P, 3) if z5_orient(a, b, c) == 0)
    else:
        col = sum(1 for a, b, c in itertools.combinations(P, 3) if orient2(a, b, c) == 0)
    rec["collinear_triples"] = col
    ok = rec["size_ok"] and rec["distinct"] and rec["invariant"] and col == 0
    if kind != "z5":
        G = affine_group(P)
        rec["affine_group"] = analyse_group(P, G)
        ok = ok and rec["affine_group"]["all_fix_centroid"] and rec["affine_group"]["averaged_form_invariant"]
    rec["ok"] = ok
    allok = allok and ok
    out[name] = rec
out["ALL_OK"] = allok
print(json.dumps(out, indent=1))
sys.exit(0 if allok else 1)
