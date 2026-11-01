#!/usr/bin/env python3
"""CNF for the Erdos-Tuza-Valtr instance ETV(n, a, b; N):
   N points (signotope model, sorted by x), no a-cap, no b-cup, no n points in convex position.

Adapted from the repository encoder experiments/es7-search-2026-10-13/encoding/gen_cnf.py (read-only),
with separate cap and cup bounds and WITHOUT the hull/angular normal form (that normal form changes the
x-order and is not valid for statements about caps and cups).

Variables
  X(i,j,k), i<j<k, numbered 1..C(N,3) in lexicographic order.
    X true  <=> orientation(p_i,p_j,p_k) > 0  (p_j below line p_i p_k: a cup triple)
    X false <=> orientation < 0                (p_j above line p_i p_k: a cap triple)
  Cap(x,w,y,r), 3 <= r <= a-1 : lower-bound flag "there is an r-cap starting at x whose last edge is (w,y)"
  Cup(x,w,y,r), 3 <= r <= b-1 : same for cups
  CapE(x,y,r), CupE(x,y,r)    : "there is an r-cap / r-cup from x to y"

Clauses (all implications point from 'a chain exists' to 'the flag is true', so every configuration
without the forbidden patterns satisfies the formula with the flags set to their true values; a model
of the formula is a signotope without the forbidden patterns, because every existing chain forces its
flag and the flags of forbidden combinations are mutually exclusive)
  * signotope axioms: for i<j<k<l the sign sequence (ijk, ijl, ikl, jkl) changes at most once
    (8 clauses per quadruple)
  * Cap(x,w,y,3) <- -X(x,w,y);  Cap(x,v,w,r-1) & -X(v,w,y) -> Cap(x,w,y,r);  forbid r = a
  * Cup analogously with +X; forbid r = b
  * Cap(x,w,y,r) -> CapE(x,y,r);  Cup(x,w,y,r) -> CupE(x,y,r)
  * n points in convex position = an r-cap and an s-cup from x to y with r + s = n + 2 (r, s >= 2;
    r = 2 or s = 2 is an n-cup/n-cap, excluded by the length bounds when a, b <= n):
    -CapE(x,y,r) | -CupE(x,y,s) for 3 <= r <= a-1, 3 <= s <= b-1, r + s = n + 2
  Chains are consecutive-triple chains; in a signotope (and in a real point set) a sequence whose
  consecutive triples are all cap triples has all its triples cap triples (monotonicity axiom), so
  these are exactly the caps/cups, and a k-subset is in convex position iff it is the union of a cap
  and a cup with common endpoints (Szekeres-Peters 2006).

Optional symmetry breaking
  --xrefl : the reflection x -> -x maps the instance to itself (caps stay caps, cups stay cups) and
            maps X(i,j,k) to X(N+1-k, N+1-j, N+1-i); clause  -X(1,2,3) | X(N-2,N-1,N)  keeps at least
            one of every mirror pair of models.
  --yrefl : only when a == b: y -> -y swaps caps and cups and complements every X; fix X(1,2,3) = true.
"""
import argparse
import itertools
import json


def build(N, n, a, b, xrefl=False, yrefl=False):
    assert a <= n and b <= n and a >= 3 and b >= 3
    nv = 0
    X = {}
    for t in itertools.combinations(range(1, N + 1), 3):
        nv += 1
        X[t] = nv
    nX = nv

    def new():
        nonlocal nv
        nv += 1
        return nv

    clauses = []
    for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
        s = [X[(i, j, k)], X[(i, j, l)], X[(i, k, l)], X[(j, k, l)]]
        for p, q, r in itertools.combinations(range(4), 3):
            clauses.append([-s[p], s[q], -s[r]])
            clauses.append([s[p], -s[q], s[r]])

    E = {}
    for kind, sgn, bound in (("cap", -1, a), ("cup", +1, b)):
        R = range(3, bound)  # tracked lengths 3..bound-1
        V = {}
        for x, w, y in itertools.combinations(range(1, N + 1), 3):
            for r in R:
                if w - x >= r - 2:
                    V[(x, w, y, r)] = new()
        EE = {}
        for x, y in itertools.combinations(range(1, N + 1), 2):
            for r in R:
                if y - x >= r - 1:
                    EE[(x, y, r)] = new()
        for x, w, y in itertools.combinations(range(1, N + 1), 3):
            lit = sgn * X[(x, w, y)]
            if bound == 3:
                clauses.append([-lit])  # a 3-chain is forbidden
            else:
                clauses.append([-lit, V[(x, w, y, 3)]])
        for x, v, w, y in itertools.combinations(range(1, N + 1), 4):
            lit = sgn * X[(v, w, y)]
            for r in range(4, bound + 1):
                key = (x, v, w, r - 1)
                if key not in V:
                    continue
                if r <= bound - 1:
                    clauses.append([-V[key], -lit, V[(x, w, y, r)]])
                else:
                    clauses.append([-V[key], -lit])
        for (x, w, y, r), v in V.items():
            clauses.append([-v, EE[(x, y, r)]])
        E[kind] = EE

    for x, y in itertools.combinations(range(1, N + 1), 2):
        for r in range(3, a):
            s = n + 2 - r
            if 3 <= s <= b - 1 and (x, y, r) in E["cap"] and (x, y, s) in E["cup"]:
                clauses.append([-E["cap"][(x, y, r)], -E["cup"][(x, y, s)]])

    if xrefl and N >= 6:
        clauses.append([-X[(1, 2, 3)], X[(N - 2, N - 1, N)]])
    if yrefl:
        assert a == b
        clauses.append([X[(1, 2, 3)]])
    return nv, nX, clauses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("n", type=int, help="forbid n points in convex position")
    ap.add_argument("a", type=int, help="forbid a-caps")
    ap.add_argument("b", type=int, help="forbid b-cups")
    ap.add_argument("--xrefl", action="store_true")
    ap.add_argument("--yrefl", action="store_true")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    nv, nX, clauses = build(args.N, args.n, args.a, args.b, args.xrefl, args.yrefl)
    with open(args.out, "w") as f:
        f.write(f"c ETV signotope CNF N={args.N} n={args.n} a(cap)={args.a} b(cup)={args.b} "
                f"xrefl={args.xrefl} yrefl={args.yrefl}\n")
        f.write(f"c X(i,j,k) for i<j<k are variables 1..{nX} in lexicographic order\n")
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(json.dumps(dict(N=args.N, n=args.n, a=args.a, b=args.b, vars=nv, clauses=len(clauses), X_vars=nX,
                          out=args.out)))


if __name__ == "__main__":
    main()
