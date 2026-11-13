#!/usr/bin/env python3
"""threefold lattice set (lines 'a b' = a + b*omega, omega = e^{2 pi i/3}) -> float orbit configuration JSON (lr, th, centre)."""
import sys, math, cmath, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'py'))
from ptsio import write_cfg
w = cmath.exp(2j * math.pi / 3)
zs = []; centre = 0
for l in open(sys.argv[1]):
    l = l.split('#')[0].split()
    if len(l) < 2: continue
    a, b = int(l[0]), int(l[1])
    if a == 0 and b == 0: centre = 1; continue
    zs.append(a + b * w)
U = 2 * math.pi / 3
reps = {}
for z in zs:
    key = round(math.log(abs(z)), 9)
    reps.setdefault(key, z)
R = sorted(reps.values(), key=lambda z: -abs(z))
r0 = abs(R[0])
lr = [math.log(abs(z) / r0) for z in R]; th = [cmath.phase(z) % U for z in R]
if len(sys.argv) > 3: centre = int(sys.argv[3])
write_cfg(sys.argv[2], 3, lr, th, centre, None, note='from ' + sys.argv[1])
print(len(zs), 'points', len(R), 'orbits', 'centre', centre)
