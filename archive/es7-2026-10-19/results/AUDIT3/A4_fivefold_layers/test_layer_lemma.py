#!/usr/bin/env python3
"""Empirical check of the layer lemma on NON-nested random m-fold sets (audit A4): orbit radii and angles independent
and uniform, exact arithmetic. For every set in general position: if it has no convex 7-gon, every convex layer must
be a single orbit; and whenever some layer is not a single orbit, the largest convex subset must have >= 2m points.
usage: test_layer_lemma.py m TMIN TMAX NPER SEED"""
import sys, random, math, cmath
from geo import Z4, Z5, Config, convex_layers, convex_counts

m, TMIN, TMAX, NPER, SEED = map(int, sys.argv[1:6])
ring = {4: Z4, 5: Z5}[m]
rnd = random.Random(SEED)
W5 = cmath.exp(2j * math.pi / 5)


def point(z):
    if ring is Z4:
        return (round(z.real), round(z.imag))
    a2, a3 = rnd.randint(-3, 3), rnd.randint(-3, 3)
    res = z - a2 * W5 ** 2 - a3 * W5 ** 3
    a1 = round(res.imag / math.sin(2 * math.pi / 5))
    a0 = round(res.real - a1 * math.cos(2 * math.pi / 5))
    return Z5.norm((a0, a1, a2, a3, 0))


st = {"sets": 0, "free": 0, "free_single": 0, "nonsingle": 0, "nonsingle_with_2m_convex": 0, "violations": 0}
for t in range(TMIN, TMAX + 1):
    n = 0
    while n < NPER:
        reps = [point(cmath.rect(20000 * rnd.uniform(0.2, 1.0), rnd.uniform(0, 2 * math.pi))) for _ in range(t)]
        cfg = Config(ring, reps)
        if not cfg.general_position():
            continue
        n += 1
        st["sets"] += 1
        layers = convex_layers(cfg)
        single = all(len(L) == m and len({i // m for i in L}) == 1 for L in layers)
        _, best = convex_counts(cfg, 7)
        if best < 7:
            st["free"] += 1
            st["free_single"] += single
            st["violations"] += not single
        if not single:
            st["nonsingle"] += 1
            st["nonsingle_with_2m_convex"] += best >= 2 * m
            st["violations"] += best < 2 * m
print(f"m={m} t={TMIN}..{TMAX}:", st)
