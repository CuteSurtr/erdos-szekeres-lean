#!/usr/bin/env python3
"""Exact, complete scan of infinitesimal *orbit doublings* of an m-fold set (m = 3, 4).

Doubling orbit l with displacement direction d: every point p_k = g^k p of the orbit gets a twin
p_k + eps * g^k d (eps a symbolic infinitesimal).  The limit order type depends on d only through the position of d
relative to the rays of the vectors q - p (q in the set, q != p) -- the only orientations that change are
orient(p, p + eps d, q) = eps * cross(d, q - p) + O(eps^2) and their rotations -- so one direction strictly inside each
open arc between consecutive critical rays gives every limit order type.  Evaluated exactly (polyeval.c).

usage: double_exact.py M FILE [orbits e.g. 0,3,5 | all] [--remove l1,l2] [--keep-centre]
"""
import sys, os, ctypes, math, time
import numpy as np
from functools import cmp_to_key

HERE = os.path.dirname(os.path.abspath(__file__))
so = os.path.join(HERE, 'libpolyeval.so')
LIB = ctypes.CDLL(so)
LIB.poly_eval.restype = ctypes.c_int
LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
LIM = 1 << 60


def peval(points, kmax=8):
    """points: list of lists of terms (e, x, y)"""
    off = [0]; E = []; X = []; Y = []
    for p in points:
        for (e, x, y) in p:
            assert abs(x) < LIM and abs(y) < LIM, (x, y)
            E.append(e); X.append(x); Y.append(y)
        off.append(len(E))
    n = len(points)
    off = np.array(off, dtype=np.int32); E = np.array(E, dtype=np.int32)
    X = np.array(X, dtype=np.int64); Y = np.array(Y, dtype=np.int64)
    cnt = np.zeros(kmax + 1, dtype=np.int64); nz = np.zeros(1, dtype=np.int32)
    ml = LIB.poly_eval(n, off.ctypes.data, E.ctypes.data, X.ctypes.data, Y.ctypes.data, cnt.ctypes.data, kmax,
                       nz.ctypes.data)
    return ml, [int(c) for c in cnt], int(nz[0])


def read_set(fn, m):
    P = []
    for line in open(fn):
        line = line.split('#')[0].strip()
        if not line:
            continue
        w = list(map(int, line.split()))
        if m == 4:
            P.append((w[0] - w[2], w[1] - w[3]))
        elif len(w) == 2:
            P.append((w[0], w[1]))
        else:
            P.append((w[0] - w[2], w[1] - w[2]))
    return P


def rot(m, p):
    a, b = p
    return (-b, a) if m == 4 else (-b, a - b)


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def half(p):
    # 0 for angle in [0, 180), 1 for [180, 360)
    return 0 if (p[1] > 0 or (p[1] == 0 and p[0] > 0)) else 1


def angcmp(p, q):
    hp, hq = half(p), half(q)
    if hp != hq:
        return hp - hq
    c = cross(p, q)
    return -1 if c > 0 else (1 if c < 0 else 0)


def prim(p):
    g = math.gcd(abs(p[0]), abs(p[1]))
    return (p[0] // g, p[1] // g)


def orbits_of(P, m):
    """group points into rotation orbits; returns list of orbits [p, g p, ..., g^{m-1} p] and centre flag"""
    S = set(P); seen = set(); orbs = []; centre = False
    for p in P:
        if p == (0, 0):
            centre = True; continue
        if p in seen:
            continue
        o = [p]
        for _ in range(m - 1):
            o.append(rot(m, o[-1]))
        for q in o:
            assert q in S, 'not symmetric'
            seen.add(q)
        orbs.append(o)
    # sort by norm (outermost first) using a quadratic form that is rotation invariant
    if m == 4:
        nrm = lambda p: p[0] ** 2 + p[1] ** 2
    else:
        nrm = lambda p: p[0] ** 2 - p[0] * p[1] + p[1] ** 2
    orbs.sort(key=lambda o: -nrm(o[0]))
    return orbs, centre


def critical_arcs(dirs):
    dirs = sorted(set(prim(d) for d in dirs if d != (0, 0)), key=cmp_to_key(angcmp))
    C = []
    for d in dirs:
        if C and angcmp(C[-1], d) == 0:
            continue
        C.append(d)
    cands = []
    for i in range(len(C)):
        a = C[i]; b = C[(i + 1) % len(C)]
        if cross(a, b) > 0:
            cands.append((a[0] + b[0], a[1] + b[1]))
        else:  # gap >= 180 degrees: use a perpendicular-ish vector
            cands.append((-a[1], a[0]) if cross(a, (-a[1], a[0])) > 0 and cross((-a[1], a[0]), b) > 0 else (a[0] + b[0], a[1] + b[1]))
    return cands


def doubled_config(orbs, centre, m, l, d):
    pts = []
    for o in orbs:
        for p in o:
            pts.append([(0, p[0], p[1])])
    if centre:
        pts.append([(0, 0, 0)])
    dk = d
    for k, p in enumerate(orbs[l]):
        pts.append([(0, p[0], p[1]), (1, dk[0], dk[1])])
        dk = rot(m, dk)
    return pts


def main():
    m = int(sys.argv[1]); fn = sys.argv[2]
    which = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 'all'
    P = read_set(fn, m)
    orbs, centre = orbits_of(P, m)
    if '--remove' in sys.argv:
        rem = set(int(x) for x in sys.argv[sys.argv.index('--remove') + 1].split(','))
        orbs = [o for i, o in enumerate(orbs) if i not in rem]
    if '--no-centre' in sys.argv:
        centre = False
    if '--add-centre' in sys.argv:
        centre = True
    t = len(orbs)
    base = [[(0, p[0], p[1])] for o in orbs for p in o] + ([[(0, 0, 0)]] if centre else [])
    ml0, cnt0, nz0 = peval(base)
    print('%s m=%d orbits=%d centre=%s base: maxlen=%d n8=%d zero=%d' % (os.path.basename(fn), m, t, centre, ml0,
                                                                         cnt0[8], nz0), flush=True)
    L = range(t) if which == 'all' else [int(x) for x in which.split(',')]
    allp = [p for o in orbs for p in o] + ([(0, 0)] if centre else [])
    tot_free = 0; t0 = time.time(); overall = None
    for l in L:
        p0 = orbs[l][0]
        dirs = [(q[0] - p0[0], q[1] - p0[1]) for q in allp if q != p0]
        dirs += [(-x, -y) for (x, y) in dirs]
        cands = critical_arcs(dirs)
        best = None; free = []
        for d in cands:
            pts = doubled_config(orbs, centre, m, l, d)
            ml, cnt, nz = peval(pts)
            if nz:
                continue
            if best is None or cnt[8] < best[0]:
                best = (cnt[8], d, ml)
            if cnt[8] == 0:
                free.append(d)
        tot_free += len(free)
        if best and (overall is None or best[0] < overall[0]):
            overall = (best[0], l, best[1])
        print('  orbit %2d: arcs=%d best n8=%s free=%d %s' % (l, len(cands), best[0] if best else None, len(free),
                                                          ('FREE ' + str(free[:3])) if free else ''), flush=True)
    print('DONE %s total_free=%d best=%s time=%.0fs' % (os.path.basename(fn), tot_free, overall, time.time() - t0),
          flush=True)


if __name__ == '__main__':
    main()
