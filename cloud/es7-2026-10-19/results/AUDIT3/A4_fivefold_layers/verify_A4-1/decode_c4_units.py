#!/usr/bin/env python3
"""Decode the 142 unit clauses of the certificate base CNF c4_n32L.cnf (sha c3933d9a...) through the variable map
c4_n32L.json (sha f72b186e...), without using the encoder, and classify them.  Then check, with exact integer
geometry, that the 14 sector units say exactly 'every (o,0), o = 1..7, lies in the open quadrant counter-clockwise
from (0,0)', and that the units equal those produced by symcnf_layers.LayerEncoding(32, 7, 4).add_sb().
usage: decode_c4_units.py UNITS_TXT MAP_JSON"""
import json, os, sys, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

units = [int(l.split()[0]) for l in open(sys.argv[1]) if l.strip()]
assert all(l.split()[1] == "0" for l in open(sys.argv[1]) if l.strip())
mp = json.load(open(sys.argv[2]))
assert mp["N"] == 32 and mp["m"] == 4 and mp["center"] == "none"
byvar = {}
for a, b, c, v, s in mp["triples"]:
    byvar.setdefault(v, []).append((a, b, c, s))

m, t = 4, 8
O = lambda i: divmod(i, m)          # label -> (orbit, r)


def parity(x, y, z):
    inv = (x > y) + (x > z) + (y > z)
    return -1 if inv & 1 else 1


# a unit L asserts chi(a,b,c) = sign(L) * s for every map row (a,b,c,v=|L|,s), (a,b,c) sorted
def asserted(L, a, b, c):
    """asserted sign of chi(a,b,c) (any order) by unit literal L, via the map row of the sorted triple"""
    S = tuple(sorted((a, b, c)))
    for (x, y, z, s) in byvar[abs(L)]:
        if (x, y, z) == S:
            return (1 if L > 0 else -1) * s * parity(a, b, c)
    return None


sector, polygon, nesting, other = [], [], [], []
for L in units:
    found = None
    # sector: chi((0,j),(0,j+2),(o,0)), j = 0,1, o >= 1
    for o in range(1, t):
        for j in (0, 1):
            s = asserted(L, j, j + 2, 4 * o)
            if s is not None:
                found = ("sector", o, j, s)
    if found is None:
        for o in range(t):
            for k in range(2, m):
                s = asserted(L, 4 * o, 4 * o + 1, 4 * o + k)
                if s is not None:
                    found = ("polygon", o, k, s)
            for o2 in range(o + 1, t):
                for r in range(m):
                    s = asserted(L, 4 * o, 4 * o + 1, 4 * o2 + r)
                    if s is not None and found is None:
                        found = ("nesting", o, (o2, r), s)
    {"sector": sector, "polygon": polygon, "nesting": nesting}.get(found[0] if found else None, other).append((L, found))
print(f"units: {len(units)}  sector {len(sector)}  polygon {len(polygon)}  nesting {len(nesting)}  other {len(other)}")
assert len(units) == 142 and not other
sec = {(f[1], f[2]): f[3] for _, f in sector}
assert sorted(sec) == [(o, j) for o in range(1, 8) for j in (0, 1)]
assert all(sec[(o, 0)] == -1 and sec[(o, 1)] == +1 for o in range(1, 8))
assert all(f[3] == +1 for _, f in polygon + nesting)
print("sector units: chi((0,0),(0,2),(o,0)) = -1 and chi((0,1),(0,3),(o,0)) = +1 for o = 1..7 (from the map, not the encoder)")

# exact meaning: with (0,0)=(X,Y), (0,1)=(-Y,X), (0,2)=(-X,-Y), (0,3)=(Y,-X) about c=0, a point p satisfies both signs
# iff det(c,(0,0),p) > 0 and det(c,p,(0,1)) > 0 (open quadrant).  Exhaustive over a grid, two different (0,0).
det = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
sg = lambda x: (x > 0) - (x < 0)
for X, Y in ((5, 0), (7, 3), (-2, 9)):
    o0 = [(X, Y), (-Y, X), (-X, -Y), (Y, -X)]
    for x in range(-30, 31):
        for y in range(-30, 31):
            p = (x, y)
            if p == (0, 0):
                continue
            units_hold = sg(det(o0[0], o0[2], p)) == -1 and sg(det(o0[1], o0[3], p)) == +1
            quadrant = det((0, 0), o0[0], p) > 0 and det((0, 0), p, o0[1]) > 0
            assert units_hold == quadrant, (X, Y, p)
print("exact: the two sector signs hold  <=>  p in the open quadrant (0, pi/2) ccw from (0,0)  [61x61 grid, 3 frames]")

from symcnf_layers import LayerEncoding
enc = LayerEncoding(32, 7, 4, body=None)
enc.stats = {}
enc.add_sb()
gen = [cl[0] for cl in enc.clauses.mem]
assert all(len(cl) == 1 for cl in enc.clauses.mem)
print("encoder add_sb units == CNF units (as a sequence):", gen == units, "| as a set:", set(gen) == set(units))
assert gen == units
