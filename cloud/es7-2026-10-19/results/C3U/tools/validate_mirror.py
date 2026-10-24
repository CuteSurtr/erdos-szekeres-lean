#!/usr/bin/env python3
"""Validate the mirror map of hullcase.mirror_layer on random H3 sets (exact coordinates).
For S with a triangular hull: canonicalize S and M(S) = {(-x, y)} independently (validate_hull's
procedure: l with label 0 on the hull, then sigma_0 = 0 by p -> -p), peel the convex layers of
both, and require: M(S) is H3 and layer j of M(S) == mirror_layer(layer j of S) for every j.
usage: validate_mirror.py M NSETS SEED"""
import json
import random
import sys

from validate_hull import hull_vertices, label_order, random_set
from c3geom import Labelled
from hullcase import mirror_layer


def canon_layers(pts, M, rng):
    n = len(pts)
    H = hull_vertices(pts)
    if len(H) != 3:
        return None
    for _ in range(200000):
        u = (rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6))
        if u == (0, 0):
            continue
        order = label_order(pts, u)
        if order is not None and order[0] in H:
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


def main():
    M, NS, seed = map(int, sys.argv[1:4])
    rng = random.Random(seed)
    res = {"m": M, "seed": seed, "sets": 0, "h3": 0, "layers_compared": 0, "fail": []}
    while res["h3"] < NS:
        pts = random_set(M, rng)
        res["sets"] += 1
        A = canon_layers(pts, M, rng)
        if A is None:
            continue
        mp = [((-p[0][0], -p[0][1]), p[1]) for p in pts]
        B = canon_layers(mp, M, rng)
        res["h3"] += 1
        if A == "nol" or B == "nol" or B is None:
            res["fail"].append({"set": res["sets"], "why": "canon failed", "B": str(B)[:40]})
            continue
        if len(A) != len(B) or any(sorted(b) != mirror_layer(M, a) for a, b in zip(A[1:], B[1:])):
            res["fail"].append({"set": res["sets"], "A": str(A), "B": str(B)})
        res["layers_compared"] += len(A) - 1
    print(json.dumps(res))


if __name__ == "__main__":
    main()
