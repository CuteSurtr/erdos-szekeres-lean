#!/usr/bin/env python3
"""Structural statistics of the distinct sets: hull size and convex
(K-1)-gon count (cgon count), per run family. usage: diversity.py K [maxper]"""
import collections, glob, os, random, statistics, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = int(sys.argv[1]); maxper = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull_size(P):
    n = len(P); h = 0
    for i in range(n):
        # extreme iff some a has all others strictly left of P[i]->P[a]
        for a in range(n):
            if a != i and all(orient(P[i], P[a], P[b]) > 0 for b in range(n) if b != i and b != a):
                h += 1; break
    return h


by = collections.defaultdict(list)
for fn in glob.glob(os.path.join(ROOT, "data", f"distinct_K{K}*.txt")):
    for l in open(fn):
        f = l.split(); by[f[0]].append(f)
rng = random.Random(1)
for run in sorted(by):
    rows = by[run]
    if len(rows) > maxper:
        rows = rng.sample(rows, maxper)
    hs = collections.Counter(); cK1 = []
    for f in rows:
        c = list(map(int, f[4:])); P = list(zip(c[0::2], c[1::2]))
        hs[hull_size(P)] += 1
        out = subprocess.run([os.path.join(ROOT, "bin", "cgon"), "count", str(K)], input="".join(f"{x} {y}\n" for x, y in P),
                             capture_output=True, text=True).stdout.split()
        d = dict(t.split("=") for t in out if "=" in t)
        assert d[f"c{K}"] == "0"
        cK1.append(int(d[f"c{K-1}"]))
    print(f"{run}: n_sets={len(rows)} hull_sizes={dict(sorted(hs.items()))} c{K-1}: min={min(cK1)} "
          f"median={statistics.median(cK1)} max={max(cK1)} distinct_values={len(set(cK1))}")
