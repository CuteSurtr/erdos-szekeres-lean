# Independent exact orientation table for an 8-fold point file (written from scratch for an independent check).
# Input rows: 8 integers w_0..w_7, point = sum_j w_j zeta^j, zeta = exp(2 pi i / 8).
# Coordinates are kept exactly in Z[sqrt2] (scaled by 2):  2*Re = sum w_j * 2cos(j pi/4),  2*Im = sum w_j * 2sin(j pi/4).
# Sign of P + Q*sqrt2 decided exactly (method 1) and, independently, by a rational interval enclosure of sqrt2
# (method 2).  Both must agree and be nonzero.  Output: "XT n\n" + n^3 signed bytes, index (i*n+j)*n+k.
import sys
from math import isqrt

R2C = [(2, 0), (0, 1), (0, 0), (0, -1), (-2, 0), (0, -1), (0, 0), (0, 1)]   # 2cos(j pi/4) = a + b sqrt2
R2S = [(0, 0), (0, 1), (2, 0), (0, 1), (0, 0), (0, -1), (-2, 0), (0, -1)]   # 2sin(j pi/4)


def read_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            w = [int(t) for t in s.split()]
            if len(w) != 8:
                raise SystemExit('bad row: %r' % s)
            rows.append(w)
    return rows


def coords(w):
    xa = sum(w[j] * R2C[j][0] for j in range(8))
    xb = sum(w[j] * R2C[j][1] for j in range(8))
    ya = sum(w[j] * R2S[j][0] for j in range(8))
    yb = sum(w[j] * R2S[j][1] for j in range(8))
    return (xa, xb), (ya, yb)


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def mul(p, q):
    return (p[0] * q[0] + 2 * p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def sign_exact(v):
    a, b = v
    if a >= 0 and b >= 0:
        return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0:
        return -1
    # opposite strict signs; a^2 == 2 b^2 impossible for (a,b) != (0,0)
    if a * a > 2 * b * b:
        return 1 if a > 0 else -1
    return 1 if b > 0 else -1


# method 2: sqrt2 in [LO/DEN, (LO+1)/DEN]
DEN = 10 ** 60
LO = isqrt(2 * DEN * DEN)
assert LO * LO <= 2 * DEN * DEN < (LO + 1) * (LO + 1)


def sign_interval(v):
    a, b = v
    # a + b*sqrt2 in [a*DEN + b*LO, a*DEN + b*(LO+1)] / DEN if b >= 0, reversed if b < 0
    e1 = a * DEN + b * LO
    e2 = a * DEN + b * (LO + 1)
    lo, hi = min(e1, e2), max(e1, e2)
    if lo > 0:
        return 1
    if hi < 0:
        return -1
    return None  # undecided


def main():
    src, out = sys.argv[1], sys.argv[2]
    rows = read_rows(src)
    n = len(rows)
    P = [coords(w) for w in rows]
    # distinctness
    assert len(set(P)) == n, 'repeated point'
    tab = bytearray(n * n * n)
    zero = undecided = mismatch = 0
    minabs = None
    for i in range(n):
        xi, yi = P[i]
        for j in range(i + 1, n):
            dxj, dyj = sub(P[j][0], xi), sub(P[j][1], yi)
            for k in range(j + 1, n):
                dxk, dyk = sub(P[k][0], xi), sub(P[k][1], yi)
                m1 = mul(dxj, dyk)
                m2 = mul(dyj, dxk)
                d = (m1[0] - m2[0], m1[1] - m2[1])
                s = sign_exact(d)
                s2 = sign_interval(d)
                if s == 0:
                    zero += 1
                if s2 is None:
                    undecided += 1
                elif s2 != s:
                    mismatch += 1
                b = s & 0xff
                nb = (-s) & 0xff
                # all 6 permutations
                tab[(i * n + j) * n + k] = b
                tab[(j * n + k) * n + i] = b
                tab[(k * n + i) * n + j] = b
                tab[(j * n + i) * n + k] = nb
                tab[(i * n + k) * n + j] = nb
                tab[(k * n + j) * n + i] = nb
    with open(out, 'wb') as f:
        f.write(('XT %d\n' % n).encode())
        f.write(bytes(tab))
    print('file=%s n=%d zero=%d interval_undecided=%d interval_mismatch=%d' % (src, n, zero, undecided, mismatch))


if __name__ == '__main__':
    main()
