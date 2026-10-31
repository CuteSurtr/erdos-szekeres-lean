#!/usr/bin/env python3
"""Exact check of realized 26-point sets: general position (chiro.chirotope_of raises on a collinear
triple), max cap / max cup in the x-direction (Python DP), exact largest convex subset, and brute.c
on the x-sorted signotope (axioms, cap, cup, largest convex subset).
usage: verify26.py BRUTE a.pts [b.pts ...]"""
import itertools, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from chiro import largest_convex_subset, chirotope_of  # noqa

def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def bits(pts):
    P = sorted(pts)
    return "".join("1" if o(P[a], P[b], P[c]) > 0 else "0" for a, b, c in itertools.combinations(range(len(P)), 3))
def capcup(pts):
    P = sorted(pts); n = len(P); best = {1: 2, -1: 2}; L = {}
    for j in range(n):
        for k in range(j + 1, n):
            for s in (1, -1):
                v = 2
                for i in range(j):
                    if (o(P[i], P[j], P[k]) > 0) == (s > 0): v = max(v, L[(i, j, s)] + 1)
                L[(j, k, s)] = v; best[s] = max(best[s], v)
    return best[-1], best[1]
brute = sys.argv[1]
for f in sys.argv[2:]:
    P = [tuple(map(int, l.split())) for l in open(f) if l.strip()]
    chirotope_of(P)
    br = subprocess.run([brute, str(len(P)), "40"], input=bits(P) + "\n", capture_output=True, text=True).stdout.split()
    print(json.dumps({"file": os.path.basename(f), "n": len(P), "distinct_x": len({p[0] for p in P}) == len(P),
                      "general_position": True, "cap_cup": capcup(P), "lcs": largest_convex_subset(P),
                      "brute_axviol_cap_cup_lcs": br[1:], "max_abs_bits": max(max(abs(x), abs(y)) for x, y in P).bit_length()}))
