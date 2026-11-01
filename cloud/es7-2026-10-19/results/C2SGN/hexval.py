#!/usr/bin/env python3
"""Real-set test of sgn.py --hexk: random centrally symmetric integer sets in general position whose hull is a hexagon,
labelled in the normal form (edge A -> B counter-clockwise, x-direction tilted towards B, k = position of the vertex
after B); formula + orientation units must be SAT iff the set has no K points in convex position.
usage: hexval.py TRIALS SEED [--centre]"""
import json, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgnval import det, general, has_convex, CAD, D
def hull(Q):
    def chain(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and det(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    Q = sorted(Q); lo, up = chain(Q), chain(Q[::-1]); return lo[:-1] + up[:-1]
T, seed = int(sys.argv[1]), int(sys.argv[2]); centre = "--centre" in sys.argv
rng = random.Random(seed); res = {"sat": 0, "unsat": 0, "mismatch": 0}; cache = {}; done = 0
while done < T:
    m = rng.choice([5, 6, 7, 8]); P = []
    for _ in range(m):
        p = (rng.randint(-80, 80), rng.randint(-80, 80)); P += [p, (-p[0], -p[1])]
    if len(set(P)) != len(P) or (0, 0) in P or not general(P): continue
    H = hull(P)
    if len(H) != 6: continue
    e = rng.randrange(6); A, Bv, Cv = H[e], H[(e + 1) % 6], H[(e + 2) % 6]
    nv = (Bv[1] - A[1], -(Bv[0] - A[0])); t = (Bv[0] - A[0], Bv[1] - A[1])
    S = sorted(P, key=lambda p: (nv[0] * p[0] + nv[1] * p[1], t[0] * p[0] + t[1] * p[1])); n = len(S)
    assert S[-1] == Bv and S[-2] == A and all(S[n - 1 - i] == (-S[i][0], -S[i][1]) for i in range(n))
    k = S.index(Cv) + 1
    mc = 3
    while mc + 1 <= n and has_convex(S, mc + 1): mc += 1
    K = mc + rng.choice([0, 1])
    if K < 4 or K > 8: continue
    key = (n, K, k)
    if key not in cache:
        f = os.path.join(D, f"hv_{n}_{K}_{k}_{int(centre)}.cnf")
        cmd = [sys.executable, os.path.join(D, "sgn.py"), str(n), str(K), "--sym", "--hexk", str(k), "-o", f, "--map", f + ".json"]
        if centre: cmd.append("--centre")
        subprocess.run(cmd, check=True, capture_output=True)
        txt = open(f).read().splitlines(); hdr = [l for l in txt if l.startswith("p cnf")][0].split()
        cache[key] = (json.load(open(f + ".json")), hdr, [l for l in txt if not l.startswith(("p", "c"))], f)
    mp, hdr, body, f = cache[key]
    units = [v if det(S[i - 1], S[j - 1], S[kk - 1]) > 0 else -v for i, j, kk, v in mp["triples"]]
    with open(f + ".t.cnf", "w") as h:
        h.write(f"p cnf {hdr[2]} {int(hdr[3]) + len(units)}\n" + "\n".join(body) + "\n" + "".join(f"{u} 0\n" for u in units))
    r = subprocess.run([CAD, "-q", f + ".t.cnf"], capture_output=True, text=True); sat = r.returncode == 10
    expect = not has_convex(S, K); res["sat" if sat else "unsat"] += 1; done += 1
    if sat != expect: res["mismatch"] += 1; print("MISMATCH", n, K, k, S)
print(json.dumps({"trials": T, "seed": seed, "centre": centre, **res}))
