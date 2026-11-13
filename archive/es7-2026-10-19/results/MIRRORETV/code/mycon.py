#!/usr/bin/env python3
"""Independent re-implementation (written from scratch) of the construction of Theorem 9.3 in
PROOFS.md section 9: Erdos-Szekeres templates G(a,b) (no a-cup, no b-cap), normalized, mirrored,
and placed with EXACTLY the constants of Lemma 9.2 (placement):
    c = 2W'+3,  G >= c n^2 (H+1) + sigma (c n^2 + 2W') + H + 1,  t_i = 2i-n,  B_i = T_i + (-c t_i^2, -G t_i).
All arithmetic is exact (Python ints / Fractions).

Usage: mycon.py k OUTFILE   -> writes "x y block" lines, header comment with parameters.
Also performs, in pure Python, the cheap checks: sizes, symmetry, axis points.
"""
import sys
from fractions import Fraction
from math import comb, ceil

def template(a, b, memo={}):
    """Points (list of (x,y) int) with distinct x, general position, no a-cup and no b-cap.
    G(a,2)=G(2,b)=one point.  G(a,b) = A=G(a-1,b) on the left, B=G(a,b-1) to the right and high above so that
    every A-B slope exceeds every slope inside A and inside B."""
    key = (a, b)
    if key in memo:
        return memo[key]
    if a == 2 or b == 2:
        res = [(0, 0)]
    else:
        A = template(a - 1, b)
        B = template(a, b - 1)
        def slopes(P):
            out = []
            for i in range(len(P)):
                for j in range(i + 1, len(P)):
                    (x1, y1), (x2, y2) = P[i], P[j]
                    out.append(Fraction(y2 - y1, x2 - x1))
            return out
        sl = slopes(A) + slopes(B)
        dx = max(p[0] for p in A) - min(q[0] for q in B) + 1
        Bs = [(x + dx, y) for (x, y) in B]
        if sl:
            smax = max(sl)
            need = max(smax * (q[0] - p[0]) - q[1] + p[1] for p in A for q in Bs)
            dy = int(need // 1) + 1   # strictly greater than need
        else:
            dy = 0
        res = A + [(x, y + dy) for (x, y) in Bs]
        # sanity: cross slopes exceed internal slopes
        if sl:
            smax = max(sl)
            for p in A:
                for q in res[len(A):]:
                    assert Fraction(q[1] - p[1], q[0] - p[0]) > smax
    assert len(res) == comb(a + b - 4, a - 2), (a, b, len(res))
    xs = [p[0] for p in res]
    assert xs == sorted(xs) and len(set(xs)) == len(xs)
    memo[key] = res
    return res

def normalize(P):
    xmin = min(p[0] for p in P); xmax = max(p[0] for p in P)
    ymin = min(p[1] for p in P); ymax = max(p[1] for p in P)
    return [(2 * x - (xmin + xmax), 2 * y - (ymin + ymax)) for (x, y) in P]

def mu(p):
    return (p[0], -p[1])

def build(k):
    n = k - 2
    T = [None] * (n + 1)
    for i in range(n + 1):
        if 2 * i < n:
            T[i] = normalize(template(k - i, i + 2))
            T[n - i] = [mu(p) for p in T[i]]
    if n % 2 == 0:
        T[n // 2] = [(-1, 0), (1, 0)]
    Wp = max(1, max(abs(p[0]) for Ti in T for p in Ti))
    H = max(abs(p[1]) for Ti in T for p in Ti)
    sig = Fraction(0)
    for Ti in T:
        for i1 in range(len(Ti)):
            for i2 in range(i1 + 1, len(Ti)):
                (x1, y1), (x2, y2) = Ti[i1], Ti[i2]
                assert x1 != x2
                sig = max(sig, abs(Fraction(y2 - y1, x2 - x1)))
    c = 2 * Wp + 3
    bound = c * n * n * (H + 1) + sig * (c * n * n + 2 * Wp) + H + 1
    G = ceil(bound)
    assert G >= bound
    pts = []
    for i in range(n + 1):
        t = 2 * i - n
        X, Y = -c * t * t, -G * t
        for (x, y) in T[i]:
            pts.append((x + X, y + Y, i))
    return pts, dict(n=n, Wp=Wp, H=H, sigma=sig, c=c, G=G, sizes=[len(Ti) for Ti in T])

def L(k):
    return 2 ** (k - 2) if k % 2 else 2 ** (k - 2) - comb(k - 2, k // 2 - 1) + 2

if __name__ == "__main__":
    k = int(sys.argv[1]); out = sys.argv[2]
    pts, par = build(k)
    P = [(x, y) for (x, y, _) in pts]
    assert len(set(P)) == len(P), "duplicate points"
    S = set(P)
    assert all(mu(p) in S for p in P), "not mirror symmetric"
    axis = [p for p in P if p[1] == 0]
    assert len(P) == L(k), (len(P), L(k))
    # blocks paired by the mirror
    n = par['n']
    byb = {}
    for (x, y, b) in pts:
        byb.setdefault(b, set()).add((x, y))
    for b in range(n + 1):
        assert {mu(p) for p in byb[b]} == byb[n - b]
    with open(out, "w") as f:
        f.write("# k=%d n_points=%d axis_points=%d W'=%d H=%d sigma=%s c=%d G=%d sizes=%s\n" % (
            k, len(P), len(axis), par['Wp'], par['H'], par['sigma'], par['c'], par['G'], par['sizes']))
        for (x, y, b) in pts:
            f.write("%d %d %d\n" % (x, y, b))
    print("k=%d points=%d L(k)=%d axis=%d maxabs x=%d y=%d G=%d sigma=%s" % (
        k, len(P), L(k), len(axis), max(abs(p[0]) for p in P), max(abs(p[1]) for p in P), par['G'], par['sigma']))
