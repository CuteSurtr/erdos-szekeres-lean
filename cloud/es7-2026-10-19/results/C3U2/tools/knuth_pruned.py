#!/usr/bin/env python3
"""Pruned convex-layer case tree: exact counts near the root and Knuth random walks below.

A node is a layer spec (hullcase.py).  Children of the root: the top hull cases; children of a
node: every choice of the next layer on the residues not used yet.  A node is pruned when
CORE + its layer units is UNSAT for CaDiCaL within PRUNE_CAP seconds, CORE being the C3a clauses
without the 7-gon part (sig, sb, prefix, forced, xorB, xorT); CORE is a subset of every case CNF,
so pruning is sound (for a certificate the pruned node still needs its own checked proof).
modes:
  count D            : number of unpruned nodes at depth 1..D (full enumeration)
  walk W [--leafcnf F --leafcap T --leafdepth L] : W Knuth walks to full depth; the estimate of
                       the number of unpruned complete decompositions is the product of the
                       unpruned-children counts; if --leafcnf, the node at depth L on the walk is
                       also solved on F (full CNF) + units with cap T (cost of a depth-L leaf).
usage: knuth_pruned.py CORE OUT.jsonl MODE N [--jobs J] [--seed S]"""
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

M, K = 11, 7
E = C3Enc(M, K)
WORK = "/opt/work/kp"


def units(layers):
    return [c[0] for c in layer_clauses(M, layers, E.ccw, E.sig)]


def solve(cnf, us, cap):
    p = os.path.join(WORK, f"n_{os.getpid()}_{random.random()}.cnf")
    with open(cnf) as f, open(p, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
        while True:
            b = f.read(1 << 24)
            if not b:
                break
            g.write(b)
        g.write("".join(f"{u} 0\n" for u in us))
    t = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(cap), p], capture_output=True, text=True).stdout
    os.remove(p)
    return next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN"), round(time.time() - t, 2)


def children(layers):
    if not layers:
        return [legacy_to_layers(c) for c in cases(M, K)]
    used = [r for L in layers for r, _ in L]
    return [layers + [o] for o in layer2_options(M, [(r, None) for r in used])]


def main():
    global WORK
    ap = argparse.ArgumentParser()
    ap.add_argument("core"); ap.add_argument("out"); ap.add_argument("mode"); ap.add_argument("n", type=int)
    ap.add_argument("--jobs", type=int, default=3); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--prune-cap", type=int, default=20)
    ap.add_argument("--leafcnf"); ap.add_argument("--leafcap", type=int, default=300); ap.add_argument("--leafdepth", type=int, default=3)
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    ex = cf.ProcessPoolExecutor(a.jobs)
    fo = open(a.out, "a")

    def alive(nodes):
        res = list(ex.map(solve, [a.core] * len(nodes), [units(x) for x in nodes], [a.prune_cap] * len(nodes)))
        return [x for x, (st, _) in zip(nodes, res) if st != "UNSATISFIABLE"], res

    if a.mode == "count":
        level = [[]]
        for d in range(1, a.n + 1):
            ch = [c for x in level for c in children(x)]
            t = time.time()
            level, res = alive(ch)
            rec = {"mode": "count", "depth": d, "children": len(ch), "unpruned": len(level),
                   "unknown": sum(1 for st, _ in res if st == "UNKNOWN"), "sat": sum(1 for st, _ in res if st == "SATISFIABLE"),
                   "check_s": round(time.time() - t, 1), "unpruned_names": [layers_name(x) for x in level] if len(level) < 3000 else None}
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps({k: v for k, v in rec.items() if k != "unpruned_names"}), flush=True)
    else:
        rng = random.Random(a.seed)
        for w in range(a.n):
            node, bs, leaf = [], [], None
            while True:
                ch = children(node)
                if not ch:
                    break
                al, _ = alive(ch)
                bs.append([len(ch), len(al)])
                if not al:
                    break
                node = rng.choice(al)
                if a.leafcnf and len(node) == a.leafdepth:
                    st, s = solve(a.leafcnf, units(node), a.leafcap)
                    leaf = {"case": layers_name(node), "status": st, "s": s, "cap": a.leafcap}
            est = 1
            for _, b in bs:
                est *= b
            done = bool(bs) and bs[-1][1] > 0
            rec = {"mode": "walk", "seed": a.seed, "walk": w, "branching": bs, "final": layers_name(node),
                   "complete": not children(node), "estimate_full_leaves": est if done else 0,
                   "depth_counts": [__import__("math").prod(b for _, b in bs[:j + 1]) for j in range(len(bs))], "leaf": leaf}
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
