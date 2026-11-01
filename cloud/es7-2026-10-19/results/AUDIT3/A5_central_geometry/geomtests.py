#!/usr/bin/env python3
"""Auditor A5: real-configuration tests of the angular normal form, the hull cubes, the second-layer cubes, and the
relabelling reductions (A) and (B), with exact integer arithmetic. My own derivations under test:

 normal form   : every hull vertex f gives a labelling X = label(P, f) (open half-plane left of c->f, ccw order).
 (A)           : start at p_a = X[2a] instead: new class j = old class (j + a) mod 17, i.e. old i -> new (i - a) mod 17;
                 new point (j,0) = old (a+j, 0) for j <= 16-a, old (0,1) for j = 17-a, old (j+a-17, 1) for j > 17-a.
                 Case P_a becomes P_(17-a); a second-layer set V becomes {(i - a) mod 17}.
 (B)           : reflect (orientation reversing, fixing c) and start at rho(p_a): old i -> new (a - i) mod 17;
                 new (j,0) = rho(old (a-j,0)) for 1 <= j < a, rho(old (0,0)) for j = a, rho(old (17+a-j, 1)) for j > a.
                 Case P_a stays P_a; V becomes {(a - i) mod 17}.
For every labelling: the 136 normal-form units and 10,880 hull clauses hold; exactly one of the 136 hull cubes holds
and it is the geometric hull; in a parallelogram case exactly one second-layer cube of the case holds iff the second
layer has 4 or 6 vertices (none otherwise), and it is the geometric one. Cubes for a <= 8 are read from the lanes' files
(C2P/cubes); for a >= 9 they are my semantic cubes (shown equal to the files for a <= 8 by static_checks.py).
usage: geomtests.py BASE_JSON RESULTS_DIR NCONF SEED"""
import itertools, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

MAPF, RES, NCONF, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
mp = Map(MAPF)
rng = random.Random(SEED)
pt = lambda o, r: 2 * o + r

# normal-form units and hull clauses (as derived in static_checks.py, which showed they equal the base's)
UNITS = [mp.lit(Z, 0, pt(o, 0)) for o in range(1, T)] + [mp.lit(Z, pt(o, 0), pt(o2, 0)) for o, o2 in itertools.combinations(range(1, T), 2)]
HCL = []
for a_, b_, d_ in itertools.combinations(range(1, N), 3):
    for s in (1, -1):
        cl = [-s * mp.lit(a_, b_, 0), -s * mp.lit(b_, d_, 0), -s * mp.lit(d_, a_, 0)]
        if not any(-l in cl for l in cl):
            HCL.append(cl)
assert len(UNITS) == 136 and len(HCL) == 10880

hull, _ = load_cubes(os.path.join(RES, "C2C34", "cubes.txt"))


def ccw_vertices(classes):
    cl = sorted(classes)
    return [pt(o, 0) for o in cl] + [pt(o, 1) for o in cl]


def semantic_l2(a, V):
    lits = set(hull[f"P{a}"])
    pts_in = [q for q in range(N) if q // 2 not in (0, a)]
    H2 = ccw_vertices(V)
    for k in range(len(H2)):
        u, w = H2[k], H2[(k + 1) % len(H2)]
        for q in pts_in:
            if q not in (u, w):
                lits.add(mp.lit(u, w, q))
    return sorted(lits, key=abs)


L2 = {}
for a in range(1, T):
    if a <= 8:
        L2[a], _ = load_cubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))
    else:
        inner = [o for o in range(1, T) if o != a]
        L2[a] = {f"P{a}_" + "-".join(map(str, V)): semantic_l2(a, V) for h in (2, 3) for V in itertools.combinations(inner, h)}

name2 = lambda a, V: f"P{a}_" + "-".join(map(str, sorted(V)))
cnt = dict(configs=0, labellings=0, hex=0, par=0, par_l2_4=0, par_l2_6=0, par_l2_big=0, A=0, B=0, Bfixed=0, Arefl=0)
fails = []
seenAV = set()


def xvals(X):
    val = [0] * (mp.nX + 1)
    for (a, b, c), (v, s) in mp.tv.items():
        ch = sgn(cross(X[a], X[b], X[c]))
        assert ch != 0
        x = s * ch
        if val[v] == 0:
            val[v] = x
        elif val[v] != x:
            raise AssertionError("triple class inconsistent")
    return val


