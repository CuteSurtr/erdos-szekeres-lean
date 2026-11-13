#!/usr/bin/env python3
"""Next-layer cubes for sgn.py --sym --par. Given a cube name for the current layers (as written by l2sgn.py / this
script: layers separated by '/', each 'Q<v1>.<v2>' or 'H<v1>.<v2>.<v3>' listing the counter-clockwise vertices v_1..v_h,
the antipodes following), the remaining points R are the inner points not on those layers. The next layer is the convex
hull of R: centrally symmetric with 4 or 6 vertices, and its leftmost point min(R) is a vertex, so v_1 = min(R). Its cube
says every other point of R is strictly left of each edge. Prints "name lits" for every child (prefix cube included).
usage: l3sgn.py MAP.json n CUBEFILE NAME [NAME...] > OUT"""
import itertools, json, sys
mapf, n, cf = sys.argv[1], int(sys.argv[2]), sys.argv[3]; names = sys.argv[4:]
mp = json.load(open(mapf)); ov = {(i, j, k): v for i, j, k, v in mp["triples"]}
cubes = {l.split()[0]: l.split()[1:] for l in open(cf)}
def o(i, j, k):
    t = (i, j, k); m = (n + 1 - k, n + 1 - j, n + 1 - i)
    return ov[t] if t in ov else -ov[m]
def chi(a, b, c):
    t = tuple(sorted((a, b, c))); inv = (a > b) + (a > c) + (b > c); l = o(*t)
    return l if inv % 2 == 0 else -l
A = lambda p: n + 1 - p
def layer_lits(verts, R):
    h = len(verts); cyc = verts + [A(v) for v in verts]; lits = set()
    for e in range(2 * h):
        u, w = cyc[e], cyc[(e + 1) % (2 * h)]
        for x in R:
            if x not in (u, w): lits.add(chi(u, w, x))
    return lits
for name in names:
    used = set()
    for layer in name.split("/"):
        for v in layer[1:].split("."):
            used |= {int(v), A(int(v))}
    R = [x for x in range(3, n - 1) if x not in used]
    if len(R) < 4: continue
    first = min(R); others = sorted({min(x, A(x)) for x in R} - {first})
    prefix = set(int(x) for x in cubes[name])
    kids = []
    for j in others:
        for v2 in (j, A(j)): kids.append(("Q", [first, v2]))
    for j, k in itertools.combinations(others, 2):
        for a, b in ((j, k), (k, j)):
            for v2 in (a, A(a)):
                for v3 in (b, A(b)): kids.append(("H", [first, v2, v3]))
    for t, verts in kids:
        lits = prefix | layer_lits(verts, R)
        if any(-l in lits for l in lits): continue
        print(f"{name}/{t}{'.'.join(map(str, verts))} " + " ".join(map(str, sorted(lits, key=abs))))
