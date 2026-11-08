import sympy as sp
# Complex form of rotAbout (fd:def:rot): z -> c + exp(i*th)*(z - c). The n-fold composite is z -> c + exp(i*n*th)*(z - c).
c, z = sp.symbols('c z')
def rot(th, w):
    return c + sp.exp(sp.I*th)*(w - c)
def it(th, n, w):
    q = w
    for _ in range(n):
        q = rot(th, q)
    return q
ok = True
for m in (2, 4, 6, 8, 10, 12):
    d = sp.simplify(sp.expand(it(2*sp.pi/m, m//2, z) - (2*c - z)))
    ok &= (d == 0)
    if d != 0: print('half-turn FAIL m =', m, d)
for s in (4, 5, 7, 8):
    for k in range(1, s):
        if sp.gcd(k, s) != 1:
            continue
        j = next(j for j in range(1, s) if (j*k) % s == 1)
        d = sp.simplify(sp.expand(it(2*sp.pi*k/s, j, z) - rot(2*sp.pi/s, z)))
        ok &= (d == 0)
        if d != 0: print('power FAIL s,k,j =', s, k, j, d)
# Real coordinates, numerically at random points, against the real formula of rotAbout.
import random, math
def rotR(cx, cy, th, p):
    return (cx + math.cos(th)*(p[0]-cx) - math.sin(th)*(p[1]-cy), cy + math.sin(th)*(p[0]-cx) + math.cos(th)*(p[1]-cy))
for _ in range(200):
    cx, cy, px, py = (random.uniform(-5, 5) for _ in range(4))
    for m in (2, 4, 6, 8, 10, 12):
        q = (px, py)
        for _ in range(m//2): q = rotR(cx, cy, 2*math.pi/m, q)
        ok &= abs(q[0] - (2*cx - px)) < 1e-9 and abs(q[1] - (2*cy - py)) < 1e-9
print('ALL OK' if ok else 'FAIL')
