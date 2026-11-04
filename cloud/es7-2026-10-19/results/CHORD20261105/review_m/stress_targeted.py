#!/usr/bin/env python3
"""Targeted corner stress test: for every clause and every full phase case of its triple's layers that falsifies the
condition part, place the phases within eps (1e-9 .. 1e-14 degrees) of every corner of the case region (and at its
centroid), with radius ratios lam in {1e-12, 1e-6, 0.5, 1-1e-12, 1+1e-12, 2, 1e6, 1e12} (radius-free claim: all lam),
compute the REAL Y/H values from the phases (must reproduce the case) and the real orientation at 80 digits, and
evaluate the clause.  Usage: stress_targeted.py m t CLAUSEFILE"""
import sys, itertools
import mpmath as mp
sys.path.insert(0, '<rot45-work-dir>/review_m')
from verify_exact import numbering
mp.mp.dps = 80
m, t, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
odd = m % 2 == 1
tv, inv, Y, H = numbering(m, t)
ntr = len(tv)
W = mp.mpf(360) / m
u = mp.mpf(180) / m
P = u if odd else W
lams = [mp.mpf('1e-12'), mp.mpf('1e-6'), mp.mpf('0.5'), 1 - mp.mpf('1e-12'), 1 + mp.mpf('1e-12'), mp.mpf(2),
        mp.mpf('1e6'), mp.mpf('1e12')]
epss = [mp.mpf('1e-9'), mp.mpf('1e-14')]
nev = viol = mismatch = 0
for line in open(fn):
    cl = [int(x) for x in line.split()[:-1]]
    lit = [x for x in cl if abs(x) <= ntr][0]
    C = inv[abs(lit)]
    S = sorted({x // m for x in C})
    nz = [L for L in S if L != 0]
    # candidate psi tuples for the layers (independent of the case; the case is read off afterwards)
    for eps in epss:
        cands = set()
        if len(nz) == 0:
            cands.add(())
        elif len(nz) == 1:
            for p in (eps, P / 2, P - eps):
                cands.add((p,))
        else:
            vals = [eps, 2 * eps, P / 2, P - 2 * eps, P - eps]
            for a in vals:
                for b in vals:
                    if a != b:
                        cands.add((a, b))
            for a in vals:          # near-equal psi
                cands.add((a, a + eps / 7)) if a + eps / 7 < P else None
                cands.add((a + eps / 7, a)) if a + eps / 7 < P else None
        hopts = list(itertools.product([True, False], repeat=len(nz))) if odd else [tuple(True for _ in nz)]
        for ps in cands:
            for hs in hopts:
                th = {0: mp.mpf(0)}
                psi = {0: mp.mpf(0)}
                for L, p, h in zip(nz, ps, hs):
                    psi[L] = p
                    th[L] = p + (0 if (h or not odd) else u)
                # real assignment of condition vars
                val = {}
                for a, b in itertools.combinations(nz, 2):
                    val[Y[(a, b)]] = psi[a] < psi[b]
                if odd:
                    for L in nz:
                        val[H[L]] = th[L] < u
                cond_true = any(val[abs(x)] == (x > 0) for x in cl if abs(x) > ntr)
                if cond_true:
                    continue
                unit = []
                for x in C:
                    L, k = divmod(x, m)
                    a = mp.radians(th[L] + W * k)
                    unit.append((L, mp.cos(a), mp.sin(a)))
                for lam in (lams if len(S) == 2 else [mp.mpf(1)]):
                    rr = {S[0]: mp.mpf(1), S[-1]: lam if len(S) == 2 else mp.mpf(1)}
                    (ax, ay), (bx, by), (cx, cy) = [(rr[L] * c_, rr[L] * s_) for L, c_, s_ in unit]
                    o = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
                    nev += 1
                    if abs(o) < mp.mpf(10) ** -60 * max(1, lam) ** 2:
                        mismatch += 1      # numerically degenerate; not counted
                        continue
                    if (o > 0) != (lit > 0):
                        viol += 1
                        if viol <= 10:
                            print('VIOLATION', cl, 'psi', {k: mp.nstr(v, 20) for k, v in psi.items()}, 'H', hs,
                                  'lam', mp.nstr(lam, 5), 'orient', mp.nstr(o, 10), flush=True)
print('%s: %d targeted evaluations with condition part false, %d violations, %d numerically degenerate skipped' %
      (fn, nev, viol, mismatch))
