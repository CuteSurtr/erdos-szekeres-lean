#!/usr/bin/env python3
"""Enumerate ALL scale-separated m-fold configurations with s levels (generic phases; one direction per open
critical arc at each level, no pruning) and count how many contain a convex K-gon.  If none does for a given s,
then every necessary condition that involves at most s layers at a time is satisfied by fully scale-separated
configurations of every length t (their s-layer subsets are again scale-separated with generic phases), so such
conditions alone cannot bound the number of layers.
usage: hier_all.py M K SMAX"""
import sys, os, time
from functools import cmp_to_key
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctypes
import double_exact as DE
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval, rot, cross, prim

m = int(sys.argv[1]); K = int(sys.argv[2]); SMAX = int(sys.argv[3])


def in_sector(p):
    return p[0] > 0 and p[1] >= 0


def to_sector(p):
    for _ in range(m):
        if in_sector(p):
            return p
        p = rot(m, p)
    raise ValueError(p)


def facs(p):
    if m == 4:
        return [p, (p[0] - p[1], p[0] + p[1]), (p[0] + p[1], p[1] - p[0])]
    return [p, (2 * p[0] - p[1], p[0] + p[1]), (p[0] + p[1], 2 * p[1] - p[0]), (p[0] - 2 * p[1], 2 * p[0] - p[1])]


def arcs(vs):
    crit = set()
    for v in vs:
        for w in facs(v):
            for s in (1, -1):
                crit.add(prim(to_sector((s * w[0], s * w[1]))))
    C = sorted(crit, key=cmp_to_key(lambda p, q: -1 if cross(p, q) > 0 else (1 if cross(p, q) < 0 else 0)))
    D = []
    for d in C:
        if D and cross(D[-1], d) == 0:
            continue
        D.append(d)
    out = []
    for i in range(len(D)):
        a = D[i]; b = D[i + 1] if i + 1 < len(D) else rot(m, D[0])
        out.append(prim((a[0] + b[0], a[1] + b[1])))
    return out


def pts_of(vs):
    P = []
    for j, v in enumerate(vs):
        q = v
        for _ in range(m):
            P.append([(j, q[0], q[1])])
            q = rot(m, q)
    return P


t0 = time.time()
level = [[(1, 0)]]
for s in range(2, SMAX + 1):
    nxt = []
    for vs in level:
        for v in arcs(vs):
            nxt.append(vs + [v])
    bad = 0; mx = 0
    for vs in nxt:
        ml, cnt, nz = peval(pts_of(vs), K)
        if nz:
            raise SystemExit('degenerate')
        if cnt[K]:
            bad += 1
        mx = max(mx, ml)
    print('m=%d K=%d levels=%d: configurations=%d, with a convex %d-gon: %d, largest convex subset over all: %d (%.0fs)'
          % (m, K, s, len(nxt), K, bad, K, mx, time.time() - t0), flush=True)
    level = nxt
    if len(level) > 200000:
        print('stop (too many)'); break
