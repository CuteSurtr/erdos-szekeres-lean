#!/usr/bin/env python3
"""Generate random exactly mirror-symmetric point sets (one axis point), classify them by an
independent exact convex hull, remove x-ties by a symmetric perturbation (checked to keep the
order type), and write the orientation assignments in both frames.

usage: gen33.py <n_sets> <seed> <outprefix> [npairs=16]
writes <out>.iix.txt (hull-vertex sets in frame ii), <out>.ii.txt (interior sets, frame ii), <out>.i.txt (hull-vertex sets, frame i),
<out>.xs.txt (every set, plain x-sorted frame without y-flip, for m33k7.cnf),
<out>.sets.txt (coordinates), <out>.stats.json
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
from multiprocessing import Pool

DISTS = ["unif", "unif", "top", "bottom", "nearhull", "circle", "parab", "small", "ties", "cluster"]


def make(rng, npairs, dist):
    R = 10**6
    while True:
        if dist == "small":
            R = 40
        if dist == "circle":
            pts = []
            for _ in range(npairs):
                import math
                t = rng.uniform(-math.pi / 2, math.pi / 2); r = rng.uniform(0.9, 1.0)
                pts.append((max(1, int(R * r * math.cos(t))), int(R * r * math.sin(t))))
        elif dist == "parab":
            pts = []
            for _ in range(npairs):
                x = rng.randrange(1, 1000); pts.append((x, x * x + rng.randrange(-3000, 3000)))
        elif dist == "cluster":
            cx = [(rng.randrange(1, R), rng.randrange(-R, R)) for _ in range(3)]
            pts = []
            for _ in range(npairs):
                c = rng.choice(cx); pts.append((max(1, c[0] + rng.randrange(-R // 50, R // 50)), c[1] + rng.randrange(-R // 50, R // 50)))
        elif dist == "ties":
            xs = rng.sample(range(1, 200), (npairs + 1) // 2) * 2  # each |x| at most twice (3 would be collinear)
            pts = [(xs[i], rng.randrange(-R, R)) for i in range(npairs)]
        else:
            pts = [(rng.randrange(1, R), rng.randrange(-R, R)) for _ in range(npairs)]
        ys = [y for _, y in pts]; lo, hi = min(ys), max(ys)
        if dist == "top": y0 = hi + rng.randrange(1, R)
        elif dist == "bottom": y0 = lo - rng.randrange(1, R)
        elif dist == "nearhull":
            span = max(2, (hi - lo) // 20); y0 = rng.choice([hi, lo]) + rng.randrange(-span, span)
        else: y0 = rng.randrange(lo - (hi - lo) // 4 - 1, hi + (hi - lo) // 4 + 1)
        P = [(x, y) for x, y in pts] + [(-x, y) for x, y in pts] + [(0, y0)]
        if len(set(P)) == len(P) and general_position(P):
            return P


def work(args):
    s, seed, npairs = args
    rng = random.Random(seed * 1000003 + s)
    dist = DISTS[s % len(DISTS)]
    P = make(rng, npairs, dist)
    assert is_mirror(P)
    st = {"ties": 0, "perturbed": 0}
    xs = [x for x, _ in P]
    o0 = orient_all(P)
    hv = hull_vertices(P)
    p = P.index([q for q in P if q[0] == 0][0])
    vertex = p in hv
    yext = all(q[1] < P[p][1] for q in P if q != P[p]) or all(q[1] > P[p][1] for q in P if q != P[p])
    assert vertex == yext, "hull vertex <=> y-extreme claim failed"
    tries = 0
    while True:
        need = len(set(abs(x) for x in xs if x != 0)) < npairs
        if vertex and not need:
            try: Hall, si = frame_i(P)
            except AssertionError: need = True
        if not need: break
        st["ties"] = 1; tries += 1
        P2 = sym_perturb(P, rng)
        assert is_mirror(P2) and np.array_equal(orient_all(P2), o0), "perturbation changed order type"
        P = P2; xs = [x for x, _ in P]; st["perturbed"] = 1
        if tries > 5: raise RuntimeError("perturb failed")
    Qx = sorted(P); sx = orient_all(Qx)
    # direct sign-rule check X(i,j,k) == X(N+1-k, N+1-j, N+1-i)
    N = len(P); T = tri(N); index = {tuple(t): n for n, t in enumerate(T.tolist())}
    rule_bad = sum(1 for n, (i, j, k) in enumerate(T.tolist()) if sx[index[(N - 1 - k, N - 1 - j, N - 1 - i)]] != sx[n])
    out = {"id": f"s{seed}_{s}_{dist}", "dist": dist, "vertex": vertex, "rule_bad": rule_bad, **st,
           "xs": bits(sx), "P": P}
    if vertex:
        Hall, si = frame_i(P); out["i"] = bits(si)
        Q, s2, fl = frame_ii(P); out["iix"] = bits(s2)  # plain frame: interior clause must fail
    else:
        Q, s2, fl = frame_ii(P); out["ii"] = bits(s2); out["flipped"] = fl
    return out


if __name__ == "__main__":
    n, seed, pre = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    npairs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    fi, fii, fxs, fs, fiix = (open(pre + e, "w") for e in (".i.txt", ".ii.txt", ".xs.txt", ".sets.txt", ".iix.txt"))
    tot = {"n": 0, "vertex": 0, "interior": 0, "rule_bad": 0, "ties": 0, "flipped": 0, "by_dist": {}}
    with Pool(os.cpu_count()) as pool:
        for r in pool.imap_unordered(work, [(s, seed, npairs) for s in range(n)], chunksize=8):
            tot["n"] += 1; tot["rule_bad"] += r["rule_bad"]; tot["ties"] += r["ties"]
            d = tot["by_dist"].setdefault(r["dist"], [0, 0]); d[0 if r["vertex"] else 1] += 1
            fxs.write(f"{r['id']} {r['xs']}\n")
            fs.write(r["id"] + " " + " ".join(f"{x} {y}" for x, y in r["P"]) + "\n")
            if r["vertex"]: tot["vertex"] += 1; fi.write(f"{r['id']} {r['i']}\n"); fiix.write(f"{r['id']} {r['iix']}\n")
            else: tot["interior"] += 1; tot["flipped"] += r["flipped"]; fii.write(f"{r['id']} {r['ii']}\n")
    json.dump(tot, open(pre + ".stats.json", "w"), indent=1); print(json.dumps(tot))
