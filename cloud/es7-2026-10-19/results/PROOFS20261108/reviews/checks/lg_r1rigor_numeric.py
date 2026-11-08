"""Numeric sanity checks of strict_nesting, lin_pos_of_peel, dist2_le_of_later, orient_next_prev_pos
on concrete layered configurations (centre c = 0), exact rational arithmetic where possible."""
import math
import random
from fractions import Fraction as Fr


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def lin(w, a, y):
    return w[0] * (y[0] - a[0]) + w[1] * (y[1] - a[1])


def rot(p, th):
    c, s = math.cos(th), math.sin(th)
    return (c * p[0] - s * p[1], s * p[0] + c * p[1])


ok = True

# 1. The review instance S4 = {(+-2,0),(0,+-2),(+-1/2,+-1/2)}, m = 4 (exact rotation by pi/2).
L0 = [(Fr(2), Fr(0)), (Fr(0), Fr(2)), (Fr(-2), Fr(0)), (Fr(0), Fr(-2))]
L1 = [(Fr(1, 2), Fr(1, 2)), (Fr(-1, 2), Fr(1, 2)), (Fr(-1, 2), Fr(-1, 2)), (Fr(1, 2), Fr(-1, 2))]
rho = lambda p: (-p[1], p[0])
for x in L0:
    for y in L1:
        if not orient(x, rho(x), y) > 0:
            ok = False; print("nesting fails", x, y)
layers = [L0, L1]
for i, Li in enumerate(layers):
    later = [q for Lk in layers[i:] for q in Lk]
    for p in Li:
        w = (-p[0], -p[1])
        for y in later:
            if y != p and not lin(w, p, y) > 0:
                ok = False; print("halfplane fails", p, y)
        pprev = rho(rho(rho(p)))
        if not orient(p, rho(p), pprev) > 0:
            ok = False; print("next_prev fails", p)
print("S4 instance:", "OK" if ok else "FAIL")

# 2. Random nested regular m-gons with decreasing radii and generic phases (floating point):
# conclusions of strict_nesting / lin_pos_of_peel hold when each layer lies strictly inside the previous
# polygon (the situation the layer lemma produces); we only sanity-check the formulas, not the lemma.
random.seed(1)
cnt = 0
for trial in range(300):
    m = random.randint(3, 9)
    t = random.randint(2, 4)
    r = 10.0
    layers = []
    for i in range(t):
        ph = random.uniform(0, 2 * math.pi)
        layers.append([rot((r, 0.0), ph + 2 * math.pi * k / m) for k in range(m)])
        # next radius strictly inside the inscribed circle of this regular m-gon
        r = r * math.cos(math.pi / m) * random.uniform(0.3, 0.95)
    th = 2 * math.pi / m
    for i, Li in enumerate(layers):
        for x in Li:
            for Lk in layers[i + 1:]:
                for y in Lk:
                    cnt += 1
                    if not orient(x, rot(x, th), y) > 1e-12:
                        ok = False; print("nesting fails", m, i)
            w = (-x[0], -x[1])
            for Lk in layers[i:]:
                for y in Lk:
                    if math.dist(x, y) > 1e-9 and not lin(w, x, y) > 1e-12:
                        ok = False; print("halfplane fails", m, i)
                    if not (y[0] ** 2 + y[1] ** 2) <= x[0] ** 2 + x[1] ** 2 + 1e-9:
                        ok = False; print("radius fails", m, i)
print("random nested regular polygons:", "OK" if ok else "FAIL", "pairs checked:", cnt)
