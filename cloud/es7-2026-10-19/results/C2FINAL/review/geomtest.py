#!/usr/bin/env python3
"""Reviewer's exact-integer test of cube semantics and reductions A and B on real centrally symmetric 34-point sets.
usage: geomtest.py BASE_JSON RESULTS_DIR NSETS SEED"""
import itertools, json, os, random, sys
from collections import Counter

info = json.load(open(sys.argv[1])); RES = sys.argv[2]; NS = int(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
T, N, Z = 17, 34, 34
trip = info["triples"]

def readcubes(p):
    return [(l.split()[0], [int(x) for x in l.split()[1:]]) for l in open(p) if l.strip()]
hull_cubes = readcubes(os.path.join(RES, "C2C34", "cubes.txt"))
l2 = {a: readcubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt")) for a in range(1, 9)}

def orient(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (d > 0) - (d < 0)

def assignment(lab):
    """lab: list of 35 points (index 2o+r, then Z=centre at index 34). Returns dict var->bool, or raises on inconsistency."""
    val = {}
    for a, b, c, v, s in trip:
        o = orient(lab[a], lab[b], lab[c])
        assert o != 0, ("zero on nonzero triple", a, b, c)
        x = (s * o) > 0
        if v in val and val[v] != x:
            raise ValueError(f"identification inconsistent at var {v}")
        val[v] = x
    return val

def sat_cube(val, lits):
    return all(val[abs(l)] == (l > 0) for l in lits)

def normal_form(P, start):
    """P: list of 17 representative points p (antipodes -p). start: a point of the set that is a hull vertex.
    Returns the labelled list of 35 points."""
    origin = (0, 0)
    pts = [p for p in P] + [(-p[0], -p[1]) for p in P]
    others = [q for q in pts if q != start and q != (-start[0], -start[1])]
    left = [q for q in others if orient(origin, start, q) > 0]
    assert len(left) == 16
    # sort by angle ccw from start: q before q2 iff orient(c, q, q2) > 0 (all within an open half-plane)
    import functools
    left.sort(key=functools.cmp_to_key(lambda q, q2: -orient(origin, q, q2)))
    lab = [None] * 35
    lab[0], lab[1] = start, (-start[0], -start[1])
    for i, q in enumerate(left, 1):
        lab[2 * i], lab[2 * i + 1] = q, (-q[0], -q[1])
    lab[34] = origin
    return lab

def hull_vertices(pts):
    pts = sorted(set(pts))
    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo, up = half(pts), half(pts[::-1])
    return lo[:-1] + up[:-1]

def geometry_case(lab):
    """true hull case and second-layer class set from geometry, in labelling lab"""
    idx = {lab[i]: i for i in range(34)}
    hv = hull_vertices(lab[:34])
    hcls = sorted({idx[p] // 2 for p in hv})
    inner = [lab[i] for i in range(34) if i // 2 not in hcls]
    iv = hull_vertices(inner)
    icls = sorted({idx[p] // 2 for p in iv})
    return hcls, icls

def gen():
    while True:
        h1 = (rng.randint(900, 1100), rng.randint(-150, 150)); h2 = (rng.randint(-150, 150), rng.randint(900, 1100))
        mode = rng.random()
        P = [h1, h2]
        if mode < 0.5:   # nested quadrilateral second layer
            g1 = (rng.randint(400, 500), rng.randint(-60, 60)); g2 = (rng.randint(-60, 60), rng.randint(400, 500))
            P += [g1, g2]
            while len(P) < 17: P.append((rng.randint(-150, 150), rng.randint(-150, 150)))
        else:            # random inner points
            while len(P) < 17: P.append((rng.randint(-350, 350), rng.randint(-350, 350)))
        pts = P + [(-x, -y) for x, y in P]
        if len(set(pts)) < 34 or (0, 0) in pts: continue
        if any(orient(p, q, r) == 0 for p, q, r in itertools.combinations(pts, 3)): continue
        if len(hull_vertices(pts)) != 4: continue
        return P

stats = Counter(); fails = []
for k in range(NS):
    P = gen()
    pts = P + [(-x, -y) for x, y in P]
    hv = hull_vertices(pts)
    for start in hv:
        lab = normal_form(P, start)
        val = assignment(lab)
        # SB units: chi(c,(0,0),(o,0)) = + ; chi(c,(o,0),(o2,0)) = + ; hull SB: geometric (start is a hull vertex)
        hcls, icls = geometry_case(lab)
        assert hcls[0] == 0 and len(hcls) == 2
        a = hcls[1]
        sat_h = [n for n, lits in hull_cubes if sat_cube(val, lits)]
        if sat_h != [f"P{a}"]: fails.append(("hull", sat_h, a)); continue
        stats["hull ok"] += 1
        # reduction A: restarting at (a,0) gives case 17-a
        labA = normal_form(P, lab[2 * a]) if False else normal_form([lab[2 * o] for o in range(17)], lab[2 * a])
        hA, _ = geometry_case(labA)
        if hA[1] != 17 - a: fails.append(("A", a, hA))
        else: stats["A ok"] += 1
        if a > 8: continue
        sat_l2 = [n for n, lits in l2[a] if sat_cube(val, lits)]
        geoV = f"P{a}_" + "-".join(map(str, icls))
        if len(icls) in (2, 3):
            if sat_l2 != [geoV]: fails.append(("l2", a, sat_l2, geoV)); continue
            stats[f"l2 ok h={len(icls)}"] += 1
            # reduction B: mirror (x -> -x), restart at the image of (a,0)
            M = [(-x, y) for x, y in (lab[2 * o] for o in range(17))]
            labB = normal_form(M, (-lab[2 * a][0], lab[2 * a][1]))
            valB = assignment(labB)
            hB, iB = geometry_case(labB)
            pred = sorted((a - i) % 17 for i in icls)
            satB = [n for n, lits in l2[a] if sat_cube(valB, lits)]
            if hB != [0, a] or iB != pred or satB != [f"P{a}_" + "-".join(map(str, pred))]:
                fails.append(("B", a, icls, hB, iB, pred, satB))
            else: stats["B ok"] += 1
        else:
            if sat_l2: fails.append(("l2 none expected", a, sat_l2, icls))
            else: stats["l2 none ok"] += 1
print(dict(stats)); print("fails:", len(fails), fails[:5])
