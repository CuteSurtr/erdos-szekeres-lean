#!/usr/bin/env python3
"""Random real-configuration validation of clause files + exact check on the certified 54-point set.
usage: lr_validate.py NCONF clausefile [clausefile ...]
Configurations: 10 nested regular hexagons, theta_0 = 0, theta_i in (0,60) (uniform / near 0 or 60 / clustered),
radii r_j = u_j * r_{j-1} cos30 / cos(delta_j) (layer j strictly inside conv(layer j-1); u_j uniform / near 1 /
tiny, multi-scale).  Orientation of every canonical triple from the exact (D,E) linear form of math_linear.py,
float64 with an mpmath (60 digits) recomputation for near-zero values."""
import sys, os, json, math, importlib.util
import numpy as np
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lr_core as C
E = C.E
R = C.R
_s = importlib.util.spec_from_file_location('ml', R + '/ROTREFINE20261104/math_linear.py'); ML = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ML)
VS = ML.variables(10); IX = {v: j for j, v in enumerate(VS)}
TS = sorted(E.tvar, key=lambda T: E.tvar[T]); NT = len(TS)
M = np.zeros((NT, len(VS)))
for r, T in enumerate(TS):
    for j, c in ML.form(T, IX).items():
        M[r, j] = c
MA = np.abs(M)


def de_vec(r, th, prec=False):
    out = []
    for v in VS:
        k, i, j = v
        if prec:
            d = mp.radians(th[j] - th[i]); x = r[i] * r[j] * (mp.cos(d) if k == 'D' else mp.sin(d) / mp.sqrt(3))
        else:
            d = math.radians(th[j] - th[i]); x = r[i] * r[j] * (math.cos(d) if k == 'D' else math.sin(d) / math.sqrt(3))
        out.append(x)
    return out


def config(rng):
    mode_t = rng.integers(3); mode_r = rng.integers(3)
    th = [0.0]
    c = rng.uniform(0, 60)
    for i in range(1, 10):
        if mode_t == 0:
            x = rng.uniform(0, 60)
        elif mode_t == 1:
            e = 60 * 10 ** (-rng.uniform(0.5, 5)); x = e if rng.random() < 0.5 else 60 - e
            if rng.random() < 0.3:
                x = rng.uniform(0, 60)
        else:
            e = 10 ** (-rng.uniform(0.3, 5)) * (1 if rng.random() < 0.5 else -1); x = min(max(c + e, 1e-6), 60 - 1e-6)
        th.append(x)
    r = [1.0]
    for j in range(1, 10):
        x = (th[j] - th[j - 1] - 30) % 60; dl = min(x, 60 - x)
        cap = r[-1] * math.cos(math.radians(30)) / math.cos(math.radians(dl))
        m = mode_r if rng.random() < 0.8 else rng.integers(3)
        if m == 0:
            u = rng.uniform(0.02, 1)
        elif m == 1:
            u = 1 - 10 ** (-rng.uniform(1, 6))
        else:
            u = 10 ** (-rng.uniform(0.3, 1.5))
        r.append(u * cap)
    return r, th


def assignment(r, th):
    x = np.array(de_vec(r, th)); val = M @ x; scale = MA @ np.abs(x)
    bad = np.where(np.abs(val) < 1e-9 * scale)[0]
    sgn = np.sign(val)
    if len(bad):
        mp.mp.dps = 60
        xp = de_vec([mp.mpf(z) for z in r], [mp.mpf(z) for z in th], prec=True)
        for b in bad:
            v = mp.fsum(M[b, j] * xp[j] for j in np.nonzero(M[b])[0])
            sgn[b] = 1 if v > 0 else (-1 if v < 0 else 0)
    true = set(int(E.tvar[TS[k]]) for k in range(NT) if sgn[k] > 0)
    if (sgn == 0).any():
        return None
    for (i, j), y in E.Y.items():
        if th[i] < th[j]:
            true.add(y)
    return true, len(bad)


def holds(cl, true):
    return any((l > 0) == (abs(l) in true) for l in cl)


