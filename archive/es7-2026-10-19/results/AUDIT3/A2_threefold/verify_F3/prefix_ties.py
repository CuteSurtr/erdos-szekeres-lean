#!/usr/bin/env python3
"""Exhaustive: for all integer triples (X'_i < X'_j < X'_k, Y' in a small grid, not collinear), the strict
inversion pattern (inv_ij, inv_ik, inv_jk), inv = [Y'_a > Y'_b], is a prefix of (ij, ik, jk) when chi' = +
and of (jk, ik, ij) when chi' = -.  Counts the triples with a Y'-tie (= an x-tie in S)."""
import itertools
G = range(-4, 5)
ok_p = {(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)}
ok_m = {(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)}
tot = ties = bad = 0
for xi, xj, xk in itertools.combinations(G, 3):
    for yi, yj, yk in itertools.product(G, repeat=3):
        d = (xj - xi) * (yk - yi) - (yj - yi) * (xk - xi)
        if d == 0:
            continue
        pat = (int(yi > yj), int(yi > yk), int(yj > yk))
        tot += 1
        t = len({yi, yj, yk}) < 3
        ties += t
        if pat not in (ok_p if d > 0 else ok_m):
            bad += 1
print({"triples": tot, "with_Y_tie": ties, "prefix_violations": bad})
