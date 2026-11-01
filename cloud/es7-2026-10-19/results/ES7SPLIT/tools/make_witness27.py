#!/usr/bin/env python3
"""Build the 27-point witness of Proposition 8(b) from the classical 32-point set (first part of
logs/prop8b_witness.txt).

Take the first (26, 6) z-split of the classical set found by tools/splits.py with cap_z(A) = 4, add the first point b of
the lower part B to the upper part A, and check: general position, largest convex subset, b a hull vertex, and the
number of convex hexagons through b (brute force over all 5-subsets of A).  The last line of the written file is b.
This is the inline code that wrote data/prop8b_witness27.txt, saved as a script; the output path is now an argument.
Usage: python3 tools/make_witness27.py OUT.txt
"""
import os
import sys
from itertools import combinations

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from geom import read_points, general_position, largest_convex_subset, hull, in_convex_position, longest_z_chains
import splits

out = sys.argv[1]
P = read_points(os.path.join(ROOT, "data", "classical32.txt"))
S = splits.all_splits(P)
for A, B, z in S:
    if len(A) == 26 and len(B) == 6:
        PA = [P[i] for i in sorted(A)]; PB = [P[i] for i in sorted(B)]
        cap, _ = longest_z_chains(PA, z)
        if cap != 4: continue
        b = PB[0]
        T = PA + [b]
        H = hull(T)
        ok_gp = general_position(T); gon = largest_convex_subset(T)
        inhull = b in H
        # is b a vertex of some convex hexagon of T?  brute force over 5-subsets of PA
        hexes = sum(1 for Q in combinations(PA, 5) if in_convex_position(list(Q) + [b]))
        print("split z =", tuple(str(v) for v in z), " cap_z(A) =", cap)
        print("27-point set: general position", ok_gp, "| largest convex subset", gon, "| b is a hull vertex", inhull,
              "| convex hexagons through b:", hexes)
        open(out, 'w').write(''.join(f"{x} {y}\n" for x, y in T))
        print(f"witness written to {out} (last line = the hull vertex b)")
        break
