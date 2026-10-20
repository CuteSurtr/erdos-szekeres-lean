#!/usr/bin/env python3
"""Shard cover check, using cover() from results/Mii-S/scripts/covercheck.py (copied here):
  shardcover.py top.icnf SHARD NSHARDS leaves.icnf
For each top cube t with 0-based line index i, i mod NSHARDS == SHARD, the leaves that extend t
(t as a literal set) with the literals of t removed must cover all assignments; a leaf that
contains -l for some l in t is not used for t."""
import sys
sys.setrecursionlimit(100000)
def restrict(z, cubes):
    return [[l for l in c if l != z] for c in cubes if -z not in c]
def cover(cubes):
    if any(len(c) == 0 for c in cubes): return True
    if not cubes: return False
    z = cubes[0][0]
    return z != 0 and cover(restrict(z, cubes)) and cover(restrict(-z, cubes))
rd = lambda f: [list(map(int, l.split()[1:-1])) for l in open(f) if l.startswith("a")]
top, s, k, leaves = rd(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), rd(sys.argv[4])
ok = bad = 0
for i, t in enumerate(top):
    if i % k != s: continue
    T = set(t); sub = [[l for l in c if l not in T] for c in leaves if not any(-l in T for l in c)]
    if cover(sub): ok += 1
    else: bad += 1; print("NOT COVERED top", i, t)
print(f"s {'COVERED' if bad == 0 else 'NOT COVERED'} {ok}/{ok + bad} top cubes, {len(leaves)} leaves")
