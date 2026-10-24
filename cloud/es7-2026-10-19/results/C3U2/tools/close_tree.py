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
C3U additions (results/C3U/TASK.md, results/C3U/sigma_split.md): node names may be sigma-cube names
"L__C" (hullcase.parse_node); the CNF of L__C is that of L followed by the units of C.  With
--sigma-split K (default 0: off, behaviour identical to C3T) a node L or L__C that times out is
sigma-split if L has at least 2 layers, |C| < S*K (S = --sigma-levels, default 2) and at least K
residues are free: its children are the 2^K nodes L__C' (C' = C plus the K smallest free
residues), record {"node", "split": true, "sigma_bits": [...], "children": 2^K}.  Otherwise it gets
the layer split; the layer children of L__C are L'__C for L' in tree_children(L) except those
whose newest layer contradicts C (hullcase.cube_layer_children).  The cap of a node is
caps[min(d, len(caps) - 1)], d = number of splits (layer or sigma, pre-splits included) from the
run's root to the node.
usage: close_tree.py BASE OUT.jsonl ROOTNODE [--jobs J] [--caps 300,300,600] [--hours H] [--cadopts=--sat]
       [--sigma-split K] [--sigma-levels S]
       close_tree.py BASE OUT.jsonl SHARD --shard I --nshards N ...
  SHARD mode: the roots are the depth-2 nodes of the layer tree (tree_children twice, H3 mirror
  reduction on; 1,630 nodes for m = 11), sorted by name; shard I of N takes those with index
  congruent to I mod N.  Caps then count from depth 2.
C3U2 changes (results/C3U2/TASK.md, results/C3AUDIT3/REPORT.md findings 2 and 3): on restart, a
record with a "cube" field (sigma_cubes.py format) is read as a record of node__C, never of node;
a timed-out node without children (layer split empty, no sigma split possible) gets no split record:
it stays in the open frontier, counted in "open_frontier" and listed in "unsplittable_nodes" at the
end of the run; an old split record with 0 children is treated as no split (the node is open)."""
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
from hullcase import cube_layer_children, free_residues, node_name, node_units, parse_node, sigma_children  # noqa: E402
from controls import dual  # noqa: E402

E = C3Enc(11, 7)
M, KC = 11, 7
WORK = "/opt/work/ct"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def solve(args):
    base, node, cap, modeldir, opts = args
    us = node_units(M, node, E.ccw, E.sig)
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
    ap.add_argument("--sigma-split", type=int, default=0, help="K: sigma-split timed-out nodes on K bits (0: off)")
    ap.add_argument("--sigma-levels", type=int, default=2, help="S: at most S sigma-splits of K bits per path")
    a = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    caps = [int(x) for x in a.caps.split(",")]
    base_sha = sha(a.base)
    done, split = set(), {}
    if os.path.exists(a.out):
        for l in open(a.out):
            r = json.loads(l)
            if "cube" in r:
                # C3U2 (C3AUDIT3 finding 3): a sigma_cubes.py record ("node" = parent N, "cube" = {r: v})
                # is a record of N__C (C sorted by residue, as compose.py reads it), never of N
                if r.get("certified"):
                    done.add(node_name(parse_node(r["node"])[0], sorted((int(x), v) for x, v in r["cube"].items())))
                continue
            if r.get("certified"):
                done.add(r["node"])
            if r.get("split"):
                split.setdefault(r["node"], r)
    deadline = time.time() + 3600 * a.hours
    if a.shard is not None:
        roots = sorted(layers_name(c2) for c1 in tree_children(11, 7, []) for c2 in tree_children(11, 7, c1))
        roots = [r for i, r in enumerate(roots) if i % a.nshards == a.shard]
    else:
        roots = [node_name(*parse_node(a.root))]
    root = roots[0] if len(roots) == 1 else f"shard {a.shard}/{a.nshards} ({len(roots)} roots)"

    def layer_kids(name):
        return [node_name(L, C) for L, C in cube_layer_children(M, KC, *parse_node(name))]

    def sigma_kids(name, K):
        return [node_name(L, C) for L, C in sigma_children(M, *parse_node(name), K)[1]]

    def kids(rec):
        # children of a split record: sigma split iff it carries sigma_bits
        if "sigma_bits" in rec:
            return sigma_kids(rec["node"], len(rec["sigma_bits"]))
        return layer_kids(rec["node"])

    def expand(name, d):
        # (name, d): d = splits from the run's root
        if name in done:
            return []
        if name in split:
            ks = kids(split[name])
            if ks:
                return [x for c in ks for x in expand(c, d + 1)]
            # C3U2: a split record without children (written before C3U2) splits nothing: still open
        return [(name, d)]

    def presplit(names):
        out = []
        for nm, d in names:
            L = parse_node(nm)[0]
            # only a single-orbit layer directly below a two-orbit layer (or below the top) is
            # pre-split; runs of single-orbit layers are solved, else the tree explodes
            if (a.split_singles and len(L) >= 2 and len(L[-1]) == 1 and (len(L) == 2 or len(L[-2]) == 2)
                    and tree_children(11, 7, L)):
                ch = layer_kids(nm)
                fo.write(json.dumps({"node": nm, "split": True, "children": len(ch), "presplit": True}) + "\n"); fo.flush()
                out += presplit([(c, d + 1) for c in ch])
            else:
                out.append((nm, d))
        return out

    fo = open(a.out, "a")
    unsplittable = []  # C3U2 (C3AUDIT3 finding 2): timed-out nodes without children, still open
    frontier = sorted((x for r in roots for x in expand(r, 0)), key=lambda x: (len(parse_node(x[0])[0]), x[0].count("-")))
    frontier = presplit(frontier)
    with cf.ProcessPoolExecutor(a.jobs) as ex:
        while frontier and time.time() < deadline:
            futs = {ex.submit(solve, (a.base, n, caps[min(d, len(caps) - 1)], a.modeldir,
                                   [o for o in a.cadopts.split(",") if o])): (n, d)
                    for n, d in frontier}
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
                n, d = futs[fu]
                L, C = parse_node(n)
                K = a.sigma_split
                if K > 0 and len(L) >= 2 and len(C) < a.sigma_levels * K and len(free_residues(M, L, C)) >= K:
                    bits = sigma_children(M, L, C, K)[0]
                    ch = sigma_kids(n, K)
                    fo.write(json.dumps({"node": n, "split": True, "sigma_bits": bits, "children": len(ch)}) + "\n"); fo.flush()
                    nxt += [(c, d + 1) for c in ch]
                    continue
                ch = layer_kids(n)
                if not ch:
                    # C3U2 (C3AUDIT3 finding 2): no split record with 0 children; the node stays open
                    unsplittable.append(n)
                    print(json.dumps({"node": n, "unsplittable": True}), flush=True)
                    continue
                fo.write(json.dumps({"node": n, "split": True, "children": len(ch)}) + "\n"); fo.flush()
                nxt += presplit([(c, d + 1) for c in ch])
            frontier = nxt
    print(json.dumps({"root": root, "open_frontier": len(frontier) + len(unsplittable),
                      "unsplittable": len(unsplittable), "unsplittable_nodes": sorted(unsplittable)}), flush=True)


if __name__ == "__main__":
    main()
