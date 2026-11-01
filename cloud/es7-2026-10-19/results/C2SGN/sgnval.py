#!/usr/bin/env python3
"""Real-set test of sgn.py: random centrally symmetric integer sets in general position (with a parallelogram hull for
--par), labelled by the encoder's normal form; the formula plus the set's orientation units must be SAT iff the set
has no K points in convex position (brute force over K-subsets with an exact convex hull).
usage: sgnval.py TRIALS SEED [--par] [--centre]"""
import itertools, json, os, random, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(D, "..", "local", "bin", "cadical")
det = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull_size(Q):
    P = sorted(Q)
    def chain(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and det(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h
    return len(chain(P)) + len(chain(P[::-1])) - 2


def has_convex(P, K):
    return any(hull_size(S) == K for S in itertools.combinations(P, K))


def general(P):
    return all(det(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def rnd_set(rng, m, par):
    while True:
        if par:
            while True:
                A = (rng.randint(-9, 9), rng.randint(-9, 9)); B = (rng.randint(-9, 9), rng.randint(-9, 9))
                if A[0] * B[1] - A[1] * B[0] > 0: break
            Dd = 1000
            c0 = (Dd * (A[0] + B[0]), Dd * (A[1] + B[1])); c1 = (Dd * (B[0] - A[0]), Dd * (B[1] - A[1]))
            P = [c0, c1, (-c0[0], -c0[1]), (-c1[0], -c1[1])]
            for _ in range(m):
                u, v = rng.randint(-Dd + 1, Dd - 1), rng.randint(-Dd + 1, Dd - 1)
                p = (u * A[0] + v * B[0], u * A[1] + v * B[1]); P += [p, (-p[0], -p[1])]
            if len(set(P)) == len(P) and general(P):
                if RS:   # take the edge pair whose diagonal class holds at least half of the inner pairs
                    inner = [p for p in P[4:]]
                    def cls(e0, e1):   # pairs with one point in the angular sector (e0, e1) around the origin
                        O = (0, 0)
                        return sum(1 for q in inner[0::2] if (det(O, e0, q) > 0) == (det(O, q, e1) > 0))
                    m = len(inner) // 2
                    if cls(c0, c1) < (m + 1) // 2:
                        c0, c1 = c1, (-c0[0], -c0[1])
                n = (c1[1] - c0[1], -(c1[0] - c0[0])); t = (c1[0] - c0[0], c1[1] - c0[1])
                key = lambda p: (n[0] * p[0] + n[1] * p[1], t[0] * p[0] + t[1] * p[1])
                S = sorted(P, key=key)
                assert S[-1] == c1 and S[-2] == c0
                return S
        else:
            P = []
            for _ in range(m):
                p = (rng.randint(-60, 60), rng.randint(-60, 60)); P += [p, (-p[0], -p[1])]
            if len(set(P)) == len(P) and (0, 0) not in P and general(P):
                return sorted(P)


RS = "--rs" in sys.argv
def run(trials, seed, par, centre):
    rng = random.Random(seed); stats = {"sat": 0, "unsat": 0, "mismatch": 0}; cache = {}
    for tr in range(trials):
        m = rng.choice([4, 5, 6, 7]) if par else rng.choice([6, 7, 8, 9])
        S = rnd_set(rng, m, par); n = len(S)
        mc = 3
        while mc + 1 <= n and has_convex(S, mc + 1): mc += 1
        K = mc + rng.choice([0, 1])
        if K < 4 or K > 8 or K > n: continue
        assert all(S[n - 1 - i] == (-S[i][0], -S[i][1]) for i in range(n))
        key = (n, K)
        if key not in cache:
            f = os.path.join(D, f"val_{n}_{K}_{int(par)}{int(centre)}.cnf"); mp = f + ".json"
            cmd = [sys.executable, os.path.join(D, "sgn.py"), str(n), str(K), "--sym", "-o", f, "--map", mp]
            if par: cmd.append("--par")
            if centre: cmd.append("--centre")
            if RS: cmd.append("--rs")
            subprocess.run(cmd, check=True, capture_output=True)
            cache[key] = (f, json.load(open(mp)))
        f, mp = cache[key]
        units = []
        for i, j, k, v in mp["triples"]:
            d = det(S[i - 1], S[j - 1], S[k - 1]); units.append(v if d > 0 else -v)
            # the symmetric image must have the opposite orientation
            i2, j2, k2 = n + 1 - k, n + 1 - j, n + 1 - i
            assert (det(S[i2 - 1], S[j2 - 1], S[k2 - 1]) > 0) == (d < 0)
        txt = open(f).read().splitlines()
        hdr = [l for l in txt if l.startswith("p cnf")][0].split()
        body = [l for l in txt if not l.startswith(("p", "c"))]
        g = f + ".t.cnf"
        with open(g, "w") as h:
            h.write(f"p cnf {hdr[2]} {int(hdr[3]) + len(units)}\n" + "\n".join(body) + "\n" + "".join(f"{u} 0\n" for u in units))
        r = subprocess.run([CAD, "-q", g], capture_output=True, text=True)
        sat = r.returncode == 10
        assert r.returncode in (10, 20), r.stdout[-500:]
        expect = not has_convex(S, K)
        stats["sat" if sat else "unsat"] += 1
        if sat != expect:
            stats["mismatch"] += 1; print("MISMATCH", n, K, S, sat, expect)
    print(json.dumps({"trials": trials, "seed": seed, "par": par, "centre": centre, **stats}))


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), "--par" in sys.argv, "--centre" in sys.argv)
