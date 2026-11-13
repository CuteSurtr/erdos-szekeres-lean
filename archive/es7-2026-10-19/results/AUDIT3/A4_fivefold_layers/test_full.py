#!/usr/bin/env python3
"""Full-size check (audit A4): random real m-fold nested configurations of the solved size, evaluated exactly against
the regenerated (hash-identical) solved CNF by chunked streaming. A real configuration of that size must have convex
7-gons (otherwise it would be a counterexample); the test checks that ONLY K-set clauses are violated, and exactly
(#convex 7-sets)/m of them, i.e. that no axiom, centre, sector, order or layer clause of the solved formula is
violated by a real configuration. One wrong labelling per configuration is a negative control.
usage: test_full.py m N ENC NCONF SEED CNF MAP"""
import sys, random, math, cmath, time, json, functools
from geo import Z4, Z5, Config, convex_layers, convex_counts
from labels import layer_labelling, angle_labelling
from evalchunk import ChunkCNF

m, N, ENC, NC, SEED = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
CNFP, MAPP = sys.argv[6], sys.argv[7]
ring = {4: Z4, 5: Z5}[m]
t = N // m
rnd = random.Random(SEED)
W5 = cmath.exp(2j * math.pi / 5)
F = ChunkCNF(CNFP, MAPP)
print(f"{CNFP}: vars {F.nv} clauses {F.nc}", flush=True)


def point(z):
    if ring is Z4:
        return (round(z.real), round(z.imag))
    a2, a3 = rnd.randint(-3, 3), rnd.randint(-3, 3)
    res = z - a2 * W5 ** 2 - a3 * W5 ** 3
    a1 = round(res.imag / math.sin(2 * math.pi / 5))
    a0 = round(res.real - a1 * math.cos(2 * math.pi / 5))
    return Z5.norm((a0, a1, a2, a3, 0))


tot = {"configs": 0, "T": 0, "D": 0, "K_mismatch": 0, "neg": 0, "neg_caught": 0}
while tot["configs"] < NC:
    reps, r = [], 1.0
    for o in range(t):
        if ENC == "L":
            lo_, hi_ = (0.80, 0.97) if m == 5 else (0.60, 0.90)
            r *= rnd.uniform(lo_, hi_) if o else 1.0
            rr = r
        else:
            rr = rnd.uniform(0.3, 1.0)
        reps.append(point(cmath.rect(10 ** 6 * rr, rnd.uniform(0, 2 * math.pi))))
    cfg = Config(ring, reps)
    if not cfg.general_position() or (m == 5 and not cfg.centre_general()):
        continue
    layers = convex_layers(cfg)
    single = all(len(L) == m and len({i // m for i in L}) == 1 for L in layers)
    if ENC == "L" and not single:
        continue
    t0 = time.time()
    cnt, best = convex_counts(cfg, 7)
    c7 = cnt[7]
    if ENC == "L":
        lo = [L[0] // m for L in layers]
        lab = layer_labelling(cfg, lo, j00=rnd.randrange(m))
        bad = layer_labelling(cfg, lo, j00=0, swap=(rnd.randrange(1, t - 1), t - 1))
    else:
        o0 = rnd.randrange(t)
        lab = angle_labelling(cfg, o0, j00=rnd.randrange(m))
        # negative control: exchange the labels of the last two orbits (wrong angular order)
        bad = dict(lab)
        for rr_ in range(m):
            bad[(t - 2) * m + rr_], bad[(t - 1) * m + rr_] = lab[(t - 1) * m + rr_], lab[(t - 2) * m + rr_]
    out = []
    for name, L in (("normal", lab), ("negative", bad)):
        if m == 5:
            L[m * t] = ring.zero
        tv = F.triple_values(lambda a, b, c: ring.orient(L[a], L[b], L[c]))
        res, passes = F.evaluate(tv)
        out.append((name, res, passes))
    tot["configs"] += 1
    n_res = out[0][1]
    tot["T"] += n_res["T"]
    tot["D"] += n_res["D"]
    tot["K_mismatch"] += n_res["K"] != c7 // m
    tot["neg"] += 1
    tot["neg_caught"] += out[1][1]["T"] > 0
    print(json.dumps({"single_orbit_layers": single, "largest_convex": best, "conv7": c7, "conv7_over_m": c7 // m,
                      "results": out, "sec": round(time.time() - t0)}), flush=True)
print("TOTAL", json.dumps(tot), flush=True)
