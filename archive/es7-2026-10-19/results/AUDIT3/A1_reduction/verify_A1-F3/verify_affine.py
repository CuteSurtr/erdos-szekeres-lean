#!/usr/bin/env python3
"""Independent check for audit finding A1-F3 (the affine-symmetry extension of Corollary 3).

Own code; it does not import or reuse the A1 scripts.  All geometry is exact (Fractions, and Q(sqrt5) for the
fivefold file).  Floats appear only in the clearly marked whitening illustration, never in a pass/fail decision that
the exact checks do not also make.

For every example set S it enumerates ALL affine bijections g(x) = L x + t of the real plane with g(S) = S, WITHOUT
assuming that g fixes the centroid, has finite order or has |det| = 1: g is determined by the images of a fixed affine
basis (p0, p1, p2) of S, and every ordered triple (q0, q1, q2) of distinct points of S is tried.  For each g found:
  (b)  g fixes the centroid c of S;
  (a') |det L| = 1 and g has finite order (consistent with step (a): G acts faithfully on S, so |G| <= |S|!);
  (c') L Sigma L^T = Sigma for the scatter matrix Sigma = sum (p - c)(p - c)^T, which is positive definite because S
       spans the plane.  This is an invariant inner product that exists without averaging and without finiteness;
       also the averaged Gram matrix B = sum_g L_g^T L_g is invariant (the averaging of step (c));
  (d)  det L = -1  =>  L^2 = I and tr L = 0 (an affine reflection); det L = +1 and order k  =>  tr L = 2 cos(2 pi j/k)
       with gcd(j, k) = 1 (an affine rotation); the set of maps is closed under composition;
  (e)  for random non-orthogonal integer affine images T(S): chirotope(T(S)) = sign(det T) * chirotope(S) on every
       triple (so general position and convex position are preserved), and the affine group of T(S) has the same
       order and type.
Coordinates: the integer files are used as they are (Eisenstein coordinates for the 3- and 6-fold files, i.e. a
linear image of the Euclidean set); the 5-fold file (a line c0 c1 c2 c3 = c0 + c1 z + c2 z^2 + c3 z^3, z = e^(2 pi i/5))
is mapped to (Re z, Im z / sin 72deg) in Q(sqrt5)^2.  Both changes of coordinates are linear bijections of R^2, so
affine symmetries correspond one to one.

usage: verify_affine.py RESULTS_DIR
"""
import itertools, json, math, os, random, sys
from fractions import Fraction as Fr


