#!/usr/bin/env python3
"""SYM16FIVE20261110: distinct order types (all relabellings and reflections merged) among integer point sets, exact arithmetic.
Canonical form: for every hull vertex p and both orientations, label p first and the others by angular order
around p; the orientation vector of all triples in that labelling; take the lexicographic minimum."""
import sys, glob, os, itertools, random
rng = random.Random(20261110)
from functools import cmp_to_key
def orient(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def sgn(x): return (x > 0) - (x < 0)
def hull(P):
    pts = sorted(set(P))
    def half(seq):
        h = []
        for q in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], q) <= 0: h.pop()
            h.append(q)
        return h
    lo, up = half(pts), half(pts[::-1])
    return lo[:-1] + up[:-1]
def canon(P):
    best = None
    for p in hull(P):
        others = [q for q in P if q != p]
        for refl in (1, -1):
            # p is a hull vertex: all others in an open half-plane around p, so orient gives a total angular order
            srt = sorted(others, key=cmp_to_key(lambda a, b: -refl * sgn(orient(p, a, b))))
            L = [p] + srt
            v = tuple(refl * sgn(orient(L[i], L[j], L[k])) for i, j, k in itertools.combinations(range(len(L)), 3))
            if best is None or v < best: best = v
    return best
def load(f): return [tuple(int(x) for x in l.split()) for l in open(f) if l.strip() and not l.startswith('#')]
for d in sys.argv[1:]:
    files = sorted(glob.glob(os.path.join(d, 'model*.pts')))
    cs = {}
    for f in files:
        P = load(f)
        assert len(set(P)) == len(P) == 16, f
        assert all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3)), f + ' collinear'
        c = canon(P)
        for t in range(4):                      # self-test: invariance under relabelling and reflection
            Q = P[:]; rng.shuffle(Q)
            if t % 2: Q = [(x, -y) for x, y in Q]
            assert canon(Q) == c, f + ' canonical form not invariant'
        cs.setdefault(c, []).append(os.path.basename(f))
    print(d.rstrip('/').split('/')[-1], 'files', len(files), '(canonical form invariant under 4 random relabellings/reflections each)', 'distinct order types', len(cs),
          'merged groups:', [g for g in cs.values() if len(g) > 1])
