#!/usr/bin/env python3
"""Realizable-side control: simulated annealing over EXACT 3-fold (or D3) symmetric point sets
(Eisenstein-integer coordinates, see symval2.py) minimising the number of convex K-gon orbits
(counted exactly by geomcount).  A K-gon-free set found here is a real symmetric configuration,
so the corresponding CNF must be satisfiable; if the CNF is UNSAT, the encoding is wrong.
usage: anneal_sym.py N K c3|d3 iters seed geomcount [restarts]
prints JSON: best count per restart, and the first K-gon-free set (if any).
"""
import json
import math
import random
import subprocess
import sys

N, K, mode, iters, seed, geom = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
restarts = int(sys.argv[7]) if len(sys.argv) > 7 else 5
rng = random.Random(seed)


def R(p, k=1):
    a, b = p
    for _ in range(k % 3):
        a, b = -b, a - b
    return (a, b)


def S(p):
    a, b = p
    return (a - b, -b)


def points(reps):
    pts = []
    if mode == "c3":
        for p in reps:
            pts += [R(p, k) for k in range(3)]
    else:
        u0 = (reps[0][0], 0)
        pts += [R(u0, k) for k in range(3)]
        for p in reps[1:]:
            pts += [R(p, k) for k in range(3)] + [R(S(p), k) for k in range(3)]
    return pts


def score(reps):
    pts = points(reps)
    if len(set(pts)) != len(pts) or (0, 0) in pts:
        return 10 ** 9, pts
    n = len(pts)
    inp = f"{n} 1 {K}\n" + "".join(f"{x} {y}\n" for x, y in pts) + " ".join(map(str, range(n))) + "\n"
    out = subprocess.run([geom], input=inp, capture_output=True, text=True).stdout
    d = dict(kv.split("=") for kv in out.split())
    if int(d["collinear"]):
        return 10 ** 9, pts
    return int(d[f"orbits{K}"]), pts


nrep = N // 3 if mode == "c3" else 1 + (N - 3) // 6
M = 10 ** 6
res = {"N": N, "K": K, "mode": mode, "iters": iters, "best": [], "free_set": None}
for r in range(restarts):
    reps = [(rng.randint(-M, M), rng.randint(-M, M)) for _ in range(nrep)]
    cur, _ = score(reps)
    best = cur
    T = 3.0
    for it in range(iters):
        i = rng.randrange(nrep)
        s = M * math.exp(rng.uniform(math.log(1e-4), 0))
        new = list(reps)
        new[i] = (reps[i][0] + int(rng.gauss(0, s)), reps[i][1] + int(rng.gauss(0, s)))
        if rng.random() < 0.05:
            new[i] = (rng.randint(-M, M), rng.randint(-M, M))
        sc, pts = score(new)
        if sc <= cur or rng.random() < math.exp(-(sc - cur) / T):
            reps, cur = new, sc
            if cur < best:
                best = cur
            if cur == 0:
                res["free_set"] = pts
                break
        T = max(0.05, T * 0.999)
    res["best"].append(best)
    if res["free_set"]:
        break
print(json.dumps(res))
