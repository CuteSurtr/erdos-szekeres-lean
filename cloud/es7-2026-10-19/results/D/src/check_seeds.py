#!/usr/bin/env python3
"""Format and count check of the near-miss seeds (nearfull_p2c/p2d).

Line format: "label E 33 x1 y1 ... x33 y33" (E = stored heptagon count).
For every seed: exact general position, convex k-gon counts (k <= 8) by the
cups/caps method (verify_exact.py) and by cgon.c, agreement, and E match.

usage: check_seeds.py OUTJSON SEEDFILES...
"""
import sys, os, json, collections
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_exact, dlib

out = {"files": {}}
for p in sys.argv[2:]:
    rows = []
    for line in open(p):
        f = line.split()
        if not f:
            continue
        n = int(f[2])
        assert len(f) == 3 + 2 * n, "bad field count"
        P = dlib.parse_line_pts(f, 2)
        gp, why = verify_exact.general_position(P)
        ex = verify_exact.count_convex(P, 8) if gp else {}
        cg = dlib.cgon_count(P, 8)
        rows.append({"label": f[0], "E_stored": int(f[1]), "n": n, "gp": gp, "c7": ex.get(7), "c8": ex.get(8),
                     "agree_cgon": cg is not None and all(cg[k] == ex[k] for k in range(3, 9)),
                     "max_abs_coord": max(max(abs(x), abs(y)) for x, y in P)})
    out["files"][os.path.basename(p)] = {
        "lines": len(rows), "n_values": sorted(set(r["n"] for r in rows)),
        "all_general_position": all(r["gp"] for r in rows),
        "c7_hist": dict(collections.Counter(r["c7"] for r in rows)),
        "c8_hist": dict(collections.Counter(r["c8"] for r in rows)),
        "E_stored_matches_c7": all(r["E_stored"] == r["c7"] for r in rows),
        "cups_caps_agrees_with_cgon": all(r["agree_cgon"] for r in rows),
        "max_abs_coord": max(r["max_abs_coord"] for r in rows),
        "distinct_labels": len(set(r["label"] for r in rows))}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
