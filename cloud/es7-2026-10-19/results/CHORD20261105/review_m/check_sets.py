#!/usr/bin/env python3
"""Evaluate chord clause families on a certified m-fold set (gen.py labelling), EXACT orientations.
Points: rows of integers w_0..w_{m-1}, point = sum_j w_j zeta^j, zeta = e^{2 pi i/m}; centre row (all 0) dropped.
orient(a,b,c) = Im(conj(b-a) (c-a)) = sum_{d} coef_d sin(360 d/m), computed exactly:
  m = 4: sin(90 d) in {0,1,0,-1} -> integer.
  m = 5: sin(144) = sin(72) * (sqrt5 - 1)/2, so orient = sin72 * (A + B (sqrt5-1)/2), sign(2A - B + B sqrt5) exactly.
Labelling: layers = orbits sorted by decreasing |z|^2 (exact), layer 0 vertex rotated to angle 0, theta_i in [0,W),
(i,k) = vertex of layer i with angle in [Wk, W(k+1)).  Angles via 80-digit mpmath (genericity margins reported).
Also evaluates gen.py's order/angle/nest families (built by gen.py, chain off) as a labelling cross-check.
Usage: check_sets.py m PTSFILE CHORDCLAUSES"""
import sys, itertools, math, importlib.util
import mpmath as mp
sys.path.insert(0, '<rot45-work-dir>/review_m')
from verify_exact import numbering
mp.mp.dps = 80
m, ptsf, chf = int(sys.argv[1]), sys.argv[2], sys.argv[3]
rows = [list(map(int, l.split())) for l in open(ptsf) if l.strip() and not l.startswith('#')]
rows = [r for r in rows if any(r)]
assert all(len(r) == m for r in rows)
n = len(rows)
t = n // m
assert n == m * t


def mul(a, b):   # product in Z[x]/(x^m - 1) (zeta^m = 1); fine for Im/Re extraction via full power basis
    c = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[(i + j) % m] += x * y
    return c


def conj(a):     # conj(zeta^j) = zeta^{-j}
    c = [0] * m
    for j, x in enumerate(a):
        c[(-j) % m] += x
    return c


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def imsign(c):
    """exact sign of Im(sum c_d zeta^d)"""
    if m == 4:
        v = c[1] - c[3]
        return (v > 0) - (v < 0)
    if m == 5:
        A = c[1] - c[4]
        B = c[2] - c[3]
        # sign(2A - B + B sqrt5)
        P, Q = 2 * A - B, B
        # sign(P + Q sqrt5)
        if P >= 0 and Q >= 0:
            return 0 if (P == 0 and Q == 0) else 1
        if P <= 0 and Q <= 0:
            return -1
        s = (P * P > 5 * Q * Q) - (P * P < 5 * Q * Q)
        return s if P > 0 else -s
    raise NotImplementedError


def resq(c):     # exact |z|^2 as element: Re(conj(z) z) -> compare via mpmath at 80 digits (exact for m=4)
    p = mul(conj(c), c)
    return sum(mp.mpf(p[d]) * mp.cos(2 * mp.pi * d / m) for d in range(m))


def cplx(c):
    return sum(mp.mpf(c[d]) * mp.expjpi(mp.mpf(2 * d) / m) for d in range(m))


# group orbits: rotation by zeta = cyclic shift of coefficients
def rot(c):
    return [c[-1]] + c[:-1]


key = lambda c: tuple(c)
left = {key(r) for r in rows}
orbits = []
for r in rows:
    if key(r) not in left:
        continue
    orb = [r]
    x = r
    for _ in range(m - 1):
        x = rot(x)
        orb.append(x)
    for x in orb:
        assert key(x) in left, 'not m-fold symmetric'
        left.discard(key(x))
    orbits.append(orb)
assert len(orbits) == t
rad = [resq(o[0]) for o in orbits]
order = sorted(range(t), key=lambda q: -rad[q])
assert all(rad[order[q]] > rad[order[q + 1]] for q in range(t - 1)), 'equal radii'
W = mp.mpf(360) / m
u = mp.mpf(180) / m
ref = mp.degrees(mp.arg(cplx(orbits[order[0]][0])))
label = {}   # (i,k) -> coefficient vector
theta = []
for i, q in enumerate(order):
    angs = [((mp.degrees(mp.arg(cplx(x))) - ref) % 360, x) for x in orbits[q]]
    th = min(a % W for a, _ in angs)
    theta.append(th)
    for a, x in angs:
        k = int(mp.floor(a / W))
        if abs(a - W * k) < mp.mpf(10) ** -60 or abs(a - W * (k + 1)) < mp.mpf(10) ** -60:
            k = int(mp.nint(a / W)) % m      # on a boundary (only layer 0's vertices at exact multiples)
        assert (i, k) not in label
        label[(i, k)] = x
theta[0] = mp.mpf(0)
odd = m % 2 == 1
psi = [x % u for x in theta] if odd else list(theta)
gap = min([abs(psi[i] - psi[j]) for i in range(t) for j in range(i)] + [p for p in psi[1:]] +
          [abs(theta[i] - u) for i in range(1, t)] + [W - x for x in theta[1:]])
print('m=%d t=%d; theta (deg) =' % (m, t), [mp.nstr(x, 12) for x in theta])
print('genericity margin (min of psi gaps, psi_i, |theta_i - 180/m|, W - theta_i) = %s degrees' % mp.nstr(gap, 6))
pt = [label[(i, k)] for i in range(t) for k in range(m)]
tv, inv, Y, H = numbering(m, t)
ntr = len(tv)


def orient(a, b, c):
    return imsign(mul(conj(sub(pt[b], pt[a])), sub(pt[c], pt[a])))


val = {}
zero = 0
for v, C in inv.items():
    s = orient(*C)
    if s == 0:
        zero += 1
    val[v] = s > 0
for (i, j), v in Y.items():
    val[v] = psi[i] < psi[j]
for i, v in H.items():
    val[v] = theta[i] < u
print('collinear triples among canonical orbits: %d' % zero)
# nesting check (exact): every vertex of layer i+1 strictly left of each ccw edge of layer i
nest_ok = all(orient(i * m + k, i * m + (k + 1) % m, (i + 1) * m + l) > 0
              for i in range(t - 1) for k in range(m) for l in range(m))
print('nested (convex layers, exact):', nest_ok)
sat = lambda c: any(val[abs(x)] == (x > 0) for x in c)
ch = [[int(x) for x in l.split()[:-1]] for l in open(chf)]
bad = [c for c in ch if not sat(c)]
applic = sum(1 for c in ch if not any(val[abs(x)] == (x > 0) for x in c if abs(x) > ntr))
print('chord clauses %d, applicable (condition part false) %d, VIOLATED %d' % (len(ch), applic, len(bad)))
for c in bad[:10]:
    print('  violated', c)
# labelling cross-check with gen.py's own order/angle/nest families
R = '<results-dir>'
s_ = importlib.util.spec_from_file_location('g', R + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(s_); s_.loader.exec_module(G)
E, cnt, st = G.build(m, 8, t, chain=False)
assert E.tvar == tv
bb = [c for c in E.cls if not sat(c)]
print('gen.py order/angle/nest clauses %d, violated %d' % (len(E.cls), len(bb)))
