#!/usr/bin/env python3
"""Calibration (a): realize chirotopes that are known to be realizable.

Each trial draws a random point set, computes its exact chirotope, throws the coordinates away
and asks the realizer to find new ones (from its own random starts).  Families:
  uniform  : n integer points uniform in a square (no symmetry, methods default ins,free)
  multiscale: n points, each a random point of a random cluster with log-uniform radius
  sym      : m-fold rotationally symmetric sets (t random orbit representatives with log-uniform
             radius, optional centre), realized in the symmetric parametrisation
  pool     : chirotopes of given integer point sets (e.g. the 32-point heptagon-free pool),
             points scrambled (random relabelling) before realization
usage: calib_random.py FAMILY --n N [--m M --center] [--trials T] [--time S] [--jobs J]
                       [--methods ...] [--pool FILE] --out OUT.jsonl
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chiro import chirotope_of, orient_exact  # noqa: E402


def gen_points(fam, n, m, center, rng, pool=None):
    while True:
        if fam == "uniform":
            pts = [(rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)) for _ in range(n)]
        elif fam == "multiscale":
            pts = []
            ncl = rng.randint(2, 6)
            cl = [(rng.uniform(-1, 1), rng.uniform(-1, 1), math.exp(rng.uniform(-6, 0))) for _ in range(ncl)]
            for _ in range(n):
                cx, cy, r = rng.choice(cl)
                pts.append((int((cx + r * rng.uniform(-1, 1)) * 2 ** 40), int((cy + r * rng.uniform(-1, 1)) * 2 ** 40)))
        elif fam == "sym":
            t = (n - (1 if center else 0)) // m
            pts = []
            for o in range(t):
                r = math.exp(rng.uniform(-2, 2))
                th = rng.uniform(0, 2 * math.pi)
                for k in range(m):
                    a = th + 2 * math.pi * k / m
                    pts.append((round(r * math.cos(a) * 2 ** 30), round(r * math.sin(a) * 2 ** 30)))
            if center:
                pts.append((0, 0))
        elif fam == "pool":
            pts = list(rng.choice(pool))
            rng.shuffle(pts)   # scramble the labels
        elif fam == "sympool":
            # centrally symmetric, extremal-structured: S u -S for a random n/2-subset S of a pool
            # set, shifted by a random point of its bounding box (orbit o = {p_o, -p_o})
            base = list(rng.choice(pool))
            xs = [p[0] for p in base]; ys = [p[1] for p in base]
            cx = rng.randint(min(xs), max(xs)); cy = rng.randint(min(ys), max(ys))
            S = rng.sample(base, n // 2)
            pts = []
            for (x, y) in S:
                pts += [(2 * (x - cx) + 1, 2 * (y - cy)), (-2 * (x - cx) - 1, -2 * (y - cy))]
        try:
            if len(set(pts)) < len(pts):
                continue
            chi = chirotope_of(pts)
            return pts, chi
        except ValueError:
            continue


def work(job):
    k, fam, n, m, center, budget, methods, seed, pool = job
    from realize import realize
    rng = random.Random(seed)
    pts, chi = gen_points(fam, n, m, center, rng, pool)
    symm = fam in ("sym", "sympool")
    r = realize(chi, n, m if symm else 1, center if symm else False,
                budget=budget, seed=seed, methods=methods)
    return {"trial": k, "family": fam, "n": n, "m": m, "realized": r["realized"], "method": r["method"],
            "cpu_seconds": r["seconds"], "wall_seconds": r["wall_seconds"], "best_violations": r["best_violations"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=["uniform", "multiscale", "sym", "pool", "sympool"])
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--center", action="store_true")
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--time", type=float, default=30, help="CPU-second budget per trial")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--methods", default=None)
    ap.add_argument("--pool")
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    methods = (a.methods or "auto").split(",")
    if methods == ["auto"]:
        from realize import default_methods
        symm = a.family in ("sym", "sympool")
        methods = default_methods(a.m if symm else 1, a.center if symm else False)
    pool = None
    if a.family in ("pool", "sympool"):
        pool = []
        for line in open(a.pool):
            p = line.split()
            # "label [label2] hash n x1 y1 ... xn yn": find the field n with 2n integers after it
            for i in range(len(p)):
                if p[i].lstrip("-").isdigit() and 2 * int(p[i]) == len(p) - i - 1:
                    cnt = int(p[i])
                    c = list(map(int, p[i + 1:]))
                    pool.append([(c[2 * j], c[2 * j + 1]) for j in range(cnt)])
                    break
        if a.family == "pool":
            a.n = len(pool[0])
    jobs = [(k, a.family, a.n, a.m, a.center, a.time, methods, a.seed + 7919 * k, pool) for k in range(a.trials)]
    t0 = time.time()
    res = []
    with open(a.out, "w") as fo, mp.Pool(a.jobs) as P:
        for r in P.imap_unordered(work, jobs):
            res.append(r)
            fo.write(json.dumps(r) + "\n")
            fo.flush()
    ok = [r for r in res if r["realized"]]
    st = sorted(r["cpu_seconds"] for r in ok)
    summ = {"family": a.family, "n": a.n, "m": a.m, "center": a.center, "methods": methods,
            "cpu_budget_s": a.time, "trials": len(res), "realized": len(ok),
            "median_cpu_seconds_realized": st[len(st) // 2] if st else None,
            "max_cpu_seconds_realized": st[-1] if st else None, "wall_s": round(time.time() - t0, 1)}
    print("CALIB " + json.dumps(summ), flush=True)
    with open(a.out, "a") as fo:
        fo.write(json.dumps({"summary": summ}) + "\n")


if __name__ == "__main__":
    main()
