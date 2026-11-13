#!/usr/bin/env python3
"""C3SIG2 refinement driver: for every open K=3 sigma cube C of NODE (no certified record in OUT), run the 8 cubes on the
6 smallest free residues of NODE that extend C, via sigma_cubes.run (imported unmodified), 3 at a time; append records to OUT.
usage: refine.py BASE OUT.jsonl NODE CAP JOBS   (run from results/C3-S/tools)"""
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
    recs = [json.loads(l) for l in open(out) if l.strip()]
    done3 = {tuple(r["cube"][str(b)] for b in bits6[:3]) for r in recs
             if r.get("node") == node and len(r.get("cube", {})) == 3 and r.get("certified")}
    opn = [c for c in itertools.product((0, 1), repeat=3) if c not in done3]
    tasks = [(base, node, bits6, c + e, cap) for c in opn for e in itertools.product((0, 1), repeat=3)]
    print(json.dumps({"node": node, "bits6": bits6, "open_k3": opn, "tasks": len(tasks)}), flush=True)
    os.makedirs(sigma_cubes.WORK, exist_ok=True)
    with open(out, "a") as fo, cf.ProcessPoolExecutor(jobs) as ex:
        for rec in ex.map(sigma_cubes.run, tasks):
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps({x: rec.get(x) for x in ("node", "cube", "status", "solve_s", "certified")}), flush=True)


if __name__ == "__main__":
    main()
