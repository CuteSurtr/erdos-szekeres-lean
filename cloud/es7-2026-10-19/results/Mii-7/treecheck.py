#!/usr/bin/env python3
"""Check that the cubes of a march_cu .icnf form a complete binary partition (every node splits
on one variable, both signs present, both children covered).  usage: treecheck.py <icnf>"""
import sys
sys.setrecursionlimit(10000)
cubes = [tuple(int(x) for x in l.split()[1:-1]) for l in open(sys.argv[1]) if l.startswith('a')]
def covers(cs, d):
    if any(len(c) == d for c in cs): return True
    vs = set(abs(c[d]) for c in cs)
    if len(vs) != 1: return False
    pos = [c for c in cs if c[d] > 0]; neg = [c for c in cs if c[d] < 0]
    return bool(pos) and bool(neg) and covers(pos, d + 1) and covers(neg, d + 1)
print({"cubes": len(cubes), "distinct": len(set(cubes)), "complete_binary_partition": covers(cubes, 0)})
