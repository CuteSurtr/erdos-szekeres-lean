#!/usr/bin/env python3
"""Check that an icnf cube file is a binary decision tree (siblings split on one variable with
both signs) and report the exact total weight sum 2^-depth (1 means the cubes cover every
assignment; less means march_cu dropped refuted leaves, which are then NOT certified).
With RESULTS (cnc_run.py JSONL) also reports the exact LRAT-verified closed weight.
usage: coverage.py CUBES [RESULTS]"""
import json
import sys
from fractions import Fraction as F

cubes = [tuple(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith("a ")]
ok = True


def check(idx, d):
    global ok
    if len(idx) == 1 and len(cubes[idx[0]]) == d:
        return
    vs = set(abs(cubes[i][d]) for i in idx if len(cubes[i]) > d)
    if any(len(cubes[i]) == d for i in idx) or len(vs) != 1:
        ok = False
        return
    for s in (1, -1):
        sub = [i for i in idx if cubes[i][d] * s > 0]
        if sub:
            check(sub, d + 1)


check(list(range(len(cubes))), 0)
w = sum(F(1, 2 ** len(c)) for c in cubes)
res = {"cubes": len(cubes), "tree_ok": ok, "total_weight": str(w), "total_weight_dec": float(w),
       "depths": sorted(set(len(c) for c in cubes))}
if len(sys.argv) > 2:
    closed = F(0)
    st = {}
    for l in open(sys.argv[2]):
        r = json.loads(l)
        st[r["status"] + ("/" + r["lrat"] if "lrat" in r else "")] = st.get(r["status"] + ("/" + r["lrat"] if "lrat" in r else ""), 0) + 1
        if r["status"] == "UNSATISFIABLE" and r.get("certified"):
            closed += F(1, 2 ** len(cubes[r["cube"]]))
    res.update({"results": st, "closed_weight": str(closed), "closed_weight_dec": float(closed)})
print(json.dumps(res))
