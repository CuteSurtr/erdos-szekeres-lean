#!/usr/bin/env python3
"""Independent exact enumeration of z-splits (|A|,|B| >= 2) of a finite planar set, no LP.

Completeness: by Lemma 4' (checked by hand: conv(A) and conv(B) are disjoint for a z-split with |A|,|B|>=2),
every such split is a linear partition, induced by a line through two points with those two points assigned
suitably.  We enumerate all such partitions (both role assignments).

Existence of z: if a direction d works then z = p + t d works for large t (finite, outside conv(S)), so it suffices
to decide existence of a FINITE z outside conv(S).  The constraints are strict affine inequalities in z:
for each A-pair (a,a'): sgn orient(a,a',z) = common side of B; for each B-pair: sgn orient(b,b',z) = -common side of A.
We clip a huge box by the closed half-planes (exact Fractions); the open region is nonempty iff the clipped polygon
has positive area; it contains a point outside conv(S) iff some clipped vertex is strictly outside conv(S).
A witness z is then constructed exactly and the split is re-verified with igeom.is_z_split.
"""
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import orient, sgn, is_z_split, finite_z_outside_hull, z_sorted, on_z_side, on_far_side

BIG = Fraction(10) ** 60


def linear_partitions(S):
    n = len(S)
    parts = set()
    for i in range(n):
        for j in range(i + 1, n):
            L = frozenset(k for k in range(n) if k not in (i, j) and orient(S[i], S[j], S[k]) > 0)
            R = frozenset(k for k in range(n) if k not in (i, j) and orient(S[i], S[j], S[k]) < 0)
            for si in (0, 1):
                for sj in (0, 1):
                    X = set(L)
                    if si == 0:
                        X.add(i)
                    if sj == 0:
                        X.add(j)
                    X = frozenset(X)
                    Y = frozenset(range(n)) - X
                    if len(X) >= 2 and len(Y) >= 2:
                        parts.add(frozenset([X, Y]))
    return parts


def one_sided_constraints(S, A, B):
    """Return list of (a, b, s) meaning: need sgn orient(a, b, z) == s, or None if one-sidedness fails."""
    cons = []
    for i, j in combinations(sorted(A), 2):
        sides = {sgn(orient(S[i], S[j], S[k])) for k in B}
        if len(sides) != 1:
            return None
        cons.append((S[i], S[j], sides.pop()))
    for i, j in combinations(sorted(B), 2):
        sides = {sgn(orient(S[i], S[j], S[k])) for k in A}
        if len(sides) != 1:
            return None
        cons.append((S[i], S[j], -sides.pop()))
    return cons


def clip(poly, a, b, s):
    """Keep the part of convex polygon poly with s*orient(a,b,z) >= 0 (exact)."""
    out = []
    m = len(poly)
    for t in range(m):
        P, Q = poly[t], poly[(t + 1) % m]
        fP, fQ = s * orient(a, b, P), s * orient(a, b, Q)
        if fP >= 0:
            out.append(P)
        if (fP > 0 and fQ < 0) or (fP < 0 and fQ > 0):
            lam = Fraction(fP, fP - fQ)
            out.append((P[0] + lam * (Q[0] - P[0]), P[1] + lam * (Q[1] - P[1])))
    # remove duplicates
    ded = []
    for p in out:
        if not ded or ded[-1] != p:
            ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def area2(poly):
    return sum(poly[t][0] * poly[(t + 1) % len(poly)][1] - poly[(t + 1) % len(poly)][0] * poly[t][1]
               for t in range(len(poly)))


def find_z(S, A, B):
    cons = one_sided_constraints(S, A, B)
    if cons is None:
        return None, 'one-sided-fail'
    poly = [(-BIG, -BIG), (BIG, -BIG), (BIG, BIG), (-BIG, BIG)]
    for a, b, s in cons:
        poly = clip(poly, a, b, s)
        if len(poly) < 3:
            return None, 'empty'
    if area2(poly) == 0:
        return None, 'empty'
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    for v in poly:
        if finite_z_outside_hull(S, v):
            t = Fraction(1, 2)
            for _ in range(400):
                zc = (v[0] + t * (cx - v[0]), v[1] + t * (cy - v[1]))
                if finite_z_outside_hull(S, zc):
                    return zc, 'ok'
                t /= 2
            return None, 'witness-fail'
    return None, 'inside-hull-only'


def longest_chain(P, z, kind):
    """Longest z-cap (kind='cap') or z-cup (kind='cup') in P (z on no line of two points of P). DP on pairs."""
    Q = z_sorted(list(P), z)
    m = len(Q)
    if m <= 2:
        return m
    test = on_far_side if kind == 'cap' else on_z_side
    best = 2
    L = {}
    for j in range(m):
        for i in range(j):
            L[(i, j)] = 2
    for k in range(m):
        for j in range(k):
            for i in range(j):
                if test(Q[j], Q[i], Q[k], z) and L[(i, j)] + 1 > L[(j, k)]:
                    L[(j, k)] = L[(i, j)] + 1
                    best = max(best, L[(j, k)])
    return best


def all_splits(S):
    S = [tuple(p) for p in S]
    out = []
    stats = dict(partitions=0, one_sided_fail=0, empty=0, inside_hull_only=0, witness_fail=0, ok=0)
    for part in linear_partitions(S):
        stats['partitions'] += 1
        X, Y = tuple(part)
        for A, B in ((X, Y), (Y, X)):
            z, why = find_z(S, A, B)
            key = why.replace('-', '_')
            stats[key] = stats.get(key, 0) + 1
            if z is None:
                continue
            PA = [S[i] for i in sorted(A)]
            PB = [S[i] for i in sorted(B)]
            zz = ('F', z)
            assert is_z_split(PA, PB, zz) and finite_z_outside_hull(S, z), "witness does not verify"
            c = longest_chain(PA, zz, 'cap')
            d = longest_chain(PB, zz, 'cup')
            out.append(dict(nA=len(A), nB=len(B), c=c, d=d, z=z, A=sorted(A), B=sorted(B)))
    return out, stats


def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                x, y = line.split()[:2]
                pts.append((int(x), int(y)))
    return pts


if __name__ == '__main__':
    for path in sys.argv[1:]:
        S = load(path)
        sp, st = all_splits(S)
        print(path.rsplit('/', 1)[-1], len(S), st)
        for s in sp:
            print('   split |A|=%d |B|=%d cap_z(A)=%d cup_z(B)=%d' % (s['nA'], s['nB'], s['c'], s['d']))
