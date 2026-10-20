#!/usr/bin/env python3
"""Validate gen_c3b.py CNFs on random exact C3-symmetric point sets.

Points: Eisenstein lattice orbits {z, wz, w^2 z} in integer coordinates (a,b); the rotation
is (a,b) -> (-b, a-b) (det 1, order 3).  A random integer linear map (x,y) = (f(a,b), g(a,b))
with det > 0 puts a random line l through the centre on the y-axis (orientation preserving,
so order type and convexity are those of a Euclidean C3 set; identities.py checks the
Euclidean case in Q(sqrt3)).  Everything below is exact (integers / Fractions) and computed
from the coordinates directly, not from the identities:
  labels by y/x, s_i = [x_i < 0], chi' = orientation of phi(p) = (y/x, 1/x),
  chi_S = orientation of S, inv_ij = [1/x_i > 1/x_j], o_ij = [x_i < x_j].
Required per sample:
  * the per-orbit variable values are consistent (no conflict in the X / Y orbit maps,
    and s_i = s_{i mod m} xor [i div m == 1]);
  * every non-k-gon clause is satisfied;
  * the k-gon clauses (least model of the chain variables) are all satisfied iff the set has
    no k points in convex position (brute force: DFS over convex subsets by the 4-point
    Caratheodory test on exact orientations).
usage: validate.py SAMPLES SEED [--mmin 3 --mmax 11] [--ks 5,6,7]
"""
import argparse
import itertools
import json
import os
import random
import subprocess
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
CNFDIR = os.environ.get("C3B_CNFDIR", "/tmp/claude-0/cnf")
CNFEVAL = os.environ.get("CNFEVAL", "/tmp/claude-0/build/cnfeval")


def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(x):
    return (x > 0) - (x < 0)


def random_set(m, rng, R):
    while True:
        base = set()
        while len(base) < m:
            a, b = rng.randint(-R, R), rng.randint(-R, R)
            if (a, b) != (0, 0):
                base.add((a, b))
        pts = []
        for z in sorted(base):
            for _ in range(3):
                pts.append(z)
                z = (-z[1], z[0] - z[1])
        while True:
            f = (rng.randint(-9, 9), rng.randint(-9, 9))
            g = (rng.randint(-9, 9), rng.randint(-9, 9))
            if f[0] * g[1] - f[1] * g[0] > 0:
                break
        P = [(f[0] * a + f[1] * b, g[0] * a + g[1] * b) for a, b in pts]
        n = len(P)
        if len(set(P)) < n or any(p[0] == 0 for p in P):
            continue
        O = (0, 0)
        if any(det(O, P[i], P[j]) == 0 for i in range(n) for j in range(i + 1, n)):
            continue
        if len(set(p[0] for p in P)) < n:
            continue
        if any(det(P[i], P[j], P[k]) == 0 for i, j, k in itertools.combinations(range(n), 3)):
            continue
        # normal form s_0 = 0 (point reflection, which keeps the labels and chi_S)
        i0 = min(range(n), key=lambda i: F(P[i][1], P[i][0]))
        if P[i0][0] < 0:
            P = [(-x, -y) for x, y in P]
        return P


def has_convex_k(chi, n, k):
    """DFS over subsets in convex position (Caratheodory: every 4-subset convex)."""
    def inside(t, a, b, c):
        s = chi(a, b, c)
        return chi(a, b, t) == s and chi(b, c, t) == s and chi(c, a, t) == s

    conv4 = {}
    for Q in itertools.combinations(range(n), 4):
        conv4[Q] = not any(inside(Q[t], *[Q[u] for u in range(4) if u != t]) for t in range(4))

    def rec(cur, start):
        if len(cur) == k:
            return True
        for x in range(start, n):
            ok = True
            if len(cur) >= 3:
                for T in itertools.combinations(cur, 3):
                    if not conv4[T + (x,)]:
                        ok = False
                        break
            if ok and rec(cur + [x], x + 1):
                return True
        return False
    return rec([], 0)


