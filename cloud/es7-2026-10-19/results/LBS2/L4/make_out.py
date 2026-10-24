#!/usr/bin/env python3
"""data/e*_w*.jsonl.part*.gz -> out.jsonl, one compact JSON line per tested set."""
import glob, gzip, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
keys = ["generator", "worker", "run", "base_mild", "base_seed", "walk_seed", "steps", "rmin", "beta", "snap", "walk_len",
        "ot_hash", "c5", "c6", "hull", "max_abs_coord", "faces", "faces_hit", "bad_candidates", "saturated", "seconds"]
n = 0
with open(os.path.join(HERE, "out.jsonl"), "w") as g:
    for f in sorted(glob.glob(os.path.join(HERE, "data", "e*_w*.jsonl.part*.gz"))):
        epoch = int(re.match(r"e(\d+)_", os.path.basename(f)).group(1))
        for l in gzip.open(f, "rt"):
            r = json.loads(l)
            o = {"epoch": epoch}
            o.update({k: r.get(k, 0 if k == "beta" else None) for k in keys})
            o["faces_euler_eq_hit"] = r.get("faces") == r.get("faces_hit")
            o["gp_and_c7"] = [r["vfy4"]["general_position"], r["vfy4"]["c7"], r.get("py_general_position"), r.get("py_largest_convex_subset")]
            g.write(json.dumps(o, separators=(",", ":")) + "\n"); n += 1
print(n)
