#!/usr/bin/env python3
"""Random test of the hull-pair split (hullsplit.py) on exactly mirror-symmetric 33-point
integer sets with the axis point strictly inside the hull.

Positive sets: a random convex 4- or 6-gon hull made of mirror pairs ((±R,0) plus 1-2 pairs),
filled with 14-15 random interior pairs and an interior axis point.  For each set:
 * exact general position, distinct x, mirror symmetry;
 * if X(1,2,3) is false, the set is reflected in the x-axis (the WLOG y-flip of the CNF);
 * the hull is recomputed independently (Andrew's monotone chain, exact ints) and the case
   (U, L) is read off from it;
 * the set's orientations satisfy every orientation-only clause of the CNF;
 * among all 450 cubes, exactly the cube of its own case is satisfied.
Uniform sets (mirlib.mirror_set 'interior'): no cube is satisfied if the hull has more than
6 vertices; otherwise exactly the cube of the case read off from the hull.
Usage: test_split.py CNF NPOS NNEG SEED
"""
import itertools, json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../C/scripts"))
import hullsplit as H
import mirlib

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def hull(P):
    P = sorted(P); lo = []; up = []
    for p in P:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]   # ccw, starting at leftmost

def inside(poly, p):
    m = len(poly)
    return all(orient(poly[t], poly[(t+1) % m], p) > 0 for t in range(m))

def pos_set(rng, R=10**6):
    typ = rng.choice(["1U", "1L", "2U", "2L", "1U1L"])
    while True:
        hp = [(R, 0)]
        nu = typ.count("U") and int(typ[typ.index("U")-1])
        nl = typ.count("L") and int(typ[typ.index("L")-1])
        for s, n in ((1, nu), (-1, nl)):
            for _ in range(n):
                hp.append((rng.randrange(1, R), s * rng.randrange(1, R)))
        pts = hp + [(-x, y) for x, y in hp]
        hv = hull(pts)
        if len(hv) != len(pts): continue
        npairs_in = 16 - len(hp)
        ins = []
        tries = 0
        while len(ins) < npairs_in and tries < 100000:
            tries += 1
            p = (rng.randrange(1, R), rng.randrange(-R, R))
            if inside(hv, p) and inside(hv, (-p[0], p[1])): ins.append(p)
        if len(ins) < npairs_in: continue
        ay = None
        for _ in range(100000):
            q = (0, rng.randrange(-R, R))
            if inside(hv, q): ay = q; break
        if ay is None: continue
        P = pts + ins + [(-x, y) for x, y in ins] + [ay]
        xs = [abs(p[0]) for p in P]
        if len(set(xs)) != 17: continue
        if not mirlib.general_position(P): continue
        return typ, P

def assign(P):
    Q = sorted(P)
    X = {}
    for t in itertools.combinations(range(33), 3):
        v = orient(Q[t[0]], Q[t[1]], Q[t[2]]); assert v != 0
        X[H.idx[(t[0]+1, t[1]+1, t[2]+1)]] = v > 0
    return Q, X

def case_of(Q):
    hv = hull(Q); lab = {p: n + 1 for n, p in enumerate(Q)}
    y0 = Q[0][1]; assert Q[-1][1] == y0
    U = sorted(lab[p] for p in hv if p[1] > y0 and lab[p] <= 16)
    L = sorted(lab[p] for p in hv if p[1] < y0 and lab[p] <= 16)
    assert 17 not in [lab[p] for p in hv]
    return tuple(U), tuple(L), [lab[p] for p in hv]

def main():
    cnf, npos, nneg, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    nX = len(H.idx)
    _, _, body = H.read_cnf(cnf)
    xcls = []
    for line in body:
        c = list(map(int, line.split()[:-1]))
        if all(abs(l) <= nX for l in c): xcls.append(c)
    cs = H.cases(); cubes = [H.cube(U, L) for U, L in cs]
    sat = lambda X, l: X[abs(l)] == (l > 0)
    rep = {"positive": 0, "flipped": 0, "types": {}, "cases_seen": set(), "fail": [], "neg": 0, "neg_fail": 0, "neg_smallhull": 0,
           "xonly_clauses": len(xcls)}
    for n in range(npos):
        typ, P = pos_set(rng)
        Q, X = assign(P)
        if not X[H.idx[(1, 2, 3)]]:
            P = [(x, -y) for x, y in P]; Q, X = assign(P); rep["flipped"] += 1
        assert X[H.idx[(1, 2, 3)]]
        for (i, j, k), v in H.idx.items():
            assert X[v] == X[H.idx[tuple(sorted((34-k, 34-j, 34-i)))]]
        U, L, hl = case_of(Q)
        assert hl == H.hull_ccw(U, L), (hl, U, L)
        ok_x = all(any(sat(X, l) for l in c) for c in xcls)
        hits = [t for t, c in enumerate(cubes) if all(sat(X, l) for l in c)]
        good = ok_x and hits == [cs.index((U, L))]
        if not good: rep["fail"].append({"n": n, "U": U, "L": L, "ok_x": ok_x, "hits": hits})
        rep["positive"] += 1; rep["types"][typ] = rep["types"].get(typ, 0) + 1
        rep["cases_seen"].add(H.name(U, L))
    for n in range(nneg):
        P = mirlib.mirror_set(16, 1, rng, where="interior")
        Q, X = assign(P)
        hits = [t for t, c in enumerate(cubes) if all(sat(X, l) for l in c)]
        hv = hull(Q)
        if len(hv) <= 6:   # uniform sets sometimes have a 4- or 6-vertex hull: a real case
            U, L, hl = case_of(Q); want = [cs.index((U, L))]; rep["neg_smallhull"] += 1
        else:
            want = []
        if hits != want: rep["neg_fail"] += 1
        rep["neg"] += 1
    rep["distinct_cases_seen"] = len(rep["cases_seen"]); rep["cases_seen"] = sorted(rep["cases_seen"])
    rep["failures"] = len(rep["fail"])
    print(json.dumps(rep))

main()
