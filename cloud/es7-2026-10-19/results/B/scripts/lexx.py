#!/usr/bin/env python3
"""Append the x-reflection lex-leader to an ETV signotope CNF.

usage: lexx.py in.cnf N out.cnf

Orientation variables are X(t), t = (i,j,k), 1 <= i < j < k <= N, numbered 1..C(N,3) in
lexicographic order (gen_etv.py and Baek-Balko share this numbering and polarity).
Reflecting x (x -> -x) maps point i to N+1-i; it reverses each triple's order and its
orientation, so the reflected signotope is s'(i,j,k) = s(N+1-k, N+1-j, N+1-i), and cups stay
cups, caps stay caps. Every ETV instance (no a-cap, no u-cup, no k-gon) is invariant under it.

We require s <=_lex s' over the variable order (false < true). Only positions t with
idx(t) < idx(rho t) matter: fixed triples compare equal, and a position t whose partner
rho(t) came earlier is equal whenever the prefix is equal. Encoding with prefix-equality
auxiliaries e_r (e_0 = true):
    e_{r-1} -> (x_r -> y_r)                     [-e, -x, y]
    e_{r-1} & (x_r = y_r) -> e_r                 [-e, -x, e_r], [-e, y, e_r]
The kept set is exactly {s : s <=_lex s o rho}: one representative per orbit.
"""
import itertools, json, sys

inp, N, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
pairs = []
for t, v in idx.items():
    i, j, k = t
    w = idx[(N + 1 - k, N + 1 - j, N + 1 - i)]
    if v < w:
        pairs.append((v, w))
pairs.sort()
with open(inp) as f:
    header = f.readline().split()
    assert header[:2] == ["p", "cnf"]
    nv, nc = int(header[2]), int(header[3])
    body = f.read()
new = []
e = None
for r, (x, y) in enumerate(pairs):
    pre = [] if e is None else [-e]
    new.append(pre + [-x, y])
    if r + 1 < len(pairs):
        nv += 1; er = nv
        new.append(pre + [-x, er]); new.append(pre + [y, er])
        e = er
with open(out, "w") as f:
    f.write(f"p cnf {nv} {nc + len(new)}\n")
    f.write(body)
    if body and not body.endswith("\n"):
        f.write("\n")
    for c in new:
        f.write(" ".join(map(str, c)) + " 0\n")
print(json.dumps({"lexx_pairs": len(pairs), "added_clauses": len(new), "vars": nv}))
