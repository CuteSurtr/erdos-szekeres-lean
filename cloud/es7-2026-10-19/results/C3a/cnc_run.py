#!/usr/bin/env python3
"""Cube-and-conquer driver for C3a.

1. Reads a march_cu cube file and completes the cube tree: march omits leaves it refuted
   itself; for every cube prefix whose sibling branch is missing, the sibling is added as
   an extra leaf (so those are re-solved here and not taken on march's word).
2. Coverage: the negations of all leaves must form an UNSAT formula; this is solved with
   CaDiCaL --lrat and dual-checked (complete_tree.cnf / coverage.json).
3. Each leaf: CNF + cube literals as unit clauses, CaDiCaL --lrat (ASCII), then
   lrat-check (with the E2 empty-clause patch) AND cake_lpr; a leaf counts as closed only if
   both accept.  Leaf weight = 2^-depth (exact).  Results append to leaves.jsonl.
usage: cnc_run.py CNF CUBES OUTDIR WORKDIR --jobs J --limit SECONDS [--only i,j,...]
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import time
from fractions import Fraction

CAD = "/opt/s/cadical/build/cadical"
LRAT = "/opt/s/drat-trim/lrat-check-E2"
CAKE = "/opt/s/cake_lpr/cake_lpr"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_cubes(path):
    cubes = []
    for line in open(path):
        p = line.split()
        if p and p[0] == "a":
            assert p[-1] == "0"
            cubes.append([int(x) for x in p[1:-1]])
    return cubes


def complete(cubes):
    prefixes = set()
    for c in cubes:
        for j in range(len(c) + 1):
            prefixes.add(tuple(c[:j]))
    extra = []
    for c in cubes:
        for j in range(len(c)):
            sib = tuple(c[:j]) + (-c[j],)
            if sib not in prefixes:
                prefixes.add(sib)
                extra.append(list(sib))
    leaves = [tuple(c) for c in cubes] + [tuple(e) for e in extra]
    # no leaf may be a proper prefix of another (tree leaves)
    ls = set(leaves)
    for c in leaves:
        for j in range(len(c)):
            assert tuple(c[:j]) not in ls, ("leaf is prefix", c)
    return [list(c) for c in cubes], extra


def dual_check(cnf, proof):
    t = time.time()
    a = subprocess.run([LRAT, cnf, proof], capture_output=True, text=True).stdout
    a = next((l for l in a.splitlines() if l.startswith("c VERIFIED") or l.startswith("c NOT VERIFIED")), "none")
    env = dict(os.environ, CML_HEAP_SIZE="6000", CML_STACK_SIZE="2000")
    b = subprocess.run([CAKE, cnf, proof], capture_output=True, text=True, env=env).stdout.strip().splitlines()
    b = b[0] if b else "none"
    return a, b, (a == "c VERIFIED" and b == "s VERIFIED UNSAT"), round(time.time() - t, 1)


def leaf_cnf(base, nv, nc, cube, path):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {nc + len(cube)}\n")
        with open(base) as b:
            b.readline()
            while True:
                chunk = b.read(1 << 24)
                if not chunk:
                    break
                f.write(chunk)
        for l in cube:
            f.write(f"{l} 0\n")


def solve_leaf(args):
    idx, cube, base, nv, nc, work, limit, modeldir = args
    cnf = os.path.join(work, f"leaf{idx}.cnf")
    prf = os.path.join(work, f"leaf{idx}.lrat")
    leaf_cnf(base, nv, nc, cube, cnf)
    t = time.time()
    p = subprocess.run(["timeout", str(limit + 60), CAD, "-q", "--lrat", "--binary=false", "-t", str(limit), cnf, prf],
                       capture_output=True, text=True)
    dt = round(time.time() - t, 1)
    st = next((l[2:] for l in p.stdout.splitlines() if l.startswith("s ")), "UNKNOWN")
    rec = {"idx": idx, "cube": cube, "depth": len(cube), "weight": f"1/{2 ** len(cube)}", "status": st,
           "solve_s": dt, "rc": p.returncode}
    if st == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(prf)
        a, b, ok, ct = dual_check(cnf, prf)
        rec.update({"lrat_check": a, "cake_lpr": b, "certified": ok, "check_s": ct})
    elif st == "SATISFIABLE":
        mp = os.path.join(modeldir, f"model_leaf{idx}.out")
        with open(mp, "w") as f:
            f.write(p.stdout)
        rec["model_file"] = mp
    for x in (cnf, prf):
        if os.path.exists(x):
            os.remove(x)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("cubes")
    ap.add_argument("outdir")
    ap.add_argument("work")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--limit", type=int, default=600)
    ap.add_argument("--only", default=None, help="comma-separated leaf indices")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    with open(a.cnf) as f:
        _, _, nv, nc = f.readline().split()
    nv, nc = int(nv), int(nc)
    cubes, extra = complete(read_cubes(a.cubes))
    leaves = cubes + extra
    info_p = os.path.join(a.outdir, "cubes.json")
    if not os.path.exists(info_p):
        info = {"cnf": a.cnf, "cnf_sha256": sha(a.cnf), "cubes": a.cubes, "cubes_sha256": sha(a.cubes),
                "march_cubes": len(cubes), "added_refuted_siblings": len(extra), "leaves": len(leaves),
                "weights_sum": str(sum(Fraction(1, 2 ** len(c)) for c in leaves))}
        # coverage: OR of leaves is a tautology  <=>  AND of negated leaves is UNSAT
        cov = os.path.join(a.work, "coverage.cnf")
        vs = sorted({abs(l) for c in leaves for l in c})
        with open(cov, "w") as f:
            f.write(f"p cnf {max(vs)} {len(leaves)}\n")
            for c in leaves:
                f.write(" ".join(str(-l) for l in c) + " 0\n")
        pr = cov + ".lrat"
        o = subprocess.run([CAD, "-q", "--lrat", "--binary=false", cov, pr], capture_output=True, text=True).stdout
        info["coverage_solver"] = next((l for l in o.splitlines() if l.startswith("s ")), "none")
        if "UNSAT" in info["coverage_solver"]:
            info["coverage_lrat_check"], info["coverage_cake_lpr"], info["coverage_certified"], _ = dual_check(cov, pr)
        json.dump(info, open(info_p, "w"), indent=1)
        json.dump(leaves, open(os.path.join(a.outdir, "leaves_list.json"), "w"))
    print(open(info_p).read())
    done = set()
    lp = os.path.join(a.outdir, "leaves.jsonl")
    if os.path.exists(lp):
        for line in open(lp):
            r = json.loads(line)
            if r.get("certified") or r["status"] == "SATISFIABLE":
                done.add(r["idx"])
    todo = list(range(len(leaves)))
    if a.only:
        todo = [int(x) for x in a.only.split(",")]
    todo = [i for i in todo if i not in done]
    modeldir = os.path.join(a.outdir, "models")
    os.makedirs(modeldir, exist_ok=True)
    jobs = [(i, leaves[i], a.cnf, nv, nc, a.work, a.limit, modeldir) for i in todo]
    with cf.ProcessPoolExecutor(a.jobs) as ex, open(lp, "a") as out:
        for fut in cf.as_completed([ex.submit(solve_leaf, j) for j in jobs]):
            rec = fut.result()
            rec["tag"] = a.tag
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(json.dumps({k: rec[k] for k in ("idx", "status", "solve_s") if k in rec}), flush=True)


if __name__ == "__main__":
    main()
