#!/usr/bin/env python3
"""Random cube probes: sample cubes from a march_cu cube file, solve CNF + cube (as unit clauses)
with CaDiCaL under a time cap, no proof (a cost measurement only; nothing here is a closure).
usage: probe.py CNF CUBES N CAP OUT.jsonl [--seed S] [--jobs J]"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import subprocess
import time


def run(args):
    cnf, cube, idx, cap, work = args
    p = os.path.join(work, f"probe_{os.getpid()}_{idx}.cnf")
    with open(cnf) as f:
        h = f.readline().split()
        nv, nc = int(h[2]), int(h[3])
        with open(p, "w") as g:
            g.write(f"p cnf {nv} {nc + len(cube)}\n")
            while True:
                b = f.read(1 << 24)
                if not b:
                    break
                g.write(b)
            for l in cube:
                g.write(f"{l} 0\n")
    t = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(cap), p], capture_output=True, text=True).stdout
    os.remove(p)
    st = next((l[2:] for l in r.splitlines() if l.startswith("s ")), "UNKNOWN")
    return {"idx": idx, "depth": len(cube), "status": st, "s": round(time.time() - t, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf"); ap.add_argument("cubes"); ap.add_argument("n", type=int); ap.add_argument("cap", type=int)
    ap.add_argument("out"); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--work", default="/opt/work/probe")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    cubes = [[int(x) for x in l.split()[1:-1]] for l in open(a.cubes) if l.startswith("a ")]
    idx = random.Random(a.seed).sample(range(len(cubes)), min(a.n, len(cubes)))
    with cf.ProcessPoolExecutor(a.jobs) as ex, open(a.out, "a") as fo:
        for r in ex.map(run, [(a.cnf, cubes[i], i, a.cap, a.work) for i in idx]):
            r.update({"cnf": os.path.basename(a.cnf), "ncubes": len(cubes), "cap": a.cap})
            fo.write(json.dumps(r) + "\n"); fo.flush()
            print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
