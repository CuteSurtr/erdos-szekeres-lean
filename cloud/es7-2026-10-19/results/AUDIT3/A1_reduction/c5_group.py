#!/usr/bin/env python3
"""A1 audit: full symmetry group of SYMMAX/c5_31points.txt (exact arithmetic in Z[zeta5]).

The set is invariant under z -> zeta5 z.  Any affine symmetry fixes the centroid (= 0, the C5 centre).  The affine
symmetry group G is finite and contains the rotation R by 72 deg; an R-invariant symmetric bilinear form on R^2 is a
multiple of the Euclidean one (R has no real eigenvector), so the G-averaged form is Euclidean and G consists of
isometries fixing 0: maps z -> w z (rotations) and z -> w conj(z) (reflections), |w| = 1.  With p a fixed nonzero point
of S, w is determined by the image q of p: w = q conj(p) / N (rotation) or w = q p / N (reflection), N = p conj(p).
We test every q in S and count the maps that send S onto S.

usage: c5_group.py PATH_TO_c5_31points.txt
"""
import sys, json


def red(c):
    """reduce a coefficient list in powers z^0..z^k (k arbitrary) to the basis 1, z, z^2, z^3"""
    w = [0] * 5
    for i, a in enumerate(c):
        w[i % 5] += a
    # z^4 = -1 - z - z^2 - z^3
    return (w[0] - w[4], w[1] - w[4], w[2] - w[4], w[3] - w[4])


def mul(a, b):
    c = [0] * 7
    for i in range(4):
        for j in range(4):
            c[i + j] += a[i] * b[j]
    return red(c)


def conj(a):
    # z^k -> z^(5-k)
    c = [0] * 5
    c[0] = a[0]
    for k in range(1, 4):
        c[5 - k] += a[k]
    return red(c)


P = [tuple(int(x) for x in l.split()) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
S = set(P)
p = next(x for x in P if any(x))
N = mul(p, conj(p))
NS = {mul(N, w) for w in S}           # N * w for all w in S: membership of (num) / N  <=>  num in NS
rot, refl = [], []
for q in P:
    if not any(q):
        continue
    # rotation: z -> q conj(p) z / N
    a = mul(q, conj(p))
    if all(mul(a, z) in NS for z in P):
        rot.append(q)
    # reflection: z -> q p conj(z) / N
    b = mul(q, p)
    if all(mul(b, conj(z)) in NS for z in P):
        refl.append(q)
res = {"points": len(P), "rotations_found": len(rot), "reflections_found": len(refl),
       "group": ("C%d" % len(rot)) if not refl else ("D%d" % len(rot))}
# control: the rotation by 72 deg must be found (q = zeta5 * p)
zp = mul((0, 1, 0, 0), p)
res["control_rotation72_found"] = zp in rot
# control 2: a reflected copy of S (z -> conj z) must be found to have a reflection (S union conj S is D5-invariant
# only if it stays a set of points of the right kind; we just test the map conj on S u conj(S))
S2 = sorted(S | {conj(z) for z in S})
p2 = next(x for x in S2 if any(x)); N2 = mul(p2, conj(p2)); NS2 = {mul(N2, w) for w in S2}
res["control_conj_union_has_reflection"] = all(mul(mul(conj(p2), p2), conj(z)) in NS2 for z in S2) or \
    any(all(mul(mul(q, p2), conj(z)) in NS2 for z in S2) for q in S2 if any(q))
print(json.dumps(res))
sys.exit(0 if res["control_rotation72_found"] and res["control_conj_union_has_reflection"] else 1)
