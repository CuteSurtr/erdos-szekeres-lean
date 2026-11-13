#!/usr/bin/env python3
"""Exact limit order types for 5-fold polynomial configurations in Z[zeta_5][eps, 1/eps], and the doubling /
new-level scans of double_exact.py / twostep.py for m = 5.

An element of Z[zeta] is a 5-tuple c (sum c_j zeta^j), reduced so that c_4 = 0 (1 + zeta + ... + zeta^4 = 0).
cr(a, b) = Im(conj(a) b) = (C1 - C4) s1 + (C2 - C3) s2 with C_d the coefficients of conj(a) b, s1 = sin 72,
s2 = sin 144 = s1 (sqrt5 - 1)/2; so cr is a positive multiple of X + Y sqrt5 with X = 2(C1 - C4) - (C2 - C3),
Y = C2 - C3.  Signs of X + Y sqrt5 are decided exactly.  Re z = c0 + (c1 + c4)(sqrt5 - 1)/4 - (c2 + c3)(sqrt5 + 1)/4,
Im z is a positive multiple of 2(c1 - c4) - (c2 - c3) + (c2 - c3) sqrt5.  The convex-polygon DP is cvxdp.c.
usage: z5.py FILE.pts [double|levels|both] [--remove i]
"""
import sys, os, ctypes, time, math
import numpy as np
from functools import cmp_to_key

HERE = os.path.dirname(os.path.abspath(__file__))
so = os.path.join(HERE, 'libcvxdp.so')
if not os.path.exists(so):
    os.system('gcc -O2 -shared -fPIC -o %s %s' % (so, os.path.join(HERE, 'cvxdp.c')))
CV = ctypes.CDLL(so)
CV.cvx_dp.restype = ctypes.c_int
CV.cvx_dp.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]


def red(c):
    c = list(c)
    t = c[4]
    return (c[0] - t, c[1] - t, c[2] - t, c[3] - t, 0)


def add(a, b):
    return red(tuple(x + y for x, y in zip(a, b)))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    r = [0] * 5
    for i in range(5):
        if a[i]:
            for j in range(5):
                r[(i + j) % 5] += a[i] * b[j]
    return red(r)


def conj(a):
    return red((a[0], a[4], a[3], a[2], a[1]))


def rotz(a):  # multiply by zeta
    return red((a[4], a[0], a[1], a[2], a[3]))


def sgn5(X, Y):
    """sign of X + Y sqrt5"""
    if X >= 0 and Y >= 0:
        return 0 if X == 0 and Y == 0 else 1
    if X <= 0 and Y <= 0:
        return -1
    d = X * X - 5 * Y * Y
    if X > 0:
        return 1 if d > 0 else (-1 if d < 0 else 0)
    return -1 if d > 0 else (1 if d < 0 else 0)


def crq(a, b):
    """cr(a, b) as (X, Y) with cr = positive const * (X + Y sqrt5)"""
    C = [0] * 5
    ca = (a[0], a[4], a[3], a[2], a[1])
    for i in range(5):
        if ca[i]:
            for j in range(5):
                C[(i + j) % 5] += ca[i] * b[j]
    return (2 * (C[1] - C[4]) - (C[2] - C[3]), C[2] - C[3])


def cross_sign(a, b):
    X, Y = crq(a, b)
    return sgn5(X, Y)


def im_q(z):
    return (2 * (z[1] - z[4]) - (z[2] - z[3]), z[2] - z[3])


def re_q(z):  # 4 Re z = 4 c0 - (c1 + c4) - (c2 + c3) + ((c1 + c4) - (c2 + c3)) sqrt5
    return (4 * z[0] - (z[1] + z[4]) - (z[2] + z[3]), (z[1] + z[4]) - (z[2] + z[3]))


def poly_orient(P, a, b, c, crcache):
    acc = {}
    for (u, v) in ((a, b), (b, c), (c, a)):
        key = (u, v)
        if key not in crcache:
            d = {}
            for (e1, z1) in P[u]:
                for (e2, z2) in P[v]:
                    X, Y = crq(z1, z2)
                    o = d.get(e1 + e2, (0, 0)); d[e1 + e2] = (o[0] + X, o[1] + Y)
            crcache[key] = d
        for e, (X, Y) in crcache[key].items():
            o = acc.get(e, (0, 0)); acc[e] = (o[0] + X, o[1] + Y)
    for e in sorted(acc):
        s = sgn5(*acc[e])
        if s:
            return s
    return 0


