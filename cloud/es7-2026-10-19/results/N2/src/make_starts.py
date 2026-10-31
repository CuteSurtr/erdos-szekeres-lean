#!/usr/bin/env python3
"""Make the N2 start sets (exact integers, general position checked exactly).
near-miss: AlphaEvolve's set (integer realization from results/D/calib) plus
7 seeds drawn with random.Random(2026) from inputs/nearfull_p2{c,d}.txt;
random: plain uniform, 3-fold rotational (11 orbits, rounded) and mirror
(16 pairs + 1 axis point) starts, |c| < 2^26."""
import random, math, itertools, os, sys
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
R = 1 << 26
def orient(p, q, r): return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
def gp(P): return len(set(P)) == len(P) and all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))
def write(name, P):
    assert len(P) == 33 and gp(P), name
    with open(os.path.join(OUT, name + ".txt"), "w") as f:
        for x, y in P: f.write(f"{x} {y}\n")
ae = [tuple(map(int, l.split())) for l in open("../D/calib/alphaevolve_int.txt")]
write("nm_ae", ae)
seeds = []
for fn in ["../../inputs/nearfull_p2c.txt", "../../inputs/nearfull_p2d.txt"]:
    for i, l in enumerate(open(fn)):
        t = l.split(); v = list(map(int, t[3:])); seeds.append((os.path.basename(fn)[9:12] + f"_{i}", list(zip(v[0::2], v[1::2]))))
rng = random.Random(2026)
for lab, P in rng.sample(seeds, 7): write("nm_" + lab, P)
rng = random.Random(7)
for s in range(int(sys.argv[2])):
    while True:
        P = [(rng.randrange(-R, R), rng.randrange(-R, R)) for _ in range(33)]
        if gp(P): break
    write(f"rnd_plain_{s}", P)
    while True:
        P = []
        for _ in range(11):
            r = R * math.sqrt(rng.random()); th = rng.uniform(0, 2 * math.pi)
            for k in range(3):
                a = th + 2 * math.pi * k / 3
                P.append((round(r * math.cos(a)), round(r * math.sin(a))))
        if gp(P): break
    write(f"rnd_rot3_{s}", P)
    while True:
        P = [(0, rng.randrange(-R, R))]
        for _ in range(16):
            x, y = rng.randrange(1, R), rng.randrange(-R, R)
            P += [(x, y), (-x, y)]
        if gp(P): break
    write(f"rnd_mirror_{s}", P)
print("ok")
