#!/usr/bin/env python3
"""Independent check (repository's exact DP only) for a set whose largest convex subset is s:
counts the points p with largest_convex_subset(S - p) < s, i.e. the size of the common
intersection of all maximum convex subsets. If it equals s, there is exactly one convex
s-gon."""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "scripts"))
from es_lower_bound_witness import largest_convex_subset, general_position
pts = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
assert len(set(pts)) == len(pts) and general_position(pts)
s = largest_convex_subset(pts)
core = [i for i in range(len(pts)) if largest_convex_subset(pts[:i] + pts[i + 1:]) < s]
print(f"{os.path.basename(sys.argv[1])}: N={len(pts)} general_position=True largest_convex_subset={s} "
      f"common_core_size={len(core)}" + (f" => exactly one convex {s}-gon" if len(core) == s else ""))
