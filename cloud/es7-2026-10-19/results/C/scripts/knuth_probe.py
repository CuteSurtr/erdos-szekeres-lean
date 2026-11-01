#!/usr/bin/env python3
"""Knuth-style random probes of the cube tree that cnc2/cncw would build.

usage: knuth_probe.py <cncw> <cnf> <cands> <outdir> <limit> <hours> [seed=1]

Each probe walks from the empty cube down a uniformly random branch: at every node the worker
runs CaDiCaL for `limit` conflicts under the cube; if that refutes the cube the node is a leaf,
otherwise the worker's restricted lookahead literal splits it and one child is chosen at random.
For a binary tree the Knuth estimator of the node count from a leaf at depth L is 2^(L+1) - 1;
leaf depths are logged so that the spread (and censoring at the time limit) is visible.  The
worker is persistent, so learned clauses carry over between probes (later probes are easier;
this biases the estimate downwards).
"""
import sys, os, json, random, subprocess, time
cncw, cnf, cands, out, limit, hours = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), float(sys.argv[6])
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
os.makedirs(out, exist_ok=True)
rng = random.Random(seed)
p = subprocess.Popen([cncw, cnf, cands, out], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
assert p.stdout.readline().startswith("READY")
log = open(os.path.join(out, "probes.jsonl"), "a")
deadline = time.time() + hours * 3600
jid = 0; probe = 0
while time.time() < deadline:
    cube = []; t0 = time.time(); path = []; status = "censored"
    while time.time() < deadline:
        jid += 1
        t1 = time.time()
        p.stdin.write(f"{jid} {limit} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        path.append(round(time.time() - t1, 1))
        if r[0] == "U": status = "leaf"; break
        if r[0] == "S": status = "SAT"; break
        lit = int(r[2])
        if lit == 0: status = "no_split"; break
        cube = cube + [lit if rng.random() < 0.5 else -lit]
    rec = {"probe": probe, "status": status, "leaf_depth": len(cube), "cube": cube, "secs": round(time.time() - t0, 1),
           "node_secs": path, "knuth_nodes": 2 ** (len(cube) + 1) - 1}
    log.write(json.dumps(rec) + "\n"); log.flush()
    probe += 1
    if status == "SAT": break
p.kill()
