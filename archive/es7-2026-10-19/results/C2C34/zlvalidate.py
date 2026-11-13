#!/usr/bin/env python3
"""Tests of the convex-layer normal form (zlayers.py) on real centrally symmetric sets with integer coordinates.

real   : zlvalidate.py real POINTS MAP CNF   -- POINTS symmetric about the origin; MAP/CNF from zcnf.py rot T K --m 2 --no-sb.
         Labels the set in the layer normal form, and checks with CaDiCaL that
           CNF + layer units of its own profile + its exact chirotope        is SAT,
           CNF + layer units of its own profile (chirotope free)             is SAT,
           CNF + layer units of a different admissible profile + chirotope   is UNSAT (if such a profile exists).
random : zlvalidate.py random T K SAMPLES SEED   -- two-way test on random centrally symmetric integer sets of 2T points:
           CNF + layer units (any layer sizes allowed) + exact chirotope is SAT  <=>  largest convex subset < K.
The solver path is read from CADICAL (default: cadical)."""
import json, os, random, subprocess, sys, tempfile
from functools import cmp_to_key
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlayers import layer_units, profiles

CAD = os.environ.get("CADICAL", "cadical")
HERE = os.path.dirname(os.path.abspath(__file__))


def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))
def chi(u, v, w):
    d = det3(u, v, w); return (d > 0) - (d < 0)
def orient(a, b, c):
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); return (d > 0) - (d < 0)
hom = lambda p: (1, p[0], p[1])
ZV = (1, 0, 0)


def hull_vertices(Q):
    return [d for d in Q if not any(orient(a, b, d) == orient(b, c, d) == orient(c, a, d)
                                    for a, b, c in combinations([q for q in Q if q != d], 3))]


def layer_label(P):
    rest, layers = list(P), []
    while rest:
        V = hull_vertices(rest) if len(rest) > 2 else list(rest)
        layers.append(V); rest = [q for q in rest if q not in V]
    prof = tuple(len(V) // 2 for V in layers)
    p00 = min(layers[0])
    neg = lambda q: (-q[0], -q[1])
    order = []
    for li, V in enumerate(layers):
        reps = []
        for q in V:
            if q == p00 or (q != neg(p00) and chi(ZV, hom(p00), hom(q)) > 0):
                reps.append(q)
        assert len(reps) == len(V) // 2
        reps.sort(key=cmp_to_key(lambda a, b: 0 if a == b else (-1 if (a == p00 or (b != p00 and chi(ZV, hom(a), hom(b)) > 0)) else 1)))
        order += reps
    lab = {}
    for o, q in enumerate(order):
        lab[2 * o] = hom(q); lab[2 * o + 1] = hom(neg(q))
    return prof, lab


def chirotope_units(info, lab):
    lab = dict(lab); lab[info["Z"]] = ZV
    val = {}
    for a, b, c, v, s in info["triples"]:
        x = chi(lab[a], lab[b], lab[c]) * s
        assert x != 0
        if v in val: assert val[v] == x, "identity violated on the real set"
        else: val[v] = x
    return [v if x > 0 else -v for v, x in sorted(val.items())]


def solve(cnf_text_parts, nv, nc_base, extra):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "t.cnf")
        with open(f, "w") as fo:
            fo.write(f"p cnf {nv} {nc_base + len(extra)}\n")
            fo.write(cnf_text_parts)
            fo.write("".join(f"{u} 0\n" for u in extra))
        r = subprocess.run([CAD, "-q", f], capture_output=True, text=True).stdout
    if "s SATISFIABLE" in r: return "SAT"
    if "s UNSATISFIABLE" in r: return "UNSAT"
    raise RuntimeError(r[:300])


def load_cnf(path):
    txt = open(path).read()
    lines = txt.split("\n", 2)
    hdr = lines[1] if lines[0].startswith("c ") else lines[0]
    body = lines[2] if lines[0].startswith("c ") else txt.split("\n", 1)[1]
    _, _, nv, nc = hdr.split()
    return int(nv), int(nc), body


def max_convex(P):
    best = min(len(P), 2)
    for a in P:
        up = [p for p in P if (p[1], p[0]) > (a[1], a[0])]
        up.sort(key=cmp_to_key(lambda p, q: -1 if orient(a, p, q) > 0 else 1))
        n = len(up); D = [[0] * n for _ in range(n)]
        for j in range(n):
            for i in range(j):
                v = 3 if orient(a, up[i], up[j]) > 0 else 0
                if v:
                    for h in range(i):
                        if D[h][i] and orient(up[h], up[i], up[j]) > 0 and D[h][i] + 1 > v: v = D[h][i] + 1
                D[i][j] = v
                if v and orient(up[i], up[j], a) > 0 and v > best: best = v
    return best


def main():
    if sys.argv[1] == "real":
        pts, mapf, cnf = sys.argv[2:5]
        P = [tuple(map(int, l.split()[:2])) for l in open(pts) if l.strip() and not l.startswith("#")]
        assert all((-p[0], -p[1]) in P for p in P)
        info = json.load(open(mapf)); tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
        nv, nc, body = load_cnf(cnf)
        prof, lab = layer_label(P)
        cu = chirotope_units(info, lab)
        lu = layer_units(tv, info["Z"], info["t"], prof)
        print(f"{os.path.basename(pts)}: profile {prof}")
        print("  own profile + chirotope:", solve(body, nv, nc, lu + cu))
        print("  own profile, chirotope free:", solve(body, nv, nc, lu))
        others = [p for p in profiles(info["t"]) if p != prof]
        for p in others[:3]:
            print(f"  other profile {p} + chirotope (must be UNSAT):", solve(body, nv, nc, layer_units(tv, info["Z"], info["t"], p) + cu))
    else:
        t, K, samples, seed = map(int, sys.argv[2:6])
        rng = random.Random(seed)
        base = os.path.join(HERE, "rt", f"lay_t{t}_k{K}")
        if not os.path.exists(base + ".cnf"):
            subprocess.run([sys.executable, os.path.join(HERE, "zcnf.py"), "rot", str(t), str(K), "--m", "2", "--no-sb",
                            "-o", base + ".cnf", "--map", base + ".json"], check=True, capture_output=True)
        info = json.load(open(base + ".json")); tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
        nv, nc, body = load_cnf(base + ".cnf")
        st = {"sat_ok": 0, "unsat_ok": 0, "mismatch": 0}
        for _ in range(samples):
            while True:
                S, P = set(), []
                for _ in range(t):
                    while True:
                        q = (rng.randint(-60, 60), rng.randint(-60, 60))
                        if q != (0, 0) and q not in S and (-q[0], -q[1]) not in S: break
                    S.update([q, (-q[0], -q[1])]); P += [q, (-q[0], -q[1])]
                if all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3)): break
            prof, lab = layer_label(P)
            res = solve(body, nv, nc, layer_units(tv, info["Z"], t, prof, allow_any=True) + chirotope_units(info, lab))
            exp = "SAT" if max_convex(P) < K else "UNSAT"
            if res == exp: st["sat_ok" if res == "SAT" else "unsat_ok"] += 1
            else:
                st["mismatch"] += 1; print("MISMATCH", res, exp, prof, P)
        print(f"layer form random t={t} K={K}: {st}")


if __name__ == "__main__":
    main()
