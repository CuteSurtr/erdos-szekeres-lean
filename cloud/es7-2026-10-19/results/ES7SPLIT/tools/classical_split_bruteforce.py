#!/usr/bin/env python3
"""Brute-force cap_z(A) and cup_z(B) for every nontrivial z-split of the classical 32-point set
(produces logs/classical_split_bruteforce.txt).

The z-splits come from tools/splits.py; the chain lengths are recomputed from the all-triples definition of z-caps and
z-cups (no dynamic program).  This is the inline code that wrote the log, saved as a script; input paths are resolved
from the location of this file.  Usage: python3 tools/classical_split_bruteforce.py
"""
import os
import sys
from itertools import combinations

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from geom import read_points, z_sorted, z_same_side
import splits

P = read_points(os.path.join(ROOT, "data", "classical32.txt"))


def chain_type(Q, z):
    Q = z_sorted(list(Q), z)
    cup = all(z_same_side(Q[i], Q[k], Q[j], z) for i, j, k in combinations(range(len(Q)), 3))
    cap = all(not z_same_side(Q[i], Q[k], Q[j], z) for i, j, k in combinations(range(len(Q)), 3))
    return cap, cup


for A, B, z in splits.all_splits(P):
    PA = [P[i] for i in sorted(A)]; PB = [P[i] for i in sorted(B)]

    def maxlen(X, want):
        best = 2
        for r in range(3, min(len(X), 7) + 1):
            if any(chain_type(Q, z)[0 if want == 'cap' else 1] for Q in combinations(X, r)): best = r
            else: break
        return best
    print((len(A), len(B)), "z at infinity" if z[2] == 0 else "finite z", "| brute-force cap_z(A) =", maxlen(PA, 'cap'),
          " cup_z(B) =", maxlen(PB, 'cup'))
