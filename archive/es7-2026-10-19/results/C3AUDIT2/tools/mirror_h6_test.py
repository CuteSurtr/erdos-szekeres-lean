#!/usr/bin/env python3
"""C3AUDIT2: independent exact test of Lemma H6M (results/C3PLAN/PLAN.md section 3a).

Own code only (no import from the repository).  Points are integer vectors (u, v); everything used
here (orientation, convex hulls, angular order about the centre 0, sides of a line through 0) is
invariant under linear maps of positive determinant, so (u, v) may be read as Eisenstein
coordinates u + v*omega: the rotation by +120 deg is the integer map R(u, v) = (-v, u - v), and the
reflection z -> conj(z) is C(u, v) = (u - v, -v) (det -1, C R C = R^-1).  A reflection in any other
line through 0 is C followed by a rotation about 0, which changes no labelling (the frame turns
with it), so testing C(S) tests the mirror image in l.

Canonical labelling (Lemma 2 of results/C3-S/soundness.md), built from scratch: for every hull
vertex p, take the directed line l with direction d = -(K p + R^2 p) (l just before the line of
p, so p gets label 0 with x > 0); labels = order of the lines through 0 by increasing y/x in the
frame (x-axis = right of d), sigma = [point left of d]; if sigma_0 = 1 apply p -> -p (flip every
sigma); keep it iff the other hull residue a satisfies a <= m // 2.  All admissible choices must
give the same layer path (checked: uniqueness).  The convention R(i) = (i - m) mod n and
sigma_{r+m} = 1 - sigma_r, sigma_{r+2m} = sigma_r is asserted on every labelling.

For each random 3-fold set S with a hexagonal hull: layer path A of S, layer path B of C(S), and
check B == [L1] + [phi(L) for L in A[1:]] with phi(r, g) = ((a - r) mod m, g ^ [r < a] ^ [s = 0]).
Layers of any number of orbits are compared (not only 1 or 2).  Mutations of phi must fail.
usage: mirror_h6_test.py M NSETS SEED  -> one JSON line
"""
import functools
import json
import random
import sys


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def orient(a, b, c):
    return cross((b[0] - a[0], b[1] - a[1]), (c[0] - a[0], c[1] - a[1]))


def R(p):
    return (-p[1], p[0] - p[1])


def C(p):
    return (p[0] - p[1], -p[1])


def neg(p):
    return (-p[0], -p[1])


def hull(pts):
    """strict hull vertices (indices into pts), general position assumed"""
    idx = sorted(range(len(pts)), key=lambda i: pts[i])
    if len(idx) <= 2:
        return set(idx)
    lo, up = [], []
    for i in idx:
        while len(lo) >= 2 and orient(pts[lo[-2]], pts[lo[-1]], pts[i]) <= 0:
            lo.pop()
        lo.append(i)
    for i in reversed(idx):
        while len(up) >= 2 and orient(pts[up[-2]], pts[up[-1]], pts[i]) <= 0:
            up.pop()
        up.append(i)
    return set(lo[:-1] + up[:-1])


def general_position(pts):
    n = len(pts)
    for i in range(n):
        if pts[i] == (0, 0):
            return False
        for j in range(i + 1, n):
            if cross(pts[i], pts[j]) == 0:  # collinear with the centre (or equal)
                return False
            for k in range(j + 1, n):
                if orient(pts[i], pts[j], pts[k]) == 0:
                    return False
    return True


def random_set(m, rng, B):
    while True:
        reps = []
        for _ in range(m):
            while True:
                u, v = rng.randint(-B, B), rng.randint(-B, B)
                # rough disk in Cartesian x = u - v/2, y = v*sqrt3/2: |z|^2 = u^2 - uv + v^2
                if 0 < u * u - u * v + v * v <= B * B:
                    break
            if rng.random() < 0.15:  # push some points outward to vary the hull
                f = rng.choice((2, 3))
                u, v = u * f, v * f
            reps.append((u, v))
        pts = []
        for p in reps:
            pts += [p, R(p), R(R(p))]
        if general_position(pts):
            return pts


def labelling(pts, p0, K):
    """labels and sigma for the line just before the line of pts[p0] (label 0)"""
    q = pts[p0]
    q2 = R(R(q))
    d = (-(K * q[0] + q2[0]), -(K * q[1] + q2[1]))
    if any(cross(d, x) == 0 for x in pts):
        return None
    sig = [1 if cross(d, x) > 0 else 0 for x in pts]
    rep = [x if s == 0 else neg(x) for x, s in zip(pts, sig)]  # the ray with x > 0
    # order by increasing y/x on x > 0: from -d counter-clockwise; u before v iff cross(u, v) > 0
    order = sorted(range(len(pts)), key=functools.cmp_to_key(lambda i, j: -1 if cross(rep[i], rep[j]) > 0 else 1))
    lab = [0] * len(pts)
    for t, i in enumerate(order):
        lab[i] = t
    if lab[p0] != 0:
        return None
    return lab, sig


