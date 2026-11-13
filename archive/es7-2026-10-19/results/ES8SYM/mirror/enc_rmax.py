#!/usr/bin/env python3
"""CNF for: n points (sorted by x, general position) with NO 4-CAP and NO 8 POINTS IN CONVEX POSITION,
in the signotope (abstract order type) relaxation.

Variables t(i,j,k), i<j<k (1-based points in x-order): true <=> orient(p_i,p_j,p_k) > 0 (left turn: p_j below
segment p_i p_k; for x-sorted points this is "slope(i,j) < slope(j,k)").
Clauses:
 (S) signotope axioms: for i<j<k<l, the sequence t(ijk), t(ijl), t(ikl), t(jkl) changes sign at most once
     (forbid +,-,+ and -,+,- on every 3 of the 4 positions). Every x-sorted point set in general position satisfies
     this (Felsner–Weil).
 (C) no 4-cap: for i<j<k<l: t(ijk) or t(jkl)   (a 4-cap is exactly ~t(ijk) & ~t(jkl)).
 (W) cup propagation: w(i,k,l,L) = "there is an L-cup starting at p_i whose last two points are p_k, p_l".
       t(i,k,l) -> w(i,k,l,3);   w(i,j,k,L) & t(j,k,l) -> w(i,k,l,L+1)   (L = 3..7).
 (8) no 8-cup:  ~w(i,k,l,8).
 (7) no 7-cup with a point above its chord inside its x-span:  w(i,k,l,7) -> t(i,x,l)  for every i < x < l, x != k.
     (If x is strictly above the chord p_i p_l, i.e. ~t(i,x,l), then the 7-cup plus x is a convex octagon: lower chain
     the cup, upper chain p_i, x, p_l.)
Soundness: a real x-sorted point set in general position with no 4-cap and no convex octagon satisfies every clause
(only forcing implications are used for w, so the real orientations extend to a model by setting w to its true
meaning). Hence UNSAT for n means: no such real set of n points.
usage: enc_rmax.py n out.cnf [assume_file]   (assume_file: optional "i j k sign" lines added as unit clauses)"""
import sys
from itertools import combinations

n = int(sys.argv[1]); out = sys.argv[2]
var = {}
def v(key):
    if key not in var:
        var[key] = len(var) + 1
    return var[key]
for i, j, k in combinations(range(1, n + 1), 3):
    v(("t", i, j, k))
def t(i, j, k): return var[("t", i, j, k)]
cl = []
for i, j, k, l in combinations(range(1, n + 1), 4):
    seq = [t(i, j, k), t(i, j, l), t(i, k, l), t(j, k, l)]
    for a, b, c in combinations(range(4), 3):
        x, y, z = seq[a], seq[b], seq[c]
        cl.append([-x, y, -z])        # forbid +,-,+
        cl.append([x, -y, z])         # forbid -,+,-
    cl.append([t(i, j, k), t(j, k, l)])   # no 4-cap
def w(i, k, l, L): return v(("w", i, k, l, L))
for i, k, l in combinations(range(1, n + 1), 3):
    cl.append([-t(i, k, l), w(i, k, l, 3)])
for i, j, k, l in combinations(range(1, n + 1), 4):
    for L in range(3, 8):
        cl.append([-w(i, j, k, L), -t(j, k, l), w(i, k, l, L + 1)])
for key in list(var):
    if key[0] == "w" and key[4] == 8:
        cl.append([-var[key]])
for i, k, l in combinations(range(1, n + 1), 3):
    for x in range(i + 1, l):
        if x != k:
            cl.append([-w(i, k, l, 7), t(i, x, l)])
if len(sys.argv) > 3:
    for line in open(sys.argv[3]):
        if line.strip():
            i, j, k, s = map(int, line.split())
            cl.append([t(i, j, k) if s > 0 else -t(i, j, k)])
with open(out, "w") as f:
    f.write(f"p cnf {len(var)} {len(cl)}\n")
    for c in cl:
        f.write(" ".join(map(str, c)) + " 0\n")
with open(out + ".vars", "w") as f:
    for key, idx in var.items():
        if key[0] == "t":
            f.write(f"{idx} {key[1]} {key[2]} {key[3]}\n")
print(f"n={n}: {len(var)} variables, {len(cl)} clauses -> {out}")
