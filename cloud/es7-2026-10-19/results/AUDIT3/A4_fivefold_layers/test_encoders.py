#!/usr/bin/env python3
"""Exact soundness tests of symcnf_layers.py (m = 5 with auxiliary centre; m = 4 without) and symcnf.py (angle normal
form, m = 5) on random nested regular-polygon configurations (audit A4).

usage: test_encoders.py m N ENC NFREE NANY SEED      ENC in {L, A}
For each configuration: exact general position (and, for m = 5, the centre off every line through two set points),
convex layers, the number of convex 7-sets (angular DP), the labelling in the encoder's normal form for EVERY choice
of the point (0,0) (and for the angle form every choice of orbit 0), and a full evaluation of the CNF.
Expected: no violated T (axiom / centre / normal-form) or D clause, and violated K clauses = (#convex 7-sets)/m.
Negative controls (wrong labellings) must violate T clauses.
"""
import sys, random, json, time, math, cmath
from geo import Z4, Z5, Config, convex_layers, convex_counts
from labels import layer_labelling, angle_labelling
from evalcnf import CNF

m, N, ENC, NFREE, NANY, SEED = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
ring = {4: Z4, 5: Z5}[m]
t = N // m
assert t * m == N
rnd = random.Random(SEED)
SCALE = 20000
W5 = cmath.exp(2j * math.pi / 5)


def point(z):
    if ring is Z4:
        return (round(z.real), round(z.imag))
    a2, a3 = rnd.randint(-3, 3), rnd.randint(-3, 3)
    res = z - a2 * W5 ** 2 - a3 * W5 ** 3
    a1 = round(res.imag / math.sin(2 * math.pi / 5))
    a0 = round(res.real - a1 * math.cos(2 * math.pi / 5))
    return Z5.norm((a0, a1, a2, a3, 0))


def inside_prev(prev_rep, q):
    """q strictly inside the regular polygon orbit(prev_rep) (ccw labelled)"""
    for j in range(m):
        if ring.orient(ring.rot(prev_rep, j), ring.rot(prev_rep, j + 1), q) <= 0:
            return False
    return True


def ok_config(reps):
    cfg = Config(ring, reps)
    if not cfg.general_position():
        return None
    if m % 2 == 1 and not cfg.centre_general():
        return None
    return cfg


def gen(nested, free, tries=400):
    while True:
        reps = []
        r = 1.0
        for o in range(t):
            for _ in range(tries):
                rr = r * rnd.uniform(0.35, 0.99) if (o and nested) else (1.0 if o == 0 else rnd.uniform(0.2, 1.0))
                q = point(cmath.rect(SCALE * rr, rnd.uniform(0, 2 * math.pi)))
                if nested and o and not inside_prev(reps[-1], q):
                    continue
                cfg = ok_config(reps + [q])
                if cfg is None:
                    continue
                if free and convex_counts(cfg, 7)[1] >= 7:
                    continue
                reps.append(q)
                if nested:
                    r = abs(ring.to_complex(q)) / SCALE
                break
            else:
                break
        if len(reps) == t:
            return reps


cnf = CNF(f"work/c{m}{ENC}_{N}.cnf", f"work/c{m}{ENC}_{N}.json")
print(f"formula c{m}{ENC}_{N}: vars {cnf.nv} clauses {cnf.nc} classes {cnf.counts}", flush=True)
summary = {"m": m, "N": N, "enc": ENC, "configs": 0, "free_configs": 0, "evaluations": 0, "T_viol": 0, "D_viol": 0,
           "K_mismatch": 0, "layer_not_orbit": 0, "neg_controls": 0, "neg_controls_caught": 0}
t0 = time.time()
for idx in range(NFREE + NANY):
    free = idx < NFREE
    nested = (ENC == "L") or (rnd.random() < 0.5)
    reps = gen(nested=nested, free=free)
    cfg = Config(ring, reps)
    layers = convex_layers(cfg)
    orb_of = {i: i // m for i in range(cfg.n)}
    single = all(len({orb_of[i] for i in L}) == 1 and len(L) == m for L in layers)
    counts, best = convex_counts(cfg, 7)
    c7 = counts[7]
    assert c7 % m == 0
    if free:
        assert best < 7 and c7 == 0
        # layer lemma check: a 7-gon-free configuration with m >= 4 must have single-orbit layers
        if not single:
            summary["layer_not_orbit"] += 1
    summary["configs"] += 1
    summary["free_configs"] += free
    evals = []
    if ENC == "L":
        if not single:
            continue
        lo = [orb_of[L[0]] for L in layers]
        labs = [(j, layer_labelling(cfg, lo, j00=j)) for j in range(m)]
    else:
        labs = []
        for o0 in range(t):
            for j in range(m):
                labs.append(((o0, j), angle_labelling(cfg, o0, j00=j)))
    for key, lab in labs:
        if cfg.m % 2 == 1:
            lab[m * t] = ring.zero
        tval = cnf.triple_values(lambda a, b, c: ring.orient(lab[a], lab[b], lab[c]))
        res, bad = cnf.evaluate(tval)
        summary["evaluations"] += 1
        summary["T_viol"] += res["T"]
        summary["D_viol"] += res["D"]
        if res["K"] != c7 // m:
            summary["K_mismatch"] += 1
        evals.append((key, res))
    # negative controls (layer form only, on the first labelling)
    neg = []
    if ENC == "L" and t >= 3:
        lo = [orb_of[L[0]] for L in layers]
        muts = {"swap12": dict(swap=(1, 2)), "clockwise": dict(ccw=False), "sector1": dict(shift=1),
                "p00_moved": dict(rotate_p00_only=True), "swap01": dict(swap=(0, 1))}
        for name, kw in muts.items():
            try:
                lab = layer_labelling(cfg, lo, j00=0, **kw)
            except AssertionError:
                continue
            if cfg.m % 2 == 1:
                lab[m * t] = ring.zero
            try:
                tval = cnf.triple_values(lambda a, b, c: ring.orient(lab[a], lab[b], lab[c]))
                res, bad = cnf.evaluate(tval)
                caught = res["T"] > 0
                neg.append((name, res))
            except ValueError as e:      # labelling not consistent with the rotation (orbit inconsistency)
                caught = True
                neg.append((name, "orbit-inconsistent"))
            summary["neg_controls"] += 1
            summary["neg_controls_caught"] += caught
    print(json.dumps({"i": idx, "free": free, "nested": nested, "single_orbit_layers": single, "conv7": c7,
                      "largest_convex": best, "evals": [r for _, r in evals][:3], "n_evals": len(evals),
                      "neg": neg}), flush=True)
summary["seconds"] = round(time.time() - t0, 1)
print("SUMMARY", json.dumps(summary), flush=True)
