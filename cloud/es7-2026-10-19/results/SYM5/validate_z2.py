#!/usr/bin/env python3
"""Soundness test of the layer normal form (symcnf_layers.py, even m = 4) on a real 4-fold set with integer coordinates
(rotation (x, y) -> (-y, x) about the origin). Checks that every convex layer is one orbit, labels the set in the
layer normal form, writes the triple-variable units of its chirotope. usage: validate_z2.py POINTS MAP OUT [--swap]"""
import json, math, sys
from itertools import combinations
swap = "--swap" in sys.argv; a = [x for x in sys.argv[1:] if not x.startswith("--")]
P = [tuple(map(int, l.split()[:2])) for l in open(a[0]) if l.strip() and not l.startswith(("#", "FOUND"))]
def orient(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]); return (d > 0) - (d < 0)
rot = lambda p: (-p[1], p[0])
orbits, seen = [], set()
for p in P:
    if p in seen: continue
    orb = [p, rot(p), rot(rot(p)), rot(rot(rot(p)))]; assert len(set(orb)) == 4 and all(q in P for q in orb)
    seen.update(orb); orbits.append(orb)
assert len(seen) == len(P)
assert not any(orient(x, y, z) == 0 for x, y, z in combinations(P, 3))
def hull_vertices(Q):
    return [d for d in Q if not any(orient(x, y, d) == orient(y, z, d) == orient(z, x, d)
                                    for x, y, z in combinations([q for q in Q if q != d], 3))]
rest, layers = list(P), []
while rest:
    V = set(hull_vertices(rest)); o = [i for i, orb in enumerate(orbits) if set(orb) <= V]
    assert len(o) == 1 and set(orbits[o[0]]) == V, ("layer is not one orbit", len(V))
    layers.append(o[0]); rest = [q for q in rest if q not in V]
print("layers:", layers, "-> every convex layer is one orbit")
if swap: layers = layers[:1] + [layers[2], layers[1]] + layers[3:]
p00 = orbits[layers[0]][0]; diam = [(p00, rot(rot(p00))), (rot(p00), rot(rot(rot(p00))))]
def rep(orb):   # the point in the open sector (0, 90 deg) from the ray to p00: angle in (0, pi/2)
    ang = lambda q: (math.atan2(q[1], q[0]) - math.atan2(p00[1], p00[0])) % (2 * math.pi)
    c = [q for q in orb if 0 < ang(q) < math.pi / 2]; assert len(c) == 1; return c[0]
lab = {}
for o, i in enumerate(layers):
    q = p00 if o == 0 else rep(orbits[i])
    for r in range(4): lab[o * 4 + r] = q; q = rot(q)
info = json.load(open(a[1])); assert info["t"] == len(orbits) and info["center_index"] is None
units = sorted({(v if orient(lab[x], lab[y], lab[z]) * s > 0 else -v) for x, y, z, v, s in info["triples"]}, key=abs)
assert len(units) == info["X_vars"]
open(a[2], "w").write("".join(f"{u} 0\n" for u in units)); print("wrote", len(units), "units")
