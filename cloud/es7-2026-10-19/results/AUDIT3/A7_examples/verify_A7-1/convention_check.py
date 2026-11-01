#!/usr/bin/env python3
"""Part 2 of the A7-1 re-check.
(1) Which embedding does the project's verifier (SYMMAX/verify5.py) implement?  Load only its function definitions
    (the source before 'path, k = sys.argv', exactly as SYM5/validate_layers.py does; nothing is written) and compare its
    orientation sign with this directory's exact orientation for zeta -> exp(2 pi i j/5), j = 1..4, on every triple.
(2) 3-fold / 6-fold files: integer pairs (a, b) = a + b w, w = exp(2 pi i/3).  Check closure under the integer maps
    R3(a,b) = (-b, a-b) and R6(a,b) = (a-b, a), their orders, that they are not orthogonal, that M(a,b) = (a - b/2, b sqrt3/2)
    conjugates them to the Euclidean rotations by 120 / 60 degrees (80-digit numerics), and that the integer
    orientation equals the orientation of the M-images on every triple (det M = sqrt3/2 > 0).
"""
import os
import sys
from decimal import Decimal, getcontext
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import embed_check as E   # this directory's independent exact code

R = E.R
src = open(R + "/SYMMAX/verify5.py").read().split("path, k = sys.argv")[0]
V = {}
exec(src, V)

print("(1) project verify5.py orientation vs exact embedding j")
for name, path, K in E.FILES:
    pts = E.parse(path)
    P5 = [V["norm"](list(c)) for c in pts]
    n = len(pts)
    res = []
    for j in (1, 2, 3, 4):
        Pj = [E.planar_exact(c, j) for c in pts]
        agree = tot = 0
        for a, b, c in combinations(range(n), 3):
            tot += 1
            agree += (V["orient"](P5[a], P5[b], P5[c]) == E.orient_exact(Pj[a], Pj[b], Pj[c]))
        res.append("j=%d: %d/%d agree" % (j, agree, tot))
    print("  %-18s %s" % (name, "; ".join(res)))

print()
print("(2) Eisenstein-coordinate files")
getcontext().prec = 80
S3 = Decimal(3).sqrt()
R3 = lambda p: (-p[1], p[0] - p[1])
R6 = lambda p: (p[0] - p[1], p[0])
M = lambda p: (Decimal(p[0]) - Decimal(p[1]) / 2, Decimal(p[1]) * S3 / 2)
c120, s120 = Decimal(-1) / 2, S3 / 2
c60, s60 = Decimal(1) / 2, S3 / 2


def matrix(f):
    a, b = f((1, 0)), f((0, 1))
    return ((a[0], b[0]), (a[1], b[1]))


def order(f):
    p, k = (1, 0), 0
    q, r = (0, 1), (0, 1)
    pp = (1, 0)
    while True:
        k += 1
        pp, r = f(pp), f(r)
        if pp == (1, 0) and r == (0, 1):
            return k


for G, f, (cr, sr) in (("3", R3, (c120, s120)), ("6", R6, (c60, s60))):
    m = matrix(f)
    mtm = ((m[0][0] ** 2 + m[1][0] ** 2, m[0][0] * m[0][1] + m[1][0] * m[1][1]),
           (m[0][0] * m[0][1] + m[1][0] * m[1][1], m[0][1] ** 2 + m[1][1] ** 2))
    print("  R%s matrix %s, order %d, M^T M = %s (orthogonal: %s)" % (G, m, order(f), mtm, mtm == ((1, 0), (0, 1))))

for name, rel, G in (("c3_27", "SYMMAX/c3_27points.txt", "3"), ("c3_30", "SYMMAX/c3_30points.txt", "3"),
                     ("c3_31", "SYMMAX/c3_31points.txt", "3"), ("c6_30", "SYMMAX/c6_30points.txt", "6"),
                     ("k6/c3_13", "SYMMAX/k6/c3_13points.txt", "3")):
    pts = [tuple(int(x) for x in l.split()) for l in open(R + "/" + rel) if l.strip() and not l.startswith("#")]
    S = set(pts)
    f = R3 if G == "3" else R6
    cr, sr = (c120, s120) if G == "3" else (c60, s60)
    closed = all(f(p) in S for p in pts)
    closed3 = all(R3(p) in S for p in pts)
    conj_err = Decimal(0)
    for p in pts:
        x, y = M(p)
        X, Y = M(f(p))
        conj_err = max(conj_err, abs(x * cr - y * sr - X), abs(x * sr + y * cr - Y))
    n = len(pts)
    mism = 0
    for a, b, c in combinations(range(n), 3):
        pa, pb, pc = pts[a], pts[b], pts[c]
        oi = (pb[0] - pa[0]) * (pc[1] - pa[1]) - (pb[1] - pa[1]) * (pc[0] - pa[0])
        A, B, C = M(pa), M(pb), M(pc)
        od = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
        mism += ((oi > 0) - (oi < 0)) != ((od > 0) - (od < 0))
    print("  %-9s n=%d closed under R%s: %s (under R3: %s); |rot(M p) - M(R p)| max %.1e; "
          "integer vs Euclidean orientation mismatches: %d" % (name, n, G, closed, closed3, conj_err, mism))
