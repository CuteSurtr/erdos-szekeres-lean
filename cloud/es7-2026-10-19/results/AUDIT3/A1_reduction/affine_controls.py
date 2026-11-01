#!/usr/bin/env python3
"""Controls for the affine-group enumerator of examples_check.py (run with RESULTS_DIR as argv[1] like it)."""
import importlib.util, json, random, sys
sys.argv = [sys.argv[0], "/nonexistent"]
spec = importlib.util.spec_from_file_location("ec", __file__.replace("affine_controls.py", "examples_check.py"))
src = open(spec.origin).read().split("\nout = {}")[0]          # definitions only, not the main loop
ns = {}
exec(compile(src, spec.origin, "exec"), ns)
res = {}
hexagon = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]            # regular hexagon in Eisenstein coords
res["regular hexagon (expect D6, order 12)"] = ns["analyse_group"](hexagon, ns["affine_group"](hexagon))
square = [(1, 0), (0, 1), (-1, 0), (0, -1)]
res["square (expect D4, order 8)"] = ns["analyse_group"](square, ns["affine_group"](square))
# an affine (non-orthogonal) image of a square: same group up to conjugation
sq2 = [(2 * x + y, x + 3 * y) for x, y in square]
res["affine image of square (expect D4, order 8)"] = ns["analyse_group"](sq2, ns["affine_group"](sq2))
random.seed(1)
while True:
    P = [(random.randint(-50, 50), random.randint(-50, 50)) for _ in range(12)]
    if len(set(P)) == 12 and all(ns["orient2"](a, b, c) for i, a in enumerate(P) for j, b in enumerate(P[i+1:], i+1) for c in P[j+1:]):
        break
res["random 12 points (expect C1, order 1)"] = ns["analyse_group"](P, ns["affine_group"](P))
for k, v in res.items():
    print(k, "->", v["type"], "order", v["order"], "fix centroid", v["all_fix_centroid"], "B-invariant", v["averaged_form_invariant"])
ok = [v["order"] for v in res.values()] == [12, 8, 8, 1]
print("CONTROLS_OK" if ok else "CONTROLS_FAIL")
sys.exit(0 if ok else 1)
