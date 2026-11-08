"""Exact-rational sanity checks of the cyclic orders in mm.tex (Theorems mirror-polygon, axis-polygon,
Lemma slope(a)), on random concave caps. Not a proof; a check that the written index formulas are right."""
import random
from fractions import Fraction as F
from itertools import combinations

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def mir(p):
    return (p[0], -p[1])

def is_cap(c):
    return all(orient(c[i], c[j], c[l]) < 0 for i, j, l in combinations(range(len(c)), 3))

def rand_cap(m, mode):
    # points on a strictly concave curve; mode: 'above', 'left', 'right'
    xs = sorted(random.sample(range(-60, 60), m))
    xs = [F(x) for x in xs]
    if mode == 'above':
        H = F(random.randint(1, 50))
        f = lambda x: H + F(4000) - x*x / F(random.randint(1, 3)) if False else H + F(4000) - x*x
    elif mode == 'left':
        x0, x1 = xs[0], xs[-1] + 1
        f = lambda x: (x - x0)*(x1 - x)
    else:
        x0, x1 = xs[0] - 1, xs[-1]
        f = lambda x: (x - x0)*(x1 - x)
    c = [(x, f(x)) for x in xs]
    # random concave perturbation keeps the cap property only if small; skip
    return c

random.seed(12345)
bad = 0
count = 0
for trial in range(400):
    m = random.randint(2, 9)
    c = rand_cap(m, 'above')
    assert is_cap(c) and all(p[1] > 0 for p in c)
    q = [mir(c[r]) if r < m else c[2*m-1-r] for r in range(2*m)]
    assert len(set(q)) == 2*m
    for r, s, t in combinations(range(2*m), 3):
        count += 1
        if not orient(q[r], q[s], q[t]) > 0:
            bad += 1
    # Lemma slope(a)
    for i, j in combinations(range(m), 2):
        for l in range(m):
            if c[l][1] > 0 and not orient(c[i], c[j], mir(c[l])) < 0:
                bad += 1
    if m >= 3:
        cl = rand_cap(m, 'left')
        assert is_cap(cl) and cl[0][1] == 0 and all(p[1] > 0 for p in cl[1:])
        ql = [mir(cl[r]) if r < m else cl[2*m-1-r] for r in range(2*m-1)]
        assert len(set(ql)) == 2*m-1
        for r, s, t in combinations(range(2*m-1), 3):
            count += 1
            if not orient(ql[r], ql[s], ql[t]) > 0:
                bad += 1
        for i, j in combinations(range(m), 2):
            for l in range(m):
                if cl[l][1] > 0 and not orient(cl[i], cl[j], mir(cl[l])) < 0:
                    bad += 1
        cr = rand_cap(m, 'right')
        assert is_cap(cr) and cr[-1][1] == 0 and all(p[1] > 0 for p in cr[:-1])
        qr = [mir(cr[r]) if r < m else cr[2*m-2-r] for r in range(2*m-1)]
        assert len(set(qr)) == 2*m-1
        for r, s, t in combinations(range(2*m-1), 3):
            count += 1
            if not orient(qr[r], qr[s], qr[t]) > 0:
                bad += 1
print('triples checked:', count, 'failures:', bad)

# Lemma slope(a) with nonnegative ordinates and an interior point at height 0 is excluded by the cap
# hypothesis; check that the hypothesis y>=0 (not >0) at i, j suffices in case i<l<j:
random.seed(7)
viol = 0
for trial in range(2000):
    xi, xl, xj = sorted(F(random.randint(-50, 50)) for _ in range(3))
    if not (xi < xl < xj):
        continue
    yi = F(random.choice([0, random.randint(0, 30)]))
    yj = F(random.choice([0, random.randint(0, 30)]))
    yl = F(random.randint(1, 30))
    if not orient((xi, yi), (xj, yj), (xl, -yl)) < 0:
        viol += 1
print('slope(a) case i<l<j violations:', viol)
