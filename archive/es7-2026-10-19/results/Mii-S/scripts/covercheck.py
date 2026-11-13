#!/usr/bin/env python3
"""Python port of results/H3 Mir.coverCheck (CoverCore.lean), for quick sanity checks only;
the verified check is `lake exe cover_check` in results/H3.  Reads `a l1 .. 0` lines."""
import sys
sys.setrecursionlimit(100000)
def restrict(z, cubes):
    return [[l for l in c if l != z] for c in cubes if -z not in c]
def cover(cubes):
    if any(len(c) == 0 for c in cubes): return True
    if not cubes: return False
    z = cubes[0][0]
    return z != 0 and cover(restrict(z, cubes)) and cover(restrict(-z, cubes))
cubes = [list(map(int, l.split()[1:-1])) for f in sys.argv[1:] for l in open(f) if l.startswith("a")]
print("s COVERED" if cover(cubes) else "s NOT COVERED", len(cubes))
