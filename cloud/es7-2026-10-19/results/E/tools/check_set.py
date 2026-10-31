#!/usr/bin/env python3
"""Evaluate a symmetric CNF on one given exact symmetric point set (Eisenstein coordinates, in
the orbit-wise order written by anneal_sym.py).  The set is relabelled into the normal form,
its orientations are mapped to the CNF variables, and cnfeval decides the CNF under them.
A K-gon-free set must give sat=1.
usage: check_set.py cnf map.json c3|d3 points.json cnfeval geomcount
(points.json: the JSON output of anneal_sym.py, field free_set)
"""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symval2  # noqa: E402

cnf, mp, mode, ptsf, cnfeval, geom = sys.argv[1:7]
info = json.load(open(mp))
pts_in = [tuple(p) for p in json.load(open(ptsf))["free_set"]]
if mode == "c3":
    reps = pts_in[0::3]
else:
    reps = [pts_in[0]]
    for i in range(3, len(pts_in), 6):
        reps += [pts_in[i], pts_in[i + 3]]
pts = symval2.label(reps)
assert pts is not None, "labelling failed (degenerate set)"
assert sorted(pts[:-1]) == sorted(pts_in), "relabelled set differs from the input set"
val = {}
conf = 0
for a, b, c, v, s in info["triples"]:
    chi = 1 if symval2.orient(pts[a], pts[b], pts[c]) > 0 else -1
    want = s * chi > 0
    if v in val and val[v] != want:
        conf += 1
    val[v] = want
nX = info["X_vars"]
with tempfile.NamedTemporaryFile("w", suffix=".asg", delete=False) as f:
    f.write(" ".join(str(v if val[v] else -v) for v in range(1, nX + 1)) + "\n")
    asg = f.name
ev = subprocess.run([cnfeval, cnf, str(nX), asg], capture_output=True, text=True, check=True).stdout.split()
os.remove(asg)
setpts = info["setpts"]
perms = symval2.group_perms(pts, setpts, "d3" if info.get("group") == "D3" else "c3")
inp = f"{len(setpts)} {len(perms)} {info['K']}\n" + "".join(f"{pts[i][0]} {pts[i][1]}\n" for i in setpts)
inp += "".join(" ".join(map(str, p)) + "\n" for p in perms)
g = subprocess.run([geom], input=inp, capture_output=True, text=True, check=True).stdout.split()
print(json.dumps({"cnf": os.path.basename(cnf), "points": len(pts_in), "map_conflicts": conf,
                  "cnfeval": dict(kv.split("=") for kv in ev), "geomcount": dict(kv.split("=") for kv in g)}))
