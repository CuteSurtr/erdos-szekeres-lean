#!/usr/bin/env python3
"""Exact, complete scan of 'add-on' orbits at a new infinitesimal scale level.

Given an m-fold set Y (m = 3 oblique Z[omega] coordinates, m = 4 Gaussian integers), add one new orbit
V = {g^k v} at scale eps^-1 (outer) or eps^+1 (inner), or at an intermediate level of a stacked Y.
The limit order type depends on dir(v) only through its position relative to a finite set of critical directions
(see the record): directions of differences y1 - y2, of points y, and of y multiplied by the fixed factors that turn
an edge/diagonal direction of V into dir(v).  We take a superset of critical directions, reduce them to the
fundamental sector of the rotation group, sort them exactly, and evaluate one direction strictly inside every
open arc between consecutive critical directions, plus the critical directions themselves are skipped (they give
degenerate configurations).  So every limit order type of 'Y + one add-on orbit at this level' is evaluated.

usage: addon_exact.py M FILE LEVELSPEC POS [--centre-inner]
  LEVELSPEC: comma list of layer cut positions for Y's own stack ('' = Y at one level; m = 4 only)
  POS: level index for the new orbit: 0 = outermost new level, ..., nblocks = innermost new level
"""
import sys, os, ctypes, math, time
import numpy as np
from functools import cmp_to_key

HERE = os.path.dirname(os.path.abspath(__file__))
so = os.path.join(HERE, 'libstackeval.so')
if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(os.path.join(HERE, 'stackeval.c')):
    os.system('gcc -O2 -shared -fPIC -o %s %s' % (so, os.path.join(HERE, 'stackeval.c')))
LIB = ctypes.CDLL(so)
LIB.stack_eval.restype = ctypes.c_int
LIB.stack_eval.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                           ctypes.c_int, ctypes.c_void_p]


def evaluate(pts, kmax=8):
    n = len(pts)
    e = np.array([p[0] for p in pts], dtype=np.int32)
    x = np.array([p[1] for p in pts], dtype=np.int64)
    y = np.array([p[2] for p in pts], dtype=np.int64)
    cnt = np.zeros(kmax + 1, dtype=np.int64)
    nz = np.zeros(1, dtype=np.int32)
    ml = LIB.stack_eval(n, e.ctypes.data, x.ctypes.data, y.ctypes.data, cnt.ctypes.data, kmax, nz.ctypes.data)
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
        elif m == 3:
            if len(w) == 2:
                P.append((w[0], w[1]))
            else:
                P.append((w[0] - w[2], w[1] - w[2]))
    return P


def rot(m, p):
    a, b = p
    return (-b, a) if m == 4 else (-b, a - b)


def in_sector(m, p):
    a, b = p
    return a > 0 and b >= 0


def to_sector(m, p):
    for _ in range(m):
        if in_sector(m, p):
            return p
        p = rot(m, p)
    raise ValueError(p)


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def prim(p):
    g = math.gcd(abs(p[0]), abs(p[1]))
    return (p[0] // g, p[1] // g) if g else p


def main():
    m = int(sys.argv[1]); fn = sys.argv[2]; levelspec = sys.argv[3]; pos = int(sys.argv[4])
    centre_inner = '--centre-inner' in sys.argv
    P = read_set(fn, m)
    has_centre = (0, 0) in P
    pts0 = [p for p in P if p != (0, 0)]
    # orbits by squared radius (m = 4) or just keep order for m = 3 (levels only for m = 4)
    if m == 4:
        orb = {}
        for p in pts0:
            orb.setdefault(p[0] ** 2 + p[1] ** 2, []).append(p)
        layers = [orb[k] for k in sorted(orb, reverse=True)]
        cuts = sorted(set(int(c) for c in levelspec.split(',') if c))
        blocks = []; prev = 0
        for c in cuts + [len(layers)]:
            blocks.append([q for o in layers[prev:c] for q in o]); prev = c
    else:
        blocks = [pts0]
    nb = len(blocks)
    # levels: block b at exponent 2b; new orbit at exponent 2*pos - 1
    base = []
    for b, bl in enumerate(blocks):
        for q in bl:
            base.append((2 * b, q[0], q[1]))
    if has_centre:
        base.append((0, 0, 0))
    ev = 2 * pos - 1
    # critical directions (superset)
    outer_pts = [q for b in range(pos) for q in blocks[b]]
    inner_pts = [q for b in range(pos, nb) for q in blocks[b]]
    allp = [q for bl in blocks for q in bl] + ([(0, 0)] if has_centre else [])
    crit = set()
    def add(d):
        if d == (0, 0):
            return
        for s in (1, -1):
            dd = (s * d[0], s * d[1])
            crit.add(prim(to_sector(m, dd)))
    # differences among inner points (v vs edges of inner part), and points (antipodal / centre cases)
    for i, p in enumerate(inner_pts):
        add(p)
        for q in inner_pts[i + 1:]:
            add((p[0] - q[0], p[1] - q[1]))
    # outer points: v's edges vs outer points' directions: dir(v) + offset = dir(x)
    if m == 4:
        facs = [lambda p: p, lambda p: (p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], p[1] - p[0])]
    else:
        # oblique coords: multiplication by (2 + omega): (a, b) -> (2a - b, a + b); also by its conjugate-type
        # factor for the other edge orientation: (1 - omega)*(...) etc. -- include several maps to be safe
        facs = [lambda p: p, lambda p: (2 * p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], 2 * p[1] - p[0]),
                lambda p: (p[0] - 2 * p[1], 2 * p[0] - p[1])]
    for p in outer_pts + ([(0, 0)] if False else []):
        for f in facs:
            add(f(p))
    # inner-centre interplay and points of the inner part with v's edges (when v is outer to them, edges of V
    # matter only through dir(v) vs differences, already added); when v is inner to some block, its edges vs
    # those block points:
    for p in outer_pts:
        add(p)
    crit = sorted(crit, key=cmp_to_key(lambda p, q: -1 if cross(p, q) > 0 else (1 if cross(p, q) < 0 else 0)))
    # dedupe parallel
    C = []
    for d in crit:
        if C and cross(C[-1], d) == 0:
            continue
        C.append(d)
    nC = len(C)
    cand = []
    for i in range(nC):
        a = C[i]
        b = C[i + 1] if i + 1 < nC else rot(m, C[0])
        # scale to comparable lengths to keep the sum strictly inside and coordinates moderate
        cand.append((a[0] + b[0], a[1] + b[1]))
    t0 = time.time()
    best = None; nfree = 0; hist = {}
    for v in cand:
        V = [v]
        for _ in range(m - 1):
            V.append(rot(m, V[-1]))
        pts = list(base) + [(ev, q[0], q[1]) for q in V]
        if centre_inner and not has_centre:
            pts.append((0, 0, 0))
        ml, cnt, nz = evaluate(pts, 8)
        if nz:
            hist['degenerate'] = hist.get('degenerate', 0) + 1
            continue
        n8 = cnt[8]
        hist[n8 == 0] = hist.get(n8 == 0, 0) + 1
        if best is None or n8 < best[0]:
            best = (n8, v, ml)
        if n8 == 0:
            nfree += 1
            print('FREE', v, 'maxlen', ml, flush=True)
    print('%s m=%d pos=%d/%d npts=%d critical=%d evaluated=%d free=%d best=%s hist=%s time=%.0fs' % (
        os.path.basename(fn), m, pos, nb, len(base) + m + (1 if centre_inner and not has_centre else 0), nC,
        len(cand), nfree, best, hist, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
