#!/usr/bin/env python3
"""Wave-2 start sets: 8 further near-miss seeds (random.Random(2027), excluding
wave 1's) and 4 fresh plain / 3-fold / mirror random starts (random.Random(8)).
Same constructions and exact general-position check as make_starts.py."""
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
seeds = []
for fn in ["../../inputs/nearfull_p2c.txt", "../../inputs/nearfull_p2d.txt"]:
    for i, l in enumerate(open(fn)):
        t = l.split(); v = list(map(int, t[3:])); seeds.append((os.path.basename(fn)[9:12] + f"_{i}", list(zip(v[0::2], v[1::2]))))
used = set(f[3:-4] for f in os.listdir("starts") if f.startswith("nm_"))
rng = random.Random(2027)
for lab, P in rng.sample([s for s in seeds if s[0] not in used], 8): write("nm_" + lab, P)
rng = random.Random(8)
for s in range(4, 8):
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
