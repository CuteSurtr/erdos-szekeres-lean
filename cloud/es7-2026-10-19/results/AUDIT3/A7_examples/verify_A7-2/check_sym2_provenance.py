#!/usr/bin/env python3
"""Independent re-check of audit finding A7-2 (provenance of SYM2/sym7_32points.txt).

(1) Does SYM2/build.py (byte-identical copy, sha256 checked by the caller) regenerate the point files exactly,
    with the parameters stated in SYM2/README.md line 49?
(2) Without using build.py at all: does the 32-point file have the cluster structure of Prop. B
    (k = 7, n = 5, clusters at x_i = 2i - 5 on the cubic, sizes C(5, i), cluster i < n/2 with no (i+2)-cup
    and no (k-i)-cap, right half = half-turn of the left half)?
(3) Write the exact orientation table for an independent C brute force over all 7-subsets (no_convex7.c),
    so that the lower bound N(C2) >= 32 can be confirmed not to depend on provenance.
All arithmetic is exact (Python integers)."""
import importlib.util
import itertools
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get("ES7_RESULTS", ".")


def read_pts(path):
    pts = []
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            assert len(t) == 2, line
            pts.append((int(t[0]), int(t[1])))
    return pts


def orient(p, q, r):
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def slope_cmp_chain(chain):
    """chain sorted by x (distinct x). Returns +1 if strictly convex-up (cup: slopes increase), -1 if cap, 0 otherwise.
    Slopes compared exactly via orientation of consecutive triples (x strictly increasing)."""
    signs = set(orient(chain[i], chain[i + 1], chain[i + 2]) for i in range(len(chain) - 2))
    if signs == {1}:
        return 1   # left turns with increasing x = increasing slopes = cup
    if signs == {-1}:
        return -1  # cap
    return 0


def has_cup_or_cap(P, length, want):
    """Does P (distinct x required) contain a 'want'-chain (+1 cup, -1 cap) of the given length? brute force."""
    Ps = sorted(P)
    if len(Ps) < length:
        return False
    for sub in itertools.combinations(Ps, length):
        if length <= 2:
            return True
        if slope_cmp_chain(list(sub)) == want:
            return True
    return False


def main():
    out = []
    f7 = read_pts(R + "/SYM2/sym7_32points.txt")
    f9 = read_pts(R + "/SYM2/sym9_128points.txt")

    # ---------- (1) regeneration by the project's own build.py (copy) ----------
    spec = importlib.util.spec_from_file_location("build_copy", os.path.join(HERE, "build_copy.py"))
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    g7 = B.sym(7, X=50, Y=10000, K=3)
    g9 = B.sym(9, X=10 ** 15, Y=10 ** 15, K=10 ** 9)
    out.append("(1) build.py sym(7, X=50, Y=10000, K=3): n=%d; file n=%d; same ordered list: %s; same set: %s"
               % (len(g7), len(f7), g7 == f7, set(g7) == set(f7)))
    out.append("(1) build.py sym(9, X=10**15, Y=10**15, K=10**9): n=%d; file n=%d; same ordered list: %s; same set: %s"
               % (len(g9), len(f9), g9 == f9, set(g9) == set(f9)))
    # sensitivity: nearby parameters do NOT reproduce (shows the match is not generic)
    for (X, Y, K) in [(50, 10000, 2), (50, 10000, 4), (49, 10000, 3), (50, 9999, 3), (10 ** 6, 10 ** 6, None)]:
        gg = B.sym(7, X=X, Y=Y, K=K)
        out.append("    control sym(7, X=%s, Y=%s, K=%s) equals file: %s" % (X, Y, K, gg == f7))

    # ---------- (2) structure of the 32-point file, without build.py ----------
    k, n = 7, 5
    S = set(f7)
    out.append("(2) distinct points: %s; file sorted: %s; max |coord| = %d"
               % (len(S) == len(f7), f7 == sorted(f7), max(max(abs(x), abs(y)) for x, y in f7)))
    out.append("(2) centrally symmetric (p in S <=> -p in S): %s; origin absent: %s"
               % (all((-x, -y) in S for x, y in f7), (0, 0) not in S))
    # cluster by x: each cluster i should have bounding-box midpoint (50*q, 10000*q^3), q = 2i - n
    xs_sorted = sorted(f7)
    clusters = []
    cur = [xs_sorted[0]]
    for p in xs_sorted[1:]:
        if p[0] - cur[-1][0] > 40:     # gaps between clusters are >= 61 in x; inside clusters <= 6
            clusters.append(cur)
            cur = [p]
        else:
            cur.append(p)
    clusters.append(cur)
    sizes = [len(c) for c in clusters]
    out.append("(2) clusters by x-gaps: sizes %s (expected C(5,i) = %s)" % (sizes, [comb(n, i) for i in range(n + 1)]))
    ok_mid = True
    for i, c in enumerate(clusters):
        q = 2 * i - n
        xs = [p[0] for p in c]
        ys = [p[1] for p in c]
        mid2 = (min(xs) + max(xs), min(ys) + max(ys))
        if mid2 != (2 * 50 * q, 2 * 10000 * q ** 3):
            ok_mid = False
        out.append("    cluster %d: q=%+d size=%d bbox-mid*2=%s expected (%d, %d); inner max |dx|=%d"
                   % (i, q, len(c), mid2, 2 * 50 * q, 2 * 10000 * q ** 3, max(xs) - min(xs)))
    out.append("(2) every cluster centred at (50 q, 10000 q^3) on the cubic: %s" % ok_mid)
    # cups/caps of left clusters: cluster i < n/2 has no (i+2)-cup and no (k-i)-cap, and contains an (i+1)-cup and a (k-i-1)-cap
    for i in range(n // 2 + 1):
        c = clusters[i]
        if len(c) < 2:
            out.append("    cluster %d: single point (G(2,%d) has 1 point)" % (i, k - i))
            continue
        assert len(set(p[0] for p in c)) == len(c)
        no_cup = not has_cup_or_cap(c, i + 2, +1)
        no_cap = not has_cup_or_cap(c, k - i, -1)
        has_cup = has_cup_or_cap(c, i + 1, +1)
        has_cap = has_cup_or_cap(c, k - i - 1, -1)
        out.append("    cluster %d (G(%d,%d), %d pts): no %d-cup %s, no %d-cap %s; has %d-cup %s, has %d-cap %s"
                   % (i, i + 2, k - i, len(c), i + 2, no_cup, k - i, no_cap, i + 1, has_cup, k - i - 1, has_cap))
    right_is_halfturn = all(sorted((-x, -y) for x, y in clusters[i]) == sorted(clusters[n - i]) for i in range(n + 1))
    out.append("(2) cluster n-i = half-turn of cluster i for all i: %s" % right_is_halfturn)

    # ---------- (3) exact orientation table and general position ----------
    N = len(f7)
    col = 0
    with open(os.path.join(HERE, "sym7_32.orient"), "w") as fo:
        fo.write("%d\n" % N)
        for a in range(N):
            for b in range(N):
                row = []
                for c in range(N):
                    o = orient(f7[a], f7[b], f7[c]) if len({a, b, c}) == 3 else 0
                    if len({a, b, c}) == 3 and o == 0:
                        col += 1
                    row.append(str(o))
                fo.write(" ".join(row) + "\n")
    out.append("(3) collinear ordered triples among distinct indices: %d (general position iff 0)" % col)
    print("\n".join(out))


if __name__ == "__main__":
    main()
