#!/usr/bin/env python3
"""Adaptive cube-and-conquer cost estimate on the convex-layer case tree (no proofs).

Policy being estimated: a node at depth d >= START is given to CaDiCaL (pysat cadical195, full
case CNF = BASE + the node's layer units as assumptions, incremental solver shared by the walk)
with a conflict budget BUDGET[d]; if it is not decided, it is split into all its children (next
convex layer; hullcase.layer2_options).  Nodes at depth < START are split without trying.
A Knuth walk follows one uniformly random child of each split node; its estimate of the total cost
is sum over visited nodes of (product of branching factors above the node) * (cost at the node),
and of the number of solver calls likewise.  Unbiased for the policy apart from the learned-clause
carry-over inside one walker process.  A SAT answer is a candidate model: written to MODELDIR.
usage: knuth_adaptive.py BASE OUT.jsonl WALKS [--seed S] [--start 2] [--budget 20000,50000,200000]"""
import argparse
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from pysat.formula import CNF  # noqa: E402
from pysat.solvers import Solver  # noqa: E402
from c3cnf import C3Enc  # noqa: E402
from hullcase import tree_children, layer_clauses, layers_name  # noqa: E402

M, K = 11, 7


MIRROR = False
TOP = None


def children(layers):
    ch = tree_children(M, K, layers, mirror=MIRROR)
    if not layers and TOP:  # stratum: only the H3 top case, or only the ten H6 cases
        ch = [c for c in ch if (len(c[0]) == 1) == (TOP == "H3")]
    if TOP == "H6single" and len(layers) == 1:  # stratum: one-orbit second layers below H6
        ch = [c for c in ch if len(c[1]) == 1]
    return ch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base"); ap.add_argument("out"); ap.add_argument("walks", type=int)
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--start", type=int, default=2)
    ap.add_argument("--budget", default="20000,50000,200000")
    ap.add_argument("--modeldir", default="/opt/work/models")
    ap.add_argument("--hours", type=float, default=100)
    ap.add_argument("--mirror", action="store_true", help="H3 mirror reduction at layer 2")
    ap.add_argument("--top", choices=["H3", "H6", "H6single"], help="stratum: estimate only this part of the tree")
    a = ap.parse_args()
    global MIRROR, TOP
    MIRROR, TOP = a.mirror, a.top
    budgets = [int(x) for x in a.budget.split(",")]
    E = C3Enc(M, K)
    S = Solver(name="cadical195", bootstrap_with=CNF(from_file=a.base).clauses)
    rng = random.Random(a.seed)
    deadline = time.time() + 3600 * a.hours
    fo = open(a.out, "a")
    for w in range(a.walks):
        if time.time() > deadline:
            break
        node, weight, path = [], 1, []
        est_s, est_calls, est_conf = 0.0, 0, 0
        outcome = "open"
        while True:
            d = len(node)
            if d >= a.start:
                us = [c[0] for c in layer_clauses(M, node, E.ccw, E.sig)]
                b = budgets[min(d - a.start, len(budgets) - 1)]
                S.conf_budget(b)
                c0 = S.accum_stats().get("conflicts", 0)
                t = time.time()
                r = S.solve_limited(assumptions=us)
                dt = time.time() - t
                dc = S.accum_stats().get("conflicts", 0) - c0
                path.append({"d": d, "case": layers_name(node), "w": weight, "res": r, "s": round(dt, 2), "conf": dc})
                est_s += weight * dt
                est_calls += weight
                est_conf += weight * dc
                if r is False:
                    outcome = "closed"
                    break
                if r is True:
                    os.makedirs(a.modeldir, exist_ok=True)
                    mp = os.path.join(a.modeldir, f"model_{layers_name(node)}_{a.seed}_{w}.json")
                    json.dump({"case": layers_name(node), "assumptions": us, "model": S.get_model()}, open(mp, "w"))
                    outcome = "SAT:" + mp
                    break
            ch = children(node)
            if not ch:
                outcome = "leaf-undecided"
                break
            weight *= len(ch)
            node = rng.choice(ch)
        rec = {"walk": w, "seed": a.seed, "outcome": outcome, "est_seconds": round(est_s, 1), "est_solver_calls": est_calls,
               "est_conflicts": est_conf, "path": path, "budgets": budgets, "start": a.start,
               "top": a.top, "mirror": a.mirror}
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        print(json.dumps({k: rec[k] for k in ("walk", "outcome", "est_seconds", "est_solver_calls")}), flush=True)


if __name__ == "__main__":
    main()
