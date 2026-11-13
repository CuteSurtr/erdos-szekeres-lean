#!/usr/bin/env python3
"""Exact check of cell-rule clauses on an exact 8-fold set.  B = 2 (default): Z(i,1) = [psi_i < pi/8], decided by
doubling the angle (w = v_i conj(p0); psi_i < pi/8 iff arg(w^2) < pi/4 iff det(w^2, zeta) > 0, in Z[sqrt2]).
B = 4 (env CELLB=4): Z(i,b) = [psi_i < b pi/16], b = 1, 2, 3, via arg(w^4) = 4 psi_i in (0, pi) compared with
pi/4 (b = 1), arg(w^2) with pi/4 (b = 2), arg(w^4) with 3 pi/4 (b = 3).
usage: [CELLB=4] check_cells.py SET.pts NV0 CLAUSEFILE..."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import label8 as L8
rows = L8.read_pts(sys.argv[1]); NV0 = int(sys.argv[2])
t, P, ids, reps = L8.label(rows)
E, val = L8.assignment(t, P, ids, reps)
p0 = reps[0]
def cmul(a, b):   # complex multiplication of (X, Y) pairs over Z[sqrt2]
    return (L8.zsub(L8.zmul(a[0], b[0]), L8.zmul(a[1], b[1])), L8.zadd(L8.zmul(a[0], b[1]), L8.zmul(a[1], b[0])))
conj0 = (p0[0], (-p0[1][0], -p0[1][1]))
zeta = ((0, 1), (0, 1))     # sqrt2*zeta = (1 + i): direction pi/4
zeta3 = ((0, -1), (0, 1))   # sqrt2*zeta^3 = (-1 + i): direction 3 pi/4
B = int(os.environ.get('CELLB', '2'))
for i in range(1, t):
    w = cmul(reps[i], conj0); w2 = cmul(w, w); w4 = cmul(w2, w2)
    if B == 2:
        d = L8.zsign(*L8.det(w2, zeta)); assert d != 0
        val[NV0 + i] = d > 0
    else:
        for b, (ww, zz) in ((1, (w4, zeta)), (2, (w2, zeta)), (3, (w4, zeta3))):
            d = L8.zsign(*L8.det(ww, zz)); assert d != 0
            val[NV0 + (i - 1) * 3 + b] = d > 0
bad = 0; n = 0
for f in sys.argv[3:]:
    for line in open(f):
        if not line.strip(): continue
        cl = [int(x) for x in line.split()[:-1]]
        n += 1
        if not any(val[abs(l)] == (l > 0) for l in cl):
            bad += 1
print('%s: t=%d, Z = %s, clauses %d, VIOLATED %d' % (os.path.basename(sys.argv[1]), t,
      ''.join('1' if val[NV0 + i] else '0' for i in range(1, t)) if B == 2 else 'B4', n, bad))
