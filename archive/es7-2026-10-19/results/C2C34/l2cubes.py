#!/usr/bin/env python3
"""Second-layer cubes for a quadrilateral-hull case P_a of the central 34-point formula (zcnf.py rot 17 7 --m 2 --hull,
angular normal form). In P_a the hull is (0,0), (a,0), (0,1), (a,1). The remaining 15 pairs are inside; their hull (the
second layer) is a centrally symmetric quadrilateral or hexagon, so its vertex classes V2 are 2 or 3 of the remaining
classes. With the representatives (o,0), o >= 1, sorted by angle in the open half-plane left of c -> (0,0), the second
layer has the vertices (v_1,0), ..., (v_h,0), (v_1,1), ..., (v_h,1) in counter-clockwise order (v_1 < ... < v_h).
The cube of (a, V2) is the hull cube of P_a plus: for every edge u -> w of the second layer, every other point of the
inner 30 lies strictly left of it.
usage: l2cubes.py MAP.json A OUT   (writes one line per V2: name and literals)"""
import itertools, json, sys


def parity_sort(x):
    a, b, c = x
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(x)), (-1 if inv & 1 else 1)


def main():
    mapf, A, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    info = json.load(open(mapf))
    t, N = info["t"], info["N"]
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    def lit(a, b, c):
        S, s = parity_sort((a, b, c)); v, sg = tv[S]; return s * sg * v
    pt = lambda o, r: 2 * o + r
    hull = [pt(0, 0), pt(A, 0), pt(0, 1), pt(A, 1)]
    hcube = set()
    for k in range(4):
        u, w = hull[k], hull[(k + 1) % 4]
        for q in range(N):
            if q not in (u, w): hcube.add(lit(u, w, q))
    inner_cls = [o for o in range(1, t) if o != A]
    inner = [pt(o, r) for o in inner_cls for r in (0, 1)]
    with open(out, "w") as f:
        for h in (2, 3):
            for V in itertools.combinations(inner_cls, h):
                verts = [pt(o, 0) for o in V] + [pt(o, 1) for o in V]
                cube = set(hcube)
                for k in range(len(verts)):
                    u, w = verts[k], verts[(k + 1) % len(verts)]
                    for x in inner:
                        if x not in (u, w): cube.add(lit(u, w, x))
                assert not any(-l in cube for l in cube)
                f.write(f"P{A}_{'-'.join(map(str, V))} " + " ".join(map(str, sorted(cube, key=abs))) + "\n")


if __name__ == "__main__":
    main()
