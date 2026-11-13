#!/usr/bin/env python3
"""Exact helpers (Python ints only).

  points_tools.py tosig points.txt out.sig     # x-sort integer points, write signotope (+1 = ccw)
  points_tools.py verify points.txt file.sig K # exact check that the points realize the signotope
                                               # (same labels), general position, repo DP largest
                                               # convex subset, and convex K-subset count (brute force)
"""
import itertools
import sys
import os

REPO = "."
sys.path.insert(0, os.path.join(REPO, "scripts"))
from es_lower_bound_witness import largest_convex_subset, orient, general_position  # noqa: E402


def read_points(p):
    pts = []
    with open(p) as f:
        for line in f:
            t = line.replace(",", " ").split()
            if len(t) >= 2:
                pts.append((int(t[0]), int(t[1])))
    return pts


def read_sig(p):
    sig = {}
    with open(p) as f:
        for line in f:
            i, j, k, s = map(int, line.split())
            sig[(i, j, k)] = s
    return sig


def sgn(v):
    return (v > 0) - (v < 0)


def main():
    cmd = sys.argv[1]
    if cmd == "tosig":
        pts = read_points(sys.argv[2])
        if len(set(p[0] for p in pts)) != len(pts):
            # exact shear (x,y) -> (L x + y, y), det = L > 0: same order type, distinct x
            L = 2 * max(abs(p[1]) for p in pts) + 1
            pts = [(L * x + y, y) for x, y in pts]
            print("applied shear L =", L)
        pts = sorted(pts)
        xs = [p[0] for p in pts]
        assert len(set(xs)) == len(xs), "distinct x needed"
        n = len(pts)
        with open(sys.argv[3], "w") as f:
            for i, j, k in itertools.combinations(range(n), 3):
                o = sgn(orient(pts[i], pts[j], pts[k]))
                assert o != 0
                f.write(f"{i+1} {j+1} {k+1} {o}\n")
        print(f"wrote signotope of {n} x-sorted points")
    elif cmd == "verify":
        pts = read_points(sys.argv[2])
        sig = read_sig(sys.argv[3])
        K = int(sys.argv[4])
        n = len(pts)
        mism = 0
        for (i, j, k), s in sig.items():
            if sgn(orient(pts[i - 1], pts[j - 1], pts[k - 1])) != s:
                mism += 1
        print("points:", n, "triples:", len(sig), "orientation mismatches:", mism)
        print("general position:", general_position(pts))
        print("repo largest_convex_subset:", largest_convex_subset(pts))
        # brute force convex K-subsets using real geometry (4-point / point-in-triangle, exact)
        def inside(d, a, b, c):
            o1, o2, o3 = sgn(orient(a, b, d)), sgn(orient(b, c, d)), sgn(orient(c, a, d))
            return o1 == o2 == o3
        conv4 = {}
        for q in itertools.combinations(range(n), 4):
            P = [pts[t] for t in q]
            conv4[q] = not any(inside(P[t], *[P[u] for u in range(4) if u != t]) for t in range(4))
        cnt = 0
        def dfs(cur, start):
            nonlocal cnt
            if len(cur) == K:
                cnt += 1
                return
            for p in range(start, n):
                if all(conv4[tuple(sorted(c3 + (p,)))] for c3 in itertools.combinations(cur, 3)):
                    dfs(cur + [p], p + 1)
        dfs([], 0)
        print(f"convex {K}-subsets (exact geometric DFS):", cnt)
    else:
        raise SystemExit("unknown command")


if __name__ == "__main__":
    main()
