#!/usr/bin/env python3
"""Second-layer cubes for sgn.py --sym --par (n points, inner pairs {p_i, p_{n+1-i}}, 3 <= i <= n/2).
The inner n-4 points have a centrally symmetric convex hull with 4 or 6 vertices (8 would give a convex 7-gon). A cube
fixes the vertex pairs and their counter-clockwise order v_1, ..., v_h, -v_1, ..., -v_h and says that every other inner
point lies strictly left of each edge. Quadrilaterals: pairs {i, j}, orders (i, j) and (i, n+1-j); hexagons: pairs
{i, j, k}, v_1 = p_i, v_2 any point of the other two pairs, v_3 either point of the remaining pair. Cubes with
contradictory literals are dropped (no labelling realizes them). Writes "name lits" lines and a cover CNF
(base + one clause per cube: some cube literal fails).
usage: l2sgn.py BASE.cnf MAP.json n OUT.cubes OUT_cover.cnf"""
import itertools, json, sys
base, mapf, n, outc, outv = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
mp = json.load(open(mapf)); ov = {(i, j, k): v for i, j, k, v in mp["triples"]}
def o(i, j, k):
    t = (i, j, k); m = (n + 1 - k, n + 1 - j, n + 1 - i)
    return ov[t] if t in ov else -ov[m]
def chi(a, b, c):
    t = tuple(sorted((a, b, c))); inv = (a > b) + (a > c) + (b > c); l = o(*t)
    return l if inv % 2 == 0 else -l
inner = list(range(3, n - 1)); A = lambda p: n + 1 - p
cubes = []
def add(name, verts):
    h = len(verts); cyc = verts + [A(v) for v in verts]; lits = set()
    for e in range(2 * h):
        u, w = cyc[e], cyc[(e + 1) % (2 * h)]
        for x in inner:
            if x not in (u, w): lits.add(chi(u, w, x))
    if any(-l in lits for l in lits): return
    cubes.append((name, sorted(lits, key=abs)))
pairs = list(range(3, n // 2 + 1))
for i, j in itertools.combinations(pairs, 2):
    add(f"Q{i}.{j}", [i, j]); add(f"Q{i}.{A(j)}", [i, A(j)])
for i, j, k in itertools.combinations(pairs, 3):
    for a, b in ((j, k), (k, j)):
        for v2 in (a, A(a)):
            for v3 in (b, A(b)):
                add(f"H{i}.{v2}.{v3}", [i, v2, v3])
with open(outc, "w") as f:
    for name, lits in cubes: f.write(name + " " + " ".join(map(str, lits)) + "\n")
hdr = None; body = []
with open(base) as f, open(outv, "w") as g:
    for line in f:
        if line.startswith("p cnf"):
            _, _, nv, nc = line.split(); g.write(f"p cnf {nv} {int(nc) + len(cubes)}\n")
        else: g.write(line)
    for name, lits in cubes: g.write(" ".join(str(-l) for l in lits) + " 0\n")
nq = sum(1 for c in cubes if c[0][0] == "Q"); print(json.dumps({"cubes": len(cubes), "quadrilateral": nq, "hexagonal": len(cubes) - nq}))
