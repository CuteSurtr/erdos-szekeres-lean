#!/usr/bin/env python3
"""Scratch: signotope CNF for N x-sorted points with no A-cap, no U-cup, no convex K-gon
(Erdos-Tuza-Valtr instance N(A,U,K)), optional mirror identification and x-reflection lex-leader.
Derived from experiments/es7-search-2026-10-13/encoding/gen_cnf.py (same variable convention:
X(i,j,k) true <=> ccw <=> cup triple)."""
import itertools, json, sys, argparse
ap = argparse.ArgumentParser()
ap.add_argument("N", type=int); ap.add_argument("A", type=int); ap.add_argument("U", type=int); ap.add_argument("K", type=int)
ap.add_argument("--xsb", action="store_true", help="x-reflection lex-leader clause")
ap.add_argument("--hull", action="store_true", help="point 1 at vertical infinity: X(1,i,j)=true")
ap.add_argument("--mirror", action="store_true", help="impose X(i,j,k)=X(m-k,m-j,m-i) on points (2..N if --hull else 1..N)")
ap.add_argument("-o", required=True)
a = ap.parse_args(); N, A, U, K = a.N, a.A, a.U, a.K
X = {}; nv = 0
for t in itertools.combinations(range(1, N+1), 3):
    nv += 1; X[t] = nv
nX = nv
def new():
    global nv; nv += 1; return nv
cl = []
for i, j, k, l in itertools.combinations(range(1, N+1), 4):
    s = [X[(i,j,k)], X[(i,j,l)], X[(i,k,l)], X[(j,k,l)]]
    for p, q, r in itertools.combinations(range(4), 3):
        cl.append([-s[p], s[q], -s[r]]); cl.append([s[p], -s[q], s[r]])
ends = {}
for kind, sgn, B in (("cap", -1, A), ("cup", +1, U)):
    R = range(3, B)  # tracked lengths 3..B-1, B forbidden
    V = {}; E = {}
    for x, aa, b in itertools.combinations(range(1, N+1), 3):
        for r in R:
            if aa - x >= r - 2: V[(x, aa, b, r)] = new()
    for x, b in itertools.combinations(range(1, N+1), 2):
        for r in R:
            if b - x >= r - 1: E[(x, b, r)] = new()
    for x, aa, b in itertools.combinations(range(1, N+1), 3):
        lit = sgn * X[(x, aa, b)]
        if 3 < B: cl.append([-lit, V[(x, aa, b, 3)]])
        else: cl.append([-lit])
    for x, w, aa, b in itertools.combinations(range(1, N+1), 4):
        lit = sgn * X[(w, aa, b)]
        for r in range(4, B+1):
            key = (x, w, aa, r-1)
            if key not in V: continue
            if r <= B-1: cl.append([-V[key], -lit, V[(x, aa, b, r)]])
            else: cl.append([-V[key], -lit])
    for (x, aa, b, r), v in V.items():
        cl.append([-v, E[(x, b, r)]])
        if r >= 4: cl.append([-v, V[(x, aa, b, r-1)]])
    for (x, b, r), v in E.items():
        if r >= 4: cl.append([-v, E[(x, b, r-1)]])
    ends[kind] = E
for x, b in itertools.combinations(range(1, N+1), 2):
    for r in range(3, A):
        s = K + 2 - r
        if 3 <= s <= U-1 and (x, b, r) in ends["cap"] and (x, b, s) in ends["cup"]:
            cl.append([-ends["cap"][(x, b, r)], -ends["cup"][(x, b, s)]])
if a.hull:
    for i, j in itertools.combinations(range(2, N+1), 2): cl.append([X[(1, i, j)]])
if a.mirror:
    lo = 2 if a.hull else 1; m = N + lo
    for (i, j, k), v in X.items():
        if i < lo: continue
        w = X[tuple(sorted((m-k, m-j, m-i)))]
        if w > v: cl.append([-v, w]); cl.append([v, -w])
if a.xsb:
    cl.append([-X[(1, 2, 3)], X[(N-2, N-1, N)]])
with open(a.o, "w") as f:
    f.write(f"p cnf {nv} {len(cl)}\n")
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
print(json.dumps({"N": N, "A": A, "U": U, "K": K, "vars": nv, "X": nX, "clauses": len(cl), "mirror": a.mirror, "hull": a.hull}))
