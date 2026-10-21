#!/usr/bin/env python3
"""Knuth-style random probes of the convex-layer case tree (cost measurement, no proofs).

Tree: level 1 = the top hull cases of hullcase.cases(m, k) (in layer form); level j > 1 = the
choices of layer j below the chosen layers (hullcase.layer2_options on the residues not used yet),
until depth D or no residue is left.  Optionally the sigma bits of all residues not yet fixed are
also chosen at random (--sigma), adding a factor 2 per bit.  A walk picks a child uniformly at each
level; the leaf CNF = base CNF (gen_case.py ... none) + the layer clauses (units), solved with
CaDiCaL under a cap.  Knuth's estimator: (product of branching factors) * leaf time is an unbiased
estimate of the total leaf time of the depth-D tree (timeouts make it a lower bound).
usage: knuth_layers.py M K BASE_CNF D WALKS CAP OUT.jsonl [--seed S] [--jobs J] [--sigma]"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import cases, legacy_to_layers, layer2_options, layer_clauses, layers_name  # noqa: E402

E = None


def walk(rng, m, k, D, sigma):
    tops = [legacy_to_layers(c) for c in cases(m, k)]
    layers = [rng.choice(tops)[0]]
    w = len(tops)
    while len(layers) < D:
        top_used = [r for L in layers for r, _ in L]
        opts = layer2_options(m, [(r, None) for r in top_used])
        if not opts:
            break
        w *= len(opts)
        layers.append(rng.choice(opts))
    extra = []
    if sigma:
        fixed = {r for L in layers for r, s in L if s is not None} | {0}
        for r in range(m):
            if r not in fixed:
                b = rng.randint(0, 1)
                extra.append(E.s[r] if b else -E.s[r])
                w *= 2
    return layers, extra, w


def solve(args):
    base, units, cap, tag, work = args
    p = os.path.join(work, f"kl_{os.getpid()}_{tag}.cnf")
    with open(base) as f, open(p, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(units)}\n")
        while True:
            b = f.read(1 << 24)
            if not b:
                break
            g.write(b)
        for u in units:
            g.write(f"{u} 0\n")
    t = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(cap), p], capture_output=True, text=True).stdout
    os.remove(p)
    return next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN"), round(time.time() - t, 1)


def main():
    global E
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int); ap.add_argument("k", type=int); ap.add_argument("base")
    ap.add_argument("D", type=int); ap.add_argument("walks", type=int); ap.add_argument("cap", type=int)
    ap.add_argument("out"); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--sigma", action="store_true"); ap.add_argument("--work", default="/opt/work/probe")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    E = C3Enc(a.m, a.k)  # literal maps only (same numbering as the base CNF)
    rng = random.Random(a.seed)
    jobs = []
    for i in range(a.walks):
        layers, extra, w = walk(rng, a.m, a.k, a.D, a.sigma)
        units = [c[0] for c in layer_clauses(a.m, layers, E.ccw, E.sig)] + extra
        jobs.append((layers, extra, w, units, i))
    with cf.ProcessPoolExecutor(a.jobs) as ex, open(a.out, "a") as fo:
        futs = [ex.submit(solve, (a.base, j[3], a.cap, f"{a.seed}_{j[4]}", a.work)) for j in jobs]
        for j, fu in zip(jobs, futs):
            st, s = fu.result()
            rec = {"case": layers_name(j[0]), "sigma_units": j[1], "weight": j[2], "D": a.D, "status": st, "s": s,
                   "cap": a.cap, "seed": a.seed, "walk": j[4]}
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
