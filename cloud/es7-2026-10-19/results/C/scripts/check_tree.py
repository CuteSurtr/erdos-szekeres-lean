#!/usr/bin/env python3
"""Check that the closed cubes of a cnc2 run (plus, optionally, its open cubes) form a complete
binary partition of the search space.

usage: check_tree.py <closed.txt> [state.json]

Cubes are literal sequences in split order.  A node (common prefix of length d) is covered if
some listed cube ends there, or if every listed cube below it continues with the same variable
v, both signs of v occur, and both children are covered.  Prints the exact closed weight, the
open weight (from state.json), whether closed + open covers the root, and whether the closed
cubes alone cover it.
"""
import sys, json
from fractions import Fraction
sys.setrecursionlimit(100000)
closed = set()
for line in open(sys.argv[1]):
    t = line.split()
    if t: closed.add(tuple(int(x) for x in t[1:-1]))
opn = set()
if len(sys.argv) > 2:
    opn = set(tuple(c) for c, _ in json.load(open(sys.argv[2]))["open"])
def covers(cubes, d):
    if any(len(c) == d for c in cubes): return True
    vs = set(abs(c[d]) for c in cubes)
    if len(vs) != 1: return False
    pos = [c for c in cubes if c[d] > 0]; neg = [c for c in cubes if c[d] < 0]
    return bool(pos) and bool(neg) and covers(pos, d + 1) and covers(neg, d + 1)
cw = sum((Fraction(1, 2 ** len(c)) for c in closed), Fraction(0))
ow = sum((Fraction(1, 2 ** len(c)) for c in opn), Fraction(0))
overlap = len(closed & opn)
res = {"closed_distinct": len(closed), "open": len(opn), "closed_and_open_overlap": overlap,
       "closed_weight": str(cw), "open_weight": str(ow), "sum": str(cw + ow),
       "closed_plus_open_cover_root": covers(list(closed | opn), 0),
       "closed_alone_cover_root": covers(list(closed), 0) if closed else False}
print(json.dumps(res))
