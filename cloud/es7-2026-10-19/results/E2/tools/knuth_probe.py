#!/usr/bin/env python3
"""Knuth-style random-probe estimate of the cube-and-conquer tree below the current frontier.

Mimics cnc2.py's policy exactly: a cube of depth d is run with budget
min(cap, base * grow^d) (cnc2 children get parent*grow, rounded down at each step;
we reproduce that rounding), and if ccworker answers K with split literal l, one child
(cube+[l] or cube+[-l]) is chosen uniformly at random and the walk continues.  The walk
stops when the cube closes (U), a model is found (S), or max depth is hit.
Knuth's estimator: a walk from a frontier cube of depth d0 that closes at depth D gives
2^(D-d0) leaves for that cube's subtree (unbiased for the leaf count under this policy,
ignoring the incremental solver state).  Each record is written to OUT (jsonl).

usage: knuth_probe.py CNF NX STATE_JSON OUT --worker BIN [--walks N] [--seed S]
                      [--maxdepth 40] [--hours H] [--solver-opt=--elim=0]
"""
import argparse, json, random, subprocess, time
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("nx", type=int); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--worker", required=True); ap.add_argument("--walks", type=int, default=100)
ap.add_argument("--seed", type=int, default=7); ap.add_argument("--maxdepth", type=int, default=40)
ap.add_argument("--base", type=int, default=10000); ap.add_argument("--grow", type=float, default=1.2)
ap.add_argument("--cap", type=int, default=2_000_000); ap.add_argument("--hours", type=float, default=1e9)
ap.add_argument("--maxcand", type=int, default=400)
ap.add_argument("--solver-opt", action="append", default=[])
a = ap.parse_args()
rng = random.Random(a.seed)
frontier = json.load(open(a.state))["open"]
p = subprocess.Popen([a.worker, a.cnf, str(a.nx), "/tmp", str(a.maxcand)] + a.solver_opt,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
assert p.stdout.readline().startswith("READY")
deadline = time.time() + a.hours * 3600
jid = 0
for w in range(a.walks):
    if time.time() > deadline: break
    cube, budget = rng.choice(frontier)
    cube = list(cube); d0 = len(cube); steps = []
    t0 = time.time(); outcome = "maxdepth"
    while len(cube) < a.maxdepth and time.time() < deadline:
        jid += 1
        p.stdin.write(f"{jid} {budget} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        steps.append({"depth": len(cube), "budget": budget, "res": r[0], "ms": int(r[2])})
        with open(a.out + ".steps", "a") as f: f.write(json.dumps({"walk": w, **steps[-1], "lit": int(r[3]) if r[0] == "K" else None, "t": round(time.time() - t0, 1)}) + "\n")
        if r[0] == "U": outcome = "closed"; break
        if r[0] == "S": outcome = "SAT"; break
        lit = int(r[3]); budget = min(a.cap, int(budget * a.grow))
        if lit == 0: continue          # cnc2 retries with a bigger budget
        cube.append(lit if rng.random() < 0.5 else -lit)
    else:
        if time.time() >= deadline: outcome = "timeout"
    rec = {"walk": w, "start_depth": d0, "end_depth": len(cube), "outcome": outcome,
           "subtree_leaves_est": 2 ** (len(cube) - d0) if outcome == "closed" else None,
           "wall_s": round(time.time() - t0, 1), "steps": steps, "cube": cube}
    with open(a.out, "a") as f: f.write(json.dumps(rec) + "\n")
    print(json.dumps({k: rec[k] for k in ("walk", "start_depth", "end_depth", "outcome", "wall_s")}), flush=True)
    if outcome == "SAT": break
p.kill()
