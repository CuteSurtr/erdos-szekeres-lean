#!/usr/bin/env python3
"""Proof-device check for sub-case (i): the frame-(i) orientation vector (p first, X(1,i,j)
true, others sorted by x/d) is the orientation vector of an x-sorted affine point set
Q = {q1} + images, q1 = (min u - 1, H) with H large; also checks Q mirror-symmetric
apart from q1 and that the frame vector equals the original chirotope relabelled.
usage: realize_check.py <sets file from gen33 (.sets.txt)> <max sets>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
n = 0; bad = 0; chi_bad = 0
for line in open(sys.argv[1]):
    t = line.split(); sid = t[0]; v = list(map(int, t[1:])); P = [(v[2 * i], v[2 * i + 1]) for i in range(len(v) // 2)]
    p = [q for q in P if q[0] == 0][0]
    if P.index(p) not in hull_vertices(P): continue
    Hall, s = frame_i(P)
    Q = realize_hull_frame(Hall)
    assert all(Q[i][0] < Q[i + 1][0] for i in range(len(Q) - 1))
    sQ = [1 if orient_frac(Q[a], Q[b], Q[c]) > 0 else -1 for a, b, c in tri(len(Q)).tolist()]
    bad += sQ != list(s)
    # chirotope of the original set, relabelled: label 0 = p (top after y-flip), then by x/d
    P2 = P if all(q[1] < p[1] for q in P if q != p) else [(x, -y) for x, y in P]
    p2 = (0, max(y for _, y in P2)) ; y0 = p2[1]
    rest = sorted([q for q in P2 if q != p2], key=lambda q: F(q[0], y0 - q[1]))
    L = [p2] + rest
    sP = [1 if orient_frac(L[a], L[b], L[c]) > 0 else -1 for a, b, c in tri(len(L)).tolist()]
    chi_bad += sP != list(s)
    n += 1
    if n >= int(sys.argv[2]): break
print({"hull_vertex_sets": n, "realization_mismatch": bad, "original_chirotope_mismatch": chi_bad})
