#!/usr/bin/env python3
"""Random test of layers.py (two-layer split) on exactly mirror-symmetric 33-point integer sets
with an interior axis point.  Each set has a random symmetric convex 4- or 6-gon hull, a
random symmetric convex second layer (3 to 6 vertices, possibly with the axis point as top or
bottom vertex) strictly inside it, and the remaining points strictly inside the second layer.
For each set (y-flipped if X(1,2,3) is false):
 * both layers are recomputed independently (monotone chain) and the spec is read off;
 * the orientations satisfy every orientation-only clause of the CNF;
 * among all layer-2 cubes below the set's own layer-1 case, exactly its own is satisfied,
   and among all 450 layer-1 cubes exactly its layer-1 case is satisfied.
Usage: test_layers.py CNF NSETS SEED
"""
import itertools, json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "../../C/scripts"))
import layers as LY, hullsplit as H, mirlib
from test_split import orient, hull, inside, assign

def symm(pairs, axis=()):
    return list(pairs) + [(-x, y) for x, y in pairs] + list(axis)

def gen(rng, R=10**6):
    while True:
        k1 = rng.choice([1, 2]); hp = [(R, 0)]
        for _ in range(k1): hp.append((rng.randrange(1, R), rng.choice([1, -1]) * rng.randrange(1, R)))
        P1 = symm(hp); h1 = hull(P1)
        if len(h1) != len(P1): continue
        typ = rng.choice(["0A", "1", "1A", "2"])
        k2 = int(typ[0]) + 1; ax = "A" in typ
        for _ in range(1000):
            pp = [(rng.randrange(1, R), rng.randrange(-R, R)) for _ in range(k2)]
            axis = [(0, rng.randrange(-R, R))] if ax else []
            P2 = symm(pp, axis)
            if all(inside(h1, p) for p in P2) and len(hull(P2)) == len(P2): break
        else: continue
        h2 = hull(P2); rest = []; need = 16 - len(hp) - len(pp)
        for _ in range(200000):
            if len(rest) == need: break
            p = (rng.randrange(1, R), rng.randrange(-R, R))
            if inside(h2, p) and inside(h2, (-p[0], p[1])): rest.append(p)
        if len(rest) < need: continue
        axis_pts = axis
        if not ax:
            for _ in range(100000):
                q = (0, rng.randrange(-R, R))
                if inside(h2, q): axis_pts = [q]; break
            else: continue
        P = symm(hp + pp + rest) + axis_pts
        if len(P) != 33 or len(set(abs(p[0]) for p in P)) != 17: continue
        if not mirlib.general_position(P): continue
        return typ, P

def spec_of(Q):
    lab = {p: n + 1 for n, p in enumerate(Q)}; rem = list(Q); out = []
    for t in range(2):
        hv = hull(rem); L = [lab[p] for p in hv]
        p0 = min(L); y0 = Q[p0 - 1][1]; assert Q[34 - p0 - 1][1] == y0
        U = tuple(sorted(l for l in L if l < 17 and Q[l - 1][1] > y0 and l != p0))
        Lo = tuple(sorted(l for l in L if l < 17 and Q[l - 1][1] < y0 and l != p0))
        A = "-"
        if 17 in L: A = "T" if Q[16][1] > y0 else "B"
        assert t == 1 or A == "-"
        out.append((U, Lo, A)); rem = [p for p in rem if p not in hv]
    return out, None

def main():
    cnf, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed); nX = len(H.idx)
    _, _, body = H.read_cnf(cnf)
    xcls = [c for c in (list(map(int, l.split()[:-1])) for l in body) if all(abs(x) <= nX for x in c)]
    l1cases = H.cases(); l1cubes = [H.cube(U, L) for U, L in l1cases]
    sat = lambda X, l: X[abs(l)] == (l > 0)
    rep = {"sets": 0, "flipped": 0, "types": {}, "fail": [], "specs_seen": set()}
    cache = {}
    for t in range(n):
        typ, P = gen(rng)
        Q, X = assign(P)
        if not X[H.idx[(1, 2, 3)]]:
            P = [(x, -y) for x, y in P]; Q, X = assign(P); rep["flipped"] += 1
        sp, _ = spec_of(Q)
        (U1, L1, _), c2 = sp
        if (U1, L1) not in cache:
            subs = LY.sub_cases(U1, L1); cache[(U1, L1)] = (subs, [LY.cube([(U1, L1, "-"), s])[0] for s in subs])
        subs, cubes2 = cache[(U1, L1)]
        ok_x = all(any(sat(X, l) for l in c) for c in xcls)
        h1 = [i for i, c in enumerate(l1cubes) if all(sat(X, l) for l in c)]
        h2 = [i for i, c in enumerate(cubes2) if all(sat(X, l) for l in c)]
        good = ok_x and h1 == [l1cases.index((U1, L1))] and c2 in subs and h2 == [subs.index(c2)]
        if not good: rep["fail"].append({"t": t, "spec": LY.spec(sp), "ok_x": ok_x, "h1": h1, "h2": h2})
        rep["sets"] += 1; rep["types"][typ] = rep["types"].get(typ, 0) + 1; rep["specs_seen"].add(LY.spec(sp))
    rep["distinct_specs"] = len(rep["specs_seen"]); rep["specs_seen"] = sorted(rep["specs_seen"])
    rep["failures"] = len(rep["fail"]); print(json.dumps(rep))

main()
