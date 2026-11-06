#!/usr/bin/env python3
"""Line-modules of a planar point set in general position, own implementation (T2d verification).

C (2 <= |C| <= n-2) is a line-module iff no line through two points of S \\ C has points of C strictly on both sides.

Enumeration (complete; proof): let C be a module and q a point outside C.  Since |S \\ C| >= 2 there is another
outside point r, and every line q r (r outside, r != q) leaves C on one side, so C lies in one open cone at q
bounded by consecutive cut directions (the directions of r - q and q - r for outside r != q); such a cone spans an
angle <= pi.  In the circular order of the 2(n-1) "items" around q (direction s - q, "real", and q - s, "ghost",
for s != q; all distinct by general position), the cone therefore contains exactly the real items of C (cut items
are excluded by definition, ghosts of C points are antipodal to their real items, hence outside an arc <= pi).
So C is a run of |C| consecutive real items around q.  Enumerating, around every q, all runs of consecutive real
items of length 2..n-2 yields every module (pick any q outside C); each candidate is then tested directly against
the definition.

Angular order: exact upper/lower half-plane classification of directions from coordinates (function `upper`),
then the cross-product sign (orientation table) inside a half.
"""
import functools


def left_masks(n, O):
    L = [[0] * n for _ in range(n)]
    for p in range(n):
        for r in range(n):
            if p == r:
                continue
            m = 0
            for s in range(n):
                if s != p and s != r and O(p, r, s) > 0:
                    m |= 1 << s
            L[p][r] = m
    return L


def is_module(n, C, L):
    """direct test of the definition; C bitmask"""
    outside = [s for s in range(n) if not (C >> s) & 1]
    for i, p in enumerate(outside):
        Lp = L[p]
        for r in outside[i + 1:]:
            lft = C & Lp[r]
            if lft and (C & ~lft):
                return False
    return True


def angular_items(n, q, O, upper):
    """items (s, g): g = 0 real (direction s - q), g = 1 ghost (direction q - s), sorted by angle in [0, 2pi)"""
    items = []
    for s in range(n):
        if s == q:
            continue
        u = upper(q, s)
        items.append((s, 0, 0 if u else 1))
        items.append((s, 1, 1 if u else 0))

    def cmp(x, y):
        if x[2] != y[2]:
            return -1 if x[2] < y[2] else 1
        sg = O(q, x[0], y[0])
        if x[1] ^ y[1]:
            sg = -sg
        assert sg != 0
        return -1 if sg > 0 else 1
    items.sort(key=functools.cmp_to_key(cmp))
    # sanity: total order consistency inside halves and antipodality (real and ghost exactly n-1 apart)
    m = len(items)
    pos = {(s, g): i for i, (s, g, _) in enumerate(items)}
    for s in range(n):
        if s != q:
            assert (pos[(s, 1)] - pos[(s, 0)]) % m == n - 1
    for i in range(m - 1):
        assert cmp(items[i], items[i + 1]) < 0
    return [(s, g) for s, g, _ in items]


def enumerate_modules(n, O, upper, L=None):
    if L is None:
        L = left_masks(n, O)
    cands = set()
    for q in range(n):
        it = angular_items(n, q, O, upper)
        m = len(it)
        for a in range(m):
            C = 0
            for k in range(n - 2):
                s, g = it[(a + k) % m]
                if g:
                    break
                C |= 1 << s
                if k >= 1:
                    cands.add(C)
    mods = sorted((C for C in cands if is_module(n, C, L)), key=lambda C: (bin(C).count('1'), C))
    return mods, len(cands), L


def brute_modules(n, L):
    """all subsets, definition test; for validation (small n only)"""
    out = []
    for C in range(1 << n):
        k = bin(C).count('1')
        if 2 <= k <= n - 2 and is_module(n, C, L):
            out.append(C)
    return sorted(out, key=lambda C: (bin(C).count('1'), C))