def true_assignment(P, info, mp):
    m, n = info["m"], info["n"]
    order = sorted(range(n), key=lambda i: F(P[i][1], P[i][0]))
    pts = [P[o] for o in order]
    phi = [(F(p[1], p[0]), F(1, p[0])) for p in pts]
    s = [1 if p[0] < 0 else 0 for p in pts]
    conflicts = 0
    val = {}

    def setv(v, b):
        nonlocal conflicts
        if v in val and val[v] != b:
            conflicts += 1
        val[v] = b
    for a, b, c, v, sg in mp["X"]:
        setv(v, sgn(det(phi[a], phi[b], phi[c])) * sg > 0)
    for a, b, c, v, sg in mp["Y"]:
        setv(v, sgn(det(pts[a], pts[b], pts[c])) * sg > 0)
    for r, v in enumerate(mp["s"]):
        setv(v, s[r] == 1)
    for i in range(n):
        if s[i] != s[i % m] ^ (1 if i // m == 1 else 0):
            conflicts += 1
    for i, j, v in mp["I"]:
        setv(v, phi[i][1] > phi[j][1])
    for i, j, v in mp["O"]:
        setv(v, pts[i][0] < pts[j][0])
    assert len(val) == info["primary_vars"]
    chi = lambda a, b, c: sgn(det(pts[a], pts[b], pts[c]))
    return val, conflicts, chi


class Evaluator:
    def __init__(self, m, k):
        base = os.path.join(CNFDIR, f"c3b_m{m}k{k}")
        if not os.path.exists(base + ".cnf"):
            subprocess.run([sys.executable, os.path.join(HERE, "gen_c3b.py"), str(m), str(k),
                            "-o", base + ".cnf", "--map", base + ".json"], check=True,
                           stdout=subprocess.DEVNULL)
        self.mp = json.load(open(base + ".json"))
        self.p = subprocess.Popen([CNFEVAL, base + ".cnf", str(self.mp["primary_vars"]),
                                   str(self.mp["nonkgon_clauses"])],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    def eval(self, val):
        line = " ".join(str(v if b else -v) for v, b in sorted(val.items()))
        self.p.stdin.write(line + "\n")
        self.p.stdin.flush()
        return tuple(map(int, self.p.stdout.readline().split()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("samples", type=int)
    ap.add_argument("seed", type=int)
    ap.add_argument("--mmin", type=int, default=3)
    ap.add_argument("--mmax", type=int, default=11)
    ap.add_argument("--ks", default="5,6,7")
    ap.add_argument("--log")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    ks = [int(x) for x in a.ks.split(",")]
    evs = {}
    stats = {}
    fails = 0
    logf = open(a.log, "a") if a.log else None
    for t in range(a.samples):
        m = a.mmin + t % (a.mmax - a.mmin + 1)
        k = ks[(t // (a.mmax - a.mmin + 1)) % len(ks)]
        if (m, k) not in evs:
            evs[m, k] = Evaluator(m, k)
        ev = evs[m, k]
        R = rng.choice([m, m + 2, 2 * m, 4 * m, 30])
        P = random_set(m, rng, R)
        val, conf, chi = true_assignment(P, ev.mp, ev.mp)
        f1, f2, aux = ev.eval(val)
        gon = has_convex_k(chi, 3 * m, k)
        ok = conf == 0 and f1 == 0 and ((f2 == 0) == (not gon))
        st = stats.setdefault(f"m{m}k{k}", {"n": 0, "kgon_free": 0, "fail": 0})
        st["n"] += 1
        st["kgon_free"] += (not gon)
        if not ok:
            st["fail"] += 1
            fails += 1
            print("FAIL", m, k, R, conf, f1, f2, gon, P, flush=True)
        if logf:
            logf.write(json.dumps({"m": m, "k": k, "R": R, "conflicts": conf, "nonkgon_falsified": f1,
                                   "kgon_falsified": f2, "true_aux": aux, "has_kgon": gon, "ok": ok}) + "\n")
    print(json.dumps({"samples": a.samples, "seed": a.seed, "failures": fails, "per": stats}))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
