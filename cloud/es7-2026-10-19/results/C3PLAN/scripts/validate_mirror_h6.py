#!/usr/bin/env python3
"""Validate the H6 mirror map of PLAN.md (Lemma H6M) on random C3 sets with exact coordinates.
For S with a hexagonal hull: canonicalize S and M(S) = {(-x, y)} independently, each with the
C3-S procedure (validate_hull: a line l with label 0 on the hull, found by random search) plus the
normalization a <= m//2 of Lemma 2(c) (the search continues until the other hull residue is
<= m//2), then sigma_0 = 0 by p -> -p.  Peel the convex layers of both and require that the
layer path of M(S) is the image of the layer path of S under
    phi_{a,s}: (r, sig) -> ((a - r) mod m, sig xor [r < a] xor [s = 0])   (sigma None stays None)
for r not in {0, a}, and layer 1 of M(S) equal to layer 1 of S (M(S) is in the same case H6(a, s)).
A mutation (no sigma rule: sig kept) is run too and must fail on some sets.
usage: validate_mirror_h6.py M NSETS SEED   (run from results/C3-S/tools)"""
import json
import random
import os
import sys

sys.path.insert(0, os.getcwd())

from validate_hull import hull_vertices, label_order, random_set
from c3geom import Labelled


def canon_layers(pts, M, rng):
    n = len(pts)
    H = hull_vertices(pts)
    if len(H) != 6:
        return None
    for _ in range(400000):
        u = (rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6))
        if u == (0, 0):
            continue
        order = label_order(pts, u)
        if order is None or order[0] not in H:
            continue
        lab = {p: i for i, p in enumerate(order)}
        a = sorted({lab[h] % M for h in H} - {0})
        if len(a) == 1 and a[0] <= M // 2:
            break
    else:
        return "nol"
    L = Labelled(pts, rng, u=u)
    if L.sigma[0]:
        L = Labelled([((-p[0][0], -p[0][1]), (-p[1][0], -p[1][1])) for p in pts], rng, u=u)
    rest, layers = set(range(n)), []
    while rest:
        sub = sorted(rest)
        Hs = {sub[i] for i in hull_vertices([pts[j] for j in sub])} if len(sub) > 3 else set(sub)
        if len(Hs) not in (3, 6):
            break
        resid = sorted({L.lab[h] % M for h in Hs})
        layers.append([(resid[0], None)] if len(resid) == 1 else [(r, L.sigma[r]) for r in resid])
        rest -= Hs
    return layers


def phi(M, a, s, lay, flip=True):
    if any(r == 0 for r, _ in lay):  # layer 1 maps to itself
        return sorted(lay)
    return sorted(((a - r) % M, None if g is None else (g ^ (r < a) ^ (s == 0) if flip else g)) for r, g in lay)


def main():
    M, NS, seed = map(int, sys.argv[1:4])
    rng = random.Random(seed)
    res = {"m": M, "seed": seed, "sets": 0, "h6": 0, "layers_compared": 0, "cases": {}, "fail": [], "mutation_fail": 0}
    while res["h6"] < NS and res["sets"] < 200 * NS:
        pts = random_set(M, rng)
        res["sets"] += 1
        A = canon_layers(pts, M, rng)
        if A is None:
            continue
        mp = [((-p[0][0], -p[0][1]), p[1]) for p in pts]
        B = canon_layers(mp, M, rng)
        res["h6"] += 1
        if A == "nol" or B in ("nol", None):
            res["fail"].append({"set": res["sets"], "why": "canon failed", "B": str(B)[:40]})
            continue
        a, s = A[0][1]
        res["cases"][f"H6({a},{s})"] = res["cases"].get(f"H6({a},{s})", 0) + 1
        if len(A) != len(B) or any(sorted(b) != phi(M, a, s, x) for x, b in zip(A, B)):
            res["fail"].append({"set": res["sets"], "A": str(A), "B": str(B)})
        if len(A) != len(B) or any(sorted(b) != phi(M, a, s, x, flip=False) for x, b in zip(A, B)):
            res["mutation_fail"] += 1
        res["layers_compared"] += len(A)
    res["fail"] = res["fail"][:5] + ([f"... {len(res['fail'])} in all"] if len(res["fail"]) > 5 else [])
    print(json.dumps(res))


if __name__ == "__main__":
    main()
