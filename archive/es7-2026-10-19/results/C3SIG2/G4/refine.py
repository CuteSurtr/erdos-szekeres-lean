#!/usr/bin/env python3
"""C3SIG2 refinement driver: for each open K=3 cube C of NODE, solve the 8 cubes on the 6 smallest free
residues that extend C, via sigma_cubes.run unmodified (3 at a time), appending records to OUT.
usage: refine.py BASE OUT.jsonl NODE CAP JOBS   (run from results/C3-S/tools)"""
import concurrent.futures as cf
import itertools
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import sigma_cubes  # noqa: E402
from hullcase import parse_layers  # noqa: E402

base, out, node, cap, jobs = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
used = {r for L in parse_layers(node) for r, _ in L}
bits6 = [r for r in range(1, 11) if r not in used][:6]
recs = [json.loads(l) for l in open(out)]
k3 = {tuple(x["cube"].get(str(r)) for r in bits6[:3]): x.get("certified") is True
      for x in recs if x.get("node") == node and "cube" in x and len(x["cube"]) == 3}
opn = [c for c in itertools.product((0, 1), repeat=3) if not k3.get(c, False)]
print(json.dumps({"node": node, "bits6": bits6, "open_k3": opn}), flush=True)
tasks = [(base, node, bits6, list(c) + list(v), cap) for c in opn for v in itertools.product((0, 1), repeat=3)]
os.makedirs(sigma_cubes.WORK, exist_ok=True)
with open(out, "a") as fo, cf.ProcessPoolExecutor(jobs) as ex:
    for rec in ex.map(sigma_cubes.run, tasks):
        fo.write(json.dumps(rec) + "\n"); fo.flush()
        print(json.dumps({x: rec.get(x) for x in ("node", "cube", "status", "solve_s", "certified")}), flush=True)