def coord_cmp(P, a, b, f):
    acc = {}
    for (e, z) in P[a]:
        X, Y = f(z); o = acc.get(e, (0, 0)); acc[e] = (o[0] + X, o[1] + Y)
    for (e, z) in P[b]:
        X, Y = f(z); o = acc.get(e, (0, 0)); acc[e] = (o[0] - X, o[1] - Y)
    for e in sorted(acc):
        s = sgn5(*acc[e])
        if s:
            return s
    return 0


BASECACHE = {}
NBASE = [0]


def evaluate(P, kmax=8):
    n = len(P)
    S = np.zeros((n, n, n), dtype=np.int8)
    cache = {k: v for k, v in BASECACHE.items()} if NBASE[0] else {}
    nz = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = poly_orient(P, i, j, k, cache)
                if s == 0:
                    nz += 1
                S[i, j, k] = S[j, k, i] = S[k, i, j] = s
                S[j, i, k] = S[i, k, j] = S[k, j, i] = -s
    if nz:
        return None, None, nz
    def cmp(a, b):
        c = coord_cmp(P, a, b, im_q)
        if c == 0:
            c = coord_cmp(P, a, b, re_q)
        return c
    order = sorted(range(n), key=cmp_to_key(cmp))
    R = np.zeros(n, dtype=np.int32)
    for pos, i in enumerate(order):
        R[i] = pos
    cnt = np.zeros(kmax + 1, dtype=np.int64)
    S = np.ascontiguousarray(S)
    ml = CV.cvx_dp(n, S.ctypes.data, R.ctypes.data, cnt.ctypes.data, kmax)
    return ml, [int(x) for x in cnt], 0


def read5(fn):
    pts = []
    for line in open(fn):
        line = line.split('#')[0].strip()
        if line:
            pts.append(red(tuple(map(int, line.split()))))
    return pts


def angcmp(u, v):
    hu = 0 if sgn5(*im_q(u)) > 0 or (sgn5(*im_q(u)) == 0 and sgn5(*re_q(u)) > 0) else 1
    hv = 0 if sgn5(*im_q(v)) > 0 or (sgn5(*im_q(v)) == 0 and sgn5(*re_q(v)) > 0) else 1
    if hu != hv:
        return hu - hv
    c = cross_sign(u, v)
    return -1 if c > 0 else (1 if c < 0 else 0)


def arcs(dirs):
    ds = sorted([d for d in dirs if any(d)], key=cmp_to_key(angcmp))
    C = []
    for d in ds:
        if C and angcmp(C[-1], d) == 0:
            continue
        C.append(d)
    out = []
    for i in range(len(C)):
        a = C[i]; b = C[(i + 1) % len(C)]
        if cross_sign(a, b) > 0:
            out.append(add(a, b))
    return out


def in_sector5(w):
    zeta = (0, 1, 0, 0, 0)
    a = sgn5(*im_q(w)); b = sgn5(*re_q(w))
    return (a > 0 or (a == 0 and b > 0)) and cross_sign(w, zeta) > 0


def to_sector5(z):
    w = z
    for _ in range(5):
        if in_sector5(w):
            return w
        w = rotz(w)
    raise ValueError(z)


def arcs_sector(dirs):
    ds = sorted({to_sector5(d) for d in dirs if any(d)}, key=cmp_to_key(angcmp))
    C = []
    for d in ds:
        if C and angcmp(C[-1], d) == 0:
            continue
        C.append(d)
    out = []
    for i in range(len(C)):
        a = C[i]; b = C[i + 1] if i + 1 < len(C) else rotz(C[0])
        out.append(add(a, b))
    return out


def lead(terms):
    d = {}
    for (e, z) in terms:
        d[e] = add(d.get(e, (0, 0, 0, 0, 0)), z)
    for e in sorted(d):
        if any(d[e]):
            return d[e]
    return (0, 0, 0, 0, 0)


