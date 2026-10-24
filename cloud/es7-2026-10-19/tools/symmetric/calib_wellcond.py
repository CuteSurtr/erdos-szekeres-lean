#!/usr/bin/env python3
"""Well-conditioned known-realizable symmetric chirotopes: random symmetric sets whose every
triple has |sin(angle)| >= margin; writes calib/wc_<tag>_<i>.sig (0-based, all P points)."""
import itertools, json, math, random, sys
sys.path.insert(0, ".")
from symvalidate import sample_points
from es_lower_bound_witness import orient
mp, tag, count, margin = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
info = json.load(open(mp)); rng = random.Random(2024)
got = 0; tried = 0
while got < count and tried < 20000:
    tried += 1
    pts = sample_points(info, rng)
    if pts is None: continue
    ok = True
    for a, b, c in itertools.combinations(range(len(pts)), 3):
        A, B, C = pts[a], pts[b], pts[c]
        d = orient(A, B, C)
        ux, uy, vx, vy = B[0]-A[0], B[1]-A[1], C[0]-A[0], C[1]-A[1]
        if abs(d) < margin * math.hypot(ux, uy) * math.hypot(vx, vy):
            ok = False; break
    if not ok: continue
    got += 1
    with open(f"calib/wc_{tag}_{got}.sig", "w") as f:
        for a, b, c in itertools.combinations(range(len(pts)), 3):
            f.write(f"{a} {b} {c} {1 if orient(pts[a], pts[b], pts[c]) > 0 else -1}\n")
print(f"{tag}: margin={margin} found {got} well-conditioned sets in {tried} samples")
