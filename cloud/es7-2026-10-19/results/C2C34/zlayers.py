#!/usr/bin/env python3
"""Convex-layer normal form for centrally symmetric sets in the zcnf.py model (kind rot, m = 2, generated with --no-sb).

Fact. Let S be a centrally symmetric set of 2t points in general position (centre c not in S) with no 7 points in convex
position. Peel convex layers: the remaining set R is always centrally symmetric, so its hull is a centrally symmetric
polygon. If |R| >= 4 this polygon has an even number >= 4 of vertices (R is not collinear), and at most 6 (8 vertices
would be 8 points in convex position); if |R| = 2 the last layer is one antipodal pair. So the layer sizes in pairs form
a profile (h_1, ..., h_L) with h_i in {2, 3} for i < L, h_L in {1, 2, 3}, and sum t.

Normal form for a profile. Orbits (antipodal pairs) are numbered layer by layer, outermost first. (0,0) is a vertex of
the outer layer (any one). For every orbit o >= 1 the representative (o,0) is the point of the pair in the open
half-plane left of the ray c -> (0,0) (no other point lies on that line, by general position), and within each layer the
orbits are sorted by the angle of their representatives. Then a layer with orbits o_1 < ... < o_h has the vertices
(o_1,0), ..., (o_h,0), (o_1,1), ..., (o_h,1) in counter-clockwise order around c, which is inside every layer polygon.
Units (all true for every real S labelled this way):
  chi(c, (0,0), (o,0)) = +                      for every o >= 1          (half-plane)
  chi(c, (o_i,0), (o_j,0)) = +                  for i < j in one layer     (angular order within a layer)
  chi(u, w, x) = +   for every edge u -> w of a layer polygon (h >= 2) and every other point x of that layer or of a
                     deeper layer                                            (convex position, nesting)
Every real S with profile H has such a labelling, so the CNFs of all admissible profiles together cover every real
counterexample (this is an argument about real sets, not a statement about the CNF's models).

usage: zlayers.py MAP.json PROFILE OUT_UNITS [--any]      PROFILE like 3,2,2,2,2,2,2,2 ; --any: allow h >= 4 (tests)
       zlayers.py --list T                                  print all admissible profiles for t = T
"""
import itertools, json, sys


def parity_sort(x):
    a, b, c = x
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(x)), (-1 if inv & 1 else 1)


def profiles(t):
    out = []
    def rec(pre, rest):
        if rest == 0:
            out.append(tuple(pre)); return
        for h in (1, 2, 3):
            if h > rest: continue
            if h == 1 and rest != 1: continue          # a one-pair layer is the last one
            rec(pre + [h], rest - h)
    rec([], t)
    return [p for p in out if all(h >= 2 for h in p[:-1])]


def layer_units(tv, Z, t, profile, allow_any=False):
    assert sum(profile) == t, (profile, t)
    if not allow_any:
        assert all(h in (2, 3) for h in profile[:-1]) and profile[-1] in (1, 2, 3), profile
    def lit(a, b, c):
        S, s = parity_sort((a, b, c))
        v, sg = tv[S]
        return s * sg * v
    pt = lambda o, r: 2 * o + r
    layers, o = [], 0
    for h in profile:
        layers.append(list(range(o, o + h))); o += h
    u = set()
    for o in range(1, t):
        u.add(lit(Z, pt(0, 0), pt(o, 0)))
    for L in layers:
        for i, j in itertools.combinations(L, 2):
            u.add(lit(Z, pt(i, 0), pt(j, 0)))
    for li, L in enumerate(layers):
        if len(L) < 2:
            continue
        verts = [pt(o, 0) for o in L] + [pt(o, 1) for o in L]
        inner = [pt(o, r) for L2 in layers[li + 1:] for o in L2 for r in (0, 1)]
        for k in range(len(verts)):
            a, b = verts[k], verts[(k + 1) % len(verts)]
            for x in verts + inner:
                if x not in (a, b):
                    u.add(lit(a, b, x))
    assert not any(-l in u for l in u), "contradictory layer units"
    return sorted(u, key=abs)


def main():
    if sys.argv[1] == "--list":
        for p in profiles(int(sys.argv[2])):
            print(",".join(map(str, p)))
        return
    mapf, prof, out = sys.argv[1:4]
    info = json.load(open(mapf))
    assert info["kind"] == "rot" and info["m"] == 2
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    profile = tuple(int(x) for x in prof.split(","))
    u = layer_units(tv, info["Z"], info["t"], profile, allow_any="--any" in sys.argv)
    open(out, "w").write("".join(f"{l} 0\n" for l in u))
    print(f"profile {prof}: {len(u)} units")


if __name__ == "__main__":
    main()
