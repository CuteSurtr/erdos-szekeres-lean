#!/usr/bin/env python3
"""Exact soundness test of a symmetric no-K-gon CNF (symcnf.py with odd m = 3, or d3cnf.py)
against random point sets with EXACT 3-fold (or D3) symmetry.

Exactness: points are Eisenstein integers a + b*w (w = exp(2 pi i/3)) stored as (a, b).
In these coordinates the rotation by 120 degrees is the integer map R(a,b) = (-b, a-b)
(det +1) and the reflection in the real axis is S(a,b) = (a-b, -b) (det -1).  The linear map
(a,b) -> a + b*w has determinant sqrt(3)/2 > 0, so orientations computed from (a,b) with
integer arithmetic are exactly the Euclidean orientations.  No rounding anywhere.

Per sample:
  * random orbit representatives (several distributions), the centre at the origin;
  * the labelling normal form of symcnf.py applied geometrically (orbit 0 / point (0,0)
    arbitrary; every other orbit represented by its point in the open sector of 120 degrees
    measured at the centre from the ray to (0,0); orbits sorted by angle);
    for D3 the 3-orbit lies on a mirror axis and is labelled orbit 0;
  * chi of every triple of all P points (incl. the auxiliary centre) from coordinates, mapped
    to the CNF variables through the map file (a conflict = the map is not consistent with
    the symmetry: failure);
  * cnfeval: orientation-only clauses must all hold; least-model counts of true convexity
    flags per level; falsified K-set clauses;
  * geomcount: number of group orbits of convex r-subsets from exact convex hulls.
Required: xonly_violated = 0, map conflicts = 0, true_level_r = orbits_r (4 <= r < K),
kfalse = orbits_K, and sat = (orbits_K == 0).

usage: symval2.py cnf map.json c3|d3|d3c3 samples seed cnfeval geomcount [workdir]
  (d3c3: exact D3 samples against a 3-fold CNF with reflection clauses, see c3refl.py)
"""
import json
import random
import subprocess
import sys
import os


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def R(p, k=1):
    a, b = p
    for _ in range(k % 3):
        a, b = -b, a - b
    return (a, b)


def S(p):
    a, b = p
    return (a - b, -b)


