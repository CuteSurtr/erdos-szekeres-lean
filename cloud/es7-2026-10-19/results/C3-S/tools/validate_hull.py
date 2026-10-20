#!/usr/bin/env python3
"""C3-S validation of the hull normalization and case cover on random 3-fold symmetric sets.

For each random set S (exact Z[sqrt3] coordinates, C3a's c3geom):
  1. compute the hull vertex set H of S exactly (independently of the labels);
  2. if |H| is 3 or 6: search integer directions u for the line l until the point labelled 0
     is a hull vertex and, when |H| = 6, the other hull orbit has residue a <= m // 2;
     if sigma_0 = 1 replace S by -S with the same l (labels unchanged);
  3. the case is H3 or H6(a, sigma_a); evaluate EVERY clause of that case's CNF (C3a
     encoding = base CNF + hull clauses, exactly what gen_case.py writes) on the true
     assignment (C3a validate.true_assignment).  Required: all non-gon clauses true, all hull
     clauses true, gon clauses all true <=> convk finds no convex k-set.
  4. sanity (not needed for soundness): the hull clauses of every other case are violated.
  5. convex layers: peel S (exactly, by coordinates) into layers L1 = hull, L2 = hull of the
     rest, ...; while a layer has 3 or 6 points, its layer-case name (hullcase.layers_name, with
     the sigma of each residue of a two-orbit layer) is formed, and the layer clauses of every
     prefix L1..Lj are evaluated on the true assignment (all must be true).
usage: validate_hull.py M K NSETS SEED"""
import itertools
import json
import os
import random
import sys
from functools import cmp_to_key

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from c3geom import Labelled, orient, rot, zsgn, zsub, zmul, zadd, general_position  # noqa: E402
from validate import flat, brute, true_assignment  # noqa: E402
from hullcase import cases, case_name, hull_clauses, layer_clauses, parse_layers, layers_name  # noqa: E402


def hull_vertices(pts):
    n = len(pts)
    H = set()
    for i in range(n):
        for j in range(n):
            if i != j and all(orient(pts[i], pts[j], pts[w]) > 0 for w in range(n) if w != i and w != j):
                H.add(i)
                H.add(j)
    return H


def label_order(pts, u):
    u1, u2 = u
    xt = [zadd(zmul((u2, 0), p[0]), zmul((-u1, 0), p[1])) for p in pts]
    yt = [zadd(zmul((u1, 0), p[0]), zmul((u2, 0), p[1])) for p in pts]
    if any(zsgn(*v) == 0 for v in xt) or len(set(xt)) != len(xt):
        return None

    def cmp(i, j):
        return zsgn(*zsub(zmul(yt[i], xt[j]), zmul(yt[j], xt[i]))) * zsgn(*xt[i]) * zsgn(*xt[j])
    return sorted(range(len(pts)), key=cmp_to_key(cmp))


