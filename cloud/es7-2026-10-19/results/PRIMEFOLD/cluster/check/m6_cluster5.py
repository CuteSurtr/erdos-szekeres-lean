#!/usr/bin/env python3
"""Lower bound N(6) >= 5 of Theorem E, checked exactly.

A 5-point cluster C (rational coordinates, outward radial frame of v_0 = (1, 0)) found by a floating-point search.
This script checks it exactly: Proposition C (i) from the definition (sound_te.direct_profile), the Lemma 1 formula
over all base polygons of the hexagon (e2e.formula), and then the actual 6-fold set S_e = union_j R^j(v_0 + e C)
(30 points, exact coordinates in Z[sqrt 3]) for three values of e: general position and the exact largest convex
subset (e2e.mc_exact raises an error on a collinear triple).
With an argument SIGNS it also writes the orientation signs of S_e (e = 1/10^13) in the format read by
../../check64/cvxenum, which counts the convex k-subsets a second way.
Usage: python3 -I m6_cluster5.py [SIGNS]   (about a second; output in m6_cluster5_exact.log)
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import e2e, sound_te as st

Cs = [('3544133193619/250000000000', '15081955227/8000000000'),
      ('131767003059/100000000000', '-1157690931191/1000000000000'),
      ('201640221411/100000000000', '-7093188889/50000000000'),
      ('-442606999403/125000000000', '286647962601/250000000000'),
      ('-2442999636277/500000000000', '253844340681/1000000000000')]
C_fr = [(Fr(x), Fr(y)) for x, y in Cs]
Den = 10**12
C = [(int(x * Den), int(y * Den)) for x, y in C_fr]
assert all(Fr(a, Den) == x and Fr(b, Den) == y for (a, b), (x, y) in zip(C, C_fr))
m = 6
g, h, F11 = st.direct_profile(C_fr, m)
fval, cond_i, g2, h2 = e2e.formula(C_fr, m)
print('m=6 cluster of 5 points: F11=%d g=%s h=%s (i)=%s formula max=%d' % (
    F11, [g[x] for x in range(1, m)], [h[x] for x in range(1, m)], cond_i, fval))
for E in (10**9, 10**13, 10**17):
    pts, d = e2e.build_set(C, m, E, Den)
    print('e = 1/%d: |S_e| = %d, exact mc(S_e) = %d' % (E, len(pts), e2e.mc_exact(pts, d)))
if len(sys.argv) > 1:
    pts, d = e2e.build_set(C, m, 10**13, Den)
    n = len(pts)
    signs = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = pts[i], pts[j], pts[k]
                det = e2e.sub(e2e.mul(e2e.sub(b[0], a[0]), e2e.sub(c[1], a[1]), d),
                              e2e.mul(e2e.sub(b[1], a[1]), e2e.sub(c[0], a[0]), d))
                s = e2e.sgn_sqrt(det[0], det[1], d)
                assert s != 0
                signs.append('+' if s > 0 else '-')
    with open(sys.argv[1], 'w') as fh:
        fh.write('%d\n%s\n' % (n, ''.join(signs)))
    print('wrote the signs of S_e (e = 1/10^13) to %s' % __import__('os').path.basename(sys.argv[1]))