def parity(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv & 1 else 1


def rand_point(rng, dist, M):
    if dist == "box":
        return (rng.randint(-M, M), rng.randint(-M, M))
    if dist == "cluster":
        cx, cy = rng.choice([(M // 2, M // 7), (-M // 3, M // 2), (M // 5, -M // 2)])
        s = M // rng.choice([4, 8, 30])
        return (cx + rng.randint(-s, s), cy + rng.randint(-s, s))
    if dist == "annulus":
        # roughly on a few concentric hexagonal "rings" with noise (many convex subsets)
        k = rng.choice([1, 2, 3])
        base = R((k * M // 3, 0), rng.randint(0, 2))
        s = M // 20
        return (base[0] + rng.randint(-s, s), base[1] + rng.randint(-s, s))
    if dist == "small":
        return (rng.randint(-60, 60), rng.randint(-60, 60))
    raise ValueError(dist)


def sample(info, mode, rng):
    m, t = info["m"], info["t"]
    assert m == 3 and info["center"] == "aux"
    M = 10 ** 6
    dist = rng.choice(["box", "cluster", "annulus", "small"])
    c = (0, 0)
    if mode == "c3":
        reps = [rand_point(rng, dist, M) for _ in range(t)]
    else:
        n6 = (t - 1) // 2
        a = rng.randint(1, M) * rng.choice([1, -1])
        reps = [(a, 0)]
        for _ in range(n6):
            p = rand_point(rng, dist, M)
            reps += [p, S(p)]
    r = label(reps)
    return None if r is None else (r, dist)


def label(reps):
    """labelling normal form for rotation-orbit representatives reps (reps[0] -> orbit 0)"""
    c = (0, 0)
    if any(p == c for p in reps):
        return None
    u0 = reps[0]
    Ru0 = R(u0)
    lab = [u0]
    for p in reps[1:]:
        cand = [R(p, k) for k in range(3) if orient(c, u0, R(p, k)) > 0 and orient(c, Ru0, R(p, k)) < 0]
        if len(cand) != 1:
            return None
        lab.append(cand[0])
    rest = lab[1:]
    # sort by angle inside the sector (insertion sort with the exact comparator)
    srt = []
    for q in rest:
        i = 0
        while i < len(srt) and orient(c, srt[i], q) > 0:
            i += 1
        srt.insert(i, q)
    for i in range(len(srt)):
        for j in range(i + 1, len(srt)):
            if orient(c, srt[i], srt[j]) <= 0:
                return None
    order = [u0] + srt
    pts = []
    for q in order:
        for r in range(3):
            pts.append(R(q, r))
    pts.append(c)
    P = len(pts)
    if len(set(pts)) != P:
        return None
    for i in range(P):
        for j in range(i + 1, P):
            for k in range(j + 1, P):
                if orient(pts[i], pts[j], pts[k]) == 0:
                    return None
    return pts


def group_perms(pts, setpts, mode):
    idx = {p: i for i, p in enumerate(pts)}
    perms = []
    maps = [lambda p, k=k: R(p, k) for k in range(3)]
    if mode == "d3":   # (mode "d3c3": D3-symmetric samples, flags counted per rotation orbit)
        maps += [lambda p, k=k: R(S(p), k) for k in range(3)]
    sidx = {pi: j for j, pi in enumerate(setpts)}
    for f in maps:
        perms.append([sidx[idx[f(pts[i])]] for i in setpts])
    return perms


def main():
    cnf, mp, mode, samples, seed, cnfeval, geomcount = sys.argv[1:8]
    workdir = sys.argv[8] if len(sys.argv) > 8 else "."
    samples, seed = int(samples), int(seed)
    info = json.load(open(mp))
    K, nX = info["K"], info["X_vars"]
    rng = random.Random(seed)
    tag = os.path.basename(cnf).replace(".cnf", "") + f"_{mode}_s{seed}"
    asg_path = os.path.join(workdir, tag + ".asg")
    rows = []
    conflicts = 0
    tries = 0
    with open(asg_path, "w") as fa:
        while len(rows) < samples:
            tries += 1
            s = sample(info, mode, rng)
            if s is None:
                continue
            pts, dist = s
            val = {}
            bad = False
            for a, b, cc, v, sg in info["triples"]:
                chi = 1 if orient(pts[a], pts[b], pts[cc]) > 0 else -1
                want = sg * chi > 0
                if v in val and val[v] != want:
                    bad = True
                val[v] = want
            if bad:
                conflicts += 1
            if len(val) != nX:
                print("map does not cover all orientation variables", len(val), nX)
                sys.exit(1)
            fa.write(" ".join(str(v if val[v] else -v) for v in range(1, nX + 1)) + "\n")
            setpts = info["setpts"]
            perms = group_perms(pts, setpts, mode)
            inp = f"{len(setpts)} {len(perms)} {K}\n" + "".join(f"{pts[i][0]} {pts[i][1]}\n" for i in setpts)
            inp += "".join(" ".join(map(str, p)) + "\n" for p in perms)
            out = subprocess.run([geomcount], input=inp, capture_output=True, text=True, check=True).stdout
            g = dict(kv.split("=") for kv in out.split())
            rows.append({"dist": dist, "geom": g, "pts": pts})
    ev = subprocess.run([cnfeval, cnf, str(nX), asg_path], capture_output=True, text=True, check=True)
    evrows = [dict(kv.split("=") for kv in line.split()) for line in ev.stdout.strip().splitlines()]
    assert len(evrows) == len(rows)
    mism = 0
    nfree = 0
    details = []
    for r, e in zip(rows, evrows):
        g = r["geom"]
        ok = int(g["collinear"]) == 0 and int(e["xonly_violated"]) == 0 and int(e["missing"]) == 0
        top = K if info.get("kgon", "layered") == "layered" else 5   # direct: only conv_4 flags
        for lev in range(4, top):
            ok &= int(e.get(f"true_level{lev}", 0)) == int(g[f"orbits{lev}"])
        ok &= int(e["kfalse"]) == int(g[f"orbits{K}"])
        ok &= int(e["sat"]) == (1 if int(g[f"orbits{K}"]) == 0 else 0)
        nfree += int(g[f"orbits{K}"]) == 0
        if not ok:
            mism += 1
            if mism <= 3:
                details.append({"eval": e, "geom": g, "dist": r["dist"]})
    summary = {"cnf": os.path.basename(cnf), "mode": mode, "N": info["N"], "K": K, "samples": len(rows),
               "tries": tries, "map_conflicts": conflicts, "mismatches": mism, "kgon_free_samples": nfree,
               "dists": {d: sum(1 for r in rows if r["dist"] == d) for d in ("box", "cluster", "annulus", "small")},
               "kgon_orbits_range": [min(int(r["geom"][f"orbits{K}"]) for r in rows),
                                     max(int(r["geom"][f"orbits{K}"]) for r in rows)],
               "cnfeval_stderr": ev.stderr.strip().splitlines()}
    if details:
        summary["first_mismatches"] = details
    print(json.dumps(summary))
    sys.exit(1 if (mism or conflicts) else 0)


if __name__ == "__main__":
    main()