def rand_pt(rng, M, shape):
    while True:
        if shape == "disk":
            x, y = rng.randint(-M, M), rng.randint(-M, M)
            if 0 < x * x + y * y <= M * M:
                return x, y
        elif shape == "thin":
            return rng.randint(M // 2, 3 * M // 2), rng.randint(-M // 400, M // 400)
        elif shape == "ring":
            x, y = rng.randint(-M, M), rng.randint(-M, M)
            if (M // 2) ** 2 <= x * x + y * y <= M * M:
                return x, y
        else:
            cx, cy = shape
            x, y = cx + rng.randint(-M // 8, M // 8), cy + rng.randint(-M // 8, M // 8)
            if x or y:
                return x, y


def random_set(m, rng):
    """1 or 2 far base points (hull 3 or 6 likely) plus m-1 or m-2 inner points of mixed shapes."""
    while True:
        nout = rng.choice([1, 2, 2]) if m >= 2 else 1
        R = 10 ** 6
        base = []
        for _ in range(nout):
            while True:
                x, y = rng.randint(-R, R), rng.randint(-R, R)
                if (0.8 * R) ** 2 <= x * x + y * y <= R * R:
                    break
            base.append((x, y))
        inner_M = rng.choice([R // 4, R // 5, R // 8])
        shape = rng.choice(["disk", "thin", "thin", "ring", "cl"])
        for _ in range(m - nout):
            sh = shape if shape != "cl" else (rng.randint(-inner_M // 2, inner_M // 2), rng.randint(-inner_M // 2, inner_M // 2))
            base.append(rand_pt(rng, inner_M if shape != "thin" else inner_M // 2, sh))
        if rng.random() < 0.15:  # occasionally a fully random set (often larger hull)
            base = [rand_pt(rng, 1000, "disk") for _ in range(m)]
        pts = []
        for (x, y) in base:
            p = ((4 * x, 0), (4 * y, 0))
            q = rot(p)
            pts += [p, q, rot(q)]
        if general_position(pts):
            return pts


def main():
    M, K, NS, seed = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    n = 3 * M
    e = C3Enc(M, K)
    e.build()
    lits, starts = flat(e.clauses)
    gon_start = [s for s in e.sections if s[0] == "gon"][0][1]
    del e.clauses
    allcases = cases(M, K)
    hc = {case_name(c): hull_clauses(M, c, e.ccw, e.sig) for c in allcases}
    res = {"m": M, "k": K, "seed": seed, "sets": 0, "hull_sizes": {}, "tested": 0, "case_counts": {},
           "gon": 0, "nogon": 0, "other_case_hull_ok": 0, "fail": []}
    for t in range(NS):
        pts = random_set(M, rng)
        res["sets"] += 1
        H = hull_vertices(pts)
        res["hull_sizes"][len(H)] = res["hull_sizes"].get(len(H), 0) + 1
        if len(H) not in (3, 6) or (len(H) == 6 and K < 7):
            has = brute_pts(pts, K, rng)
            if not has:
                res["fail"].append({"set": t, "why": "hull not 3/6 but no k-gon", "hull": len(H)})
            continue
        found = None
        for _ in range(20000):
            u = (rng.randint(-10 ** 4, 10 ** 4), rng.randint(-10 ** 4, 10 ** 4))
            if u == (0, 0):
                continue
            order = label_order(pts, u)
            if order is None or order[0] not in H:
                continue
            lab = {o: l for l, o in enumerate(order)}
            Hl = sorted(lab[h] for h in H)
            if len(H) == 6:
                res6 = sorted({l % M for l in Hl})
                assert res6[0] == 0 and len(res6) == 2, Hl
                if res6[1] > M // 2:
                    continue
            found = u
            break
        if found is None:
            res["fail"].append({"set": t, "why": "no canonical l found"})
            continue
        L = Labelled(pts, rng, u=found)
        if L.sigma[0]:
            P2 = [((-p[0][0], -p[0][1]), (-p[1][0], -p[1][1])) for p in pts]
            L2 = Labelled(P2, rng, u=found)
            assert L2.sigma[0] == 0 and L2.orig == L.orig
            L = L2
        Hl = sorted(L.lab[h] for h in H)
        # label-level sanity: hull orbit structure
        assert all(L.Rlab[i] == (i - M) % n for i in range(n))
        if len(H) == 3:
            assert Hl == [0, M, 2 * M], Hl
            cn = "H3"
        else:
            a = min(l for l in Hl if l % M)
            a %= M
            cn = f"H6a{a}s{L.sigma[a]}"
        A, conf, chain_gon = true_assignment(e, L)
        val = A[np.abs(lits)] ^ (lits < 0)
        sat = np.logical_or.reduceat(val, starts)
        core_ok = bool(sat[:gon_start].all())
        gon_ok = bool(sat[gon_start:].all())
        hullval = lambda cls: all(any(A[abs(l)] ^ (l < 0) for l in c) for c in cls)
        hull_ok = hullval(hc[cn])
        others_ok = [c for c in hc if c != cn and hullval(hc[c])]
        has = brute(n, K, L.chiS)
        # convex layers
        rest = set(range(n))
        layers = []
        while rest:
            sub = sorted(rest)
            Hs = {sub[i] for i in hull_vertices([pts[j] for j in sub])} if len(sub) > 3 else set(sub)
            if len(Hs) not in (3, 6):
                break
            labs = sorted(L.lab[h] for h in Hs)
            resid = sorted({l % M for l in labs})
            if len(resid) == 1:
                layers.append([(resid[0], None)])
            else:
                layers.append([(r, L.sigma[r]) for r in resid])
            rest -= Hs
        layers[0] = [(r, L.sigma[r]) for r, _ in layers[0]] if len(layers[0]) == 2 else [(0, 0)]
        lname = layers_name(layers)
        if len(layers[0]) == 2:
            assert lname.split("_")[0] == f"0s0-{cn[3:].split('s')[0]}s{cn.split('s')[-1]}", (lname, cn)
        lay_ok = all(hullval(layer_clauses(M, layers[:j + 1], e.ccw, e.sig)) for j in range(len(layers)))
        res["layers_checked"] = res.get("layers_checked", 0) + len(layers)
        res["layer_depth_hist"] = res.get("layer_depth_hist", {})
        res["layer_depth_hist"][len(layers)] = res["layer_depth_hist"].get(len(layers), 0) + 1
        if not lay_ok:
            res["fail"].append({"set": t, "case": cn, "layers": lname, "why": "layer clauses false"})
        res["tested"] += 1
        res["case_counts"][cn] = res["case_counts"].get(cn, 0) + 1
        res["gon" if has else "nogon"] += 1
        res["other_case_hull_ok"] += len(others_ok)
        if conf or not core_ok or not hull_ok or gon_ok == has or chain_gon != has:
            res["fail"].append({"set": t, "case": cn, "conf": conf[:3], "core_ok": core_ok, "hull_ok": hull_ok,
                                "gon_ok": gon_ok, "brute_gon": has})
    print(json.dumps(res))


def brute_pts(pts, K, rng):
    L = Labelled(pts, rng)
    return brute(len(pts), K, L.chiS)


if __name__ == "__main__":
    main()
