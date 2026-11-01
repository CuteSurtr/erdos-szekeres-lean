#!/usr/bin/env python3
"""A4-2 check 2: exact Z[zeta5] verification of the facts behind the layer units, written independently.

A point is a 5-tuple (a0..a4) meaning sum a_j z^j, z = exp(2 pi i/5); the rotation is multiplication by z, the centre
is 0. Orientation sign of (p,q,r) = sign Im(conj(q-p)(r-p)); with w = sum w_j z^j,
  Im(w) = (w1-w4) sin72 + (w2-w3) sin144,  sin144/sin72 = (sqrt5-1)/2,
so sign Im(w) = sign(A + B sqrt5) with A = 2(w1-w4)-(w2-w3), B = w2-w3 (integers, decided exactly).
Re(w)*4 = [4w0-(w1+w4)-(w2+w3)] + [(w1+w4)-(w2+w3)] sqrt5 (used only to sort for the hull).

Convex layers use the vertex-set definition: L1 = strict vertices of conv(P) (monotone chain, collinear points dropped),
then recurse on P minus L1.

For every input set it reports:
  GP          no three points collinear (exact)
  orbit       every layer is exactly one rotation orbit (size 5, or {0} if the centre is in the set)
  ccw         the hull order of each 5-point layer is p, zp, z^2p, ... (counter-clockwise labelling of the orbit)
  nesting     every point of every later layer is STRICTLY left of every CCW edge of every earlier layer polygon
  centre      the centre 0 is strictly left of every CCW edge of every 5-point layer polygon
  units       the three unit families of symcnf_layers.py hold in the layer normal form built from the set
usage: python3 -B check_layers_exact.py FILE [FILE...]     (lines "c0 c1 c2 c3")
       python3 -B check_layers_exact.py --random NSETS SEED   (random 5-fold sets, see below)
       python3 -B check_layers_exact.py --nongp               (pentagon + edge midpoints: GP is needed for nesting)
"""
import itertools
import random
import sys
from functools import cmp_to_key


def norm(c):
    c = list(c) + [0] * (5 - len(c))
    return tuple(x - c[4] for x in c[:4]) + (0,)


def sgn5(A, B):  # sign of A + B*sqrt(5), exact
    if A >= 0 and B >= 0:
        return 1 if (A or B) else 0
    if A <= 0 and B <= 0:
        return -1
    s = A * A - 5 * B * B
    return 0 if s == 0 else (1 if (s > 0) == (A > 0) else -1)


def sub(p, q):
    return tuple(p[i] - q[i] for i in range(5))


def mul(u, v):
    w = [0] * 5
    for a in range(5):
        if u[a]:
            for b in range(5):
                w[(a + b) % 5] += u[a] * v[b]
    return w


def conj(u):
    return [u[(-j) % 5] for j in range(5)]


def sign_im(w):
    return sgn5(2 * (w[1] - w[4]) - (w[2] - w[3]), w[2] - w[3])


def sign_re(w):
    return sgn5(4 * w[0] - (w[1] + w[4]) - (w[2] + w[3]), (w[1] + w[4]) - (w[2] + w[3]))


def orient(p, q, r):
    return sign_im(mul(conj(sub(q, p)), sub(r, p)))


def rot(p, k=1):
    q = p
    for _ in range(k % 5):
        q = norm([q[4]] + list(q[:4]))
    return q


ZERO = (0, 0, 0, 0, 0)


def cmp_xy(p, q):
    d = sub(p, q)
    s = sign_re(d)
    return s if s else sign_im(d)


def hull_vertices(P):
    """strict vertices of conv(P), counter-clockwise, by Andrew's monotone chain with exact predicates"""
    pts = sorted(set(P), key=cmp_to_key(cmp_xy))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def layers(P):
    rest, out = list(P), []
    while rest:
        h = hull_vertices(rest)
        out.append(h)
        hs = set(h)
        rest = [p for p in rest if p not in hs]
    return out


