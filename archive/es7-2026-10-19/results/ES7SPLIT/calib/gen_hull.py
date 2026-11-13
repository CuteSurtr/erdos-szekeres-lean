#!/usr/bin/env python3
"""ES(K) signotope CNF on N points in the 'hull' normal form (point 1 extreme, points 2..N sorted around
it), plus an exact constraint on the size h of the convex hull.

The base CNF is produced by the repository encoder experiments/es7-search-2026-10-13/encoding/gen_cnf.py
(read-only, imported as a module from its path) with --hull [--mirror]; this script appends:

  u_j  (3 <= j <= N-1)  <->  AND_{2<=i<j<l<=N} X(i,j,l)
       (the normal form re-inserts point 1 as (-M, M^2) for large M, i.e. near the UPWARD point at infinity,
       leftmost; the x-order of 2..N is the angular order around point 1.  u_j says that j is below every
       segment il (i < j < l), i.e. j lies on the lower hull of {2..N}; points 2 and N always do.  The hull
       of the whole set is {1} plus that lower hull, so h = 3 + sum_j u_j.  First version used the upper
       hull by mistake; the independent model checker check_hull_model.py caught it.)
  sum_j u_j = h - 3     (sequential-counter encoding, both directions)

Soundness: every realizable set has the normal form (projective map sending an extreme point to vertical
infinity; see gen_cnf.py), and the hull size is invariant under such admissible projective maps.
"""
import argparse
import importlib.util
import json
import sys

# Repository encoder: <repo>/experiments/es7-search-2026-10-13/encoding/gen_cnf.py, found from this file's place
# in cloud/es7-2026-10-19/results/ES7SPLIT/calib/ (override with the environment variable ES7_GEN_CNF).
import os
ENC = os.environ.get("ES7_GEN_CNF") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), *[".."] * 5, "experiments", "es7-search-2026-10-13", "encoding", "gen_cnf.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("K", type=int)
    ap.add_argument("h", type=int, help="hull size")
    ap.add_argument("--mirror", action="store_true")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    N, K, h = args.N, args.K, args.h
    base = args.out + ".base"
    sys.argv = [ENC, str(N), str(K), "--hull"] + (["--mirror"] if args.mirror else []) + ["-o", base]
    spec = importlib.util.spec_from_file_location("gen_cnf", ENC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main()
    info = json.loads(buf.getvalue())
    nv, nc = info["vars"], info["clauses"]
    X = {}
    v = 0
    import itertools
    for t in itertools.combinations(range(1, N + 1), 3):
        v += 1
        X[t] = v
    extra = []

    def new():
        nonlocal nv
        nv += 1
        return nv

    U = {}
    for j in range(3, N):
        U[j] = new()
        trip = [X[(i, j, l)] for i in range(2, j) for l in range(j + 1, N + 1)]
        for x in trip:
            extra.append([-U[j], x])
        extra.append([U[j]] + [-y for y in trip])
    # exactly t = h-3 of the u_j true: standard sequential counter
    # s(k,c) <-> s(k-1,c) or (s(k-1,c-1) and x_k), s(0,c>=1) = False, s(k,0) = True
    t = h - 3
    js = sorted(U)
    m = len(js)
    s = {}
    for k in range(1, m + 1):
        for c in range(1, t + 2):
            s[(k, c)] = new()
    TRUE, FALSE = "T", "F"

    def sv(k, c):
        if c == 0:
            return TRUE
        if k == 0:
            return FALSE
        return s[(k, c)]

    for k in range(1, m + 1):
        x = U[js[k - 1]]
        for c in range(1, t + 2):
            cur, A, Bv = s[(k, c)], sv(k - 1, c), sv(k - 1, c - 1)
            # cur -> A or Bv ; cur -> A or x ; A -> cur ; (Bv and x) -> cur
            cl1 = [-cur] + ([A] if A not in (TRUE, FALSE) else []) + ([Bv] if Bv not in (TRUE, FALSE) else [])
            if not (A == TRUE or Bv == TRUE):
                extra.append(cl1)
            if A != TRUE:
                extra.append([-cur] + ([A] if A != FALSE else []) + [x])
            if A not in (TRUE, FALSE):
                extra.append([-A, cur])
            if Bv != FALSE:
                extra.append(([-Bv] if Bv != TRUE else []) + [-x, cur])
    if t >= 1:
        extra.append([s[(m, t)]])
    extra.append([-s[(m, t + 1)]])
    lines = open(base).read().splitlines()
    import os
    os.remove(base)
    body = [l for l in lines if not l.startswith("p ") and not l.startswith("c ")]
    with open(args.out, "w") as f:
        f.write(f"c gen_hull N={N} K={K} h={h} mirror={args.mirror}\n")
        f.write(f"p cnf {nv} {nc + len(extra)}\n")
        f.write("\n".join(body) + "\n")
        for c in extra:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(json.dumps(dict(N=N, K=K, h=h, vars=nv, clauses=nc + len(extra), out=args.out)))


if __name__ == "__main__":
    main()