def main():
    fn = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
    pts = read5(fn)
    centre = (0, 0, 0, 0, 0) in pts
    nonc = [p for p in pts if any(p)]
    # orbits
    seen = set(); reps = []
    for p in nonc:
        if p in seen:
            continue
        o = [p]
        for _ in range(4):
            o.append(rotz(o[-1]))
        for q in o:
            seen.add(q)
        reps.append(p)
    if '--remove' in sys.argv:
        rem = set(int(x) for x in sys.argv[sys.argv.index('--remove') + 1].split(','))
        reps = [r for i, r in enumerate(reps) if i not in rem]
    def config(rr):
        P = []
        for r in rr:
            cur = r
            for _ in range(5):
                P.append(cur)
                cur = [(e, rotz(z)) for (e, z) in cur]
        if centre:
            P.append([(0, (0, 0, 0, 0, 0))])
        return P
    R0 = [[(0, r)] for r in reps]
    t0 = time.time()
    ml, cnt, nz = evaluate(config(R0))
    # cache cr of base pairs (base points come first in every config below; the centre, if any, is last, so
    # only pairs among the non-centre base points are cached)
    PB = config(R0)
    nb = len(PB) - (1 if centre else 0)
    for u in range(nb):
        for v in range(nb):
            if u != v:
                d = {}
                for (e1, z1) in PB[u]:
                    for (e2, z2) in PB[v]:
                        X, Y = crq(z1, z2)
                        o = d.get(e1 + e2, (0, 0)); d[e1 + e2] = (o[0] + X, o[1] + Y)
                BASECACHE[(u, v)] = d
    NBASE[0] = nb
    print('%s: orbits=%d centre=%s maxlen=%s n8=%s zero=%d (%.1fs)' % (os.path.basename(fn), len(R0), centre, ml,
          cnt[8] if cnt else None, nz, time.time() - t0), flush=True)
    print('  counts', cnt, flush=True)
    allpts = config(R0)
    tot = 0; free = 0; best = None
    if mode in ('double', 'both'):
        for l in range(len(R0)):
            p0 = R0[l]
            dirs = []
            for q in allpts:
                if q == p0:
                    continue
                v = lead(q + [(e, neg(z)) for (e, z) in p0])
                if any(v):
                    dirs.append(v); dirs.append(neg(v))
            bl = None; fl = 0
            for d in arcs(dirs):
                RR = R0 + [p0 + [(1, d)]]
                ml, cnt, nz = evaluate(config(RR))
                tot += 1
                if nz:
                    continue
                if bl is None or cnt[8] < bl:
                    bl = cnt[8]
                if cnt[8] == 0:
                    fl += 1; free += 1
                    print('  FREE doubling orbit', l, d, flush=True)
            if best is None or (bl is not None and bl < best[0]):
                best = (bl, 'D', l)
            print('  orbit %d: best n8 %s free %d (%.0fs)' % (l, bl, fl, time.time() - t0), flush=True)
    if mode in ('levels', 'both'):
        facs = [(1, 0, 0, 0, 0)] + [add(red(tuple(1 if k == (5 - j) % 5 else 0 for k in range(5))), (-1, 0, 0, 0, 0)) for j in range(1, 5)]
        for E in (-4, 4):
            dirs = []
            base = [lead(q) for q in allpts if any(lead(q))]
            src = list(base)
            if E < 0:
                for i in range(len(allpts)):
                    for j in range(i + 1, len(allpts)):
                        v = lead(allpts[i] + [(e, neg(z)) for (e, z) in allpts[j]])
                        if any(v):
                            src.append(v)
            for v in src:
                for f in facs:
                    w = mul(v, f)
                    dirs.append(w); dirs.append(neg(w))
            bl = None; fl = 0
            A = arcs_sector(dirs)
            for v in A:
                RR = R0 + [[(E, v)]]
                ml, cnt, nz = evaluate(config(RR))
                tot += 1
                if nz:
                    continue
                if bl is None or cnt[8] < bl:
                    bl = cnt[8]
                if cnt[8] == 0:
                    fl += 1; free += 1
                    print('  FREE level', E, v, flush=True)
            print('  level %d: arcs %d best n8 %s free %d (%.0fs)' % (E, len(A), bl, fl, time.time() - t0), flush=True)
    print('DONE %s evaluated=%d free=%d (%.0fs)' % (os.path.basename(fn), tot, free, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
