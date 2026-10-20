#!/usr/bin/env python3
"""Deep-below construction (plan/es7_plan.md, Proposition): for an exact point set S with no
geometric 5-cap (x-direction), put a 6-point cap A deep below S: every A-point is below every
line through two S-points and every S-point is above every line through two A-points.  Then a
convex subset meeting both parts is a cup in A (at most 2 points, A is a cap) plus a cap in S (at
most 4 points), so A u S has no convex 7-gon iff S has none.  If S has no 5-cup instead, S is
reflected in y (caps <-> cups) first.  Everything is exact (Python ints / Fractions), and the
32-point result is re-verified directly: distinct x, general position, exact largest convex subset
(chiro.largest_convex_subset).  Coordinates are then compressed below 2^27 for sat.c by
re-realizing the exact chirotope (results/F realizer) and re-checking it exactly.
usage: build32.py IN.jsonl OUT.jsonl   (IN lines: {"id":..., "points": [[x,y],...]})"""
import sys, os, json, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../F/realizer"))
import chiro
def orient(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
def longest_chain(P, sgn):
    """longest cap (sgn=-1) / cup (sgn=+1) of P (sorted by distinct x), exact DP"""
    n = len(P); best = {}; mx = min(n, 2)
    for b in range(n):
        for a in range(b):
            v = 2
            for z in range(a):
                if (orient(P[z], P[a], P[b]) > 0) == (sgn > 0) and best[(z, a)] + 1 > v: v = best[(z, a)] + 1
            best[(a, b)] = v; mx = max(mx, v)
    return mx
def deep_below(S, m=6):
    xs = [p[0] for p in S]; x0 = min(xs); W = max(xs) - x0 + 1
    ys = [p[1] for p in S]; ylo = min(ys)
    D = 1
    while True:
        # A: m-point cap centred under S: (x0 + W/2 + i, Y - (i - c)^2), very flat relative to D
        A = [(x0 + W // 2 + i, ylo - D - (2 * i - (m - 1)) ** 2) for i in range(m)]
        ok = True
        for b1, b2 in itertools.combinations(S, 2):
            l, r = (b1, b2) if b1[0] < b2[0] else (b2, b1)
            # A strictly below line(l, r): orient(l, r, a) < 0
            if any(orient(l, r, a) >= 0 for a in A): ok = False; break
        if ok:
            for a1, a2 in itertools.combinations(A, 2):
                if any(orient(a1, a2, b) <= 0 for b in S): ok = False; break
        if ok: return A, D
        D *= 4
def main():
    out = open(sys.argv[2], "a")
    for line in open(sys.argv[1]):
        rec = json.loads(line); S = [tuple(map(int, p)) for p in rec["points"]]
        res = {"id": rec["id"], "n_S": len(S)}
        if len({p[0] for p in S}) < len(S):
            L = 2 * max(abs(p[1]) for p in S) + 1; S = [(L * x + y, y) for x, y in S]; res["sheared"] = True
        S.sort()
        cap, cup = longest_chain(S, -1), longest_chain(S, +1)
        res.update(S_longest_cap=cap, S_longest_cup=cup, S_largest_convex=chiro.largest_convex_subset(S))
        if cap <= 4: res["construction"] = "6-cap deep below S"; T = S
        elif cup <= 4: res["construction"] = "6-cup deep above S (y-reflection)"; T = [(x, -y) for x, y in S]
        else:
            res["construction"] = None; out.write(json.dumps(res) + "\n"); continue
        A, D = deep_below(T)
        P = A + T
        if res["construction"].startswith("6-cup"): P = [(x, -y) for x, y in P]
        P.sort()
        gp = all(orient(P[i], P[j], P[k]) != 0 for i, j, k in itertools.combinations(range(len(P)), 3))
        res.update(n=len(P), distinct_x=len({p[0] for p in P}) == len(P), general_position=gp,
                   largest_convex=chiro.largest_convex_subset(P), D=D, points_exact=[list(p) for p in P])
        # compressed realization of the same chirotope for sat.c
        chi = chiro.chirotope_of(P)
        mx = max(max(abs(x), abs(y)) for x, y in P)
        if mx < 2 ** 26: Q = P
        else:
            import realize as R
            Q = None
            for seed in range(1, 6):
                r = R.realize(chi, len(P), budget=60, seed=seed)
                if r["realized"]: Q = [tuple(p) for p in r["points"]]; break
        if Q is not None:
            ok, bad, zero = chiro.verify_exact(Q, chi)
            res.update(compressed_ok=bool(ok), compressed_max=max(max(abs(x), abs(y)) for x, y in Q), points=[list(p) for p in Q])
        out.write(json.dumps(res) + "\n"); out.flush()
        print(json.dumps({k: v for k, v in res.items() if "points" not in k}), flush=True)
main()
