#!/usr/bin/env python3
"""Two-way random test of zcnf.py: random symmetric integer point sets (general position), labelled in zcnf's normal
form (for rot with --hull: (0,0) = the lexicographically smallest point, a hull vertex), chirotope fixed as units.
Required: CNF + units satisfiable  <=>  the largest subset in convex position (exact DP, independent of the chirotope
code) has fewer than K points.
usage: zrandtest.py rot|mirror M T K CNF MAP SAMPLES SEED [--hull] [--axis B]"""
import json, os, random, subprocess, sys, tempfile
from functools import cmp_to_key
from itertools import combinations

kind, m, t, K, cnf, mapf, samples, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
    sys.argv[5], sys.argv[6], int(sys.argv[7]), int(sys.argv[8])
hull = "--hull" in sys.argv
axis = int(sys.argv[sys.argv.index("--axis") + 1]) if "--axis" in sys.argv else 0
CAD = os.environ.get("CADICAL", "cadical")
info = json.load(open(mapf))
assert info["kind"] == kind and info["m"] == m and info["t"] == t and info["K"] == K and info.get("axis", 0) == axis
Zi = info["Z"]
triples = info["triples"]
base = open(cnf).read().split("\n", 2)
hdr = [l for l in base[:2] if l.startswith("p cnf")][0].split()
body = open(cnf).read()
nv, nc = int(hdr[2]), int(hdr[3])
rng = random.Random(seed)

if kind == "rot":
    R = (lambda p: (-p[0], -p[1])) if m == 2 else (lambda p: (-p[1], p[0]))
else:
    R = lambda p: (-p[0], p[1])
def orient(a, b, c):
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]); return (d > 0) - (d < 0)
def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))
def chi(u, v, w):
    d = det3(u, v, w); return (d > 0) - (d < 0)
hom = lambda p: (1, p[0], p[1])
Zvec = (1, 0, 0) if kind == "rot" else (0, 1, 0)

def max_convex(P):          # largest subset in convex position: DP over chains anchored at the lowest point
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

def sample():
    while True:
        S = set(); P = []
        for _ in range(t):
            while True:
                q = (rng.randint(-60, 60), rng.randint(-60, 60))
                if kind == "mirror" and q[0] >= 0: q = (q[0] - 61, q[1])
                orb = [q]
                while R(orb[-1]) != q: orb.append(R(orb[-1]))
                if len(orb) == m and not (set(orb) & S) and q != (0, 0): break
            S.update(orb); P.extend(orb)
        for _ in range(axis):
            while True:
                q = (0, rng.randint(-60, 60))
                if q not in S: break
            S.add(q); P.append(q)
        if all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3)):
            return P

def label(P):
    orbits, seen = [], set()
    for p in P:
        if p in seen: continue
        orb = [p]
        while R(orb[-1]) != p: orb.append(R(orb[-1]))
        seen.update(orb); orbits.append(orb)
    if kind == "rot":
        p00 = min(P) if hull else orbits[0][0]
        k0 = next(i for i, o in enumerate(orbits) if p00 in o); orbits[0], orbits[k0] = orbits[k0], orbits[0]
        Z = (1, 0, 0)
        def rep(orb):
            c = [q for q in orb if chi(Z, hom(p00), hom(q)) > 0 and (m == 2 or chi(Z, hom(R(p00)), hom(q)) < 0)]
            assert len(c) == 1; return c[0]
        reps = [p00] + [rep(o) for o in orbits[1:]]
        rest = sorted(range(1, t), key=cmp_to_key(lambda i, j: -1 if chi(Z, hom(reps[i]), hom(reps[j])) > 0 else 1))
        order = [0] + rest
    else:
        ax = sorted([o[0] for o in orbits if len(o) == 1], key=lambda q: -q[1])
        orbits = [o for o in orbits if len(o) == 2]
        reps = [min(o) for o in orbits]
        order = sorted(range(t), key=lambda i: -reps[i][1])
    lab = {}
    for o, i in enumerate(order):
        q = reps[i]
        for r in range(m):
            lab[o * m + r] = hom(q); q = R(q)
    if kind == "mirror":
        for j, q in enumerate(ax):
            lab[t * m + j] = hom(q)
    lab[Zi] = Zvec
    val = {}
    for a, b, c, v, s in triples:
        x = chi(lab[a], lab[b], lab[c]) * s
        assert x != 0
        if v in val: assert val[v] == x, "identity violated"
        else: val[v] = x
    return [v if x > 0 else -v for v, x in sorted(val.items())]

stats = {"sat_ok": 0, "unsat_ok": 0, "mismatch": 0}
with tempfile.TemporaryDirectory() as d:
    for k in range(samples):
        P = sample()
        units = label(P)
        mc = max_convex(P)
        f = os.path.join(d, "t.cnf")
        with open(f, "w") as fo:
            fo.write(f"p cnf {nv} {nc + len(units)}\n")
            fo.write(body.split("\n", 2)[2] if body.startswith("c ") else body.split("\n", 1)[1])
            fo.write("".join(f"{u} 0\n" for u in units))
        r = subprocess.run([CAD, "-q", f], capture_output=True, text=True).stdout
        sat = "s SATISFIABLE" in r
        assert sat or "s UNSATISFIABLE" in r, r[:200]
        if sat == (mc < K): stats["sat_ok" if sat else "unsat_ok"] += 1
        else:
            stats["mismatch"] += 1
            print("MISMATCH", "sat" if sat else "unsat", "maxconvex", mc, P)
print(f"{kind} m={m} t={t} axis={axis} K={K} hull={hull} samples={samples}: {stats}")
