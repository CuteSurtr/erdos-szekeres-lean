#!/usr/bin/env python3
"""Exact check that no hull vertex q of a Z[zeta_7] point set is 'deep' with respect to the inner points:
the vectors V_q = { c' - c : c, c' inner, orient(c, c', q) < 0 } do not lie in an open half-plane.
Certificate: three vectors of V_q with 0 strictly inside their triangle (all three cross products positive),
signs decided exactly in Z[zeta_7] (orient.py's ZetaSign).  Usage: deep_check.py PTSFILE NHULL"""
import sys, math, cmath
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from orient import ZetaSign, conj_mul, read_rows
M = 7
rows = [r + [0] * (M - len(r)) for r in read_rows(sys.argv[1])]
nh = int(sys.argv[2])
zs = ZetaSign(M)
z = cmath.exp(2j * math.pi / M)
fl = [sum(c * z ** j for j, c in enumerate(r)) for r in rows]
def sub(a, b): return [x - y for x, y in zip(a, b)]
def cross(a, b): return zs.sign_im(conj_mul(a, b, M))
def orient(i, j, k): return cross(sub(rows[j], rows[i]), sub(rows[k], rows[i]))
n = len(rows)
inner = list(range(nh, n))
# hull vertices: the first nh rows (outer layer) -- check exactly that they are extreme? done by inv.c (layers).
allok = True
for q in range(nh):
    V = []
    for c in inner:
        for d in inner:
            if c != d and orient(c, d, q) < 0:
                V.append((c, d))
    ang = sorted((cmath.phase(fl[d] - fl[c]), c, d) for c, d in V)
    # pick the vectors closest to angles a0, a0 + 2pi/3, a0 + 4pi/3 for a few offsets; verify exactly
    found = None
    for off in [i * 0.1 for i in range(63)]:
        pick = []
        for t in (off, off + 2 * math.pi / 3, off + 4 * math.pi / 3):
            t = (t + math.pi) % (2 * math.pi) - math.pi
            best = min(ang, key=lambda x: abs(cmath.phase(cmath.exp(1j * (x[0] - t)))))
            pick.append(best)
        vs = [sub(rows[d], rows[c]) for _, c, d in pick]
        s = [cross(vs[0], vs[1]), cross(vs[1], vs[2]), cross(vs[2], vs[0])]
        if s[0] == s[1] == s[2] != 0:
            found = [(c, d) for _, c, d in pick], s
            break
    gaps = [ang[i + 1][0] - ang[i][0] for i in range(len(ang) - 1)] + [ang[0][0] + 2 * math.pi - ang[-1][0]]
    print('q=%d |V_q|=%d max angular gap (float, info) = %.3f rad; exact certificate: %s' % (q, len(V), max(gaps), found))
    if not found:
        allok = False
print('ALL HULL VERTICES NON-DEEP (exact):', allok)
