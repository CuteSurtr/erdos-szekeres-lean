#!/usr/bin/env python3
"""Check a real centrally symmetric set against sgn.py: find its hull, label it in the --par normal form (if the hull is a
parallelogram) or by x (plain --sym), and test formula + orientation units with CaDiCaL (expect SAT iff no convex K-gon).
usage: realtest.py POINTS K [--centre]"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgnval import det, general, CAD, D
P = [tuple(int(x) for x in l.split()) for l in open(sys.argv[1]) if l.strip()]
K = int(sys.argv[2]); centre = "--centre" in sys.argv
n = len(P); assert sorted(P) == sorted((-x, -y) for x, y in P) and general(P)
Ps = sorted(P)
def hull(Q):
    def chain(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and det(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo, up = chain(Q), chain(Q[::-1]); return lo[:-1] + up[:-1]       # counter-clockwise
H = hull(Ps); print("hull size", len(H))
for par in ([True, False] if len(H) == 4 else [False]):
    if par:
        c0, c1 = H[0], H[1]
        nv = (c1[1] - c0[1], -(c1[0] - c0[0])); t = (c1[0] - c0[0], c1[1] - c0[1])
        S = sorted(P, key=lambda p: (nv[0] * p[0] + nv[1] * p[1], t[0] * p[0] + t[1] * p[1]))
        assert S[-1] == c1 and S[-2] == c0
    else:
        S = sorted(P)
    assert all(S[n - 1 - i] == (-S[i][0], -S[i][1]) for i in range(n))
    f = os.path.join(D, f"real_{n}_{K}_{int(par)}{int(centre)}.cnf")
    cmd = [sys.executable, os.path.join(D, "sgn.py"), str(n), str(K), "--sym", "-o", f, "--map", f + ".json"]
    if par: cmd.append("--par")
    if centre: cmd.append("--centre")
    subprocess.run(cmd, check=True, capture_output=True); mp = json.load(open(f + ".json"))
    units = [v if det(S[i - 1], S[j - 1], S[k - 1]) > 0 else -v for i, j, k, v in mp["triples"]]
    txt = open(f).read().splitlines(); hdr = [l for l in txt if l.startswith("p cnf")][0].split()
    body = [l for l in txt if not l.startswith(("p", "c"))]
    with open(f + ".t.cnf", "w") as h:
        h.write(f"p cnf {hdr[2]} {int(hdr[3]) + len(units)}\n" + "\n".join(body) + "\n" + "".join(f"{u} 0\n" for u in units))
    r = subprocess.run([CAD, "-q", f + ".t.cnf"], capture_output=True, text=True)
    print(json.dumps({"n": n, "K": K, "par": par, "centre": centre, "result": {10: "SAT", 20: "UNSAT"}.get(r.returncode, r.returncode)}))
