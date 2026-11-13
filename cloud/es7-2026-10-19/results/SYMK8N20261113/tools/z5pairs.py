#!/usr/bin/env python3
"""5-fold: remove one orbit of the 56-point set, then add one or two infinitesimal orbits (doublings of any orbit,
new outer/inner scale levels), exact limit order types in Z[zeta_5] (z5.py).  Pairs: for every octagon-free first
move a, the arcs of every other move family are recomputed on B + a and every second move lying in an arc that was
octagon-free for B alone is evaluated (other arcs already contain an octagon).
usage: z5pairs.py FILE.pts REMOVE"""
import sys, os, time
from functools import cmp_to_key
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z5
from z5 import (read5, rotz, red, add, neg, mul, lead, angcmp, cross_sign, to_sector5, evaluate, crq, BASECACHE,
                NBASE)

fn = sys.argv[1]; r = int(sys.argv[2])
pts = read5(fn)
centre = (0, 0, 0, 0, 0) in pts
seen = set(); reps = []
for p in pts:
    if not any(p) or p in seen:
        continue
    o = [p]
    for _ in range(4):
        o.append(rotz(o[-1]))
    seen.update(o)
    reps.append(p)
reps = [rr for i, rr in enumerate(reps) if i != r]
R0 = [[(0, p)] for p in reps]


def config(RR):
    P = []
    for rep in RR:
        cur = rep
        for _ in range(5):
            P.append(cur)
            cur = [(e, rotz(z)) for (e, z) in cur]
    if centre:
        P.append([(0, (0, 0, 0, 0, 0))])
    return P


def n8(RR):
    ml, cnt, nz = evaluate(config(RR))
    return None if nz else cnt[8]


t0 = time.time()
base_n8 = n8(R0)
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
print('%s remove=%d orbits=%d centre=%s base n8=%s' % (os.path.basename(fn), r, len(R0), centre, base_n8), flush=True)

FACS = [(1, 0, 0, 0, 0)] + [add(red(tuple(1 if k == (5 - j) % 5 else 0 for k in range(5))), (-1, 0, 0, 0, 0))
                            for j in range(1, 5)]


def sorted_unique(ds):
    ds = sorted([d for d in ds if any(d)], key=cmp_to_key(angcmp))
    C = []
    for d in ds:
        if C and angcmp(C[-1], d) == 0:
            continue
        C.append(d)
    return C


def moves_of(RR, fam):
    allp = config(RR)
    if fam[0] == 'D':
        l = fam[1]
        p0 = RR[l]
        dirs = []
        for q in allp:
            if q == p0:
                continue
            v = lead(q + [(e, neg(z)) for (e, z) in p0])
            if any(v):
                dirs.append(v); dirs.append(neg(v))
        C = sorted_unique(dirs)
        E = 1 + max(e for (e, z) in p0)
        out = []
        for i in range(len(C)):
            a = C[i]; b = C[(i + 1) % len(C)]
            if cross_sign(a, b) > 0:
                d = add(a, b)
                out.append((('D', l, E, d), a, b, RR[:] + [p0 + [(E, d)]]))
        return out
    E = fam[1]
    src = [lead(q) for q in allp if any(lead(q))]
    if E < 0:
        for i in range(len(allp)):
            for j in range(i + 1, len(allp)):
                v = lead(allp[i] + [(e, neg(z)) for (e, z) in allp[j]])
                if any(v):
                    src.append(v)
    dirs = []
    for v in src:
        for f in FACS:
            w = mul(v, f)
            dirs.append(w); dirs.append(neg(w))
    C = sorted_unique([to_sector5(d) for d in dirs if any(d)])
    out = []
    for i in range(len(C)):
        a = C[i]; b = C[i + 1] if i + 1 < len(C) else rotz(C[0])
        v = add(a, b)
        out.append((('A', E, v), a, b, RR[:] + [[(E, v)]]))
    return out


fams = [('D', l) for l in range(len(R0))] + [('A', -4), ('A', 4)]
free = []; freearcs = {}; best = None; nsingle = 0
for fam in fams:
    for (mv, lo, hi, RR) in moves_of(R0, fam):
        v = n8(RR); nsingle += 1
        if v is None:
            continue
        if best is None or v < best[0]:
            best = (v, mv[:2])
        if v == 0:
            free.append((fam, mv, RR))
            freearcs.setdefault(fam, []).append((lo, hi))
print('  singles=%d free=%d best=%s (%.0fs)' % (nsingle, len(free), best, time.time() - t0), flush=True)
npairs = 0; found = 0; bestp = None
for (fa, mv, RA) in free:
    for fam in fams:
        if fam == fa or fam not in freearcs:
            continue
        for (mv2, lo, hi, RR) in moves_of(RA, fam):
            d = mv2[-1]
            if not any(cross_sign(a, d) > 0 and cross_sign(d, b) > 0 for (a, b) in freearcs[fam]):
                continue
            npairs += 1
            v = n8(RR)
            if v is None:
                continue
            if bestp is None or v < bestp[0]:
                bestp = (v, mv[:2], mv2[:2])
            if v == 0:
                found += 1
                print('  FOUND PAIR', mv, mv2, flush=True)
print('  pairs=%d found=%d best=%s (%.0fs)' % (npairs, found, bestp, time.time() - t0), flush=True)
print('DONE', os.path.basename(fn), 'remove', r, flush=True)