def analyse(P, label, verbose=True):
    P = [norm(p) for p in P]
    S = set(P)
    res = {"set": label, "n": len(P), "distinct": len(S) == len(P), "invariant": all(rot(p) in S for p in P),
           "centre_in_set": ZERO in S}
    res["GP"] = all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))
    L = layers(P)
    res["layer_sizes"] = [len(x) for x in L]
    orbit_ok, ccw_ok = True, True
    polys = []
    for lay in L:
        if lay == [ZERO]:
            continue
        orb = {rot(lay[0], k) for k in range(5)}
        if set(lay) != orb or len(lay) != 5:
            orbit_ok = False
            continue
        i0 = 0
        ccw_ok &= all(lay[(i0 + k) % 5] == rot(lay[i0], k) for k in range(5))
        polys.append(lay)
    res["orbit"] = orbit_ok
    res["ccw"] = ccw_ok
    # nesting and centre, with the exact orientation sign (0 counts as failure: strictness)
    worst_nest, worst_centre = 1, 1
    for i, lay in enumerate(L):
        if len(lay) < 3:
            continue
        edges = [(lay[j], lay[(j + 1) % len(lay)]) for j in range(len(lay))]
        for later in L[i + 1:]:
            for q in later:
                for a, b in edges:
                    worst_nest = min(worst_nest, orient(a, b, q))
        for a, b in edges:
            worst_centre = min(worst_centre, orient(a, b, ZERO))
    res["nesting_min_sign"] = worst_nest
    res["centre_min_sign"] = worst_centre
    # the unit families of symcnf_layers.py in the layer normal form built from the set (needs 5-point layers only)
    if orbit_ok and not res["centre_in_set"] and len(polys) >= 2:
        O = []
        p00 = polys[0][0]
        for o, lay in enumerate(polys):
            if o == 0:
                rep = p00
            else:  # point of the orbit in the open sector (0, 72 deg) from the ray to (0,0): sector units
                cand = [q for q in lay if orient(ZERO, p00, q) > 0 and orient(ZERO, rot(p00), q) < 0]
                if len(cand) != 1:
                    res["units"] = f"sector representative not unique ({len(cand)}): centre not generic"
                    break
                rep = cand[0]
            O.append([rot(rep, r) for r in range(5)])
        else:
            bad = 0
            for o in range(len(O)):
                e0, e1 = O[o][0], O[o][1]
                bad += sum(orient(e0, e1, O[o][k]) != 1 for k in range(2, 5))          # polygon units
                bad += orient(e0, e1, ZERO) != 1                                       # centre unit
                bad += sum(orient(ZERO, O[o][0], O[o][1]) != 1 for _ in [0])           # base centre fact k=1
                bad += sum(orient(ZERO, O[o][0], O[o][2]) != 1 for _ in [0])           # base centre fact k=2
                for o2 in range(o + 1, len(O)):
                    bad += sum(orient(e0, e1, O[o2][r]) != 1 for r in range(5))       # nesting units
            for o in range(1, len(O)):
                bad += orient(ZERO, O[0][0], O[o][0]) != 1
                bad += orient(ZERO, O[0][1], O[o][0]) != -1
            res["units"] = "all hold" if bad == 0 else f"{bad} violated"
    if verbose:
        print(res)
    return res


def random_set(rng, t, coef, with_centre):
    P = []
    for _ in range(t):
        p = norm([rng.randint(-coef, coef) for _ in range(4)])
        P += [rot(p, k) for k in range(5)]
    if with_centre:
        P.append(ZERO)
    return P


def main():
    a = sys.argv[1:]
    if a and a[0] == "--random":
        nsets, seed = int(a[1]), int(a[2])
        rng = random.Random(seed)
        tally = {"tested": 0, "GP": 0, "all_layers_single_orbit": 0, "nest_strict_ok": 0, "centre_ok": 0,
                 "units_ok": 0, "units_tested": 0, "multi_orbit_layer_convex": 0, "multi_orbit_layers": 0}
        while tally["tested"] < nsets:
            t = rng.randint(2, 6)
            P = random_set(rng, t, rng.choice([3, 6, 20, 60]), rng.random() < 0.3)
            if len(set(P)) != len(P):
                continue
            r = analyse(P, "random", verbose=False)
            if not r["GP"]:
                continue
            tally["tested"] += 1
            tally["GP"] += 1
            tally["nest_strict_ok"] += r["nesting_min_sign"] == 1
            if r["orbit"]:
                tally["all_layers_single_orbit"] += 1
                tally["centre_ok"] += r["centre_min_sign"] == 1
            if "units" in r:
                tally["units_tested"] += 1
                tally["units_ok"] += r["units"] == "all hold"
            # contrapositive of the lemma: a layer with >= 2 orbits has >= 10 = 2m points in convex position
            for lay in layers([norm(p) for p in P]):
                if len(lay) >= 10:
                    tally["multi_orbit_layers"] += 1
                    ok = all(orient(lay[j], lay[(j + 1) % len(lay)], lay[(j + 2) % len(lay)]) == 1
                             for j in range(len(lay)))
                    tally["multi_orbit_layer_convex"] += ok
        print(tally)
        return
    if a and a[0] == "--nongp":
        # outer regular pentagon 2 z^k and the midpoints z^k + z^(k+1) of its edges: 5-fold, centre not in the set,
        # NOT in general position; 10 points, so no K = 10 = 2m points in (strict) convex position.
        P = [norm([0] * k + [2]) for k in range(5)] + [rot(norm([1, 1]), k) for k in range(5)]
        r = analyse(P, "pentagon+edge-midpoints (not GP)")
        print("=> layers are single orbits:", r["orbit"], "; strict nesting holds:", r["nesting_min_sign"] == 1,
              "(min orientation sign of a later point w.r.t. an earlier edge =", r["nesting_min_sign"], ")")
        return
    for path in a:
        P = [list(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith(("FOUND", "#"))]
        analyse(P, path.split("/")[-1])


if __name__ == "__main__":
    main()
