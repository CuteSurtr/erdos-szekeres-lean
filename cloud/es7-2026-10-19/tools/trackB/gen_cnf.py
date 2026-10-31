#!/usr/bin/env python3
"""CNF for: N points (signotope model, x-sorted), no K points in convex position.

Variables
  X(i,j,k), i<j<k, numbered 1..C(N,3) in lexicographic order.
    X true  <=> orientation(p_i,p_j,p_k) > 0 (counter-clockwise; p_j below line p_i p_k: a "cup" triple)
    X false <=> orientation < 0 (clockwise; p_j above line p_i p_k: a "cap" triple)
  Cap(x,a,b,r) (3<=r<=K-1): lower-bound flag "there is an r-cap x=c1<...<c_{r-1}=a<c_r=b"
  Cup(x,a,b,r): same for cups
  CapE(x,b,r) / CupE(x,b,r): "there is an r-cap / r-cup from x to b"

Clauses
  * signotope axioms: for i<j<k<l the sequence (ijk, ijl, ikl, jkl) changes sign at most once
    (forbid patterns +-+ and -+- on every 3 of the 4 positions; 8 clauses per quadruple)
  * Cap(x,a,b,3) <- -X(x,a,b);  Cap(x,a,b,r) <- Cap(x,w,a,r-1) & -X(w,a,b)
  * forbid K-caps: Cap(x,w,a,K-1) & -X(w,a,b) -> false   (cups symmetric)
  * Cap(x,a,b,r) -> CapE(x,b,r); monotonicity Cap(..,r) -> Cap(..,r-1), CapE(..r)->CapE(..r-1)
  * convex K-gon = cap from x to b (r points) + cup from x to b (s points), r+s-2 = K:
    -CapE(x,b,r) | -CupE(x,b,s) for r,s>=3, r+s=K+2   (r=2 / s=2 are the K-cup / K-cap clauses)

Optional sound symmetry breaking
  --hull   : point 1 is extreme and points 2..N are sorted around it: X(1,i,j)=true for all 1<i<j.
             (Realizable sets: projective map (x,y)->(y/x,1/x) with an extreme point at the origin
             preserves the order type; re-insert p as (-M, M^2).)
  --mirror : (needs --hull) x-reflection of points 2..N keeps the normal form; lex-leader on the
             first triple: X(2,3,4) -> X(N-2,N-1,N).
  --flip   : (only without --hull) y-reflection complements every X; fix X(1,2,3)=true.
"""
import argparse
import itertools
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("K", type=int)
    ap.add_argument("--hull", action="store_true")
    ap.add_argument("--mirror", action="store_true")
    ap.add_argument("--flip", action="store_true")
    ap.add_argument("--no-mono", action="store_true", help="omit monotonicity clauses")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    N, K = args.N, args.K
    assert K >= 4 and N >= 3
    if args.mirror:
        assert args.hull
    if args.flip:
        assert not args.hull

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

    # signotope axioms
    for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
        s = [X[(i, j, k)], X[(i, j, l)], X[(i, k, l)], X[(j, k, l)]]
        for a, b, c in itertools.combinations(range(4), 3):
            clauses.append([-s[a], s[b], -s[c]])
            clauses.append([s[a], -s[b], s[c]])

    # caps (sign=-1 means the triple literal is -X) and cups (+X)
    R = range(3, K)  # tracked lengths 3..K-1
    for kind, sgn in (("cap", -1), ("cup", +1)):
        V = {}  # (x,a,b,r) -> var
        for x, a, b in itertools.combinations(range(1, N + 1), 3):
            for r in R:
                if a - x >= r - 2:
                    V[(x, a, b, r)] = new()
        E = {}
        for x, b in itertools.combinations(range(1, N + 1), 2):
            for r in R:
                if b - x >= r - 1:
                    E[(x, b, r)] = new()
        # base r=3: triple literal -> V
        for x, a, b in itertools.combinations(range(1, N + 1), 3):
            lit = sgn * X[(x, a, b)]
            clauses.append([-lit, V[(x, a, b, 3)]])
        # extension
        for x, w, a, b in itertools.combinations(range(1, N + 1), 4):
            lit = sgn * X[(w, a, b)]
            for r in range(4, K + 1):
                key = (x, w, a, r - 1)
                if key not in V:
                    continue
                if r <= K - 1:
                    clauses.append([-V[key], -lit, V[(x, a, b, r)]])
                else:  # r == K: forbidden K-cap / K-cup
                    clauses.append([-V[key], -lit])
        # end flags
        for (x, a, b, r), v in V.items():
            clauses.append([-v, E[(x, b, r)]])
        if not args.no_mono:
            for (x, a, b, r), v in V.items():
                if r >= 4:
                    clauses.append([-v, V[(x, a, b, r - 1)]])
            for (x, b, r), v in E.items():
                if r >= 4:
                    clauses.append([-v, E[(x, b, r - 1)]])
        if kind == "cap":
            CapE = E
        else:
            CupE = E

    # combine caps and cups with common endpoints
    for x, b in itertools.combinations(range(1, N + 1), 2):
        for r in R:
            s = K + 2 - r
            if s < 3 or s > K - 1:
                continue
            if (x, b, r) in CapE and (x, b, s) in CupE:
                clauses.append([-CapE[(x, b, r)], -CupE[(x, b, s)]])

    # symmetry breaking
    sb = []
    if args.hull:
        for i, j in itertools.combinations(range(2, N + 1), 2):
            sb.append([X[(1, i, j)]])
    if args.mirror and N >= 7:
        sb.append([-X[(2, 3, 4)], X[(N - 2, N - 1, N)]])
    if args.flip:
        sb.append([X[(1, 2, 3)]])
    clauses += sb

    with open(args.out, "w") as f:
        f.write(f"c ES signotope CNF N={N} K={K} hull={args.hull} mirror={args.mirror} flip={args.flip} mono={not args.no_mono}\n")
        f.write(f"c X(i,j,k) for i<j<k are variables 1..{nX} in lexicographic order\n")
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(json.dumps({"N": N, "K": K, "vars": nv, "clauses": len(clauses), "X_vars": nX,
                      "hull": args.hull, "mirror": args.mirror, "flip": args.flip, "out": args.out}))


if __name__ == "__main__":
    main()