def check_conventions(pts, lab, sig, m):
    n = 3 * m
    pos = {x: i for i, x in enumerate(pts)}
    bylab = [None] * n
    for i in range(n):
        bylab[lab[i]] = i
    for t in range(n):
        i = bylab[t]
        j = pos[R(pts[i])]
        assert lab[j] == (t - m) % n, "R(i) = (i - m) mod n"
    for r in range(m):
        s0, s1, s2 = sig[bylab[r]], sig[bylab[r + m]], sig[bylab[r + 2 * m]]
        assert s1 == 1 - s0 and s2 == s0, "sigma convention"


def layer_path(pts, lab, sig, m):
    n = 3 * m
    bylab = [None] * n
    for i in range(n):
        bylab[lab[i]] = i
    rest = list(range(n))
    out = []
    while rest:
        H = hull([pts[i] for i in rest])
        Hs = [rest[i] for i in H]
        res = sorted({lab[i] % m for i in Hs})
        assert len(Hs) == 3 * len(res), "layer not a union of orbits"
        if len(Hs) >= 3:  # Lemma 3: ccw boundary order = order of the keys (sigma_i, i)
            ks = sorted(Hs, key=lambda i: (sig[i], lab[i]))
            for t in range(len(ks)):
                u, v = pts[ks[t]], pts[ks[(t + 1) % len(ks)]]
                assert all(orient(u, v, pts[w]) > 0 for w in rest if w not in (ks[t], ks[(t + 1) % len(ks)])), "Lemma 3"
            if not out:  # top layer: the hull order of soundness.md Lemma 3
                a = res[1]
                sa = sig[bylab[a]]
                want = [0, a, 2 * m, a + 2 * m, m, a + m] if sa == 0 else [0, a + m, 2 * m, a, m, a + 2 * m]
                assert [lab[i] for i in ks] == want, "top hull order"
        if len(res) == 1:
            out.append(((res[0], None),))
        else:
            out.append(tuple((r, sig[bylab[r]]) for r in res))
        Hset = set(Hs)
        rest = [i for i in rest if i not in Hset]
    return out


def canon(pts, m, K):
    H = hull(pts)
    if len(H) != 6:
        return None, None
    paths, n_adm = set(), 0
    for p0 in H:
        r = labelling(pts, p0, K)
        assert r is not None, "K too small or degenerate direction"
        lab, sig = r
        check_conventions(pts, lab, sig, m)
        bylab0 = lab.index(0)
        if sig[bylab0] == 1:  # Lemma 2(b): p -> -p keeps labels, flips every sigma
            sig = [1 - s for s in sig]
        hres = sorted({lab[i] % m for i in H})
        assert len(hres) == 2 and hres[0] == 0
        a = hres[1]
        if a > m // 2:
            continue
        n_adm += 1
        paths.add(tuple(layer_path(pts, lab, sig, m)))
    assert n_adm >= 1
    return paths, n_adm


def phi_layer(L, m, a, s, mode="ok"):
    out = []
    for r, g in L:
        if mode == "res_m_minus_r":
            rr = (m - r) % m
        elif mode == "res_a_plus_r":
            rr = (a + r) % m
        else:
            rr = (a - r) % m
        if g is None:
            gg = None
        elif mode == "no_lt_flip":
            gg = g ^ (s == 0)
        elif mode == "no_s0_term":
            gg = g ^ (r < a)
        elif mode == "no_flip":
            gg = g
        else:
            gg = g ^ (r < a) ^ (s == 0)
        out.append((rr, gg))
    return tuple(sorted(out))


MODES = ["ok", "no_lt_flip", "no_s0_term", "no_flip", "res_m_minus_r", "res_a_plus_r"]


def main():
    m, NS, seed = map(int, sys.argv[1:4])
    rng = random.Random(seed)
    B = 2000
    K = 10 ** 9  # >> (coordinate bound)^2, angular gaps are >= 1/|p||q|
    res = {"m": m, "seed": seed, "tried": 0, "h6": 0, "cases": {}, "layers": 0, "layer_sizes": {},
           "nonunique": 0, "admissible_choices": {}, "fail": {k: 0 for k in MODES}, "examples": []}
    while res["h6"] < NS:
        pts = random_set(m, rng, B)
        res["tried"] += 1
        P, na = canon(pts, m, K)
        if P is None:
            continue
        res["h6"] += 1
        res["admissible_choices"][na] = res["admissible_choices"].get(na, 0) + 1
        Q, nb = canon([C(x) for x in pts], m, K)
        if len(P) != 1 or len(Q) != 1:
            res["nonunique"] += 1
            continue
        A, Bp = next(iter(P)), next(iter(Q))
        L1 = A[0]
        a, s = L1[1]
        assert L1[0] == (0, 0)
        key = f"H6({a},{s})"
        res["cases"][key] = res["cases"].get(key, 0) + 1
        res["layers"] += len(A)
        for L in A:
            res["layer_sizes"][len(L)] = res["layer_sizes"].get(len(L), 0) + 1
        for mode in MODES:
            pred = (L1,) + tuple(phi_layer(L, m, a, s, mode) for L in A[1:])
            if pred != Bp:
                res["fail"][mode] += 1
                if mode == "ok" and len(res["examples"]) < 5:
                    res["examples"].append({"A": str(A), "B": str(Bp)})
    print(json.dumps(res, sort_keys=True))


if __name__ == "__main__":
    main()
