#!/usr/bin/env python3
"""Decode and brute-force check a SAT model of m33k7int.sub.cnf (or check a point set).

usage: verify_sat.py model <model_file> [N=33]      (model: DIMACS literals, as cadical prints)
       verify_sat.py points <file with x1 y1 x2 y2 ...>   (exact integer coordinates)

Model decoding: X(i,j,k) = value of the orbit representative min(idx(i,j,k), idx(m-k,m-j,m-i)),
m = N+1, exactly the substitution of C/scripts/mirgen.py.  Checks, by brute force:
 * signotope axioms: for every i<j<k<l the sequence X(jkl), X(ikl), X(ijl), X(ijk) has at most
   one sign change (monotone);
 * mirror consistency X(i,j,k) == X(m-k,m-j,m-i) for every triple, the interior condition on
   the axis point c = (N+1)/2, and the unit X(1,2,3);
 * no 7 points in convex position: a set is in convex position iff it contains no point inside
   a triangle of three others (Caratheodory; chirotope from X with permutation signs), searched
   exhaustively over all 7-subsets with pruning on non-convex 4-subsets.
"""
import sys, itertools, json

def chi_from_X(X):
    def chi(a, b, c):
        s = 1; t = [a, b, c]
        for p in range(3):
            for q in range(2 - p):
                if t[q] > t[q + 1]: t[q], t[q + 1] = t[q + 1], t[q]; s = -s
        return s * (1 if X[tuple(t)] else -1)
    return chi

def count_kgons(N, chi, k=7, stop_at=None):
    pts = range(1, N + 1)
    def inside(q, p, r, s):
        o = chi(p, r, s)
        return chi(p, r, q) == o and chi(r, s, q) == o and chi(s, p, q) == o
    bad = set()
    for f in itertools.combinations(pts, 4):
        for q in f:
            o = [x for x in f if x != q]
            if inside(q, *o): bad.add(f); break
    found = []
    def ext(cur, start):
        if len(cur) == k:
            found.append(tuple(cur)); return stop_at is not None and len(found) >= stop_at
        for v in range(start, N + 1):
            if all(tuple(sorted(t + (v,))) not in bad for t in itertools.combinations(cur, 3)):
                cur.append(v)
                if ext(cur, v + 1): return True
                cur.pop()
        return False
    ext([], 1)
    return found, len(bad)

def main():
    mode = sys.argv[1]
    if mode == "points":
        vals = [int(x) for x in open(sys.argv[2]).read().split()]
        P = sorted(zip(vals[0::2], vals[1::2])); N = len(P)
        assert len(set(p[0] for p in P)) == N, "x-coordinates not distinct"
        X = {}
        for t in itertools.combinations(range(1, N + 1), 3):
            a, b, c = (P[i - 1] for i in t)
            o = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            assert o != 0, "collinear triple"
            X[t] = o > 0
        res = {"N": N}
    else:
        N = int(sys.argv[3]) if len(sys.argv) > 3 else 33
        lits = [int(x) for x in open(sys.argv[2]).read().split() if x not in ("v",)]
        val = {abs(l): l > 0 for l in lits if l != 0}
        idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
        m = N + 1
        X = {}
        for (i, j, k), v in idx.items():
            w = idx[tuple(sorted((m - k, m - j, m - i)))]
            X[(i, j, k)] = val[min(v, w)]
        res = {"N": N}
        res["mirror_violations"] = sum(X[t] != X[tuple(sorted((m - t[2], m - t[1], m - t[0])))] for t in X)
        c = (N + 1) // 2
        cs = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
        res["interior_axis_point"] = any(cs) and not all(cs)
        res["unit_X123"] = X[(1, 2, 3)]
    viol = 0
    for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
        s = [X[(j, k, l)], X[(i, k, l)], X[(i, j, l)], X[(i, j, k)]]
        if sum(s[q] != s[q + 1] for q in range(3)) > 1: viol += 1
    res["signotope_violations"] = viol
    gons, nbad = count_kgons(N, chi_from_X(X), 7, stop_at=1)
    res["nonconvex_4sets"] = nbad
    res["convex_7gon_found"] = gons[0] if gons else None
    print(json.dumps(res))

if __name__ == "__main__":
    main()