def classify(X):
    """returns (hull classes, second-layer classes or None, number of second-layer vertices) from coordinates, and
    checks the CNF-side statements for this labelling"""
    val = xvals(X)
    for l in UNITS:
        if not lit_true(val, l):
            raise AssertionError("normal-form unit false")
    for cl in HCL:
        if not any(lit_true(val, l) for l in cl):
            raise AssertionError("hull clause false")
    Hc, Hidx = hull_classes(X)
    sat = [n for n, c in hull.items() if cube_true(val, c)]
    if len(Hc) == 2:
        exp = f"P{Hc[1]}"
    elif len(Hc) == 3:
        exp = f"H{Hc[1]}-{Hc[2]}"
    else:
        exp = None
    if sat != ([exp] if exp else []):
        raise AssertionError(f"hull cubes true {sat}, geometry {Hc}")
    if len(Hc) != 2:
        return Hc, None, None
    a = Hc[1]
    inner_idx = [q for q in range(N) if q // 2 not in (0, a)]
    V2, V2idx = hull_classes(X, inner_idx)
    sat2 = [n for n, c in L2[a].items() if cube_true(val, c)]
    if len(V2idx) in (4, 6):
        if sat2 != [name2(a, V2)]:
            raise AssertionError(f"l2 cubes true {sat2}, geometry {V2}")
    else:
        if sat2:
            raise AssertionError(f"second layer has {len(V2idx)} vertices but {sat2} true")
    return Hc, V2, len(V2idx)


def predicted_A(X, a):
    Y = [X[0]] * 0
    newfirst = X[pt(a, 0)]
    Y = [newfirst, neg(newfirst)]
    for j in range(1, T):
        if j <= 16 - a:
            p = X[pt(a + j, 0)]
        elif j == 17 - a:
            p = X[pt(0, 1)]
        else:
            p = X[pt(j + a - 17, 1)]
        Y += [p, neg(p)]
    return Y + [ORIGIN]


def predicted_B(X, a, rho):
    Y = [rho(X[pt(a, 0)]), rho(X[pt(a, 1)])]
    for j in range(1, T):
        if j < a:
            p = rho(X[pt(a - j, 0)])
        elif j == a:
            p = rho(X[pt(0, 0)])
        else:
            p = rho(X[pt(17 + a - j, 1)])
        Y += [p, neg(p)]
    return Y + [ORIGIN]


t0 = time.time()
kinds = ["par2", "par3", "par_free", "hex", "disc"]
for k in range(NCONF):
    kind = kinds[k % len(kinds)]
    while True:
        if kind == "par2":
            P = gen_parallelogram(rng, inner_kind=2)
        elif kind == "par3":
            P = gen_parallelogram(rng, inner_kind=3)
        elif kind == "par_free":
            P = gen_parallelogram(rng)
        elif kind == "hex":
            P = gen_hexagon(rng)
        else:
            P = gen_random_disc(rng)
        if general_position(P):
            break
    cnt["configs"] += 1
    try:
        H = hull_ccw(P)
        for f in H:
            X = label(P, f)
            assert X is not None, "normal form failed for a hull vertex"
            Hc, V2, nv2 = classify(X)
            cnt["labellings"] += 1
            if len(Hc) == 3:
                cnt["hex"] += 1
            if len(Hc) != 2:
                continue
            cnt["par"] += 1
            a = Hc[1]
            if nv2 == 4:
                cnt["par_l2_4"] += 1
            elif nv2 == 6:
                cnt["par_l2_6"] += 1
            else:
                cnt["par_l2_big"] += 1
            # (A)
            for start in (pt(a, 0), pt(a, 1)):
                Y = label(P, X[start])
                if start == pt(a, 0) and Y != predicted_A(X, a):
                    fails.append(f"(A) relabelling differs from prediction, a={a}")
                Hc2, V22, _ = classify(Y)
                cnt["labellings"] += 1
                cnt["A"] += 1
                if Hc2 != [0, 17 - a]:
                    fails.append(f"(A) hull {Hc} -> {Hc2}")
                if nv2 in (4, 6) and sorted(V22) != sorted((i - a) % T for i in V2):
                    fails.append(f"(A) V {V2} -> {V22}")
            # (B)
            if nv2 in (4, 6):
                seenAV.add((a, tuple(V2)))
            kindr = rng.randrange(4)
            rho = lambda p, kr=kindr: reflect([p], kr)[0]
            Q = reflect(P, kindr)
            for start in (pt(a, 0), pt(a, 1)):
                Y = label(Q, rho(X[start]))
                if start == pt(a, 0) and Y != predicted_B(X, a, rho):
                    fails.append(f"(B) relabelling differs from prediction, a={a}")
                Hc2, V22, _ = classify(Y)
                cnt["labellings"] += 1
                cnt["B"] += 1
                if Hc2 != [0, a]:
                    fails.append(f"(B) hull {Hc} -> {Hc2}")
                if nv2 in (4, 6):
                    W = sorted((a - i) % T for i in V2)
                    if sorted(V22) != W:
                        fails.append(f"(B) V {V2} -> {V22}, predicted {W}")
                    if W == sorted(V2):
                        cnt["Bfixed"] += 1
            # reflection started at rho(p0): P_(17-a), V -> -V
            Y = label(Q, rho(X[0]))
            Hc2, V22, _ = classify(Y)
            cnt["labellings"] += 1
            cnt["Arefl"] += 1
            if Hc2 != [0, 17 - a] or (nv2 in (4, 6) and sorted(V22) != sorted((-i) % T for i in V2)):
                fails.append(f"reflection at p0: {Hc},{V2} -> {Hc2},{V22}")
    except AssertionError as e:
        fails.append(f"config {k} ({kind}): {e}")
    if (k + 1) % 200 == 0:
        print(f"{k + 1} configs, {time.time() - t0:.0f}s, fails {len(fails)}", flush=True)
print("counts", cnt, "distinct (a, V) with 4/6-vertex second layer:", len(seenAV))
print("FAILURES", len(fails))
for x in fails[:20]:
    print("  ", x[:400])
