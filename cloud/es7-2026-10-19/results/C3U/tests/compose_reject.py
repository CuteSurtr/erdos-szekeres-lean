#!/usr/bin/env python3
"""Mutation tests of compose.py (C3U) on a small sigma-split run (via tests/small.py).
usage: compose_reject.py TOOLSDIR m k BASE OUT.jsonl WORKDIR
Each mutation writes a copy of OUT with one change and runs compose.py on it; the brute-force
checker (check_small.py) is run on the same copy where the change removes a leaf."""
import json, os, subprocess, sys

tools, m, k, base, out, work = sys.argv[1:7]
sys.path.insert(0, tools)
import hullcase as h  # noqa: E402
here = os.path.dirname(os.path.abspath(__file__))
R = [json.loads(l) for l in open(out)]
os.makedirs(work, exist_ok=True)
cert = lambda r: r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"


def compose(recs, tag, brute=False):
    p = os.path.join(work, f"mut_{tag}.jsonl")
    with open(p, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in recs)
    c = subprocess.run([sys.executable, os.path.join(here, "small.py"), tools, m, k, "compose", base, p],
                       capture_output=True, text=True)
    last = (c.stdout.strip().splitlines() or [""])[-1]
    try:
        d = json.loads(last)
    except Exception:
        d = {"raw": (c.stdout + c.stderr)[-300:]}
    res = {"mutation": tag, "rc": c.returncode,
           "class_covered": d.get("class_covered"), "error": d.get("error"), "uncovered_sample": d.get("uncovered_sample", [])[:3]}
    if brute:
        b = subprocess.run([sys.executable, os.path.join(here, "check_small.py"), tools, m, k, base, p], capture_output=True, text=True)
        res["brute_force_holes"] = json.loads(b.stdout)["brute_force"]["holes"]
    return res


rows = [compose(R, "none", brute=True)]
sig = [i for i, r in enumerate(R) if r.get("split") and "sigma_bits" in r]
# a sigma-split parent with the most certified cube leaves (all of them if possible)
names = {r["node"]: i for i, r in enumerate(R) if cert(r)}
best = None
for i in sig:
    L, C = h.parse_node(R[i]["node"])
    kids = [c for c in (h.node_name(*c) for c in h.sigma_children(int(m), L, C, len(R[i]["sigma_bits"]))[1]) if c in names]
    if best is None or len(kids) > len(best[1]):
        best = (i, kids)
i, kids = best
# 1. missing cube
rows.append(compose([r for j, r in enumerate(R) if j != names[kids[-1]]], "missing_cube", brute=True))
rows[-1]["detail"] = kids[-1]
# 2. cube record with a wrong cnf_sha256
R2 = [dict(r) for r in R]
R2[names[kids[0]]]["cnf_sha256"] = "0" * 64
rows.append(compose(R2, "cube_wrong_cnf_sha256")); rows[-1]["detail"] = kids[0]
# 3. sigma-split record with wrong sigma_bits (a) reversed order, (b) the next free residue instead of the last
for tag, f in (("sigma_bits_reversed", lambda b, fr: b[::-1]), ("sigma_bits_not_smallest", lambda b, fr: b[:-1] + [fr[len(b)]] if len(fr) > len(b) else b[:-1] + [0])):
    R3 = [dict(r) for r in R]
    L, C = h.parse_node(R3[i]["node"])
    R3[i]["sigma_bits"] = f(R3[i]["sigma_bits"], h.free_residues(int(m), L, C))
    rows.append(compose(R3, tag)); rows[-1]["detail"] = f"{R3[i]['node']} sigma_bits {R[i]['sigma_bits']} -> {R3[i]['sigma_bits']}"
# 4. sigma split at depth 1 (H3 node) is refused
R4 = R + [{"node": "0s0", "split": True, "sigma_bits": h.free_residues(int(m), [[(0, 0)]], [])[:2], "children": 4}]
rows.append(compose(R4, "sigma_split_at_depth_1"))
# 5. a layer child of a cube node that does not conflict with C is dropped (its certified record removed)
done = False
for j, r in enumerate(R):
    if r.get("split") and "sigma_bits" not in r and "__" in r["node"]:
        L, C = h.parse_node(r["node"])
        for c in h.tree_children(int(m), int(k), L):
            nm = h.node_name(c, C)
            if not h.conflicts(c[-1], C) and nm in names and any(s is not None and rr in dict(C) for rr, s in c[-1]):
                rows.append(compose([x for jj, x in enumerate(R) if jj != names[nm]], "nonconflicting_layer_child_dropped", brute=True))
                rows[-1]["detail"] = f"{nm} (child of {r['node']}; its newest layer fixes a residue of C to C's value)"
                done = True
                break
        if done:
            break
for line in rows:
    print(json.dumps(line))
expect = {"none": (0, True), "missing_cube": (0, False), "cube_wrong_cnf_sha256": (1, None),
          "sigma_bits_reversed": (1, None), "sigma_bits_not_smallest": (1, None), "sigma_split_at_depth_1": (1, None),
          "nonconflicting_layer_child_dropped": (0, False)}
bad = [x["mutation"] for x in rows if (x["rc"], x["class_covered"]) != expect[x["mutation"]]
       or (x["mutation"] != "none" and x.get("brute_force_holes") == 0)]
missing = set(expect) - {x["mutation"] for x in rows}
print("FAILURES", len(bad) + len(missing), bad, sorted(missing))