# ----------------------------------------------------------------------------------------------------------- Q(sqrt5)
class K:
    """a + b*sqrt(5), a, b rational.  Q is the subfield b = 0."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fr(a)
        self.b = Fr(b)

    def __add__(s, o):
        o = o if isinstance(o, K) else K(o)
        return K(s.a + o.a, s.b + o.b)

    __radd__ = __add__

    def __neg__(s):
        return K(-s.a, -s.b)

    def __sub__(s, o):
        o = o if isinstance(o, K) else K(o)
        return K(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return K(o) - s

    def __mul__(s, o):
        o = o if isinstance(o, K) else K(o)
        return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)

    __rmul__ = __mul__

    def inv(s):
        d = s.a * s.a - 5 * s.b * s.b
        if d == 0:
            raise ZeroDivisionError
        return K(s.a / d, -s.b / d)

    def __truediv__(s, o):
        o = o if isinstance(o, K) else K(o)
        return s * o.inv()

    def __eq__(s, o):
        o = o if isinstance(o, K) else K(o)
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0:
            return 0 if (a == 0 and b == 0) else 1
        if a <= 0 and b <= 0:
            return -1
        d = a * a - 5 * b * b          # opposite strict signs; d != 0 since sqrt5 is irrational
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)

    def __float__(s):
        return float(s.a) + float(s.b) * math.sqrt(5)

    def __repr__(s):
        return str(s.a) if s.b == 0 else "%s+%s*sqrt5" % (s.a, s.b)


ZERO, ONE = K(0), K(1)
SQ5 = K(0, 1)


# ------------------------------------------------------------------------------------------------- 2x2 linear algebra
def mmul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def mT(A):
    return ((A[0][0], A[1][0]), (A[0][1], A[1][1]))


def mdet(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def minv(A):
    d = mdet(A)
    return ((A[1][1] / d, -A[0][1] / d), (-A[1][0] / d, A[0][0] / d))


def mvec(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def madd(A, B):
    return tuple(tuple(A[i][j] + B[i][j] for j in range(2)) for i in range(2))


I2 = ((ONE, ZERO), (ZERO, ONE))


def orient(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])).sign()


# ------------------------------------------------------------------------------------------------------ input files
def read_int_file(path):
    pts = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pts.append(tuple(int(x) for x in line.split()))
    return pts


def z5_to_plane(c):
    """c0 + c1 z + c2 z^2 + c3 z^3 (z = e^(2 pi i/5)) -> (Re, Im / sin72) in Q(sqrt5)^2.
    cos72 = (sqrt5-1)/4, cos144 = cos216 = -(sqrt5+1)/4; sin144/sin72 = (sqrt5-1)/2 = -sin216/sin72."""
    c0, c1, c2, c3 = c
    cos72 = K(Fr(-1, 4), Fr(1, 4))
    cos144 = K(Fr(-1, 4), Fr(-1, 4))
    r = K(Fr(-1, 2), Fr(1, 2))         # (sqrt5 - 1)/2
    x = K(c0) + K(c1) * cos72 + K(c2 + c3) * cos144
    y = K(c1) + K(c2 - c3) * r
    return (x, y)


# ------------------------------------------------------------------------------------------------ affine enumeration
def affine_symmetries(P):
    """all (L, t) with x -> L x + t mapping the finite set P (list of K-pairs, spanning the plane) onto itself."""
    S = set(P)
    n = len(P)
    # base: p0 = first point, p1 = second, p2 = a point maximising |area| with them (any affine basis would do)
    p0, p1 = P[0], P[1]
    best, p2 = None, None
    for c in P[2:]:
        ar = (p1[0] - p0[0]) * (c[1] - p0[1]) - (p1[1] - p0[1]) * (c[0] - p0[0])
        v = abs(float(ar))
        if ar.sign() != 0 and (best is None or v > best):
            best, p2 = v, c
    assert p2 is not None, "P does not span the plane"
    M = ((p1[0] - p0[0], p2[0] - p0[0]), (p1[1] - p0[1], p2[1] - p0[1]))
    Minv = minv(M)
    others = [p for p in P if p not in (p0, p1, p2)]
    found = []
    for q0 in P:
        for q1 in P:
            if q1 == q0:
                continue
            for q2 in P:
                if q2 == q0 or q2 == q1:
                    continue
                Q = ((q1[0] - q0[0], q2[0] - q0[0]), (q1[1] - q0[1], q2[1] - q0[1]))
                if mdet(Q).sign() == 0:
                    continue            # cannot happen in general position, kept for safety
                L = mmul(Q, Minv)
                Lp0 = mvec(L, p0)
                t = (q0[0] - Lp0[0], q0[1] - Lp0[1])
                ok = True
                for p in others:
                    Lp = mvec(L, p)
                    if (Lp[0] + t[0], Lp[1] + t[1]) not in S:
                        ok = False
                        break
                if ok:
                    found.append((L, t))
    return found


def compose(g, h):
    """g o h"""
    (L1, t1), (L2, t2) = g, h
    Lt = mvec(L1, t2)
    return (mmul(L1, L2), (Lt[0] + t1[0], Lt[1] + t1[1]))


IDENT = (I2, (ZERO, ZERO))


def order_of(g, cap=200):
    h, k = g, 1
    while h != IDENT:
        h, k = compose(h, g), k + 1
        if k > cap:
            return None
    return k


def rot_traces(k):
    """exact set {2 cos(2 pi j / k) : gcd(j, k) = 1} for the k that can occur here (k <= 6, and 5 via sqrt5)."""
    if k == 1:
        return {K(2)}
    if k == 2:
        return {K(-2)}
    if k == 3:
        return {K(-1)}
    if k == 4:
        return {K(0)}
    if k == 5:
        return {K(Fr(-1, 2), Fr(1, 2)), K(Fr(-1, 2), Fr(-1, 2))}
    if k == 6:
        return {K(1)}
    return None


def cholesky_upper(Mf):
    """float 2x2 SPD -> upper R with Mf = R^T R"""
    a, b, d = Mf[0][0], Mf[0][1], Mf[1][1]
    r11 = math.sqrt(a)
    r12 = b / r11
    r22 = math.sqrt(d - r12 * r12)
    return ((r11, r12), (0.0, r22))


def fmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def finv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def analyse(P, G):
    n = len(P)
    c = (sum((p[0] for p in P), ZERO) / n, sum((p[1] for p in P), ZERO) / n)
    Sig = ((ZERO, ZERO), (ZERO, ZERO))
    for p in P:
        d = (p[0] - c[0], p[1] - c[1])
        Sig = madd(Sig, ((d[0] * d[0], d[0] * d[1]), (d[1] * d[0], d[1] * d[1])))
    sig_pd = Sig[0][0].sign() > 0 and mdet(Sig).sign() > 0
    rec = {"order": len(G), "centroid": [repr(c[0]), repr(c[1])], "scatter_positive_definite": sig_pd}
    fix_c, unimod, sig_inv, elems = True, True, True, []
    B = ((ZERO, ZERO), (ZERO, ZERO))
    for (L, t) in G:
        B = madd(B, mmul(mT(L), L))
    b_inv = all(mmul(mmul(mT(L), B), L) == B for (L, t) in G)
    closed = all(compose(g, h) in G for g in G for h in G)
    has_ident = IDENT in G
    std_orth = all(mmul(mT(L), L) == I2 for (L, t) in G)
    classification_ok = True
    axis_counts = []
    Minv_sig = minv(Sig)
    # float whitening (illustration only): R from Sigma^{-1} = R^T R, then R L R^{-1} should be orthogonal
    Mf = [[float(Minv_sig[i][j]) for j in range(2)] for i in range(2)]
    Rf = cholesky_upper(Mf)
    Rfi = finv(Rf)
    max_orth_err = 0.0
    for g in G:
        L, t = g
        img_c = mvec(L, c)
        if not (img_c[0] + t[0] == c[0] and img_c[1] + t[1] == c[1]):
            fix_c = False
        d = mdet(L)
        if not (d == ONE or d == K(-1)):
            unimod = False
        if mmul(mmul(L, Sig), mT(L)) != Sig:
            sig_inv = False
        k = order_of(g)
        tr = L[0][0] + L[1][1]
        kind = None
        if d == K(-1):
            ok = mmul(L, L) == I2 and tr == ZERO and k == 2
            kind = "reflection"
            # axis = fixed line of g through c: points p with g(p) = p; count points of S on it
            fixed = [p for p in P if (lambda Lp: (Lp[0] + t[0], Lp[1] + t[1]))(mvec(L, p)) == p]
            axis_counts.append(len(fixed))
        else:
            rt = rot_traces(k) if k else None
            ok = rt is not None and tr in rt
            kind = "identity" if k == 1 else "rotation"
        classification_ok = classification_ok and ok
        A = fmul(fmul(Rf, [[float(L[i][j]) for j in range(2)] for i in range(2)]), Rfi)
        AtA = fmul([[A[0][0], A[1][0]], [A[0][1], A[1][1]]], A)
        err = max(abs(AtA[0][0] - 1), abs(AtA[1][1] - 1), abs(AtA[0][1]), abs(AtA[1][0]))
        max_orth_err = max(max_orth_err, err)
        elems.append({"det": repr(d), "order": k, "trace": repr(tr), "kind": kind})
    nrefl = sum(1 for e in elems if e["kind"] == "reflection")
    rec.update({
        "type": ("C%d" % len(G)) if nrefl == 0 else ("D%d" % (len(G) // 2)),
        "element_orders": sorted(e["order"] for e in elems),
        "reflections": nrefl,
        "points_on_reflection_axes": axis_counts,
        "contains_identity": has_ident, "closed_under_composition": closed,
        "all_fix_centroid": fix_c, "all_det_pm1": unimod,
        "scatter_invariant_L_Sig_LT_eq_Sig": sig_inv,
        "averaged_gram_invariant": b_inv,
        "classification_ok(refl: L^2=I,tr=0; rot: tr=2cos(2pi j/k))": classification_ok,
        "orthogonal_in_given_coordinates": std_orth,
        "float_whitening_max_orthogonality_error": max_orth_err,
    })
    rec["ok"] = all([sig_pd, has_ident, closed, fix_c, unimod, sig_inv, b_inv, classification_ok, max_orth_err < 1e-9])
    return rec


def general_position(P):
    return all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def chirotope(P):
    return [orient(a, b, c) for a, b, c in itertools.combinations(P, 3)]


def kpt(p):
    return (K(p[0]), K(p[1]))


# --------------------------------------------------------------------------------------------------------------- main
def main():
    R = sys.argv[1]
    files = {
        "C3 (Eisenstein coords)": ("SYMMAX/c3_31points.txt", "int"),
        "C4": ("SYMMAX/c4_28points.txt", "int"),
        "C5 (Q(sqrt5) coords)": ("SYMMAX/c5_31points.txt", "z5"),
        "C6 (Eisenstein coords)": ("SYMMAX/c6_30points.txt", "int"),
        "mirror": ("SYMMAX/mirror_32points.txt", "int"),
        "C2": ("SYM2/sym7_32points.txt", "int"),
    }
    out = {"examples": {}, "controls": {}}
    allok = True
    rng = random.Random(20261101)
    for name, (rel, kind) in files.items():
        raw = read_int_file(os.path.join(R, rel))
        P = [z5_to_plane(c) for c in raw] if kind == "z5" else [kpt(p) for p in raw]
        assert len(set(P)) == len(P)
        gp = general_position(P)
        G = affine_symmetries(P)
        rec = analyse(P, G)
        rec["points"] = len(P)
        rec["general_position"] = gp
        rec["ok"] = rec["ok"] and gp
        out["examples"][name] = rec
        allok = allok and rec["ok"]
        # control (e): a random non-orthogonal integer affine image (integer files only)
        if kind == "int":
            while True:
                A = [[rng.randint(-5, 5) for _ in range(2)] for _ in range(2)]
                dA = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                # reject zero det and similarities (A^T A scalar), so the image is genuinely non-orthogonal
                ata = (A[0][0] ** 2 + A[1][0] ** 2, A[0][0] * A[0][1] + A[1][0] * A[1][1], A[0][1] ** 2 + A[1][1] ** 2)
                if dA != 0 and not (ata[1] == 0 and ata[0] == ata[2]):
                    break
            t = (rng.randint(-1000, 1000), rng.randint(-1000, 1000))
            P2 = [(A[0][0] * x + A[0][1] * y + t[0], A[1][0] * x + A[1][1] * y + t[1]) for (x, y) in raw]
            Q2 = [kpt(p) for p in P2]
            chi1, chi2 = chirotope(P), chirotope(Q2)
            sd = 1 if dA > 0 else -1
            chi_ok = all(b == sd * a for a, b in zip(chi1, chi2))
            G2 = affine_symmetries(Q2)
            r2 = analyse(Q2, G2)
            same = r2["order"] == rec["order"] and r2["type"] == rec["type"] and \
                r2["element_orders"] == rec["element_orders"]
            ok2 = r2["ok"] and chi_ok and same
            out["controls"]["affine image of " + name] = {
                "A": A, "det": dA, "t": t, "chirotope_equals_signdet_times_original": chi_ok,
                "group_order": r2["order"], "type": r2["type"], "same_group_as_original": same,
                "all_fix_centroid": r2["all_fix_centroid"], "scatter_invariant": r2["scatter_invariant_L_Sig_LT_eq_Sig"],
                "orthogonal_in_given_coordinates": r2["orthogonal_in_given_coordinates"], "ok": ok2}
            allok = allok and ok2
    # control: regular polygons (expected dihedral groups)
    hexa = [kpt(p) for p in [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]]   # Eisenstein coords
    pent = [z5_to_plane(c) for c in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (-1, -1, -1, -1)]]
    sq = [kpt(p) for p in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
    shear_mirror = None
    raw_m = read_int_file(os.path.join(R, "SYMMAX/mirror_32points.txt"))
    shear_mirror = [kpt((x + 3 * y, y)) for (x, y) in raw_m]      # oblique reflection after the shear
    expect = {"regular hexagon (expect D6, 12)": (hexa, 12, "D6"), "regular pentagon (expect D5, 10)": (pent, 10, "D5"),
              "square (expect D4, 8)": (sq, 8, "D4"),
              "sheared mirror_32 (expect D1, 2, oblique reflection)": (shear_mirror, 2, "D1")}
    for nm, (P, o, ty) in expect.items():
        r = analyse(P, affine_symmetries(P))
        ok = r["ok"] and r["order"] == o and r["type"] == ty
        if "sheared" in nm:
            ok = ok and not r["orthogonal_in_given_coordinates"] and r["points_on_reflection_axes"] == [0]
        out["controls"][nm] = {"order": r["order"], "type": r["type"],
                               "orthogonal_in_given_coordinates": r["orthogonal_in_given_coordinates"],
                               "all_fix_centroid": r["all_fix_centroid"], "ok": ok}
        allok = allok and ok
    # control: random sets in general position (expect trivial group)
    for trial in range(3):
        while True:
            raw = [(rng.randint(-60, 60), rng.randint(-60, 60)) for _ in range(14)]
            Pk = [kpt(p) for p in raw]
            if len(set(raw)) == 14 and general_position(Pk):
                break
        r = analyse(Pk, affine_symmetries(Pk))
        ok = r["ok"] and r["order"] == 1
        out["controls"]["random 14 points #%d (expect 1)" % trial] = {"order": r["order"], "ok": ok}
        allok = allok and ok
    out["ALL_OK"] = allok
    print(json.dumps(out, indent=1, default=str))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
