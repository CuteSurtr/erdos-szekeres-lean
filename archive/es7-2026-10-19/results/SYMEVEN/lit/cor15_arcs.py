#!/usr/bin/env python3
"""Independent check of the Baek-Balko Corollary 15 route (SoCG 2025, Sec. 6.2).

For a centrally symmetric base S (N even, general position, no m points in convex position), enumerate EVERY
arc of sweep directions exactly (critical directions are the normals of p_i - p_j, sorted exactly by angle;
the representative of an arc is the sum of its two bounding critical vectors), and for each arc compute the
left-gon / right-gon profile with threshold L = N/2 and the size of the x-blow-up from Corollary 15:
    |b| = 2*sum_{l<=x} C(k-2,l) + sum_{j=2}^{k-2x-1} v_j * C(k-j-1, x),   k = m + 2x.
Method (independent of the other checks' code): enumerate all subsets of S in convex position once (DFS, using
the fact that a planar set in general position is in convex position iff all its 4-subsets are), then for each
direction the s-value of a left point is the largest convex subset whose maximum in that direction is the point,
and for a right point the largest convex subset whose minimum is the point.  Exact integer arithmetic only.
Usage: python3 -I cor15_arcs.py FILE [m]
"""
import sys
from math import comb
from functools import cmp_to_key
from itertools import combinations


def load(fn):
    pts = []
    for line in open(fn):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        a, b = line.replace(',', ' ').split()[:2]
        pts.append((int(a), int(b)))
    return pts


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def half(v):
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def angcmp(u, v):
    hu, hv = half(u), half(v)
    if hu != hv:
        return -1 if hu < hv else 1
    c = u[0] * v[1] - u[1] * v[0]
    return -1 if c > 0 else (1 if c < 0 else 0)


def main():
    S = load(sys.argv[1])
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    N = len(S)
    assert len(set(S)) == N
    Sset = set(S)
    assert all((-p[0], -p[1]) in Sset for p in S), 'not centrally symmetric'
    assert (0, 0) not in Sset
    O = {}
    for i, j, l in combinations(range(N), 3):
        o = orient(S[i], S[j], S[l])
        assert o != 0, 'collinear triple'
        s = 1 if o > 0 else -1
        for (a, b, c), sg in (((i, j, l), s), ((j, l, i), s), ((l, i, j), s), ((j, i, l), -s), ((i, l, j), -s), ((l, j, i), -s)):
            O[(a, b, c)] = sg
    def conv4(a, b, c, d):
        # a 4-set in general position is in convex position iff no point is inside the triangle of the others
        for p, (x, y, z) in ((a, (b, c, d)), (b, (a, c, d)), (c, (a, b, d)), (d, (a, b, c))):
            s = O[(x, y, z)]
            if O[(x, y, p)] == s and O[(y, z, p)] == s and O[(z, x, p)] == s:
                return False
        return True
    convex = []  # list of tuples (sorted indices) in convex position, size >= 1
    def dfs(cur, start):
        convex.append(tuple(cur))
        for nx in range(start, N):
            ok = True
            if len(cur) >= 3:
                for t in combinations(cur, 3):
                    if not conv4(t[0], t[1], t[2], nx):
                        ok = False
                        break
            if ok:
                cur.append(nx)
                dfs(cur, nx + 1)
                cur.pop()
    dfs([], 0)
    maxc = max(len(t) for t in convex)
    counts = {}
    for t in convex:
        counts[len(t)] = counts.get(len(t), 0) + 1
    print(f'file={sys.argv[1]} N={N} centrally symmetric, general position; convex subsets by size: {dict(sorted(counts.items()))}; largest={maxc}')
    if maxc >= m:
        print(f'base has a convex {maxc}-gon >= m={m}; Corollary 15 not applicable')
        return
    # critical directions
    crit = []
    for i, j in combinations(range(N), 2):
        w = (S[i][0] - S[j][0], S[i][1] - S[j][1])
        crit.append((-w[1], w[0]))
        crit.append((w[1], -w[0]))
    crit.sort(key=cmp_to_key(angcmp))
    uniq = []
    for v in crit:
        if uniq and angcmp(uniq[-1], v) == 0:
            continue
        uniq.append(v)
    if angcmp(uniq[-1], uniq[0]) == 0:
        uniq.pop()
    reps = []
    for idx in range(len(uniq)):
        u, v = uniq[idx], uniq[(idx + 1) % len(uniq)]
        assert u[0] * v[1] - u[1] * v[0] > 0, 'consecutive critical directions not within pi'
        reps.append((u[0] + v[0], u[1] + v[1]))
    L = N // 2
    stats = {}
    good = []
    for d in reps:
        key = [d[0] * p[0] + d[1] * p[1] for p in S]
        assert len(set(key)) == N
        order = sorted(range(N), key=lambda i: key[i])
        pos = {order[r]: r for r in range(N)}
        s = [0] * N  # indexed by position in the sweep order
        for t in convex:
            if not t:
                continue
            hi = max(t, key=lambda i: key[i])
            lo = min(t, key=lambda i: key[i])
            if pos[hi] < L:
                s[pos[hi]] = max(s[pos[hi]], len(t))
            if pos[lo] >= L:
                s[pos[lo]] = max(s[pos[lo]], len(t))
        assert s[0] == 1 and s[N - 1] == 1
        assert all(s[r] == s[N - 1 - r] for r in range(N)), 'profile not mirrored'
        v = {}
        for x in s:
            v[x] = v.get(x, 0) + 1
        vt = tuple(v.get(j, 0) for j in range(1, m))
        sizes = []
        for x in (1, 2, 3):
            k = m + 2 * x
            size = 2 * sum(comb(k - 2, l) for l in range(x + 1)) + sum(v.get(j, 0) * comb(k - j - 1, x) for j in range(2, k - 2 * x))
            sizes.append((k, size, 2 ** (k - 2)))
        stats[vt] = stats.get(vt, [0, sizes])
        stats[vt][0] += 1
        if all(sz == tgt for (_, sz, tgt) in sizes):
            good.append((d, tuple(s[:L])))
    print(f'arcs (distinct sweep orders over the full circle): {len(reps)}')
    for vt, (cnt, sizes) in sorted(stats.items(), key=lambda kv: -kv[1][1][0][1]):
        print(f'  v_1..v_{m-1} = {vt}: {cnt} arcs; sizes ' + ', '.join(f'k={k}: {sz}/{tgt}' for (k, sz, tgt) in sizes))
    print(f'arcs giving exactly 2^(k-2) for k = m+2, m+4, m+6: {len(good)}')
    if good:
        print('  example direction', good[0][0], 'left s-profile', good[0][1])


main()
