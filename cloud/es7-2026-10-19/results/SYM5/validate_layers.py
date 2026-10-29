#!/usr/bin/env python3
"""Soundness test of the layer normal form on a real 5-fold set (exact arithmetic in Z[zeta5], as in verify5.py).
Checks that every convex layer is one orbit, labels the set in the layer normal form, and writes the triple-variable
units of its chirotope for the CNF made by symcnf_layers.py (or, with --angle, by symcnf.py's angle normal form).
usage: validate_layers.py POINTS.txt MAP.json OUT_UNITS [--angle] [--swap]   (--swap: deliberately wrong layer order)"""
import json, sys
from itertools import combinations
sys.argv, args = sys.argv[:1] + [a for a in sys.argv[1:] if not a.startswith("--")], [a for a in sys.argv[1:] if a.startswith("--")]
src = open(sys.argv[0].replace("validate_layers.py", "../SYMMAX/verify5.py")).read().split("path, k = sys.argv")[0]
exec(src)                                   # sgn, norm, mul, conj, orient, rot, key_cmp, max_convex
pts_path, map_path, out_path = sys.argv[1:4]
P = [norm(list(map(int, l.split()))) for l in open(pts_path) if l.strip() and not l.startswith(("FOUND", "#"))]
O = (0, 0, 0, 0, 0)
orbits, seen = [], set()
for p in P:
    if p in seen: continue
    orb = [p]
    for _ in range(4): orb.append(rot(orb[-1]))
    seen.update(orb); orbits.append(orb)
assert all(len(set(o)) == 5 for o in orbits) and len(seen) == len(P)
def hull_vertices(Q):
    V = []
    for d in Q:
        R = [q for q in Q if q != d]
        inside = any(orient(a, b, d) == orient(b, c, d) == orient(c, a, d) for a, b, c in combinations(R, 3))
        if not inside: V.append(d)
    return V
rest, layers = list(P), []
while rest:
    V = set(hull_vertices(rest))
    orbs = [i for i, o in enumerate(orbits) if set(o) <= V]
    assert len(orbs) == 1 and set(orbits[orbs[0]]) == V, ("layer is not one orbit", len(V))
    layers.append(orbs[0]); rest = [q for q in rest if q not in V]
print("layers (orbit indices, outermost first):", layers, "-> every convex layer is one orbit")
order = layers if "--angle" not in args else None
p00 = orbits[layers[0]][0]
p01 = rot(p00)
def rep(orb):
    c = [q for q in orb if orient(O, p00, q) > 0 and orient(O, p01, q) < 0]
    assert len(c) == 1; return c[0]
if "--angle" in args:
    # symcnf.py normal form: orbit 0 = the orbit of p00 (any), others sorted by angle of their sector representative
    others = [i for i in range(len(orbits)) if i != layers[0]]
    reps = {i: rep(orbits[i]) for i in others}
    from functools import cmp_to_key
    others.sort(key=cmp_to_key(lambda i, j: -1 if orient(O, reps[i], reps[j]) > 0 else 1))
    order = [layers[0]] + others
if "--swap" in args:
    order = order[:1] + [order[2], order[1]] + order[3:]
lab = {}
for o, i in enumerate(order):
    q = p00 if o == 0 else rep(orbits[i])
    for r in range(5):
        lab[o * 5 + r] = q; q = rot(q)
info = json.load(open(map_path)); c = info["center_index"]; lab[c] = O
assert info["t"] == len(orbits) and c == 5 * len(orbits)
units = []
for a, b, cc, v, s in info["triples"]:
    chi = orient(lab[a], lab[b], lab[cc]); assert chi != 0
    units.append(v if chi * s > 0 else -v)
units = sorted(set(units), key=abs)
assert len(units) == info["X_vars"], (len(units), info["X_vars"])
open(out_path, "w").write("".join(f"{u} 0\n" for u in units))
print("wrote", len(units), "units; largest convex subset of the set:", max_convex(P))
