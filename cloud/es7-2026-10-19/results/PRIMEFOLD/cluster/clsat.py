#!/usr/bin/env python3
"""SAT relaxation of Proposition C (single orbit, NO centre, i.e. even m) for a cluster of n points.

Real configuration -> model.  Work in the radial frame of the cluster's base vertex (x-axis = inward radial
direction).  By Prop. C (F(1,1) = 1) no edge direction is within pi/m of the tangent, so all slopes are finite:
sort the n points by x.  For i < j let t_ij in (1, m-1) be the direction of the segment p_i p_j measured from the
ccw tangent direction (which points straight down in this frame) in units of pi/m; t is an increasing function of the slope.  Generic: t_ij is never an
integer.  Bin b_ij = floor(t_ij) in {1, ..., m-2}.  Facts used (all true for real points sorted by x):
  (a) left turn at j for i<j<k  iff  t_ij < t_jk;  so b_ij < b_jk forces a left turn, b_ij > b_jk a right turn;
  (b) t_ik lies strictly between t_ij and t_jk, so b_ik lies between b_ij and b_jk;
  (c) for i<j<k<l the turn signs of (ijk, ijl, ikl, jkl) change sign at most once (signotope axiom);
  (d) a cup = left turns at consecutive triples; its directions increase, so "all t < x" iff last edge bin <= x-1;
      a cap = right turns; its directions decrease, so "all t > m-x" iff last edge bin >= m-x;
  (e) Prop. C (i): g(x) + h(x) <= x+1 for x = 1..m-1, where g(x) = longest cup with all t < x and h(x) = longest
      cap with all t > m-x (these are exactly the ccw chains with directions in (0,x) resp. (-x,0) of Prop. C).
UNSAT  =>  no cluster of n points satisfies Prop. C (i)  =>  no single-orbit construction with |C| = n.
usage: clsat.py m n out.cnf
"""
import sys
from itertools import combinations
m, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
B = m - 2                      # bins 1..B
nv = 0
def new():
    global nv; nv += 1; return nv
L = {}                         # L[i,j,v]  <=>  b_ij <= v   (v = 1..B-1)
for i, j in combinations(range(n), 2):
    for v in range(1, B):
        L[i, j, v] = new()
T = {}                         # T[i,j,k] <=> left turn
for t in combinations(range(n), 3):
    T[t] = new()
maxlen = n
G = {}; H = {}                 # G[x,a] <=> g(x) >= a ; H[x,a] <=> h(x) >= a   (a = 2..x+1, capped)
for x in range(1, m):
    for a in range(2, n + 1):
        G[x, a] = new(); H[x, a] = new()
cl = []
def le(i, j, v):               # literal for b_ij <= v  (v = 0: false, v >= B: true)
    if v <= 0: return None     # constant false
    if v >= B: return True
    return L[i, j, v]
# order encoding
for i, j in combinations(range(n), 2):
    for v in range(1, B - 1):
        cl.append([-L[i, j, v], L[i, j, v + 1]])
def clause(lits):
    """lits: list of ints or True/None constants (True = satisfied, None = false literal dropped)."""
    out_ = []
    for l in lits:
        if l is True: return
        if l is None or l is False: continue
        out_.append(l)
    cl.append(out_)
def notle(i, j, v):            # literal for b_ij > v
    x = le(i, j, v)
    if x is None: return True
    if x is True: return None
    return -x
for i, j, k in combinations(range(n), 3):
    t = T[i, j, k]
    for v in range(1, B):
        # b_ij <= v and b_jk > v  ->  left turn
        clause([notle(i, j, v), le(j, k, v), t])
        # b_jk <= v and b_ij > v  ->  right turn
        clause([notle(j, k, v), le(i, j, v), -t])
    for v in range(1, B + 1):
        # b_ik >= min(b_ij, b_jk):  b_ij >= v and b_jk >= v -> b_ik >= v   i.e. not(b_ik <= v-1)
        clause([le(i, j, v - 1), le(j, k, v - 1), notle(i, k, v - 1)])
        # b_ik <= max:  b_ij <= v and b_jk <= v -> b_ik <= v
        clause([notle(i, j, v), notle(j, k, v), le(i, k, v)])
# signotope axiom: for i<j<k<l the sequence (ijk, ijl, ikl, jkl) has at most one sign change
for i, j, k, l in combinations(range(n), 4):
    s = [T[i, j, k], T[i, j, l], T[i, k, l], T[j, k, l]]
    for a, b, c in combinations(range(4), 3):
        # forbid s_a = s_c != s_b  (two sign changes)
        cl.append([-s[a], s[b], -s[c]])
        cl.append([s[a], -s[b], s[c]])
# chains: every a-cup with last edge bin <= x-1 forces G[x,a]; every a-cap with last edge bin >= m-x forces H[x,a]
for a in range(2, min(n, m) + 1):     # a cup/cap of length > m contains one of length m with the same window
    for sub in combinations(range(n), a):
        cupturns = [-T[sub[q], sub[q + 1], sub[q + 2]] for q in range(a - 2)]
        capturns = [T[sub[q], sub[q + 1], sub[q + 2]] for q in range(a - 2)]
        i, j = sub[-2], sub[-1]
        for x in range(1, m):
            clause(cupturns + [notle(i, j, x - 1), G[x, a]])
            clause(capturns + [le(i, j, m - x - 1), H[x, a]])
# profile: monotone in a; g(x) + h(x) <= x+1 (with g, h >= 1)
for x in range(1, m):
    for a in range(3, n + 1):
        cl.append([-G[x, a], G[x, a - 1]]); cl.append([-H[x, a], H[x, a - 1]])
    for a in range(2, n + 1):
        if a + 1 > x + 1: cl.append([-G[x, a]]); cl.append([-H[x, a]])
        for b in range(2, n + 1):
            if a + b > x + 1: cl.append([-G[x, a], -H[x, b]])
with open(out, 'w') as f:
    f.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl:
        f.write(' '.join(map(str, c)) + ' 0\n')
print('m=%d n=%d vars=%d clauses=%d' % (m, n, nv, len(cl)))
