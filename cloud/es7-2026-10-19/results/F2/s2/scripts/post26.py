#!/usr/bin/env python3
"""Independent exact re-check of realized 26-point sets (output lines of arm_f.py with "points"):
recompute the chirotope from the integer points (Python ints), require distinct x and no collinear
triple, compare with the recorded model string, and write the x-sorted signs for brute26.c.
usage: post26.py OUT_sets26.jsonl OUT_signs.txt IN.jsonl..."""
import sys, json, itertools, hashlib
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
out = open(sys.argv[1], "w"); sg = open(sys.argv[2], "w"); seen = set()
for path in sys.argv[3:]:
    for line in open(path):
        r = json.loads(line)
        if "points" not in r: continue
        P = [tuple(p) for p in r["points"]]; n = len(P)
        xs_ok = len({p[0] for p in P}) == n
        Q = sorted(P)
        signs = []; gp = True
        for i, j, k in itertools.combinations(range(n), 3):
            d = orient(Q[i], Q[j], Q[k]); gp &= d != 0; signs.append("+" if d > 0 else "-")
        signs = "".join(signs)
        rec = {"id": r["id"], "n": n, "distinct_x": xs_ok, "general_position": gp,
               "labels_x_sorted": P == Q, "model_matches_points": signs == r.get("model"),
               "max_abs_coord_bits": max(max(abs(x), abs(y)) for x, y in P).bit_length(),
               "sha1_signs": hashlib.sha1(signs.encode()).hexdigest()[:16], "points": [list(p) for p in Q]}
        if rec["sha1_signs"] in seen: continue
        seen.add(rec["sha1_signs"])
        out.write(json.dumps(rec) + "\n"); sg.write(signs + "\n")
        print(json.dumps({k: v for k, v in rec.items() if k != "points"}))
