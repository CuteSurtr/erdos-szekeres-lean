#!/usr/bin/env python3
"""Evidence: random real configurations of t nested regular octagons (random phases in any order, random strictly
decreasing radii over many scales) must satisfy every clause of the given clause files that uses only triple-orbit
and Y variables (float orientations with a margin filter: triples with |normalized orientation| < 1e-9 are skipped
by skipping the configuration).  usage: rand_check.py t N CLAUSEFILE..."""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
t, N = int(sys.argv[1]), int(sys.argv[2])
E = gen.Enc(8, 9, t)
vs = sorted(E.tvar.values()); inv = {v: C for C, v in E.tvar.items()}
T = np.array([inv[v] for v in vs]); L = T // 8; K = T % 8
files = sys.argv[3:]
cls = []
for f in files:
    for line in open(f):
        if line.strip():
            cls.append([int(x) for x in line.split()[:-1]])
rng = np.random.default_rng(12345)
nbad = 0; ncfg = 0; nskip = 0; vmin = None
for s in range(N):
    th = np.concatenate([[0.0], rng.uniform(0, math.pi / 4, t - 1)])
    if s % 3 == 0:
        lr = -np.cumsum(rng.exponential(rng.choice([0.01, 0.3, 2.0]), t)); lr -= lr[0]
    else:
        lr = -np.sort(rng.uniform(0, rng.choice([0.5, 3, 12]), t)); lr[0] = 0; lr = np.sort(lr)[::-1]
    if os.environ.get('EXTREME'):     # near-generator radii: levels separated by huge factors, tiny steps inside
        k = int(rng.integers(1, t)); k2 = int(rng.integers(k, t + 1))
        gap = rng.choice([5.0, 12.0, 25.0])
        lr = -np.arange(t) * 1e-4 - gap * (np.arange(t) >= k) - gap * (np.arange(t) >= k2)
    if np.any(np.diff(lr) >= 0):
        nskip += 1; continue
    if os.environ.get('NEST'):        # keep only configurations whose octagons are convex layers (L_{i+1} inside conv L_i)
        ok = True
        for i in range(t - 1):
            A = np.exp(lr[i] + 1j * (th[i] + 2 * np.pi * np.arange(8) / 8)); Bv = np.exp(lr[i + 1] + 1j * (th[i + 1] + 2 * np.pi * np.arange(8) / 8))
            for k in range(8):
                e0, e1 = A[k], A[(k + 1) % 8]
                if np.any((np.conj(e1 - e0) * (Bv - e0)).imag <= 0):
                    ok = False; break
            if not ok: break
        if not ok:
            nskip += 1; continue
    z = np.exp(lr + 1j * th)
    P = z[L] * np.exp(2j * np.pi * K / 8)
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    o = (np.conj(b - a) * (c - a)).imag
    sc = np.maximum(np.maximum(abs(b - a), abs(c - b)), abs(a - c)) ** 2
    if np.min(np.abs(o) / sc) < 1e-9:
        nskip += 1; continue
    val = {v: bool(o[q] > 0) for q, v in enumerate(vs)}
    for (i, j), y in E.Y.items():
        val[y] = bool(th[i] < th[j])
    if os.environ.get('NV0'):          # cell-rule bin variables Z(i,b) = [psi_i < b (pi/4)/B], B from env CELLB
        B = int(os.environ.get('CELLB', '2'))
        for i in range(1, t):
            for b in range(1, B):
                val[int(os.environ['NV0']) + (i - 1) * (B - 1) + b] = bool(th[i] < b * math.pi / 4 / B)
    ncfg += 1
    for ci, cl in enumerate(cls):
        if all(abs(l) in val for l in cl) and not any(val[abs(l)] == (l > 0) for l in cl):
            nbad += 1
            vmin = ci if vmin is None else min(vmin, ci)
            if nbad <= 3:
                print('VIOLATED clause #%d' % ci, cl, 'cfg', s)
print('configurations checked %d (skipped %d), clauses %d, violations %d%s' % (ncfg, nskip, len(cls), nbad,
      '' if vmin is None else ' (smallest violated clause index %d)' % vmin))
