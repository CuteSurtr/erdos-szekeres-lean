#!/usr/bin/env python3
"""Auditor A5, static checks on the regenerated base and the case-split files (no solver, no geometry).

1. Unit clauses of base.cnf (streamed by base_structure.awk into base_units.txt) = exactly the angular-normal-form
   units I derive from the map: chi(c,(0,0),(o,0)) = + (o = 1..16) and chi(c,(o,0),(o',0)) = + (1 <= o < o' <= 16).
2. The 10,880 three-literal clauses at the end of base.cnf = exactly "(0,0) is not strictly inside a triangle of three
   other points" (my own enumeration), and nothing else in the tail.
3. My reconstruction of the auxiliary-variable numbering gives the header's variable count.
4. My own semantic hull cubes and second-layer cubes (all edges of the ccw polygon, derived from the normal form) equal
   the cube files used by the lanes, as literal sets per case name; every file has the expected names.
5. The orbit files use exactly the map i -> (a - i) mod 17 that I derive for reduction (B); orbit counts.
usage: static_checks.py BASE_CNF BASE_JSON RESULTS_DIR"""
import itertools, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

BASE, MAPF, RES = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))
mp = Map(MAPF)
fails = []
pt = lambda o, r: 2 * o + r

# 1. units
exp_units = set()
for o in range(1, T):
    exp_units.add(mp.lit(Z, pt(0, 0), pt(o, 0)))
for o, o2 in itertools.combinations(range(1, T), 2):
    exp_units.add(mp.lit(Z, pt(o, 0), pt(o2, 0)))
assert not any(-l in exp_units for l in exp_units)
got_units = [int(l.split()[2]) for l in open(os.path.join(HERE, "base_units.txt"))]
print("1. units in base:", len(got_units), "distinct", len(set(got_units)), "expected", len(exp_units),
      "equal" if set(got_units) == exp_units else "DIFFERENT")
if set(got_units) != exp_units or len(got_units) != len(exp_units):
    fails.append("units differ")

# 2. hull clauses (tail of the file)
q0 = pt(0, 0)
exp_h = set()
for a, b, d in itertools.combinations([x for x in range(N) if x != q0], 3):
    for s in (1, -1):
        cl = [-s * mp.lit(a, b, q0), -s * mp.lit(b, d, q0), -s * mp.lit(d, a, q0)]
        if any(-l in cl for l in cl):
            continue                          # tautology: q0 can never be inside such a triangle
        exp_h.add(frozenset(cl))
tail = subprocess.run(["tail", "-n", "10880", BASE], stdout=subprocess.PIPE, check=True).stdout.decode().split("\n")
tail = [l for l in tail if l.strip()]
got_h = [frozenset(int(x) for x in l.split()[:-1]) for l in tail]
print("2. hull clauses in tail:", len(got_h), "all 3-literal", all(len(c) == 3 for c in got_h), "expected", len(exp_h),
      "equal" if set(got_h) == exp_h else "DIFFERENT")
if set(got_h) != exp_h:
    fails.append("hull clauses differ")
# the 32 skipped triangles: which are they?
skipped = []
for a, b, d in itertools.combinations([x for x in range(N) if x != q0], 3):
    cl = [mp.lit(a, b, q0), mp.lit(b, d, q0), mp.lit(d, a, q0)]
    if any(-l in cl for l in cl):
        skipped.append((a, b, d))
print("   triangles whose clause is a tautology:", len(skipped), "all contain an antipodal pair and -q0:",
      all(1 in S and any((x ^ 1) in S for x in S if x != 1) for S in skipped))

# 3. auxiliary numbering
convnum, last = conv_numbering(mp.nX)
print("3. X vars", mp.nX, "+ conv vars", len(convnum), "=", last, "header vars", mp.nv, "OK" if last == mp.nv else "MISMATCH")
if last != mp.nv:
    fails.append("var count")


# 4. cubes
def ccw_vertices(classes):
    cl = sorted(classes)
    return [pt(o, 0) for o in cl] + [pt(o, 1) for o in cl]


