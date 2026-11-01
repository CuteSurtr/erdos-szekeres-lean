#!/usr/bin/env python3
"""Independent check of a SAT model of a gen_c3b.py CNF (does not use the generator's clauses).

Decodes chi' (X), chi_S (Y), s, inv, o from the model via the map JSON and verifies:
  * orbit/sign bookkeeping: chi_S(Ri,Rj,Rk) = chi_S(ijk), chi'(R.) = chi'(.) e e e
  * the identities chi_S = chi' (-1)^(s_i+s_j+s_k), s_{Ri} = s_i xor [i>=m], o = inv xor s xor s
  * chi' is a signotope (every 4-tuple monotone), the inv prefix rule, s-forced inv
  * chi_S is a uniform rank-3 oriented matroid: 3-term Grassmann-Pluecker on every 5-set,
    and acyclic (no totally cyclic 4-set)
  * no k points in convex position under chi_S (DFS, Caratheodory 4-point test);
    reports the largest convex subset size
Writes the decoded chi_S (and chi') as JSON for realization attempts.
usage: modelcheck.py map.json model.out [--json out.json]
"""
import itertools
import json
import sys


def par(t):
    a, b, c = t
    return -1 if ((a > b) + (a > c) + (b > c)) & 1 else 1


def main():
    mp = json.load(open(sys.argv[1]))
    lits = set()
    for line in open(sys.argv[2]):
        if line.startswith("v"):
            lits.update(int(x) for x in line.split()[1:])
    val = lambda v: v in lits
    m, n, k = mp["m"], mp["n"], mp["k"]
    Xs, Ys = {}, {}
    for a, b, c, v, s in mp["X"]:
        Xs[a, b, c] = s * (1 if val(v) else -1)
    for a, b, c, v, s in mp["Y"]:
        Ys[a, b, c] = s * (1 if val(v) else -1)
    assert len(Xs) == len(Ys) == n * (n - 1) * (n - 2) // 6
    X = lambda a, b, c: par((a, b, c)) * Xs[tuple(sorted((a, b, c)))]
    Y = lambda a, b, c: par((a, b, c)) * Ys[tuple(sorted((a, b, c)))]
    sv = [1 if val(v) else 0 for v in mp["s"]]
    s = [sv[i % m] ^ (1 if i // m == 1 else 0) for i in range(n)]
    I = {(i, j): val(v) for i, j, v in mp["I"]}
    Oo = {(i, j): val(v) for i, j, v in mp["O"]}
    R = lambda i: (i - m) % n
    e = lambda i: 1 if i < m else -1
    err = {}

    def bad(key):
        err[key] = err.get(key, 0) + 1
    for T in itertools.combinations(range(n), 3):
        a, b, c = T
        if Y(R(a), R(b), R(c)) != Y(a, b, c):
            bad("symY")
        if X(R(a), R(b), R(c)) != X(a, b, c) * e(a) * e(b) * e(c):
            bad("symX")
        if Y(a, b, c) != X(a, b, c) * (-1) ** (s[a] + s[b] + s[c]):
            bad("chiS=chi'*sign")
        x = X(a, b, c)
        seq = [I[a, b], I[a, c], I[b, c]] if x > 0 else [I[b, c], I[a, c], I[a, b]]
        if seq not in ([0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]):
            bad("invprefix")
    for i in range(n):
        if s[R(i)] != s[i] ^ (1 if i >= m else 0):
            bad("sR")
    if s[0] != 0:
        bad("s0")
    for (i, j), v in I.items():
        if s[i] != s[j] and v != (s[j] == 1):
            bad("sinv")
        if Oo[i, j] != (v ^ s[i] ^ s[j]):
            bad("o")
    for a, b, c, d in itertools.combinations(range(n), 4):
        seq = [X(a, b, c), X(a, b, d), X(a, c, d), X(b, c, d)]
        ch = sum(1 for t in range(3) if seq[t] != seq[t + 1])
        if ch > 1:
            bad("signotope")
        pat = (Y(a, b, c), Y(a, b, d), Y(a, c, d), Y(b, c, d))
        if pat in ((1, -1, 1, -1), (-1, 1, -1, 1)):
            bad("cyclic")
    for S in itertools.combinations(range(n), 5):
        for x in S:
            y1, y2, y3, y4 = [y for y in S if y != x]
            t1 = Y(x, y1, y2) * Y(x, y3, y4)
            t2 = -Y(x, y1, y3) * Y(x, y2, y4)
            t3 = Y(x, y1, y4) * Y(x, y2, y3)
            if t1 == t2 == t3:
                bad("GP")
    # convex subsets under chi_S

    def inside(t, a, b, c):
        q = Y(a, b, c)
        return Y(a, b, t) == q and Y(b, c, t) == q and Y(c, a, t) == q
    conv4 = {}
    for Q in itertools.combinations(range(n), 4):
        conv4[Q] = not any(inside(Q[t], *[Q[u] for u in range(4) if u != t]) for t in range(4))
    best = [0, None]

    def rec(cur, start):
        if len(cur) > best[0]:
            best[0], best[1] = len(cur), list(cur)
        if len(cur) >= k:
            return
        for x in range(start, n):
            if len(cur) < 3 or all(conv4[T + (x,)] for T in itertools.combinations(cur, 3)):
                rec(cur + [x], x + 1)
    rec([], 0)
    if best[0] >= k:
        bad("convex_k_gon")
    res = {"m": m, "n": n, "k": k, "errors": err, "max_convex_found": best[0], "example": best[1],
           "ok": not err}
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"n": n, "m": m, "k": k, "s": s,
                   "chiS": {f"{a},{b},{c}": Y(a, b, c) for a, b, c in itertools.combinations(range(n), 3)},
                   "chiP": {f"{a},{b},{c}": X(a, b, c) for a, b, c in itertools.combinations(range(n), 3)},
                   "inv": {f"{i},{j}": int(v) for (i, j), v in I.items()}}, open(out, "w"))
    print(json.dumps(res))
    sys.exit(0 if not err else 1)


if __name__ == "__main__":
    main()
