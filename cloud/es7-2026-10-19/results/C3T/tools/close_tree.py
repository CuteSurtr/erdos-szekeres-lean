#!/usr/bin/env python3
"""Adaptive certified closure of a subtree of the layer tree.
Starting from ROOTNODE (a layer name), each node is solved by close_node's procedure (BASE + layer
units, CaDiCaL --lrat with cap CAP[d], dual-checked by lrat-check (E2 patch) and cake_lpr); a node
that is not closed within its cap is replaced by its children (hullcase.tree_children, H3 mirror
reduction on).  Every record goes to OUT (jsonl, same format as close_node.py, plus "split":
true for nodes that were split).  Restartable: certified nodes and split nodes in OUT are reused.
A SAT answer stops the run (candidate model, saved under MODELDIR).
C3T (FIX1) additions, all other fields unchanged: every solve record also has "cadical_args" (the
full CaDiCaL argument list without the CNF and proof paths) and "proof_sha256" (sha256 of the LRAT
file that both checkers read, computed before they run and before the proof is deleted; null when
CaDiCaL did not answer UNSATISFIABLE).
usage: close_tree.py BASE OUT.jsonl ROOTNODE [--jobs J] [--caps 300,300,600] [--hours H] [--cadopts=--sat]
       close_tree.py BASE OUT.jsonl SHARD --shard I --nshards N ...
  SHARD mode: the roots are the depth-2 nodes of the layer tree (tree_children twice, H3 mirror
  reduction on; 1,630 nodes for m = 11), sorted by name; shard I of N takes those with index
  congruent to I mod N.  Caps then count from depth 2."""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, layers_name, parse_layers, tree_children  # noqa: E402
from controls import dual  # noqa: E402

E = C3Enc(11, 7)
WORK = "/opt/work/ct"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def solve(args):
    base, node, cap, modeldir, opts = args
    us = [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]
    cnf, prf = os.path.join(WORK, node + ".cnf"), os.path.join(WORK, node + ".lrat")
    with open(base) as f, open(cnf, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
        while True:
            b = f.read(1 << 24)
            if not b:
                break
            g.write(b)
        g.write("".join(f"{u} 0\n" for u in us))
    rec = {"node": node, "units": len(us), "cnf_sha256": sha(cnf), "cap": cap, "cadical_opts": opts}
    cargs = ["-q", "-t", str(cap)] + opts + ["--lrat", "--binary=false"]
    rec["cadical_args"] = cargs
    t = time.time()
    r = subprocess.run(["cadical"] + cargs + [cnf, prf], capture_output=True, text=True).stdout
    rec["status"] = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
    rec["solve_s"] = round(time.time() - t, 1)
    rec["proof_sha256"] = None
    if rec["status"] == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(prf)
        rec["proof_sha256"] = sha(prf)
        t = time.time()
        a, b, ok = dual(cnf, prf)
        rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok, "check_s": round(time.time() - t, 1)})
    elif rec["status"] == "SATISFIABLE":
        os.makedirs(modeldir, exist_ok=True)
        mp = os.path.join(modeldir, f"model_{node}.out")
        open(mp, "w").write(r)
        rec["model_file"] = mp
    for x in (cnf, prf):
        if os.path.exists(x):
            os.remove(x)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base"); ap.add_argument("out"); ap.add_argument("root")
    ap.add_argument("--jobs", type=int, default=2); ap.add_argument("--caps", default="300,300,600")
    ap.add_argument("--hours", type=float, default=100); ap.add_argument("--modeldir", default="/opt/work/models")
    ap.add_argument("--cadopts", default="", help="extra CaDiCaL options, comma-separated (e.g. --sat)")
    ap.add_argument("--shard", type=int); ap.add_argument("--nshards", type=int)
    ap.add_argument("--split-singles", action="store_true",
                    help="split (without solving) a node whose newest layer is a single orbit and whose previous layer is not")
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    caps = [int(x) for x in a.caps.split(",")]
    base_sha = sha(a.base)
    done, split = set(), set()
    if os.path.exists(a.out):
        for l in open(a.out):
            r = json.loads(l)
            if r.get("certified"):
                done.add(r["node"])
            if r.get("split"):
                split.add(r["node"])
    deadline = time.time() + 3600 * a.hours
    if a.shard is not None:
        roots = sorted(layers_name(c2) for c1 in tree_children(11, 7, []) for c2 in tree_children(11, 7, c1))
        roots = [r for i, r in enumerate(roots) if i % a.nshards == a.shard]
        depth0 = 2
    else:
        roots = [layers_name(parse_layers(a.root))]
        depth0 = len(parse_layers(roots[0]))
    root = roots[0] if len(roots) == 1 else f"shard {a.shard}/{a.nshards} ({len(roots)} roots)"

    def expand(name):
        if name in done:
            return []
        if name in split:
            return [x for c in tree_children(11, 7, parse_layers(name)) for x in expand(layers_name(c))]
        return [name]

    def presplit(names):
        out = []
        for nm in names:
            L = parse_layers(nm)
            # only a single-orbit layer directly below a two-orbit layer (or below the top) is
            # pre-split; runs of single-orbit layers are solved, else the tree explodes
            if (a.split_singles and len(L) >= 2 and len(L[-1]) == 1 and (len(L) == 2 or len(L[-2]) == 2)
                    and tree_children(11, 7, L)):
                ch = [layers_name(c) for c in tree_children(11, 7, L)]
                fo.write(json.dumps({"node": nm, "split": True, "children": len(ch), "presplit": True}) + "\n"); fo.flush()
                out += presplit(ch)
            else:
                out.append(nm)
        return out

    fo = open(a.out, "a")
    frontier = sorted((x for r in roots for x in expand(r)), key=lambda x: (len(parse_layers(x)), x.count("-")))
    frontier = presplit(frontier)
    with cf.ProcessPoolExecutor(a.jobs) as ex:
        while frontier and time.time() < deadline:
            futs = {ex.submit(solve, (a.base, n, caps[min(len(parse_layers(n)) - depth0, len(caps) - 1)], a.modeldir,
                                   [o for o in a.cadopts.split(",") if o])): n
                    for n in frontier}
            nxt = []
            for fu in cf.as_completed(futs):
                r = fu.result()
                r["base_sha256"] = base_sha
                fo.write(json.dumps(r) + "\n"); fo.flush()
                print(json.dumps({k: r.get(k) for k in ("node", "status", "solve_s", "certified")}), flush=True)
                if r["status"] == "SATISFIABLE":
                    print("SAT FOUND", r["node"], flush=True)
                    return
                if r.get("certified"):
                    continue
                if r["status"] == "UNSATISFIABLE":
                    print("PROOF NOT ACCEPTED", r["node"], flush=True)
                    return
                ch = tree_children(11, 7, parse_layers(r["node"]))
                fo.write(json.dumps({"node": r["node"], "split": True, "children": len(ch)}) + "\n"); fo.flush()
                nxt += presplit([layers_name(c) for c in ch])
            frontier = nxt
    print(json.dumps({"root": root, "open_frontier": len(frontier)}), flush=True)


if __name__ == "__main__":
    main()
