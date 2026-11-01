#!/usr/bin/env python3
"""Goal (2) experiments on a centrally symmetric integer point file S (exact arithmetic throughout).

A. Halving analysis. For every one of the m combinatorially distinct halves H (m consecutive points in the cyclic
   angular order around 0; H and -H are equivalent), with H read in counterclockwise angular order:
   - longest OUTWARD chain (every consecutive triple turns left = middle point beyond the chord, seen from 0),
   - longest INWARD chain (every consecutive triple turns right),
   - number of outward 4-chains, and how many of them CLOSE (p1..p4,-p1..-p4 convex <=> the two closing turns
     orient(p3,p4,-p1) > 0 and orient(-p4,p1,p2) > 0 also hold),
   - largest j such that some outward j-chain closes (= half the size of the largest centrally symmetric convex
     polygon of S).
B. Projective transfer. Shear (x,y) -> (x, y - lam*x) (determinant 1), then psi(x,y') = (x/y', 1/y'). psi sends the
   line y' = 0 through 0 to infinity and turns p -> -p into the reflection (u,w) -> (u,-w). Checks exactly:
   T = psi(S) is mirror symmetric; chi_T(a,b,c) = -chi_S(a,b,c) * sgn(y'_a y'_b y'_c) for every triple; writes T's
   orientation table (points in increasing (w,u) order) and sides (sign of w) for enum_table.c.
usage: projective_check.py FILE OUTPREFIX"""
import sys, struct
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(v):
    return (v > 0) - (v < 0)


path, outp = sys.argv[1], sys.argv[2]
S = [tuple(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith("#")]
n = len(S); m = n // 2
idx = {p: i for i, p in enumerate(S)}
neg = [idx[(-x, -y)] for x, y in S]

# ---------- A. halving analysis ----------
def half_key(p):        # angle order: upper half-plane first (y>0 or y==0,x>0), then cross-product comparison
    return 0 if (p[1] > 0 or (p[1] == 0 and p[0] > 0)) else 1
O0 = (0, 0)
ang = sorted(range(n), key=cmp_to_key(lambda i, j: (half_key(S[i]) - half_key(S[j])) or (-1 if orient(O0, S[i], S[j]) > 0 else 1)))
for t in range(n):      # sanity: consecutive points of the cyclic order are within angle < pi and in ccw order
    a, b = S[ang[t]], S[ang[(t + 1) % n]]
    assert orient(O0, a, b) > 0, "angular order"
assert all(ang[(t + m) % n] == neg[ang[t]] for t in range(n)), "antipodal structure"

def chains(H, sign):
    """longest chain with all consecutive triples of orientation `sign`, H in ccw order."""
    L = len(H); best = min(L, 2)
    D = [[2] * L for _ in range(L)]
    for j in range(L):
        for i in range(j):
            v = 2
            for h in range(i):
                if D[h][i] + 1 > v and sgn(orient(S[H[h]], S[H[i]], S[H[j]])) == sign:
                    v = D[h][i] + 1
            D[i][j] = v; best = max(best, v)
    return best

def closes(ch):
    p = [S[i] for i in ch]; q = [S[neg[i]] for i in ch]
    return orient(p[-2], p[-1], q[0]) > 0 and orient(q[-1], p[0], p[1]) > 0

summary = []
example_open4 = None
for start in range(m):
    H = [ang[(start + t) % n] for t in range(m)]
    out_len = chains(H, 1); in_len = chains(H, -1)
    n4 = c4 = 0; best_close = 1
    # DFS over outward chains, recording the longest closing one and the 4-chain statistics
    stack = [[i] for i in range(m)]
    while stack:
        ch = stack.pop()
        if len(ch) >= 2:
            pts = [H[i] for i in ch]
            if len(ch) >= 3 or True:
                if len(ch) >= 2 and closes(pts) and len(ch) > best_close:
                    best_close = len(ch)
            if len(ch) == 4:
                n4 += 1
                if closes(pts):
                    c4 += 1
                elif example_open4 is None:
                    example_open4 = (start, pts)
        last = ch[-1]
        for j in range(last + 1, m):
            if len(ch) >= 2 and orient(S[H[ch[-2]]], S[H[ch[-1]]], S[H[j]]) <= 0:
                continue
            if len(ch) < 7:
                stack.append(ch + [j])
    summary.append((start, out_len, in_len, n4, c4, best_close))
print("A. halves (start, longest outward, longest inward, #outward 4-chains, #closing, largest closing j):")
for row in summary:
    print("  ", row)
print("  min/max longest outward:", min(r[1] for r in summary), max(r[1] for r in summary),
      " min/max longest inward:", min(r[2] for r in summary), max(r[2] for r in summary))
print("  outward 4-chains that close (would give a symmetric octagon): total", sum(r[4] for r in summary))
print("  largest centrally symmetric convex polygon: 2 *", max(r[5] for r in summary))
if example_open4:
    st, pts = example_open4
    p = [S[i] for i in pts]; q = [S[neg[i]] for i in pts]
    print("  example outward 4-chain (half start %d):" % st, p)
    print("    inner turns:", [sgn(orient(p[i], p[i + 1], p[i + 2])) for i in range(2)],
          " closing turns orient(p3,p4,-p1), orient(-p4,p1,p2):", sgn(orient(p[2], p[3], q[0])), sgn(orient(q[3], p[0], p[1])))

# ---------- B. projective transfer ----------
lam = Fraction(1, 7919)
yp = [Fraction(y) - lam * x for x, y in S]
assert all(v != 0 for v in yp), "choose another lam"
T = [(Fraction(x) / v, 1 / v) for (x, _), v in zip(S, yp)]
Tset = set(T)
print("B. T mirror-symmetric under (u,w)->(u,-w):", all((u, -w) in Tset for u, w in T),
      "  points with w>0:", sum(1 for v in yp if v > 0))
bad = 0
order = sorted(range(n), key=lambda i: (T[i][1], T[i][0]))
pos = {i: r for r, i in enumerate(order)}
tab = bytearray(n * n * n)
for a in range(n):
    for b in range(n):
        if b == a: continue
        for c in range(n):
            if c == a or c == b: continue
            st = sgn(orient(T[a], T[b], T[c]))
            ss = sgn(orient(S[a], S[b], S[c]))
            if st != -ss * sgn(yp[a] * yp[b] * yp[c]):
                bad += 1
            tab[(pos[a] * n + pos[b]) * n + pos[c]] = st & 0xFF
print("   triples violating chi_T = -chi_S * sgn(y'y'y'):", bad)
with open(outp + "_T.bin", "wb") as f:
    f.write(struct.pack("<i", n)); f.write(tab)
with open(outp + "_T_sides.txt", "w") as f:
    f.write(" ".join(str(sgn(T[i][1])) for i in order) + "\n")
print("   wrote", outp + "_T.bin", outp + "_T_sides.txt")
