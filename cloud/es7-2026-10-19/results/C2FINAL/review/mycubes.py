#!/usr/bin/env python3
"""Reviewer's own cube generator: hull cubes (136) and second-layer cubes for P1..P8, from base.json.
Literal meaning: chi(p,q,r) = + (r strictly left of p->q). base.json triples: [a,b,c,v,s], a<b<c, chi(a,b,c) = s*x_v.
usage: mycubes.py BASE_JSON RESULTS_DIR"""
import itertools, json, os, sys

info = json.load(open(sys.argv[1])); RES = sys.argv[2]
T, N = info["t"], info["N"]
M = {}
for a, b, c, v, s in info["triples"]:
    M[(a, b, c)] = s * v

def chi_pos(p, q, r):
    """literal asserting chi(p,q,r) = +"""
    trip = [p, q, r]
    srt = sorted(trip)
    # sign of the permutation taking srt to trip
    perm = [srt.index(x) for x in trip]
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
    return (-1) ** inv * M[tuple(srt)]

P = lambda o, r: 2 * o + r
neg = lambda o, r: P(o, 1 - r)

def polygon_cube(verts, others):
    lits = set()
    k = len(verts)
    for i in range(k):
        u, w = verts[i], verts[(i + 1) % k]
        for x in others:
            if x != u and x != w:
                lits.add(chi_pos(u, w, x))
    assert not any(-l in lits for l in lits)
    return lits

def chain_cube(verts, others):
    lits = set()
    for u, w in zip(verts, verts[1:]):
        for x in others:
            if x != u and x != w:
                lits.add(chi_pos(u, w, x))
    assert not any(-l in lits for l in lits)
    return lits

def fmt(name, lits):
    return name + " " + " ".join(str(l) for l in sorted(lits, key=abs)) + "\n"

problems = []
# hull cubes: full polygon (all edges) vs file
hull_lines = open(os.path.join(RES, "C2C34", "cubes.txt")).read().splitlines()
mine = []
full_hull = {}
for a in range(1, T):
    poly = [P(0, 0), P(a, 0), P(0, 1), P(a, 1)]
    full_hull[f"P{a}"] = polygon_cube(poly, range(N))
    half = chain_cube([P(0, 0), P(a, 0), P(0, 1)], range(N))
    # check that the 2-edge description equals the full 4-edge polygon cube (half-turn identification)
    if half != full_hull[f"P{a}"]:
        problems.append(f"P{a}: 2-edge hull cube != 4-edge hull cube ({len(half)} vs {len(full_hull[f'P{a}'])})")
    mine.append(fmt(f"P{a}", full_hull[f"P{a}"]))
for a, b in itertools.combinations(range(1, T), 2):
    poly = [P(0, 0), P(a, 0), P(b, 0), P(0, 1), P(a, 1), P(b, 1)]
    full = polygon_cube(poly, range(N))
    half = chain_cube([P(0, 0), P(a, 0), P(b, 0), P(0, 1)], range(N))
    if half != full: problems.append(f"H{a}-{b}: chain cube != polygon cube")
    mine.append(fmt(f"H{a}-{b}", full))
filelines = [l + "\n" for l in hull_lines if l.strip()]
print("hull cubes: mine", len(mine), "file", len(filelines), "identical:", mine == filelines)
if mine != filelines:
    for x, y in zip(mine, filelines):
        if x != y: print(" first diff:", x[:80], "|", y[:80]); break

# second layer cubes
for a in range(1, 9):
    inner_cls = [o for o in range(1, T) if o != a]
    inner_pts = [P(o, r) for o in inner_cls for r in (0, 1)]
    out = []
    for h in (2, 3):
        for V in itertools.combinations(inner_cls, h):
            poly = [P(o, 0) for o in V] + [P(o, 1) for o in V]
            c2 = polygon_cube(poly, inner_pts)
            cube = full_hull[f"P{a}"] | c2
            assert not any(-l in cube for l in cube)
            nonhull = cube - full_hull[f"P{a}"]
            if not nonhull:
                problems.append(f"P{a} {V}: no non-hull literals")
            out.append(fmt(f"P{a}_" + "-".join(map(str, V)), cube))
    fl = open(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt")).read()
    same = "".join(out) == fl
    print(f"P{a}_cubes.txt: mine {len(out)} lines, identical: {same}; non-hull literal counts:",
          sorted({len(set(map(int, l.split()[1:])) - full_hull[f'P{a}']) for l in out}),
          "hull size", len(full_hull[f"P{a}"]))
    if not same:
        problems.append(f"P{a}_cubes.txt differs")
p8a = open(os.path.join(RES, "C2C34", "p8", "P8_cubes.txt")).read() == open(os.path.join(RES, "C2P", "cubes", "P8_cubes.txt")).read()
print("C2C34/p8/P8_cubes.txt identical to C2P/cubes/P8_cubes.txt:", p8a)
print("PROBLEMS:", problems)
