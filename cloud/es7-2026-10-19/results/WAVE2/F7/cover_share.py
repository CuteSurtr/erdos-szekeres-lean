#!/usr/bin/env python3
"""F7: check that the leaves cover every share cube: for each top cube T, every total extension of T
satisfies some leaf. Lines must be 'a ... 0'.  cover_share.py TOP.icnf LEAVES.icnf"""
import sys
def rd(p):
    out = []
    for l in open(p):
        if l.startswith("c"): continue
        assert l.startswith("a ") and l.endswith(" 0\n"), l; out.append(frozenset(map(int, l.split()[1:-1])))
    return out
top, leaves = rd(sys.argv[1]), rd(sys.argv[2])
sys.setrecursionlimit(10000)
def cov(P, L):
    L = [x for x in L if not any(-v in P for v in x)]   # leaves consistent with P
    if not L: return False
    if any(x <= P for x in L): return True
    v = next(iter(next(x for x in L) - P))
    return cov(P | {v}, L) and cov(P | {-v}, L)
bad = [t for t in top if not cov(t, leaves)]
print("s COVERED" if not bad else f"s NOT COVERED {len(bad)}", len(top), "top cubes,", len(leaves), "leaves")
