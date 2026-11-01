"""Remark 3 regime: middle cluster at scale delta with eps << delta << 1 (larger than the outer clusters).
Also: locate the collinear triples of the even-base (x_i = 2i-n) k=8 variant."""
import sys
from fractions import Fraction
from math import isqrt
from extensions import build_general, report
from rconstruct import base_abscissae
from rg import collinear_triples
for k in (6, 8):
    xs = base_abscissae(k)
    print("k=%d, proof's base, middle at delta >> eps" % k)
    for E in (2 ** 16, 2 ** 24, 2 ** 32):
        eps = Fraction(1, E)
        r2 = isqrt(E); r4 = isqrt(r2)
        report("delta = eps^(1/2), eps=1/2^%d" % (E.bit_length() - 1), build_general(k, xs, eps, Fraction(1, r2)), k, xs)
        report("delta = eps^(1/4), eps=1/2^%d" % (E.bit_length() - 1), build_general(k, xs, eps, Fraction(1, r4)), k, xs)
k = 8; n = 6
xe = [2 * i - n for i in range(n + 1)]
cl = build_general(k, xe, Fraction(1, 2 ** 16), Fraction(1, 2 ** 32))
pts = [p for B in cl for p in B]
lab = {p: j for j, B in enumerate(cl) for p in B}
bad = collinear_triples(pts, stop_at_first=False)
print("even base k=8: %d collinear triples; cluster triples involved:" % len(bad),
      sorted(set(tuple(sorted(xe[lab[pts[i]]] for i in t)) for t in bad)))
# same thing with the proof's odd+0 base: none expected
cl2 = build_general(k, base_abscissae(k), Fraction(1, 2 ** 16), Fraction(1, 2 ** 32))
print("proof's base k=8: collinear triples:", len(collinear_triples([p for B in cl2 for p in B], stop_at_first=False)))
