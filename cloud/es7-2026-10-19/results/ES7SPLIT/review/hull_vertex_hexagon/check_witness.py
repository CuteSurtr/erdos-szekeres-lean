#!/usr/bin/env python3
"""Independent exact re-verification of the 27-point witness for Prop. 8(b) and of the N* >= 26 certificate.
Usage: python3 -I check_witness.py WITNESS_FILE
Checks:
  W1 general position; W2 gon(S) = 6 (DP) and no convex 7-subset (exhaustive, both convexity tests on hits);
  W3 the last point v is a hull vertex; W4 no 6-subset through v is in convex position (exhaustive);
  W5 max convex subset through v (exhaustive) and max v-cap of S\\{v} (exhaustive, direct definition);
  W6 phi(S\\{v}) has distinct x, general position, max cap 4 (DP + exhaustive), gon <= 6 (DP);
     i.e. an explicit set certifying N(7,5,7) >= 26 in the definition used by the claim.
  W7 Prop 8(b) construction on A0 = phi(S\\{v}) scaled to integers: add v' = (x0, -M); gon <= 6, v' hull vertex,
     no convex hexagon through v'.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import combinations
from fractions import Fraction as F
from math import lcm
import g

pts = [tuple(int(t) for t in line.split()) for line in open(sys.argv[1]) if line.strip()]
S = pts
v = S[-1]
T = S[:-1]
print("points:", len(S), "v =", v, "distinct:", len(set(S)) == len(S))
print("W1 general position:", g.general_position(S))
gd = g.gon(S)
print("W2 gon(S) by DP:", gd)
# exhaustive over 7-subsets
n7 = 0
hit7 = 0
for Y in combinations(S, 7):
    n7 += 1
    if g.convex_position(Y):
        hit7 += 1
print("W2 exhaustive 7-subsets checked:", n7, "in convex position:", hit7)
# sanity: some convex 6-subset exists
six = next((Y for Y in combinations(S, 6) if g.convex_position(Y)), None)
print("W2 a convex 6-subset exists:", six is not None, "(tri-test agrees:", six is not None and g.convex_position_tri(six), ")")
H = g.hull(S)
print("W3 hull size", len(H), "v is hull vertex:", v in H)
cnt6 = 0
cntv = 0
maxthru = 1
for k in range(2, 7):
    for Y in combinations(T, k - 1):
        Z = Y + (v,)
        if g.convex_position(Z):
            maxthru = max(maxthru, k)
for Y in combinations(T, 5):
    cntv += 1
    Z = Y + (v,)
    if g.convex_position(Z) or g.convex_position_tri(Z):
        cnt6 += 1
print("W4 6-subsets through v checked:", cntv, "convex (either test):", cnt6)
print("W5 max convex subset containing v (exhaustive up to 6):", maxthru)
# max v-cap, direct definition, and equivalence Y u {v} convex <=> Y v-cap for all small Y
maxvcap = 0
mismatch = 0
checked = 0
for k in range(1, 6):
    for Y in combinations(T, k):
        c = g.is_v_cap(Y, v)
        if c:
            maxvcap = max(maxvcap, k)
        if k >= 2:
            checked += 1
            if c != g.convex_position(Y + (v,)):
                mismatch += 1
print("W5 max v-cap in S\\{v}:", maxvcap, "| equivalence (Y u {v} convex <=> Y v-cap) mismatches:", mismatch, "of", checked)

n = g.separating_normal(T, v)
print("W6 separating normal n =", n)
Q = g.phi_map(T, v, n)
A0 = list(Q.values())
xs = [q[0] for q in A0]
print("W6 phi(T): distinct x:", len(set(xs)) == len(xs), "general position:", g.general_position(A0))
# orientation preservation and order correspondence
bad_or = sum(1 for a, b, c in combinations(T, 3) if g.sgn(g.orient(a, b, c)) != g.sgn(g.orient(Q[a], Q[b], Q[c])))
bad_ord = sum(1 for a, b in combinations(T, 2) if (g.orient(v, a, b) < 0) != (Q[a][0] < Q[b][0]))
print("W6 orientation sign mismatches:", bad_or, "| v-order vs x-order mismatches:", bad_ord)
mc = g.max_cap_xsorted(A0)
ex5 = sum(1 for Y in combinations(A0, 5) if g.is_cap_xsorted(Y))
ex4 = sum(1 for Y in combinations(A0, 4) if g.is_cap_xsorted(Y))
print("W6 max cap of phi(T) (DP):", mc, "| exhaustive: #5-caps =", ex5, " #4-caps =", ex4)
# v-cap <-> cap correspondence for all 4- and 5-subsets
bad_capcorr = 0
for k in (3, 4, 5):
    for Y in combinations(T, k):
        if g.is_v_cap(Y, v) != g.is_cap_xsorted([Q[y] for y in Y]):
            bad_capcorr += 1
print("W6 v-cap <-> cap mismatches (k=3,4,5):", bad_capcorr)
print("W6 gon(phi(T)) by DP:", g.gon(A0), "| gon(T) by DP:", g.gon(T))

# W7: Prop 8(b) construction on integer-scaled A0
L = lcm(*[q[0].denominator for q in A0], *[q[1].denominator for q in A0])
A = [(int(q[0] * L), int(q[1] * L)) for q in A0]
assert g.general_position(A) and len(set(a[0] for a in A)) == len(A)
xmin = min(a[0] for a in A); xmax = max(a[0] for a in A)
# choose x0 not equal to any x, and M so large that v' is below every line through two points of A
x0 = xmin - 1 if (xmin - 1) not in [a[0] for a in A] else xmin - 2
x0 = (xmin + xmax) // 2
while x0 in [a[0] for a in A]:
    x0 += 1
lowest_line = None
for a, b in combinations(A, 2):
    yv = F(a[1]) + F(b[1] - a[1], b[0] - a[0]) * (x0 - a[0])
    lowest_line = yv if lowest_line is None or yv < lowest_line else lowest_line
M = -int(lowest_line) + 10**6
vp = (x0, -M)
Sb = A + [vp]
below_all = all(g.orient(a, b, vp) * (1 if a[0] < b[0] else -1) < 0 for a, b in combinations(A, 2))
print("W7 v' =", vp, "below every line of A0:", below_all, "general position:", g.general_position(Sb))
print("W7 gon(A0 u {v'}) by DP:", g.gon(Sb), "| v' hull vertex:", vp in g.hull(Sb))
c6 = sum(1 for Y in combinations(A, 5) if g.convex_position(Y + (vp,)))
print("W7 convex hexagons through v':", c6, "| |A0 u {v'}| =", len(Sb))
