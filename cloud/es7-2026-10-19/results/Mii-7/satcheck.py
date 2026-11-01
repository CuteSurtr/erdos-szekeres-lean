#!/usr/bin/env python3
"""Decode and brute-force check a SAT model of m33k7int.sub.cnf.

usage: satcheck.py <model.txt> [N=33] [k=7]      (model: DIMACS literals, as cadical's v lines)
       satcheck.py --selftest

Decodes X(i,j,k) = model[rep(X(i,j,k))] (orbit representative as in mirgen.py), then checks,
independently of the CNF:
  * signotope axiom: for every a<b<c<d the sequence X(abc),X(abd),X(acd),X(bcd) changes sign
    at most once;
  * mirror consistency X(i,j,k) = X(m-k,m-j,m-i), m = N+1;
  * axis point c=(N+1)/2 is not extreme (some X(i,c,k) true and some false, i<c<k);
  * no k points in convex position (a set is convex iff every 4-subset is; a 4-set is convex
    iff no point lies in the triangle of the other three, decided from the orientations).
Prints a JSON report.
"""
import sys, itertools, json

def decode(model, N):
    idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
    val = {abs(l): l > 0 for l in model}
    m = N + 1
    X = {}
    for (i, j, k), v in idx.items():
        w = idx[tuple(sorted((m - k, m - j, m - i)))]
        X[(i, j, k)] = val.get(min(v, w), False)
    return X

def check(X, N, K):
    rep = {}
    def o(p, q, r):   # chirotope of an arbitrary ordered triple
        t = [p, q, r]; s = sorted(t)
        par = sum(1 for a, b in itertools.combinations(t, 2) if a > b) % 2
        v = X[tuple(s)]
        return v if par == 0 else not v
    bad_sig = 0
    for a, b, c, d in itertools.combinations(range(1, N + 1), 4):
        s = [X[(a, b, c)], X[(a, b, d)], X[(a, c, d)], X[(b, c, d)]]
        if sum(1 for u, w in zip(s, s[1:]) if u != w) > 1: bad_sig += 1
    rep["signotope_violations"] = bad_sig
    m = N + 1
    rep["mirror_violations"] = sum(1 for (i, j, k) in X if X[(i, j, k)] != X[tuple(sorted((m - k, m - j, m - i)))])
    c = (N + 1) // 2
    vals = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
    rep["axis_point_interior"] = any(vals) and not all(vals)
    def inside(p, q, r, s):
        a, b, cc = o(q, r, p), o(r, s, p), o(s, q, p)
        return a == b == cc
    conv4 = set()
    for t in itertools.combinations(range(1, N + 1), 4):
        if not any(inside(t[x], *[t[y] for y in range(4) if y != x]) for x in range(4)):
            conv4.add(t)
    rep["convex_4sets"] = len(conv4)
    # backtracking: extend a convex set by larger indices, every new 4-subset must be convex
    found = []
    def ext(S):
        if len(S) == K:
            found.append(tuple(S)); return True
        for p in range(S[-1] + 1 if S else 1, N + 1):
            if N - p + 1 < K - len(S): break
            if all(tuple(sorted(T + (p,))) in conv4 for T in itertools.combinations(S, 3)):
                S.append(p)
                if ext(S): return True
                S.pop()
        return False
    ext([])
    rep["convex_%dgon" % K] = list(found[0]) if found else None
    rep["ok"] = (bad_sig == 0 and rep["mirror_violations"] == 0 and rep["axis_point_interior"]
                 and not found)
    return rep

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.path.insert(0, sys.argv[2])   # results/C/scripts for mirlib
        import random, mirlib
        rng = random.Random(1)
        out = []
        for N, K, npairs in ((33, 7, 16), (11, 6, 5), (9, 5, 4)):
            for _ in range(3 if N == 33 else 40):
                P = mirlib.mirror_set(npairs, 1, rng, where='interior')
                Q = mirlib.xsorted(P)
                X = mirlib.orientations(Q)
                r = check(X, N, K)
                truth = mirlib.has_kgon(Q, K)
                out.append((N, K, r["signotope_violations"], r["mirror_violations"],
                            r["convex_%dgon" % K] is not None, bool(truth)))
        agree = sum(1 for t in out if t[2] == 0 and t[3] == 0 and t[4] == t[5])
        print(json.dumps({"selftest_agree": "%d/%d" % (agree, len(out)),
                          "kgon_free": sum(1 for t in out if not t[5])}))
    else:
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 33
        K = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        model = [int(x) for x in open(sys.argv[1]).read().split() if x != '0']
        print(json.dumps(check(decode(model, N), N, K)))
