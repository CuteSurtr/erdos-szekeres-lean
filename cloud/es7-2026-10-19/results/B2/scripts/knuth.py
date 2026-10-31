#!/usr/bin/env python3
"""Knuth-style random probes of a fixed-budget cube tree (tree-size estimation).

Uses the same worker (cncw) and split heuristic as cnc2.py, but every node gets the same
conflict budget B. A probe descends from the root: if the node closes (U) the probe ends
(leaf at depth L); if it splits, the probe follows a uniformly random child. Knuth's unbiased
estimator for the tree with this budget:
    nodes ~ sum_{d=0..L} 2^d,     cost ~ sum_{d=0..L} 2^d * secs(node at depth d).
A probe stopped by --max-depth or --max-probe-secs is censored (its value is a lower bound).
Note: the worker is incremental, so later probes inherit learned clauses from earlier ones
(this lowers per-node cost relative to a cold start, as in the real cube-and-conquer run).

usage: knuth.py --cnf F --nx NX --worker-bin W --out FILE.jsonl --budget B [--seed S]
                [--max-depth D] [--max-probe-secs T] [--deadline EPOCH]
"""
import argparse, json, random, subprocess, time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cnf", required=True); ap.add_argument("--nx", type=int, required=True)
ap.add_argument("--worker-bin", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--budget", type=int, default=10000); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--max-depth", type=int, default=80); ap.add_argument("--max-probe-secs", type=float, default=5400)
ap.add_argument("--deadline", type=float, default=None)
a = ap.parse_args()
rng = random.Random(a.seed)
mdir = Path(a.out).with_suffix(".models"); mdir.mkdir(exist_ok=True)
p = subprocess.Popen([a.worker_bin, a.cnf, str(a.nx), str(mdir)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     text=True, bufsize=1)
assert p.stdout.readline().startswith("READY")
log = open(a.out, "a")
jid = 0
while not (a.deadline and time.time() > a.deadline):
    cube = []; secs = []; t0 = time.time(); end = None
    while True:
        jid += 1
        p.stdin.write(f"{jid} {a.budget} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        s = float(r[2] if r[0] != "K" else r[3]); secs.append(s)
        if r[0] == "U":
            end = "closed"; break
        if r[0] == "S":
            end = "SAT"; break
        lit = int(r[2])
        if lit == 0:
            end = "no-split"; break
        cube.append(lit if rng.random() < 0.5 else -lit)
        if len(cube) >= a.max_depth or time.time() - t0 > a.max_probe_secs or (a.deadline and time.time() > a.deadline):
            end = "censored"; break
    L = len(cube)
    est_nodes = sum(2 ** d for d in range(len(secs)))
    est_cost = sum((2 ** d) * s for d, s in enumerate(secs))
    log.write(json.dumps({"seed": a.seed, "budget": a.budget, "end": end, "leaf_depth": L, "est_nodes": est_nodes,
                          "est_cost_s": est_cost, "secs": [round(x, 2) for x in secs], "cube": cube,
                          "wall_s": round(time.time() - t0, 1)}) + "\n")
    log.flush()
    if end == "SAT":
        break
p.kill()
