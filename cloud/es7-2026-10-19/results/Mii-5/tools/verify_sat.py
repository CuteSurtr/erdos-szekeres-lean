#!/usr/bin/env python3
"""Decode and brute-force check a SAT leaf of m33k7int.sub.cnf.

usage: verify_sat.py --model leaves_line.json <bindir>     (a leaves.jsonl record with "model")
       verify_sat.py --points pts.txt <bindir>              (test mode: x-sorted orientations of a point set)
Expands the orbit-substituted variables back to all X(i,j,k) (rep = min index of the mirror orbit
{X(i,j,k), X(34-k,34-j,34-i)}, as in results/C/scripts/mirgen.py), then checks: every X equals
its mirror partner, X(1,2,3) is true, the axis point 17 is not extreme (some X(i,17,k) true and
some false), and with gon7 the signotope axiom and the number of 7-subsets in convex position.
"""
import sys, json, itertools, subprocess, os
mode, path, bindir = sys.argv[1], sys.argv[2], sys.argv[3]
if mode == "--points":
    P = sorted(tuple(map(int, l.split())) for l in open(path) if l.strip())
    N = len(P)
    idx = list(itertools.combinations(range(N), 3))
    o = lambda a, b, c: (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    X = {(i+1, j+1, k+1): o(P[i], P[j], P[k]) > 0 for i, j, k in idx}
else:
    rec = json.loads(open(path).readline())
    N = 33
    val = {abs(l): l > 0 for l in rec["model"]}
    idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
    m = N + 1
    X = {}
    for (i, j, k), v in idx.items():
        w = idx[tuple(sorted((m - k, m - j, m - i)))]
        X[(i, j, k)] = val[min(v, w)]
res = {"N": N}
if N == 33:
    m = 34
    res["mirror_violations"] = sum(X[(i, j, k)] != X[tuple(sorted((m-k, m-j, m-i)))] for (i, j, k) in X)
    res["X123_true"] = X[(1, 2, 3)]
    ax = [X[(i, 17, k)] for i in range(1, 17) for k in range(18, 34)]
    res["axis_interior"] = any(ax) and not all(ax)
inp = f"{N}\n" + " ".join("1" if X[t] else "0" for t in itertools.combinations(range(1, N + 1), 3)) + "\n"
r = subprocess.run([os.path.join(bindir, "gon7")], input=inp, capture_output=True, text=True)
res.update(json.loads(r.stdout))
print(json.dumps(res))
