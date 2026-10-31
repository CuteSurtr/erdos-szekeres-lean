#!/usr/bin/env python3
"""Baselines for sub-case (ii): closed measure of C2's and Mii's cube runs.

Collects every closed (UNSAT) cube from results/C2/logs/cnc_ii_interior/closed.txt and from
results/Mii-*/leaves.jsonl (records with a "cube" and status UNSAT/UNSATISFIABLE), plus the
CPU seconds the Mii shards logged (solve_s/time_s/split_s/march_s).  The closed measure is
the probability that a uniformly random assignment of the orientation orbits satisfies some
closed cube (Monte Carlo, NSAMP samples; the usual 2^-len weight of a cube is its measure).
Usage: baseline.py RESULTS_DIR NSAMP SEED
"""
import glob, json, os, sys
import numpy as np
R, NS, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def c2():
    out = []
    for line in open(os.path.join(R, "C2/logs/cnc_ii_interior/closed.txt")):
        f = line.split()
        out.append(tuple(int(x) for x in f[1:-1]))
    return out
def mii():
    cubes = {}; cpu = {}
    for f in sorted(glob.glob(os.path.join(R, "Mii-[0-9]/leaves.jsonl"))):
        sh = f.split("/")[-2]; cs = []; t = 0.0
        for line in open(f):
            r = json.loads(line)
            for k in ("solve_s", "time_s", "split_s", "march_s"):
                if isinstance(r.get(k), (int, float)): t += r[k]
            if "cube" in r and str(r.get("status")).startswith("UNSAT"):
                cs.append(tuple(r["cube"]))
        cubes[sh] = cs; cpu[sh] = t
    return cubes, cpu
def measure(cubes, rng):
    if not cubes: return 0.0
    vs = sorted({abs(l) for c in cubes for l in c}); pos = {v: i for i, v in enumerate(vs)}
    A = rng.random((NS, len(vs))) < 0.5; hit = np.zeros(NS, bool)
    for c in set(cubes):
        idx = [pos[abs(l)] for l in c]; sg = np.array([l > 0 for l in c])
        hit |= (A[:, idx] == sg).all(axis=1)
    return float(hit.mean())
rng = np.random.default_rng(seed)
C2 = c2(); M, cpu = mii(); allm = [c for v in M.values() for c in v]
res = {"nsamples": NS, "c2_closed_cubes": len(C2), "mii_closed_cubes": {k: len(v) for k, v in M.items()},
       "mii_cpu_core_h": {k: round(v / 3600, 2) for k, v in cpu.items()},
       "mii_cpu_core_h_total": round(sum(cpu.values()) / 3600, 2),
       "sum_2^-len_c2": sum(2.0 ** -len(c) for c in set(C2)),
       "sum_2^-len_mii": sum(2.0 ** -len(c) for c in set(allm)),
       "measure_c2": measure(C2, rng), "measure_mii": measure(allm, rng), "measure_union": measure(C2 + allm, rng)}
print(json.dumps(res, indent=1))
