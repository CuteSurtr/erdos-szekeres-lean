#!/usr/bin/env python3
"""Independent exact checker: general position and convex k-gon counts.

Method (independent of cgon.c's angular DP and satcount.c's slot count):
points are ordered lexicographically by (x, y) (an infinitesimal rotation of
the x-order, which does not change orientations); a convex polygon is the
union of a cup and a cap with the same leftmost point l and rightmost point r,
and every such pair gives a convex polygon.  So
    #convex k-gons = sum_{l<r} sum_{a+b=k+2, a,b>=2} cups(l,r,a) * caps(l,r,b)
with cups/caps counted by a dynamic program over last edges.  All arithmetic
uses Python integers or Fractions (exact).

usage:
  verify_exact.py FILE [K]      FILE: "x y" per line (ints, or p/q fractions,
                                or decimals, read exactly); prints JSON
  verify_exact.py --json FILE KEY [K]   points from a JSON list under KEY
                                (floats are converted exactly with Fraction)
"""
import sys, json, itertools
from fractions import Fraction


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def general_position(P):
    n = len(P)
    if len(set(P)) != n:
        return False, "repeated point"
    for i, j, k in itertools.combinations(range(n), 3):
        if orient(P[i], P[j], P[k]) == 0:
            return False, f"collinear {i} {j} {k}"
    return True, ""


def count_convex(P, K):
    """counts[k] for k = 3..K, by cups and caps over the lexicographic order."""
    n = len(P)
    order = sorted(range(n), key=lambda i: (P[i][0], P[i][1]))
    Q = [P[i] for i in order]
    # O[i][j][k] sign for i<j<k in sorted order
    O = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = orient(Q[i], Q[j], Q[k])
                O[(i, j, k)] = 1 if s > 0 else -1
    counts = {k: 0 for k in range(3, K + 1)}
    for l in range(n):
        # chain DP: dp[(i,j)][a] = number of chains l, ..., i, j with a points whose
        # turns all have sign `sign` (+1: cups, left turns; -1: caps, right turns)
        res = {}
        for sign in (1, -1):
            dp = {}
            # length 2 chains l->j
            for j in range(l + 1, n):
                dp[(l, j)] = {2: 1}
            # process in order of last point j so that predecessors are complete
            tot = {}  # tot[r][a] = number of chains from l ending at r with a points
            for j in range(l + 1, n):
                for i in [l] + list(range(l + 1, j)):
                    d = dp.get((i, j))
                    if not d:
                        continue
                    t = tot.setdefault(j, {})
                    for a, c in d.items():
                        t[a] = t.get(a, 0) + c
                    for k in range(j + 1, n):
                        # turn at j of the chain ..., i, j, k (i < j < k)
                        if O[(i, j, k)] == sign:
                            e = dp.setdefault((j, k), {})
                            for a, c in d.items():
                                if a + 1 <= K:
                                    e[a + 1] = e.get(a + 1, 0) + c
            res[sign] = tot
        cups, caps = res[1], res[-1]
        for r in range(l + 1, n):
            cu, ca = cups.get(r, {}), caps.get(r, {})
            for a, x in cu.items():
                for b, y in ca.items():
                    k = a + b - 2
                    if 3 <= k <= K:
                        counts[k] += x * y
    return counts


def list_kgons(P, K):
    """explicit list of convex K-gons (as sorted index tuples) via cups/caps, for small counts."""
    n = len(P)
    order = sorted(range(n), key=lambda i: (P[i][0], P[i][1]))
    Q = [P[i] for i in order]
    out = []

    def chains(l, sign):
        res = {}
        stack = [[l]]
        while stack:
            ch = stack.pop()
            last = ch[-1]
            if len(ch) >= 2:
                res.setdefault(last, []).append(ch)
            if len(ch) >= K:
                continue
            for k in range(last + 1, n):
                if len(ch) >= 2 and (1 if orient(Q[ch[-2]], Q[last], Q[k]) > 0 else -1) != sign:
                    continue
                stack.append(ch + [k])
        return res
    for l in range(n):
        cu, ca = chains(l, 1), chains(l, -1)
        for r in cu:
            for c1 in cu[r]:
                for c2 in ca.get(r, []):
                    if len(c1) + len(c2) - 2 == K:
                        out.append(tuple(sorted(order[i] for i in set(c1) | set(c2))))
    return sorted(set(out))


def read_points(path):
    P = []
    for line in open(path):
        f = line.split()
        if len(f) < 2:
            continue
        P.append((Fraction(f[0]), Fraction(f[1])))
    return P


def main():
    a = sys.argv[1:]
    if a and a[0] == "--json":
        d = json.load(open(a[1]))
        P = [(Fraction(x), Fraction(y)) for x, y in d[a[2]]]
        K = int(a[3]) if len(a) > 3 else 8
    else:
        P = read_points(a[0])
        K = int(a[1]) if len(a) > 1 else 8
    gp, why = general_position(P)
    out = {"n": len(P), "general_position": gp}
    if not gp:
        out["reason"] = why
        print(json.dumps(out))
        return
    c = count_convex(P, K)
    out["counts"] = {str(k): v for k, v in c.items()}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
