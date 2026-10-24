#!/usr/bin/env python3
"""Decode and brute-force check a SAT model of an orbit-substituted mirror CNF (mirgen.py).

usage: verify_sat.py <model.json> [N=33] [k=7]

Decodes X(i,j,k) for every triple (non-representatives take their mirror representative's
value), then checks exhaustively, independent of the CNF:
 * signotope axiom: for every i<j<k<l the sequence X(jkl), X(ikl), X(ijl), X(ijk) changes sign
   at most once;
 * mirror consistency: X(i,j,k) = X(m-k,m-j,m-i), m = N+1;
 * no k points in convex position: a 4-set is non-convex iff one point lies inside the triangle
   of the other three (chirotope test); a k-set is convex iff all its 4-subsets are; searched by
   depth-first extension over all subsets;
 * for N odd, the axis point c = (N+1)/2 is not extreme (some i<c<k has X true and some false).
Writes <model>.orient.txt (one 0/1 per triple in lexicographic order) and prints a JSON report.
"""
import sys, json, itertools

mp = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 33
K = int(sys.argv[3]) if len(sys.argv) > 3 else 7
d = json.load(open(mp))
val = {abs(l): l > 0 for l in d["model"]}
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
m = N + 1
X = {}
for (i, j, k), v in idx.items():
    w = idx[tuple(sorted((m - k, m - j, m - i)))]
    X[(i, j, k)] = val[min(v, w)]
rep = {}
bad_sig = 0
for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
    s = [X[(j, k, l)], X[(i, k, l)], X[(i, j, l)], X[(i, j, k)]]
    if sum(s[a] != s[a + 1] for a in range(3)) > 1:
        bad_sig += 1
bad_mir = sum(X[(i, j, k)] != X[tuple(sorted((m - k, m - j, m - i)))] for (i, j, k) in idx)
for c in [d["cube"]]:
    cube_ok = all(val.get(abs(l)) == (l > 0) for l in c)


def chi(a, b, c):
    """orientation of an ordered triple of distinct indices as +1/-1"""
    t = (a, b, c); s = sorted(t)
    par = sum(1 for x, y in itertools.combinations(t, 2) if x > y) % 2
    o = 1 if X[tuple(s)] else -1
    return -o if par else o


def inside(dd, a, b, c):
    o = chi(a, b, c)
    return chi(a, b, dd) == o and chi(b, c, dd) == o and chi(c, a, dd) == o


nonconvex4 = set()
for q in itertools.combinations(range(1, N + 1), 4):
    for t in range(4):
        dd = q[t]; r = [x for x in q if x != dd]
        if inside(dd, *r):
            nonconvex4.add(q); break
count = 0; example = None


def ext(S):
    global count, example
    if len(S) == K:
        count += 1
        if example is None: example = list(S)
        return
    for p in range(S[-1] + 1 if S else 1, N + 1):
        if all(tuple(sorted(T + (p,))) not in nonconvex4 for T in itertools.combinations(S, 3)):
            ext(S + [p])


ext([])
rep = {"model": mp, "N": N, "k": K, "cube_respected": cube_ok, "signotope_violations": bad_sig,
       "mirror_violations": bad_mir, "nonconvex_4sets": len(nonconvex4), f"convex_{K}gons": count,
       "example_gon": example}
if N % 2 == 1:
    c = (N + 1) // 2
    vs = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
    rep["axis_point_interior"] = any(vs) and not all(vs)
rep["ok"] = bad_sig == 0 and bad_mir == 0 and count == 0 and cube_ok
with open(mp + ".orient.txt", "w") as f:
    f.write("".join("1" if X[t] else "0" for t in sorted(idx, key=idx.get)) + "\n")
print(json.dumps(rep))
