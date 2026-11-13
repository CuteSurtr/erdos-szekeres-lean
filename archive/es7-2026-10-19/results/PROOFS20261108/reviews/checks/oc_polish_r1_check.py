"""Exact checks for the polish round of section oc (Remark oc:rem:layers(3), Remark oc:rem:ray, parity table)."""
import itertools
from fractions import Fraction as Fr

ok = True

def orient(a, b, d):
    return (b[0] - a[0]) * (d[1] - a[1]) - (b[1] - a[1]) * (d[0] - a[0])

h = Fr(1, 2)
outer = [(2, 0), (-2, 0), (0, 2), (0, -2)]
inner = [(e1 * h, e2 * h) for e1 in (1, -1) for e2 in (1, -1)]
S = [tuple(Fr(v) for v in p) for p in outer] + inner

# convex combination of Remark oc:rem:layers(3)
for e1 in (1, -1):
    for e2 in (1, -1):
        w = [(Fr(3, 8), (2 * e1, 0)), (Fr(3, 8), (0, 2 * e2)), (Fr(1, 8), (-2 * e1, 0)), (Fr(1, 8), (0, -2 * e2))]
        x = sum(c * p[0] for c, p in w)
        y = sum(c * p[1] for c, p in w)
        pts = {p for _, p in w}
        if (x, y) != (e1 * h, e2 * h) or sum(c for c, _ in w) != 1 or pts != set(outer):
            ok = False
            print("convex combination FAILED", e1, e2)

# general position: no three distinct points collinear
for a, b, d in itertools.combinations(S, 3):
    if orient(a, b, d) == 0:
        ok = False
        print("collinear", a, b, d)

# pigeonhole argument: lines through two points of the same kind contain no third point of S
for kind in (S[:4], S[4:]):
    for a, b in itertools.combinations(kind, 2):
        for d in S:
            if d not in (a, b) and orient(a, b, d) == 0:
                ok = False
                print("third point on line", a, b, d)

# rotation by pi/2 maps S onto itself
rot = lambda p: (-p[1], p[0])
if set(map(rot, S)) != set(S):
    ok = False
    print("rotation FAILED")

# Remark oc:rem:ray example: m = 2, S = {x, 2c - x}; y - c = (-1)(x - c)
c = (Fr(3), Fr(-1)); xx = (Fr(5), Fr(2)); yy = (2 * c[0] - xx[0], 2 * c[1] - xx[1])
rot2 = lambda p: (2 * c[0] - p[0], 2 * c[1] - p[1])  # rotation by pi about c
if not ({rot2(xx), rot2(yy)} == {xx, yy} and (yy[0] - c[0], yy[1] - c[1]) == (-(xx[0] - c[0]), -(xx[1] - c[1]))):
    ok = False
    print("ray example FAILED")

# parity table: (-1)^inv(tau) = sign(tau) (sign by cycle count), perm_sign on order = sign of sorting perm,
# sortpar on a list = sign of sorting perm
def inv(lst):
    return sum(1 for i in range(len(lst)) for j in range(i + 1, len(lst)) if lst[i] > lst[j])

def sign_cycles(tau):
    seen, cyc = set(), 0
    for i in range(len(tau)):
        if i not in seen:
            cyc += 1
            j = i
            while j not in seen:
                seen.add(j)
                j = tau[j]
    return (-1) ** (len(tau) - cyc)

def sortpar(lst):
    a = list(lst); par = 1
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; par = -par
    return tuple(a), par

for tau in itertools.permutations(range(3)):
    if (-1) ** inv(tau) != sign_cycles(tau):
        ok = False; print("table FAILED", tau)
for a in itertools.permutations([3, 7, 11]):
    sigma = sorted(range(3), key=lambda r: a[r])  # list sigma(0) sigma(1) sigma(2): a o sigma increasing
    if (-1) ** inv(sigma) != sign_cycles(sigma):  # perm_sign(order) = sgn sigma
        ok = False; print("perm_sign FAILED", a)
    if sortpar(a)[1] != sign_cycles(sigma):        # sortpar(a) = sgn sigma
        ok = False; print("sortpar FAILED", a)
    if inv(a) != inv([sigma.index(i) for i in range(3)]):  # inv(a) = inv(sigma^{-1})
        ok = False; print("inv(a) = inv(sigma^-1) FAILED", a)

print("ALL OK" if ok else "SOME CHECK FAILED")
