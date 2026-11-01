#!/usr/bin/env python3
"""Randomised exact tests of every step used in Prop. 8 (independent code, exact integers/Fractions).
For random sets S in general position (sizes 6..11, several coordinate scales, including near-degenerate
clustered sets), for EVERY hull vertex v and T = S \\ {v}:
  E1  gon DP == exhaustive gon                                         (validates my DP)
  E2  for every Y in T, |Y|>=2: Y u {v} convex  <=>  Y is a v-cap (direct definition)
  E3  max |convex P containing v| == 1 + max v-cap(T)                  (exhaustive)
  E4  phi(T): distinct x, orientation signs preserved, v-order == x-order, v-caps == caps, gon preserved
  E5  (b)-construction: random A with distinct x (no further condition), v' far below:
      max convex through v' == 1 + cap(A), gon(A u {v'}) == max(gon(A), cap(A)+1)  (exhaustive)
  E6  k=5 analogue of Prop 8 with exact constant N(5,3,5)=4: for random pentagon-free S, every hull vertex v,
      every T subset of S\\{v} with |T| >= 5 gives a convex quadrilateral through v; and a 5-point pentagon-free
      set with a hull vertex on no convex quadrilateral exists (4-cup + far point).
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import combinations
from fractions import Fraction as F
import g

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2026)
NSETS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
stats = dict(sets=0, hullverts=0, E1=0, E2=0, E3=0, E4=0, E5=0, E5sets=0, E2checked=0)


def exh_gon(P):
    for k in range(len(P), 2, -1):
        if any(g.convex_position(Y) for Y in combinations(P, k)):
            return k
    return min(len(P), 2)


def rand_set(n):
    mode = rng.randrange(4)
    while True:
        if mode == 0:
            P = [(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)]
        elif mode == 1:
            P = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(n)]
        elif mode == 2:  # points near a parabola (many large convex subsets)
            P = []
            for _ in range(n):
                x = rng.randint(-40, 40)
                P.append((x, x * x + rng.randint(-25, 25)))
        else:  # two clusters (split-like configurations)
            P = [(rng.randint(-20, 20), rng.randint(-20, 20) + (1000 if rng.random() < 0.5 else 0)) for _ in range(n)]
        if len(set(P)) == n and g.general_position(P):
            return P


for it in range(NSETS):
    n = rng.randint(6, 11)
    S = rand_set(n)
    stats['sets'] += 1
    gdp = g.gon(S)
    if gdp != exh_gon(S):
        stats['E1'] += 1
    H = g.hull(S)
    for v in H:
        stats['hullverts'] += 1
        T = [p for p in S if p != v]
        maxthru = 1
        maxvcap = 1
        for k in range(1, len(T) + 1):
            for Y in combinations(T, k):
                vc = g.is_v_cap(Y, v)
                cv = g.convex_position(Y + (v,))
                if k >= 2:
                    stats['E2checked'] += 1
                    if vc != cv:
                        stats['E2'] += 1
                if vc:
                    maxvcap = max(maxvcap, k)
                if cv:
                    maxthru = max(maxthru, k + 1)
        if maxthru != 1 + maxvcap:
            stats['E3'] += 1
        nrm = g.separating_normal(T, v, seed=it)
        assert nrm is not None
        Q = g.phi_map(T, v, nrm)
        A0 = [Q[p] for p in T]
        bad = False
        if len(set(q[0] for q in A0)) != len(A0):
            bad = True
        for a, b, c in combinations(T, 3):
            if g.sgn(g.orient(a, b, c)) != g.sgn(g.orient(Q[a], Q[b], Q[c])):
                bad = True
        for a, b in combinations(T, 2):
            if (g.orient(v, a, b) < 0) != (Q[a][0] < Q[b][0]):
                bad = True
        for k in range(3, min(len(T), 7) + 1):
            for Y in combinations(T, k):
                if g.is_v_cap(Y, v) != g.is_cap_xsorted([Q[y] for y in Y]):
                    bad = True
                if g.is_v_cup(Y, v) != g.is_cup_xsorted([Q[y] for y in Y]):
                    bad = True
        if g.max_cap_xsorted(A0) != maxvcap:
            bad = True
        if g.gon(A0) != g.gon(T):
            bad = True
        if bad:
            stats['E4'] += 1

# E5: (b) construction with arbitrary A (distinct x), v' far below
for it in range(NSETS):
    n = rng.randint(5, 10)
    while True:
        A = [(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(n)]
        if len(set(a[0] for a in A)) == n and g.general_position(A):
            break
    x0 = rng.randint(-60, 60)
    while x0 in [a[0] for a in A]:
        x0 += 1
    low = min(F(a[1]) + F(b[1] - a[1], b[0] - a[0]) * (x0 - a[0]) for a, b in combinations(A, 2))
    vp = (x0, int(low) - rng.randint(1, 10**4) - 1)
    S = A + [vp]
    if not g.general_position(S):
        continue
    stats['E5sets'] += 1
    capA = g.max_cap_xsorted(A)
    maxthru = 1
    for k in range(1, n + 1):
        for Y in combinations(A, k):
            if g.convex_position(Y + (vp,)):
                maxthru = max(maxthru, k + 1)
    if maxthru != capA + 1 or exh_gon(S) != max(exh_gon(A), capA + 1) or vp not in g.hull(S):
        stats['E5'] += 1

# E6: k = 5 analogue (exact constant N(5,3,5) = 4)
e6_sets = e6_fail = e6_checks = 0
tries = 0
while e6_sets < NSETS and tries < 200000:
    tries += 1
    n = rng.randint(6, 8)
    P = [(rng.randint(-40, 40), rng.randint(-40, 40)) for _ in range(n)]
    if len(set(P)) != n or not g.general_position(P):
        continue
    if g.gon(P) >= 5:
        continue
    e6_sets += 1
    for v in g.hull(P):
        R = [p for p in P if p != v]
        for m in range(5, len(R) + 1):
            for Tt in combinations(R, m):
                e6_checks += 1
                if not any(g.convex_position(Y + (v,)) for Y in combinations(Tt, 3)):
                    e6_fail += 1
cup4 = [(0, 0), (1, -3), (3, -4), (6, -2)]   # x-sorted, slopes increasing: a 4-cup
vfar = (2, -10**6)
S5 = cup4 + [vfar]
e6b = (g.general_position(S5), g.gon(S5), vfar in g.hull(S5),
       sum(1 for Y in combinations(cup4, 3) if g.convex_position(Y + (vfar,))))
print("stats:", stats)
print("E6: pentagon-free sets", e6_sets, "subset checks", e6_checks, "failures", e6_fail,
      "| 5-point example (gp, gon, v hull vertex, #convex quads through v):", e6b)
