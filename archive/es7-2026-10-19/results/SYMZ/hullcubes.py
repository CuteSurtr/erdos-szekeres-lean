#!/usr/bin/env python3
"""Hull case split for the centrally symmetric zcnf CNF with --hull (rot, m = 2): (0,0) is a hull vertex, and the
representatives (o,0), o >= 1, lie in the open half-plane left of c -> (0,0), sorted by angle. The hull of a centrally
symmetric set without 7 points in convex position has 4 or 6 vertices, (0,0) and (0,1) among them, so its other
vertices are (a,0), (a,1) (parallelogram, 1 <= a < t) or (a,0), (b,0), (a,1), (b,1) (hexagon, 1 <= a < b < t), in this
counter-clockwise order. The cube of a case says that every point not on an edge lies strictly left of that edge, for the
edges (0,0)->(a,0)->(0,1) or (0,0)->(a,0)->(b,0)->(0,1) (the other edges are their images under the half-turn).
Writes cubes.txt (one line per case: name and literals) and cover.cnf = CNF plus the negation of every cube
(it must be UNSAT for the cases to cover the CNF).
usage: hullcubes.py CNF MAP OUTDIR"""
import itertools, json, os, sys

cnf, mapf, outdir = sys.argv[1:4]
info = json.load(open(mapf))
assert info["kind"] == "rot" and info["m"] == 2
t, N = info["t"], info["N"]
tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}

def parity_sort(x):
    a, b, c = x
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(x)), (-1 if inv & 1 else 1)

def lit(a, b, c):
    S, s = parity_sort((a, b, c))
    v, sg = tv[S]
    return s * sg * v

pt = lambda o, r: 2 * o + r
cases = []
for a in range(1, t):
    cases.append((f"P{a}", [pt(0, 0), pt(a, 0), pt(0, 1)]))
for a, b in itertools.combinations(range(1, t), 2):
    cases.append((f"H{a}-{b}", [pt(0, 0), pt(a, 0), pt(b, 0), pt(0, 1)]))
os.makedirs(outdir, exist_ok=True)
cubes = []
for name, chain in cases:
    lits = set()
    for u, w in zip(chain, chain[1:]):
        for q in range(N):
            if q not in (u, w):
                lits.add(lit(u, w, q))
    assert not any(-l in lits for l in lits)
    cubes.append((name, sorted(lits, key=abs)))
with open(os.path.join(outdir, "cubes.txt"), "w") as f:
    for name, lits in cubes:
        f.write(name + " " + " ".join(map(str, lits)) + "\n")
lines = open(cnf).read().split("\n")
hdr = next(i for i, l in enumerate(lines) if l.startswith("p cnf"))
_, _, nv, nc = lines[hdr].split()
with open(os.path.join(outdir, "cover.cnf"), "w") as f:
    f.write(f"p cnf {nv} {int(nc) + len(cubes)}\n")
    f.write("\n".join(l for l in lines[hdr + 1:] if l))
    f.write("\n")
    for name, lits in cubes:
        f.write(" ".join(str(-l) for l in lits) + " 0\n")
print(len(cubes), "cases written to", outdir)
