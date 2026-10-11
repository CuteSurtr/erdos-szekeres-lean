#!/usr/bin/env python3
"""Independent verification of a point file: exact general position check and the
repository's O(N^4) largest_convex_subset DP (pure Python ints). Optional brute force
count of convex k-gons (argument k) for small sets."""
import sys, os, itertools
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from brute import general_position
from es_lower_bound_witness import largest_convex_subset
from brute_addpoint import brute_k
path = sys.argv[1]
pts = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
gp = general_position(pts)
lcs = largest_convex_subset(pts)
msg = f"{os.path.basename(path)}: N={len(pts)} general_position={gp} largest_convex_subset={lcs}"
if len(sys.argv) > 2:
    k = int(sys.argv[2])
    msg += f" brute_c{k}={brute_k(pts, k)}"
print(msg)
