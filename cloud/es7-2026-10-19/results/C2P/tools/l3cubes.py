#!/usr/bin/env python3
"""Third-layer cubes for a second-layer subcase (P_a, V2) of the central 34-point formula (zcnf.py rot 17 7 --m 2
--hull), as l2cubes.py does one layer up.

In subcase (P_a, V2) the hull classes are 0 and a and the second layer has the vertex classes V2. The remaining 13
classes (26 points) have a centrally symmetric convex hull, the third layer, with 4 or 6 vertices (8 would be a convex
7-gon). Its vertex classes W are 2 or 3 of the remaining classes. With the representatives (o, 0) sorted by angle
around c, its vertices in counter-clockwise order are (w_1, 0), ..., (w_h, 0), (w_1, 1), ..., (w_h, 1) (w_1 < ... < w_h).
The cube of (a, V2, W) is the cube of (a, V2) plus: for every edge u -> w of the third layer, every other point of
those 26 lies strictly left of it.
The cover of the split is the base plus the units of (a, V2) plus one clause per W forbidding its third-layer literals.
usage: l3cubes.py MAP.json L2CUBES.txt SUBCASE OUT   (SUBCASE as in L2CUBES, for example P8_3-11; OUT: name and literals
       per line, names SUBCASE/W, e.g. P8_3-11/2-5-9)"""
import itertools, json, sys


def parity_sort(x):
    a, b, c = x
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(x)), (-1 if inv & 1 else 1)


def main():
    mapf, l2f, sub, out = sys.argv[1:5]
    info = json.load(open(mapf))
    t = info["t"]
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    def lit(a, b, c):
        S, s = parity_sort((a, b, c)); v, sg = tv[S]; return s * sg * v
    pt = lambda o, r: 2 * o + r
    l2 = next([int(x) for x in l.split()[1:]] for l in open(l2f) if l.split(" ", 1)[0] == sub)
    A = int(sub.split("_")[0][1:]); V2 = [int(x) for x in sub.split("_")[1].split("-")]
    rest = [o for o in range(1, t) if o != A and o not in V2]
    pts = [pt(o, r) for o in rest for r in (0, 1)]
    n = 0
    with open(out, "w") as f:
        for h in (2, 3):
            for W in itertools.combinations(rest, h):
                verts = [pt(o, 0) for o in W] + [pt(o, 1) for o in W]
                cube = set(l2)
                for k in range(len(verts)):
                    u, w = verts[k], verts[(k + 1) % len(verts)]
                    for x in pts:
                        if x not in (u, w): cube.add(lit(u, w, x))
                if any(-l in cube for l in cube):
                    continue          # contradictory: no labelling realizes it (kept out of the cover as well)
                f.write(f"{sub}/{'-'.join(map(str, W))} " + " ".join(map(str, sorted(cube, key=abs))) + "\n"); n += 1
    print(json.dumps({"subcase": sub, "remaining_classes": len(rest), "cubes": n}))


if __name__ == "__main__":
    main()
