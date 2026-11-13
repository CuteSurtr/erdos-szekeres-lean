#!/usr/bin/env python3
"""Positive control for the evaluators: evalcnf (in memory), evalstream (pure Python streaming) and evalchunk (numpy
chunks) must give identical violation counts, including on configurations with convex 7-gons (K > 0) and on wrong
labellings (T > 0). usage: test_agree.py m N NCONF SEED"""
import sys, random, math, cmath
from geo import Z4, Z5, Config, convex_layers, convex_counts
from labels import layer_labelling
from evalcnf import CNF
from evalstream import StreamCNF
from evalchunk import ChunkCNF

m, N, NC, SEED = map(int, sys.argv[1:5])
ring = {4: Z4, 5: Z5}[m]
t = N // m
rnd = random.Random(SEED)
W5 = cmath.exp(2j * math.pi / 5)
base = f"work/c{m}L_{N}"
E = [CNF(base + ".cnf", base + ".json"), StreamCNF(base + ".cnf", base + ".json"),
     ChunkCNF(base + ".cnf", base + ".json", chunk=1 << 20)]


def point(z):
    if ring is Z4:
        return (round(z.real), round(z.imag))
    a2, a3 = rnd.randint(-3, 3), rnd.randint(-3, 3)
    res = z - a2 * W5 ** 2 - a3 * W5 ** 3
    a1 = round(res.imag / math.sin(2 * math.pi / 5))
    a0 = round(res.real - a1 * math.cos(2 * math.pi / 5))
    return Z5.norm((a0, a1, a2, a3, 0))


done = agree = nontriv = 0
while done < NC:
    reps, r = [], 1.0
    for o in range(t):
        r *= rnd.uniform(0.75, 0.99) if o else 1.0
        reps.append(point(cmath.rect(20000 * r, rnd.uniform(0, 2 * math.pi))))
    cfg = Config(ring, reps)
    if not cfg.general_position() or (m == 5 and not cfg.centre_general()):
        continue
    layers = convex_layers(cfg)
    if not all(len(L) == m and len({i // m for i in L}) == 1 for L in layers):
        continue
    lo = [L[0] // m for L in layers]
    c7 = convex_counts(cfg, 7)[0][7]
    for kw in ({}, {"swap": (1, 2)}, {"ccw": False}, {"shift": 1}):
        lab = layer_labelling(cfg, lo, j00=rnd.randrange(m), **kw)
        if m == 5:
            lab[m * t] = ring.zero
        outs = []
        for ev in E:
            tval = ev.triple_values(lambda a, b, c: ring.orient(lab[a], lab[b], lab[c]))
            res, _ = ev.evaluate(tval)
            outs.append(res)
        same = outs[0] == outs[1] == outs[2]
        agree += same
        nontriv += outs[0]["T"] > 0 or outs[0]["K"] > 0
        print(kw, "conv7/m =", c7 // m, outs, "AGREE" if same else "DISAGREE", flush=True)
        done += 1
print(f"agreement {agree}/{done}; non-trivial (some violated clause) {nontriv}/{done}")
