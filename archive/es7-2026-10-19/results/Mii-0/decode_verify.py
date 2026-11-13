#!/usr/bin/env python3
"""Decode a SAT model of m33k7int.sub.cnf into the full 33-point signotope and brute-force check it.

usage: decode_verify.py <model file: DIMACS literals> [N=33]

X(i,j,k), i<j<k, x-sorted, is variable lexindex(i,j,k); in the orbit-substituted CNF each
X(i,j,k) takes the value of its orbit representative min(idx(i,j,k), idx(m-k,m-j,m-i)), m = N+1.
Checks (all exhaustive):
  * signotope axioms: for every i<j<k<l, the sequence X(jkl), X(ikl), X(ijl), X(ijk) has at most
    one sign change;
  * mirror consistency X(i,j,k) == X(m-k,m-j,m-i) (by construction; checked on the raw model
    too: the representative's value is the only one used);
  * axis point c=(N+1)/2 is not extreme (some chord i<c<k above it and some below);
  * no 7 points in convex position: DFS over increasing index sets, pruned by 4-point convexity
    (a set is in convex position iff all its 4-subsets are; a 4-set is convex iff no point lies in
    the triangle of the other three, using the chirotope extended by permutation sign).
Prints a JSON summary; writes <model>.orient (the 0/1 string over lexicographic triples).
"""
import sys, itertools, json
N = int(sys.argv[2]) if len(sys.argv) > 2 else 33
m = N + 1
lits = [int(x) for x in open(sys.argv[1]).read().split()]
val = {abs(l): l > 0 for l in lits}
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
X = {}
for (i, j, k), v in idx.items():
    w = idx[tuple(sorted((m - k, m - j, m - i)))]
    X[(i, j, k)] = val[min(v, w)]
res = {"N": N}
# signotope axioms
bad = 0
for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
    s = [X[(j, k, l)], X[(i, k, l)], X[(i, j, l)], X[(i, j, k)]]
    if sum(s[t] != s[t + 1] for t in range(3)) > 1: bad += 1
res["signotope_violations"] = bad
res["mirror_violations"] = sum(X[t] != X[tuple(sorted((m - t[2], m - t[1], m - t[0])))] for t in X)
c = (N + 1) // 2
ch = [X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
res["axis_point_interior"] = any(ch) and not all(ch)
res["X123"] = X[(1, 2, 3)]


def o(a, b, cc):  # chirotope sign (+1 ccw) for distinct a,b,c
    t = sorted((a, b, cc)); s = 1 if X[tuple(t)] else -1
    # parity of the permutation (a,b,c) -> sorted
    p = [a, b, cc]; inv = sum(p[x] > p[y] for x in range(3) for y in range(x + 1, 3))
    return s if inv % 2 == 0 else -s


def inside(q, a, b, cc):
    return o(a, b, q) == o(b, cc, q) == o(cc, a, q)


conv4 = {}
for q in itertools.combinations(range(1, N + 1), 4):
    conv4[q] = not any(inside(q[t], *[q[u] for u in range(4) if u != t]) for t in range(4))
K = 7
count = 0; example = None


def dfs(S, start):
    global count, example
    if len(S) == K:
        count += 1
        if example is None: example = list(S)
        return
    for p in range(start, N + 1):
        if all(conv4[tuple(sorted(T + (p,)))] for T in itertools.combinations(S, 3)):
            S.append(p); dfs(S, p + 1); S.pop()


dfs([], 1)
res["convex_7gons"] = count; res["example_7gon"] = example
res["convex_4sets"] = sum(conv4.values())
with open(sys.argv[1] + ".orient", "w") as f:
    f.write("".join("1" if X[t] else "0" for t in sorted(idx, key=idx.get)) + "\n")
res["ok_abstract_heptagon_free"] = bad == 0 and res["mirror_violations"] == 0 and count == 0 and res["axis_point_interior"]
print(json.dumps(res))
