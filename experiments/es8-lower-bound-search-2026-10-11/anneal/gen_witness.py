#!/usr/bin/env python3
"""Dump witness(n) from the repository script (imported read-only) as 'x y' lines."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from es_lower_bound_witness import witness, general_position
n = int(sys.argv[1])
pts = witness(n)
assert general_position(pts) and len(set(pts)) == len(pts) == 2 ** (n - 2)
for x, y in pts:
    print(x, y)
