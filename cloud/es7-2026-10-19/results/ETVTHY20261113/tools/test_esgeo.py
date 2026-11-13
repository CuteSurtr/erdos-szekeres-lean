import random, sys
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import quick, brute, Analysis
random.seed(1)
bad = 0
for trial in range(300):
    n = random.randint(3, 11)
    xs = random.sample(range(-1000, 1000), n)
    P = [(x, random.randint(-1000, 1000)) for x in xs]
    q = quick(P)
    if q[0] < 0: continue
    b = brute(P)
    if (q[0] if q[0] >= 3 else b[0]) != b[0] or q[1] != b[1] or q[2] != b[2]:
        bad += 1; print('MISMATCH', P, q, b)
print('done, mismatches', bad)
