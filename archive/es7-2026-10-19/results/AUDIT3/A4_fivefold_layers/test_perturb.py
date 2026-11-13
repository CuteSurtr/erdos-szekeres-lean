#!/usr/bin/env python3
"""Adversarial test of the 'auxiliary centre in general position' step (SYM5 README section 1), audit A4.
Builds exact fivefold configurations in which the centre c is collinear with points of different orbits (orbit 1 is
a real multiple of orbit 0, so its points lie on the rays from c through orbit 0): the sector normal form is then
undefined. Then rotates the orbits by their own small angles, exactly: multiplying orbit o by w or conj(w) (w = K +
zeta, |w/conj(w)| = 1) is a per-orbit rotation by +-arg(w) composed with the common scaling |w|. Checks exactly that
the chirotope of the set points is unchanged, that c is now in general position, and that the perturbed set satisfies
the layer-form and angle-form CNFs (T = D = 0, K = convex 7-sets / 5) for every labelling choice.
usage: test_perturb.py NCONF SEED"""
import sys, random, itertools, math, cmath
from geo import Z5, Config, convex_layers, convex_counts
from labels import layer_labelling, angle_labelling
from evalcnf import CNF

NC, SEED = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(SEED)
t = 3
FL = CNF("work/c5L_15.cnf", "work/c5L_15.json")
FA = CNF("work/c5A_15.cnf", "work/c5A_15.json")
GOLD_INV = Z5.norm((0, 1, 0, 0, 1))          # zeta + zeta^4 = 2 cos 72 = 0.618..., a real element
stats = {"configs": 0, "centre_collinear_before": 0, "chirotope_preserved": 0, "centre_general_after": 0,
         "evaluations": 0, "T": 0, "D": 0, "K_mismatch": 0}
while stats["configs"] < NC:
    p = tuple(rnd.randint(-400, 400) for _ in range(4)) + (0,)
    p = Z5.norm(p)
    q1 = Z5.mul(p, GOLD_INV)                     # on the ray c -> p
    q2 = tuple(rnd.randint(-120, 120) for _ in range(4)) + (0,)
    q2 = Z5.norm(q2)
    cfg = Config(Z5, [p, q1, q2])
    if not cfg.general_position():
        continue
    layers = convex_layers(cfg)
    if not all(len(L) == 5 and len({i // 5 for i in L}) == 1 for L in layers):
        continue
    assert not cfg.centre_general()              # by construction c, p, q1 are collinear
    stats["centre_collinear_before"] += 1
    try:                                         # the sector normal form must be undefined before perturbing
        layer_labelling(cfg, [L[0] // 5 for L in layers], j00=0)
        stats["unperturbed_labelling_defined"] = stats.get("unperturbed_labelling_defined", 0) + 1
    except AssertionError:
        stats["unperturbed_labelling_undefined"] = stats.get("unperturbed_labelling_undefined", 0) + 1
    K = rnd.randint(2000, 5000)
    w = Z5.norm((K, 1, 0, 0, 0))
    wb = Z5.conj(w)
    signs = [rnd.choice((w, wb)) for _ in range(t)]
    if signs[0] == signs[1]:
        signs[1] = w if signs[0] == wb else wb   # orbits 0 and 1 must rotate relative to each other
    cfg2 = Config(Z5, [Z5.mul(x, s) for x, s in zip([p, q1, q2], signs)])
    same = all(cfg.chi(i, j, k) == cfg2.chi(i, j, k) for i, j, k in itertools.combinations(range(cfg.n), 3))
    stats["chirotope_preserved"] += same
    gen = cfg2.centre_general()
    stats["centre_general_after"] += gen
    stats["configs"] += 1
    if not (same and gen):
        print("perturbation failed", same, gen)
        continue
    c7 = convex_counts(cfg2, 7)[0][7]
    layers = convex_layers(cfg2)
    lo = [L[0] // 5 for L in layers]
    labs = [(FL, layer_labelling(cfg2, lo, j00=j)) for j in range(5)]
    labs += [(FA, angle_labelling(cfg2, o0, j00=j)) for o0 in range(t) for j in range(5)]
    for F, lab in labs:
        lab[15] = Z5.zero
        tv = F.triple_values(lambda a, b, c: Z5.orient(lab[a], lab[b], lab[c]))
        res, _ = F.evaluate(tv)
        stats["evaluations"] += 1
        stats["T"] += res["T"]
        stats["D"] += res["D"]
        stats["K_mismatch"] += res["K"] != c7 // 5
print(stats)
