#!/usr/bin/env python3
"""Coverage check tolerant of re-split cubes (C2).  results/C/scripts/check_tree.py requires
all cubes below a node to branch on one variable; after a resume a cube can be re-split on a
different variable, leaving stale entries.  Here a node (prefix of length d) is covered if a
listed cube ends there, or if for SOME variable v occurring at position d both the +v and -v
children are covered using only cubes that continue with that literal.  This is still a sound
partition argument: the chosen children form a complete binary split of the node.

usage: check_tree2.py <closed.txt> [state.json] [extra cube files (closed.txt format) ...]
"""
import sys, json
from fractions import Fraction
sys.setrecursionlimit(100000)
def read(p):
    s = set()
    for line in open(p):
        t = line.split()
        if t: s.add(tuple(int(x) for x in t[1:-1]))
    return s
closed = read(sys.argv[1])
opn = set(tuple(c) for c, _ in json.load(open(sys.argv[2]))["open"]) if len(sys.argv) > 2 else set()
memo = {}
def covers(cubes, d):
    if any(len(c) == d for c in cubes): return True
    for v in sorted(set(abs(c[d]) for c in cubes)):
        pos = [c for c in cubes if c[d] == v]; neg = [c for c in cubes if c[d] == -v]
        if pos and neg and covers(pos, d + 1) and covers(neg, d + 1): return True
    return False
print(json.dumps({"closed_distinct": len(closed), "open": len(opn),
                  "closed_plus_open_cover_root": covers(list(closed | opn), 0),
                  "closed_alone_cover_root": covers(list(closed), 0)}))
