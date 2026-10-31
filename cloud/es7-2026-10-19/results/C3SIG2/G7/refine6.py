#!/usr/bin/env python3
"""C3SIG2 step 3 refinement driver: for every open K=3 cube C of NODE recorded in OUT.jsonl, run the 8 cubes
on the 6 smallest free residues of NODE that extend C, via sigma_cubes.run (imported unmodified), 3 at a time,
appending the returned records to OUT.jsonl.   usage: refine6.py BASE OUT.jsonl NODE CAP JOBS"""
import concurrent.futures as cf
import itertools
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import sigma_cubes  # noqa: E402
from hullcase import parse_layers  # noqa: E402


def main():
    base, out, node, cap, jobs = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    used = {r for L in parse_layers(node) for r, _ in L}
    bits6 = [r for r in range(1, 11) if r not in used][:6]
    recs = [json.loads(l) for l in open(out)]
    k3 = [r for r in recs if r.get("node") == node and "cube" in r and len(r["cube"]) == 3]
    open3 = [r["cube"] for r in k3 if not r.get("certified")]
    tasks = []
    for c in open3:
        assert list(map(int, c)) == bits6[:3]
        for v in itertools.product((0, 1), repeat=3):
            tasks.append((base, node, bits6, tuple(c[str(r)] for r in bits6[:3]) + v, cap))
    print(json.dumps({"node": node, "bits6": bits6, "open_k3": open3, "tasks": len(tasks)}), flush=True)
    os.makedirs(sigma_cubes.WORK, exist_ok=True)
    with open(out, "a") as fo, cf.ProcessPoolExecutor(jobs) as ex:
        for rec in ex.map(sigma_cubes.run, tasks):
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps({x: rec.get(x) for x in ("node", "cube", "status", "solve_s", "certified")}), flush=True)


if __name__ == "__main__":
    main()
