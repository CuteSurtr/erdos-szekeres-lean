#!/usr/bin/env python3
"""SYM16FIVE20261110: for each 16-point integer realization (3 orbits of 5 in rotation order + centre): build an EXACTLY 5-fold symmetric
set in Z[zeta5] from the three orbit representatives (scaled by SCALE, nearest a + b*zeta), and compare its orientation
signs, computed exactly, with those of the integer file under the same labelling (5j + k = rep j times zeta^k).
Exact sign: for w = sum c_k zeta^k, Im w = (c1 - c4) s1 + (c2 - c3) s2 with s1 = sin 72 deg, s2 = sin 144 deg > 0,
s1^2 = (10 + 2 sqrt5)/16, s2^2 = (10 - 2 sqrt5)/16."""
import sys, glob, os, itertools, math
SCALE = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
def sgn(x): return (x > 0) - (x < 0)
def sign_x_plus_y_sqrt5(x, y):         # exact sign of x + y*sqrt(5), integers
    if x >= 0 and y >= 0: return sgn(x + y)
    if x <= 0 and y <= 0: return -sgn(-x - y)
    d = x * x - 5 * y * y               # |x| vs |y| sqrt5
    return sgn(x) if d > 0 else (sgn(y) if d < 0 else 0)
def sign_im(A, B):                      # exact sign of A s1 + B s2
    if A >= 0 and B >= 0: return sgn(A + B)
    if A <= 0 and B <= 0: return -sgn(-A - B)
    # compare A^2 s1^2 with B^2 s2^2: 16(A^2 s1^2 - B^2 s2^2) = 10(A^2 - B^2) + 2 sqrt5 (A^2 + B^2)
    d = sign_x_plus_y_sqrt5(10 * (A * A - B * B), 2 * (A * A + B * B))
    return sgn(A) if d > 0 else (sgn(B) if d < 0 else 0)
def mul(u, v):                          # in Z[x]/(x^5 - 1), coefficient vectors of length 5
    w = [0] * 5
    for i in range(5):
        if u[i]:
            for j in range(5): w[(i + j) % 5] += u[i] * v[j]
    return w
def conj(u): return [u[0], u[4], u[3], u[2], u[1]]
def sub(u, v): return [a - b for a, b in zip(u, v)]
def orient_z(p, q, r):                  # sign of Im(conj(q - p) (r - p))
    w = mul(conj(sub(q, p)), sub(r, p))
    return sign_im(w[1] - w[4], w[2] - w[3])
def rot(u, k): return [u[(i - k) % 5] for i in range(5)]   # times zeta^k
c1, sn1 = math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5)
def to_zeta(x, y):                       # nearest a + b zeta to SCALE*(x + iy)
    b = round(SCALE * y / sn1); a = round(SCALE * x - b * c1)
    return [a, b, 0, 0, 0]
def orient_int(a, b, c): return sgn((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))
ok_all = True; n = 0
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'model*.pts'))):
    P = [tuple(int(x) for x in l.split()) for l in open(f) if l.strip()]
    assert len(P) == 16 and P[15] == (0, 0)
    reps = [to_zeta(*P[5 * j]) for j in range(3)]
    Z = [rot(reps[j], k) for j in range(3) for k in range(5)] + [[0] * 5]
    zero = mism = 0
    for i, j, k in itertools.combinations(range(16), 3):
        s = orient_z(Z[i], Z[j], Z[k])
        zero += s == 0; mism += s != orient_int(P[i], P[j], P[k])
    ok = zero == 0 and mism == 0; ok_all &= ok; n += 1
    if not ok: print(os.path.basename(f), 'zero', zero, 'mismatch', mism)
print(f'{n} files, SCALE {SCALE}: exact 5-fold symmetric set with the same labelled orientations for all:', ok_all)
