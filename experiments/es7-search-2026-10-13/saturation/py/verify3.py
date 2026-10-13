#!/usr/bin/env python3
"""Three independent exact checks of "no K points in convex position".

usage: verify3.py K pointsfile [pointsfile ...]
  (1) repository DP largest_convex_subset (scripts/es_lower_bound_witness.py)
  (2) cgon count K (C, __int128)
  (3) brute force: a subset is in convex position iff every 4-subset is
      (Caratheodory); 4-subset convexity by exact point-in-triangle tests;
      all convex subsets of size K are enumerated by backtracking over
      x-sorted indices (no DP shared with (1)/(2)).
Prints one JSON line per file.
"""
import json, os, subprocess, sys
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from es_lower_bound_witness import largest_convex_subset, general_position  # noqa: E402


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def in_triangle(p, a, b, c):
    s1, s2, s3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)


def brute_count(P, K):
    n = len(P)
    bad4 = set()
    for q in combinations(range(n), 4):
        a, b, c, d = (P[i] for i in q)
        if in_triangle(a, b, c, d) or in_triangle(b, a, c, d) or in_triangle(c, a, b, d) or in_triangle(d, a, b, c):
            bad4.add(q)
    counts = [0] * (K + 1)

    def ok_add(S, v):  # S sorted, v > max(S)
        for t in combinations(S, 3):
            if t + (v,) in bad4:
                return False
        return True

    def rec(S, start):
        counts[len(S)] += 1
        if len(S) == K:
            return
        for v in range(start, n):
            if ok_add(S, v):
                S.append(v)
                rec(S, v + 1)
                S.pop()
    rec([], 0)
    return counts[K], max(i for i in range(K + 1) if counts[i] > 0)


def main():
    K = int(sys.argv[1])
    for fn in sys.argv[2:]:
        P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
        gp = general_position(P)
        dp = largest_convex_subset(P)
        cg = subprocess.run([os.path.join(ROOT, "bin", "cgon"), "count", str(K)], input=open(fn).read(),
                            capture_output=True, text=True).stdout.strip()
        bk, bmax = brute_count(P, K)
        print(json.dumps(dict(file=os.path.basename(fn), n=len(P), general_position=gp, dp_largest_convex=dp,
                              cgon=cg, brute_convex_K=bk, brute_max_upto_K=bmax)), flush=True)


if __name__ == "__main__":
    main()