def semantic_cube(outer, inner=None):
    """hull polygon of classes `outer` (incl. 0) over all 34 points; optionally inner polygon of classes `inner` over
    the points not in outer classes. All edges of each ccw polygon, all relevant points strictly left."""
    lits = set()
    H = ccw_vertices(outer)
    for k in range(len(H)):
        u, w = H[k], H[(k + 1) % len(H)]
        for q in range(N):
            if q not in (u, w):
                lits.add(mp.lit(u, w, q))
    if inner is not None:
        pts_in = [q for q in range(N) if q // 2 not in outer]
        H2 = ccw_vertices(inner)
        for k in range(len(H2)):
            u, w = H2[k], H2[(k + 1) % len(H2)]
            for q in pts_in:
                if q not in (u, w):
                    lits.add(mp.lit(u, w, q))
    assert 0 not in lits and not any(-l in lits for l in lits)
    return lits


hull, horder = load_cubes(os.path.join(RES, "C2C34", "cubes.txt"))
exp_names = [f"P{a}" for a in range(1, T)] + [f"H{a}-{b}" for a, b in itertools.combinations(range(1, T), 2)]
ok = horder == exp_names
for a in range(1, T):
    ok &= set(hull[f"P{a}"]) == semantic_cube({0, a})
for a, b in itertools.combinations(range(1, T), 2):
    ok &= set(hull[f"H{a}-{b}"]) == semantic_cube({0, a, b})
print("4a. hull cubes (136) equal my semantic cubes:", ok, "sizes P:", sorted({len(hull[f'P{a}']) for a in range(1, T)}),
      "H:", sorted({len(hull[n]) for n in exp_names if n[0] == 'H'}))
if not ok:
    fails.append("hull cubes")
allok = True
for a in range(1, 9):
    cubes, order = load_cubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))
    inner_cls = [o for o in range(1, T) if o != a]
    names = [f"P{a}_" + "-".join(map(str, V)) for h in (2, 3) for V in itertools.combinations(inner_cls, h)]
    good = order == names and len(set(order)) == 560
    nbad = 0
    for h in (2, 3):
        for V in itertools.combinations(inner_cls, h):
            n = f"P{a}_" + "-".join(map(str, V))
            if set(cubes[n]) != semantic_cube({0, a}, set(V)) or len(cubes[n]) != len(set(cubes[n])):
                nbad += 1
            if not set(hull[f"P{a}"]) <= set(cubes[n]):
                nbad += 1
    extra = sorted({len(cubes[n]) - len(hull[f'P{a}']) for n in order})
    print(f"4b. P{a}_cubes.txt: names as expected {good}; cubes differing from my semantic cubes {nbad}; "
          f"second-layer literal counts {extra}")
    allok &= good and nbad == 0
if not allok:
    fails.append("l2 cubes")
# the pilot cube file
cubes8, order8 = load_cubes(os.path.join(RES, "C2C34", "p8", "P8_cubes.txt"))
c8, o8 = load_cubes(os.path.join(RES, "C2P", "cubes", "P8_cubes.txt"))
print("4c. pilot P8_cubes.txt identical to C2P/cubes/P8_cubes.txt (as data):", cubes8 == c8 and order8 == o8)

# 5. orbits
for a in range(1, 9):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(RES, "C2P", "orbits", f"P{a}.tsv"))][1:]
    rep = dict(rows)
    key = lambda s: tuple(int(x) for x in s.split("_")[1].split("-"))
    bad = 0
    fixed = 0
    for n in rep:
        V = key(n)
        W = tuple(sorted((a - i) % T for i in V))
        m = f"P{a}_" + "-".join(map(str, W))
        if m not in rep:
            bad += 1
            continue
        if rep[n] != min(n, m, key=key) or rep[m] != rep[n]:
            bad += 1
        if m == n:
            fixed += 1
    norb = len(set(rep.values()))
    print(f"5. P{a}: subcases {len(rep)}, orbits {norb}, fixed {fixed}, rows inconsistent with i -> ({a} - i) mod 17: {bad}")
    if bad or len(rep) != 560 or norb != 287 or fixed != 14:
        fails.append(f"orbits P{a}")
print("FAILURES", fails)
