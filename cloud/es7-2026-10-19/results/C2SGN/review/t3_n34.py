#!/usr/bin/env python3
"""n = 34 clause-level tests of sgn.py --sym --par --centre --rs (the formula of interest, K=7) and of the same options
with K = maxconv+1 (then EVERY clause must hold), on random and adversarial real configurations.

Generators (all exact integers, centrally symmetric, general position, parallelogram hull, 15 inner pairs):
  uniform   : uniform inner points in the parallelogram
  ext32     : the real 7-gon-free 32-point set plus one random inner pair
  ties      : many inner points sharing u- or v-coordinates (equal distance to a hull edge => tie in nu)
  axis      : one inner pair with nu.p = 0 for some edge (p and -p tie in nu)
  diag      : inner points within 1 of the diagonals u = +-v
  edge      : inner points within 1-2 of the hull edges
  ctr       : inner pairs nearly collinear with the centre (det(p,q) = +-1)
usage: t3_n34.py GEN SEED TRIALS [--k7only]"""
import json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build
from t2_cnf import check, summarize, load32

N = 34; MP = 15


def gen(kind, rng):
    R = 1000
    while True:
        if kind == "uniform":
            P = rand_par_set(rng, MP, R=R)
        elif kind == "ext32":
            Q = load32(); H = hull_ccw(Q)
            # random point inside the parallelogram H, via barycentric combination with integer weights
            w = [rng.randint(1, 50) for _ in range(4)]; sw = sum(w)
            Qs = [(x * sw, y * sw) for x, y in Q]
            p = (sum(w[i] * H[i][0] for i in range(4)) + rng.randint(-sw, sw) * 0,
                 sum(w[i] * H[i][1] for i in range(4)) + rng.randint(-sw * 1000, sw * 1000))
            P = Qs + [p, neg(p)]
            if len(set(P)) != len(P) or not general_position(P) or len(hull_ccw(P)) != 4:
                continue
        elif kind == "ties":
            vals = rng.sample(range(-R + 1, R), 10)
            def f(rng, R, vals=vals):
                return (rng.choice(vals), rng.randint(-R + 1, R - 1)) if rng.random() < 0.5 else (rng.randint(-R + 1, R - 1), rng.choice(vals))
            P = rand_par_set(rng, MP, R=R, inner_fn=f)
        elif kind == "axis":
            first = [True]
            def f(rng, R, first=first):
                if first[0]:
                    first[0] = False
                    return (0, rng.randint(1, R - 1)) if rng.random() < 0.5 else (rng.randint(1, R - 1), 0)
                return rng.randint(-R + 1, R - 1), rng.randint(-R + 1, R - 1)
            P = rand_par_set(rng, MP, R=R, inner_fn=f)
        elif kind == "diag":
            def f(rng, R):
                if rng.random() < 0.4:
                    u = rng.randint(-R + 60, R - 60); e = rng.randint(-50, 50) or 1
                    return (u, u + e) if rng.random() < 0.5 else (u, -u + e)
                return rng.randint(-R + 1, R - 1), rng.randint(-R + 1, R - 1)
            P = rand_par_set(rng, MP, R=100000, inner_fn=f)
        elif kind == "edge":
            def f(rng, R):
                if rng.random() < 0.4:
                    a = rng.choice([R - 1, R - 2, -R + 1, -R + 2]) + 0; b = rng.randint(-R + 1, R - 1)
                    a = a - (rng.randint(0, 40) if a > 0 else -rng.randint(0, 40))
                    return (a, b) if rng.random() < 0.5 else (b, a)
                return rng.randint(-R + 1, R - 1), rng.randint(-R + 1, R - 1)
            P = rand_par_set(rng, MP, R=100000, inner_fn=f)
        elif kind == "ctr":
            base = []
            def f(rng, R, base=base):
                if base and rng.random() < 0.7:
                    u, v = rng.choice(base)
                    # q with u*q2 - v*q1 = +-1 does not exist in general; use q = k*(u,v) + small, det = small
                    k = rng.choice([2, 3]) if max(abs(u), abs(v)) * 3 < R else 1
                    q = (k * u + rng.choice([-1, 1]), k * v)
                    if max(abs(q[0]), abs(q[1])) < R:
                        return q
                u, v = rng.randint(-R // 3, R // 3), rng.randint(-R // 3, R // 3); base.append((u, v)); return (u, v)
            P = rand_par_set(rng, MP, R=R, inner_fn=f)
        else:
            raise ValueError(kind)
        if P is not None and len(P) == N and len(hull_ccw(P)) == 4:
            return P


if __name__ == "__main__":
    kind, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); k7only = "--k7only" in sys.argv
    rng = random.Random(seed); t0 = time.time()
    F7 = build(N, 7, par=True, centre=True, rs=True)
    res7, resK = [], []
    Fs = {}
    for tr in range(T):
        P = gen(kind, rng)
        S, info = par_normal_form(P, rs=True, choice=rng.randrange(2))
        assert info["m"] == MP and info["class"] >= 8 and info["ngood"] == 2
        r = check(F7, S, use_sat=(tr % 4 == 0)); res7.append(r)
        if not k7only:
            K = r["maxconv"] + 1
            if K not in Fs:
                Fs[K] = build(N, K, par=True, centre=True, rs=True)
            resK.append(check(Fs[K], S, use_sat=(tr % 4 == 1)))
    summarize(res7, f"n=34 K=7 formula of interest, gen={kind}")
    from collections import Counter
    print("  maxconv distribution", sorted(Counter(r["maxconv"] for r in res7).items()),
          " falsified (K=7) min/max", min(r["falsified"] for r in res7), max(r["falsified"] for r in res7),
          " sat-checked", sum(1 for r in res7 if "sat_with_o_units" in r),
          " SAT among them", sum(1 for r in res7 if r.get("sat_with_o_units")))
    if not k7only:
        summarize(resK, f"n=34 K=maxconv+1 (every clause must hold), gen={kind}")
        print("  sat-checked", sum(1 for r in resK if "sat_with_o_units" in r), "SAT", sum(1 for r in resK if r.get("sat_with_o_units")))
    print("time", round(time.time() - t0, 1))
