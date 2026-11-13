#!/usr/bin/env python3
"""Soundness at scale: random antipodal sub-sets of a real symmetric set without a convex K-gon (sym7_32points for
K=7, sym9_128points for K=9) must satisfy sgn.py's formula under the normal-form labelling (--par when the sub-set's
hull is a parallelogram, else plain --sym), with and without --centre.  usage: realsub.py POINTS K TRIALS SEED"""
import json, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgnval import det, CAD, D
P = [tuple(int(x) for x in l.split()) for l in open(sys.argv[1]) if l.strip()]
K, T, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); rng = random.Random(seed)
pairs = sorted({min(p, (-p[0], -p[1])) for p in P})
def hull(Q):
    def chain(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and det(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    Q = sorted(Q); lo, up = chain(Q), chain(Q[::-1]); return lo[:-1] + up[:-1]
cache = {}; res = {"SAT": 0, "UNSAT": 0}
for tr in range(T):
    m = rng.randint(max(4, K - 2), min(len(pairs), 20)); sub = rng.sample(pairs, m)
    Q = sub + [(-x, -y) for x, y in sub]; n = len(Q); H = hull(Q); par = len(H) == 4 and rng.random() < 0.8
    centre = rng.random() < 0.5
    if par:
        c0, c1 = H[0], H[1]; nv = (c1[1] - c0[1], -(c1[0] - c0[0])); t = (c1[0] - c0[0], c1[1] - c0[1])
        S = sorted(Q, key=lambda p: (nv[0] * p[0] + nv[1] * p[1], t[0] * p[0] + t[1] * p[1]))
        assert S[-1] == c1 and S[-2] == c0
    else:
        S = sorted(Q)
    key = (n, par, centre)
    if key not in cache:
        f = os.path.join(D, f"sub_{n}_{K}_{int(par)}{int(centre)}.cnf")
        cmd = [sys.executable, os.path.join(D, "sgn.py"), str(n), str(K), "--sym", "-o", f, "--map", f + ".json"]
        if par: cmd.append("--par")
        if centre: cmd.append("--centre")
        subprocess.run(cmd, check=True, capture_output=True)
        txt = open(f).read().splitlines(); hdr = [l for l in txt if l.startswith("p cnf")][0].split()
        cache[key] = (f, json.load(open(f + ".json")), hdr, [l for l in txt if not l.startswith(("p", "c"))])
    f, mp, hdr, body = cache[key]
    units = [v if det(S[i - 1], S[j - 1], S[k - 1]) > 0 else -v for i, j, k, v in mp["triples"]]
    with open(f + ".t.cnf", "w") as h:
        h.write(f"p cnf {hdr[2]} {int(hdr[3]) + len(units)}\n" + "\n".join(body) + "\n" + "".join(f"{u} 0\n" for u in units))
    r = subprocess.run([CAD, "-q", f + ".t.cnf"], capture_output=True, text=True)
    st = {10: "SAT", 20: "UNSAT"}[r.returncode]; res[st] += 1
    if st != "SAT": print("UNSOUND?", n, par, centre, sorted(sub))
print(json.dumps({"points": os.path.basename(sys.argv[1]), "K": K, "trials": T, **res}))