def pts54():
    """exact assignment of the certified 54-point set (layers 0..8): oblique integer coordinates"""
    P = []
    for line in open(R + '/ES8SYM/sets/c6_54pts_9layers.pts'):
        if line.startswith('#') or not line.strip():
            continue
        w = list(map(int, line.split()))
        P.append((w[0] - w[2] - w[3] + w[5], w[1] + w[2] - w[4] - w[5]))
    det = lambda p, q: p[0] * q[1] - p[1] * q[0]       # positive multiple of the real determinant
    dot2 = lambda p, q: 2 * p[0] * q[0] + p[0] * q[1] + p[1] * q[0] + 2 * p[1] * q[1]   # 2*dot
    rot = lambda p: (-p[1], p[0] + p[1])
    n2 = lambda p: dot2(p, p)
    radii = sorted({n2(p) for p in P}, reverse=True); assert len(radii) == 9
    layer = {}
    for p in P:
        layer.setdefault(radii.index(n2(p)), []).append(p)
    u0 = layer[0][0]; wu0 = rot(u0)
    def in_sector(p):   # relative angle in [0,60)
        return det(u0, p) >= 0 and dot2(u0, p) > 0 and det(wu0, p) < 0
    pt = {}
    for i in range(9):
        seeds = [p for p in layer[i] if in_sector(p)]; assert len(seeds) == 1, (i, seeds)
        z = seeds[0]
        for k in range(6):
            pt[6 * i + k] = z; z = rot(z)
    true = set(); vmax = E.tvar
    for T, v in E.tvar.items():
        if max(T) >= 54:
            continue
        a, b, c = (pt[x] for x in T)
        o = det(a, b) + det(b, c) + det(c, a); assert o != 0
        if o > 0:
            true.add(v)
    for (i, j), y in E.Y.items():
        if j <= 8 and det(pt[6 * i], pt[6 * j]) > 0:
            true.add(y)
    # nesting check: is every layer j > i strictly inside conv(layer i)?
    nest_ok = all(det((pt[6*i+1][0]-pt[6*i][0], pt[6*i+1][1]-pt[6*i][1]), (pt[6*j+l][0]-pt[6*i][0], pt[6*j+l][1]-pt[6*i][1])) > 0
                  for i in range(9) for j in range(i + 1, 9) for l in range(6))
    return true, nest_ok


def clause_in54(cl):
    for l in cl:
        v = abs(l)
        if v <= C.NT:
            if max(C.INV[v]) >= 54:
                return False
        else:
            (i, j) = next(k for k, y in E.Y.items() if y == v)
            if j > 8:
                return False
    return True


def main():
    n = int(sys.argv[1]); files = sys.argv[2:]
    cls = {f: [list(map(int, l.split()))[:-1] for l in open(f) if l.strip() and not l.startswith(('c', 'p'))] for f in files}
    rng = np.random.default_rng(20261105)
    viol = {f: {} for f in files}; done = 0; mpfix = 0; skipped = 0
    while done < n:
        r, th = config(rng)
        a = assignment(r, th)
        if a is None:
            skipped += 1; continue
        true, nb = a; mpfix += nb; done += 1
        for f in files:
            for c in cls[f]:
                if not holds(c, true):
                    viol[f][tuple(c)] = viol[f].get(tuple(c), 0) + 1
    true54, nest_ok = pts54()
    rep = {'configs': done, 'skipped_degenerate': skipped, 'mp_recomputed_values': mpfix, '54pt_nested': nest_ok}
    for f in files:
        c54 = [c for c in cls[f] if clause_in54(c)]
        bad54 = [c for c in c54 if not holds(c, true54)]
        rep[os.path.basename(f)] = {'clauses': len(cls[f]), 'violated_clauses': len(viol[f]),
                                    'examples': [list(k) for k in list(viol[f])[:10]],
                                    '54pt_clauses_checked': len(c54), '54pt_violated': len(bad54), '54pt_examples': bad54[:10]}
    print(json.dumps(rep, indent=1))


if __name__ == '__main__':
    main()
