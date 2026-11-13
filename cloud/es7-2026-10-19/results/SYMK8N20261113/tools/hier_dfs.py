#!/usr/bin/env python3
"""Exhaustive DFS over *scale-separated* (hierarchical) m-fold configurations: orbit j lies at scale eps^(2j)
(eps -> 0), orbit 0 outermost; every orbit is a regular m-gon {g^k v_j}.  For generic directions the limit order
type depends on the direction of each new innermost orbit only through its position among the critical directions
(points of the existing orbits, and their images under the edge factors of the new polygon; plus the antipodal
case for even m), taken modulo the rotation group.  The DFS adds innermost orbits one at a time, one direction per
open critical arc, prunes configurations with a convex octagon, and reports the largest depth and the number of
octagon-free configurations per depth (with an optional centre for odd m).
usage: hier_dfs.py M [--centre] [--K 8] [--maxdepth 30]
"""
import sys, os, time
from functools import cmp_to_key
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import double_exact as DE
import ctypes
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval, rot, cross, prim

m = int(sys.argv[1])
centre = '--centre' in sys.argv
K = int(sys.argv[sys.argv.index('--K') + 1]) if '--K' in sys.argv else 8
maxdepth = int(sys.argv[sys.argv.index('--maxdepth') + 1]) if '--maxdepth' in sys.argv else 40


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
    if m == 3:
        return [p, (2 * p[0] - p[1], p[0] + p[1]), (p[0] + p[1], 2 * p[1] - p[0]), (p[0] - 2 * p[1], 2 * p[0] - p[1])]
    raise ValueError


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
    if not D:
        return [(1, 0)] if m == 4 else [(2, 1)]
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
    if centre:
        P.append([(0, 0, 0)])
    return P


counts = {}
best = [0, None]
nodes = [0]
t0 = time.time()


def dfs(vs):
    d = len(vs)
    counts[d] = counts.get(d, 0) + 1
    if d > best[0]:
        best[0] = d; best[1] = list(vs)
        print('depth %d reached (%.0fs, nodes %d): %s' % (d, time.time() - t0, nodes[0], vs), flush=True)
    if d >= maxdepth:
        return
    for v in arcs(vs):
        # keep coordinates small: primitive direction, scaled copies are irrelevant (scale separated)
        nodes[0] += 1
        ml, cnt, nz = peval(pts_of(vs + [v]), K)
        if nz:
            continue
        if cnt[K] == 0:
            dfs(vs + [v])


# first orbit: direction irrelevant up to rotation; take (1, 0) for m = 4, (1, 0) for m = 3 (oblique)
dfs([(1, 0)] if m == 4 else [(1, 0)])
print('DONE m=%d centre=%s K=%d best depth=%d nodes=%d counts=%s time=%.0fs' % (m, centre, K, best[0], nodes[0],
      dict(sorted(counts.items())), time.time() - t0), flush=True)
print('example:', best[1])
