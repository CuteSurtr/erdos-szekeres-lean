#!/usr/bin/env python3
"""Soundness test of zcnf.py on a real symmetric set with integer coordinates.
  rot m=2: half-turn about the origin; rot m=4: (x, y) -> (-y, x); mirror: (x, y) -> (-x, y), no point on the y-axis.
Computes the chirotope of the set plus Z exactly (Z = origin for rot, the direction (1, 0) at infinity for mirror),
labels the set in zcnf's normal form, checks that the zero triples are exactly {Z, p, tau p} and that every class of
identified triples has one consistent value on the real set, and writes the class values as unit clauses.
usage: zvalidate.py rot|mirror M POINTS MAP OUT_UNITS [--swap] [--hull | --nothull]
(--swap: deliberately wrong orbit order; --hull: (0,0) a hull vertex; --nothull: (0,0) deliberately not one)"""
import json, sys
from functools import cmp_to_key
from itertools import combinations

kind, m, pts_path, map_path, out_path = sys.argv[1], int(sys.argv[2]), *sys.argv[3:6]
swap = "--swap" in sys.argv
hull = "--hull" in sys.argv
nothull = "--nothull" in sys.argv
P = [tuple(map(int, l.split()[:2])) for l in open(pts_path) if l.strip() and not l.startswith(("#", "FOUND"))]
Pset = set(P)
if kind == "rot":
    R = (lambda p: (-p[0], -p[1])) if m == 2 else (lambda p: (-p[1], p[0]))
    assert m in (2, 4)
else:
    R = lambda p: (-p[0], p[1])
    m = 2
assert all(R(p) in Pset for p in P) and len(Pset) == len(P)

def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))
hom = lambda p: (1, p[0], p[1])
Zvec = (1, 0, 0) if kind == "rot" else (0, 1, 0)
def chi(a, b, c):
    d = det3(a, b, c); return (d > 0) - (d < 0)
assert not any(chi(hom(a), hom(b), hom(c)) == 0 for a, b, c in combinations(P, 3)), "not in general position"
# orbits
orbits, seen = [], set()
for p in P:
    if p in seen: continue
    orb = [p]
    while R(orb[-1]) != p: orb.append(R(orb[-1]))
    assert len(orb) == m or (kind == "mirror" and len(orb) == 1)
    seen.update(orb); orbits.append(orb)
axpts = sorted([o[0] for o in orbits if len(o) == 1], key=lambda q: -q[1])   # mirror: points on the axis, top first
orbits = [o for o in orbits if len(o) == m]
t = len(orbits)
Z = (1, 0, 0)
if kind == "rot":
    p00 = orbits[0][0]
    if hull or nothull:
        def is_vertex(d):
            R_ = [q for q in P if q != d]
            return not any(chi(hom(a), hom(b), hom(d)) == chi(hom(b), hom(c), hom(d)) == chi(hom(c), hom(a), hom(d))
                           for a, b, c in combinations(R_, 3))
        p00 = min(P) if hull else next(q for q in P if not is_vertex(q))
        assert is_vertex(p00) == hull
        k0 = next(i for i, o in enumerate(orbits) if p00 in o)
        orbits[0], orbits[k0] = orbits[k0], orbits[0]
    def rep(orb):
        c = [q for q in orb if chi(Z, hom(p00), hom(q)) > 0 and (m == 2 or chi(Z, hom(R(p00)), hom(q)) < 0)]
        assert len(c) == 1, c; return c[0]
    reps = [p00] + [rep(o) for o in orbits[1:]]
    rest = list(range(1, t))
    rest.sort(key=cmp_to_key(lambda i, j: -1 if chi(Z, hom(reps[i]), hom(reps[j])) > 0 else 1))
    order = [0] + rest
else:
    lefts = [min(o) for o in orbits]                       # x < 0 first
    assert all(q[0] < 0 for q in lefts)
    order = sorted(range(t), key=lambda i: -lefts[i][1])   # top to bottom
    reps = lefts
if swap:
    k = 1 if kind == "rot" else 0
    order[k], order[k + 1] = order[k + 1], order[k]
lab = {}
for o, i in enumerate(order):
    q = reps[i]
    for r in range(m):
        lab[o * m + r] = hom(q); q = R(q)
for j, q in enumerate(axpts):
    lab[t * m + j] = hom(q)
info = json.load(open(map_path))
assert info["t"] == t and info["m"] == m and info["kind"] == kind and info.get("axis", 0) == len(axpts), (info["t"], t)
Zi = info["Z"]; lab[Zi] = Zvec
N = t * m + len(axpts)
NP = t * m
tau = lambda i: (i // m) * m + (i % m + m // 2) % m
val, nz = {}, 0
listed = {(a, b, c) for a, b, c, v, s in info["triples"]}
for a, b, c in combinations(range(N + 1), 3):
    x = chi(lab[a], lab[b], lab[c])
    expect_zero = False
    if Zi in (a, b, c):
        u, w = [y for y in (a, b, c) if y != Zi]
        expect_zero = u < NP and w < NP and tau(u) == w
    assert (x == 0) == expect_zero, ("zero pattern", a, b, c, x)
    assert ((a, b, c) in listed) == (x != 0)
for a, b, c, v, s in info["triples"]:
    x = chi(lab[a], lab[b], lab[c]) * s
    if v in val:
        assert val[v] == x, ("identity violated on the real set", a, b, c)
    else:
        val[v] = x
assert len(val) == info["X_vars"]
open(out_path, "w").write("".join(f"{v if x > 0 else -v} 0\n" for v, x in sorted(val.items())))
print(f"{kind} m={m} t={t}: zero pattern ok, identities consistent on the real set, wrote {len(val)} units"
      + (" (labelling deliberately wrong)" if swap else ""))
