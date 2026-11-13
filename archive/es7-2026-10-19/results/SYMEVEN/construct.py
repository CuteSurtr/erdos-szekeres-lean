#!/usr/bin/env python3
"""
Construction (exact integers) of a centrally symmetric set S of 2^(k-2) points, k even >= 6,
in general position, 0 not in S, intended to have no k points in convex position.

Design (see PROOF.md, Sections 2-4):
  n = k-2 (even), m = k/2.
  base abscissae x_j (j = 0..n): odd integers -(n-1),...,-3,-1 for j < n/2, x_{n/2} = 0,
  1,3,...,n-1 for j > n/2;  base points q_j = Lam*(x_j, x_j^3).
  cluster j < n/2 : Lam*q_j + flatten_c(G(j+2, k-j))   (no (j+2)-cup, no (k-j)-cap)
  cluster n-j     : minus cluster j
  cluster n/2     : M0 = X' u (-X'),  X' = flattened G(m, m+1) shifted to about (-4T, -T)
                    (tiny compared with the outer clusters: scale separation)
Only exact integer / Fraction arithmetic is used.

Usage: python3 construct.py K OUTFILE
Writes lines "x y cluster_index".
"""
import sys
from fractions import Fraction
from math import comb


def max_abs_slope(P):
    s = Fraction(0)
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            dx = P[j][0] - P[i][0]
            dy = P[j][1] - P[i][1]
            assert dx != 0, "equal x-coordinates inside a cluster"
            v = abs(Fraction(dy, dx))
            if v > s:
                s = v
    return s


def normalize(P):
    mx = min(p[0] for p in P)
    my = min(p[1] for p in P)
    return [(p[0] - mx, p[1] - my) for p in P]


def ceil_frac(f):
    f = Fraction(f)
    return -((-f.numerator) // f.denominator)


def G(a, b):
    """Erdos-Szekeres cups-caps set: no a-cup, no b-cap, C(a+b-4, a-2) points.
    Recursive: L = G(a-1,b), R = G(a,b-1) placed to the right of L so that every L->R slope
    exceeds every slope inside L and inside R."""
    if a <= 2 or b <= 2:
        return [(0, 0)]
    L = normalize(G(a - 1, b))
    R = normalize(G(a, b - 1))
    s = max(max_abs_slope(L), max_abs_slope(R))
    WL = max(p[0] for p in L)
    WR = max(p[0] for p in R)
    HL = max(p[1] for p in L)
    dx = WL + 1
    t = s * (dx + WR)
    dy = HL + (t.numerator // t.denominator) + 1      # dy - HL > s*(dx+WR)
    out = L + [(p[0] + dx, p[1] + dy) for p in R]
    out.sort()
    assert len(out) == comb(a + b - 4, a - 2)
    return out


def flatten(P, c):
    return [(c * p[0], p[1]) for p in P]


def center(P):
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    cx = (min(xs) + max(xs)) // 2
    cy = (min(ys) + max(ys)) // 2
    return [(p[0] - cx, p[1] - cy) for p in P]


def neg(P):
    return [(-p[0], -p[1]) for p in P]


def middle_cluster(m):
    """Centrally symmetric set, no (m+1)-cup, no (m+1)-cap, C(2m-2, m-1) points,
    all slopes in (-1/2, 1/2), every point (u,v) with |v| < |u|/2."""
    X = G(m, m + 1)                      # no m-cup, no (m+1)-cap
    sX = max_abs_slope(X)
    cX = max(1, ceil_frac(16 * sX))      # flattened slopes <= 1/16
    Xf = center(flatten(X, cX))
    w = max(abs(p[0]) for p in Xf)
    h = max(abs(p[1]) for p in Xf)
    T = 8 * (w + h) + 1
    Xp = [(p[0] - 4 * T, p[1] - T) for p in Xf]
    M0 = Xp + neg(Xp)
    assert len(M0) == comb(2 * m - 2, m - 1)
    return M0


def build(k):
    assert k % 2 == 0 and k >= 4
    n = k - 2
    m = k // 2
    xs = []
    for j in range(n + 1):
        if j < n // 2:
            xs.append(2 * j - n + 1)
        elif j == n // 2:
            xs.append(0)
        else:
            xs.append(2 * j - n - 1)
    Gs = {j: G(j + 2, k - j) for j in range(n // 2)}
    M0 = middle_cluster(m)
    RM = max(abs(p[0]) + abs(p[1]) for p in M0)
    s_max = max([max_abs_slope(Gs[j]) for j in Gs] + [Fraction(0)])
    H_max = max(max(p[1] for p in normalize(Gs[j])) for j in Gs)
    c = max(ceil_frac(16 * s_max), 8 * RM, 8 * H_max) + 1
    flat = {j: center(flatten(Gs[j], c)) for j in Gs}
    Rc = max(max(abs(p[0]) + abs(p[1]) for p in flat[j]) for j in flat)
    Lam = max(4096 * Rc, 16 * (Rc * Rc) // c + 1)
    # round Lam up to a power of 10 for readability
    L10 = 1
    while L10 < Lam:
        L10 *= 10
    Lam = L10
    pts = []
    for j in range(n // 2):
        qx, qy = Lam * xs[j], Lam * xs[j] ** 3
        Bj = [(qx + p[0], qy + p[1]) for p in flat[j]]
        pts += [(p[0], p[1], j) for p in Bj]
        pts += [(-p[0], -p[1], n - j) for p in Bj]
    pts += [(p[0], p[1], n // 2) for p in M0]
    params = dict(k=k, n=n, m=m, xs=xs, c=c, Lam=Lam, RM=RM, Rc=Rc, s_max=str(s_max), H_max=H_max)
    return pts, params


if __name__ == "__main__":
    k = int(sys.argv[1])
    out = sys.argv[2]
    pts, params = build(k)
    assert len(pts) == 2 ** (k - 2)
    with open(out, "w") as f:
        f.write("# k=%d  centrally symmetric construction; columns: x y cluster\n" % k)
        f.write("# params: %s\n" % params)
        for x, y, j in sorted(pts, key=lambda t: (t[0], t[1])):
            f.write("%d %d %d\n" % (x, y, j))
    print(params)
    print("points:", len(pts), " max|coord|:", max(max(abs(p[0]), abs(p[1])) for p in pts))
