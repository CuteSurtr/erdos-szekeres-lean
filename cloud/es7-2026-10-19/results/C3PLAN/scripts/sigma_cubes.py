#!/usr/bin/env python3
"""Experiment: split a layer-tree node on K free sigma bits (the K smallest residues r != 0 not in
any layer of the node) instead of on its next layer, and solve each of the 2^K cubes with the same
solve/check procedure as close_tree.py (CaDiCaL --sat --lrat, lrat-check E2 + cake_lpr).
The 2^K cubes cover every assignment of those bits, so the node is closed iff all cubes are UNSAT.
usage: sigma_cubes.py BASE OUT.jsonl NODE K CAP JOBS   (run from results/C3-S/tools)"""
import concurrent.futures as cf
import itertools
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.getcwd(), "..", "..", "C3a"))
sys.path.insert(0, os.getcwd())
from c3cnf import C3Enc  # noqa: E402
from hullcase import layer_clauses, parse_layers  # noqa: E402
from controls import dual  # noqa: E402
from close_tree import sha  # noqa: E402

E = C3Enc(11, 7)
WORK = "/opt/work/exp"


def run(args):
    base, node, bits, vals, cap = args
    us = [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]
    us += [E.sig(r) if v else -E.sig(r) for r, v in zip(bits, vals)]
    tag = node + "__" + "-".join(f"{r}s{v}" for r, v in zip(bits, vals))
    cnf, prf = os.path.join(WORK, tag + ".cnf"), os.path.join(WORK, tag + ".lrat")
    with open(base) as f, open(cnf, "w") as g:
        h = f.readline().split()
        g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n")
        g.write(f.read())
        g.write("".join(f"{u} 0\n" for u in us))
    rec = {"node": node, "cube": dict(zip(map(str, bits), vals)), "units": len(us), "cnf_sha256": sha(cnf), "cap": cap,
           "cadical_opts": ["--sat"]}
    t = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(cap), "--sat", "--lrat", "--binary=false", cnf, prf],
                       capture_output=True, text=True).stdout
    rec["status"] = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
    rec["solve_s"] = round(time.time() - t, 1)
    if rec["status"] == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(prf)
        t = time.time()
        a, b, ok = dual(cnf, prf)
        rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok, "check_s": round(time.time() - t, 1)})
    for x in (cnf, prf):
        if os.path.exists(x):
            os.remove(x)
    return rec


def main():
    base, out, node, k, cap, jobs = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    used = {r for L in parse_layers(node) for r, _ in L}
    bits = [r for r in range(1, 11) if r not in used][:k]
    os.makedirs(WORK, exist_ok=True)
    with open(out, "a") as fo, cf.ProcessPoolExecutor(jobs) as ex:
        for rec in ex.map(run, [(base, node, bits, v, cap) for v in itertools.product((0, 1), repeat=k)]):
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps({x: rec.get(x) for x in ("node", "cube", "status", "solve_s", "certified")}), flush=True)


if __name__ == "__main__":
    main()
