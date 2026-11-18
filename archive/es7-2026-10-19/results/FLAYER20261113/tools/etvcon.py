"""Exact ETV / Erdos-Szekeres block constructions with integer coordinates."""
from fractions import Fraction as Fr
import math

def slopes_max(P):
    m = None
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            s = Fr(P[j][1]-P[i][1], P[j][0]-P[i][0])
            if m is None or abs(s) > m: m = abs(s)
    return m or Fr(0)

def place_high(L, R):
    """Translate R to the right of L and high, so every L->R slope exceeds all internal slopes."""
    if not L: return list(R)
    if not R: return list(L)
    smax = max(slopes_max(L), slopes_max(R)) + 1
    xl0 = min(p[0] for p in L); xl1 = max(p[0] for p in L)
    xr0 = min(p[0] for p in R); xr1 = max(p[0] for p in R)
    yl1 = max(p[1] for p in L); yr0 = min(p[1] for p in R)
    D = xl1 - xr0 + 1               # shift so R starts right of L
    W = (xr1 + D) - xl0              # max horizontal distance of a cross pair
    H = math.ceil(smax * W) + (yl1 - yr0) + 1
    return list(L) + [(x + D, y + H) for (x, y) in R]

def cupcap(k, l):
    """Set with no k-cup and no l-cap, size C(k+l-4, k-2)."""
    if k <= 2 or l <= 2: return [(0, 0)]
    return place_high(cupcap(k-1, l), cupcap(k, l-1))

def shear(P, K):
    return [(x, y + K*x) for (x, y) in P]

def etv(n, a, b):
    """ES-type block construction: blocks T_i, i in [n-b, a-2], T_i with caps <= i+1, cups <= n-1-i,
    blocks steep (internal slopes > all macro slopes), macro centres on a cap."""
    blocks = []
    for i in range(max(0, n-b), a-1):
        T = cupcap(n-i, i+2)   # no (n-i)-cup, no (i+2)-cap
        blocks.append(T)
    # make each block have all internal slopes in [lo, hi] with lo > 0 large: shear by K
    out = []
    # macro: block centres on a cap with chord slopes in (0, 1); internal slopes > M
    # scale blocks tiny relative to macro distances: put block j at (X_j, Y_j)
    m = len(blocks)
    # internal: make each block width w_j <= 1 unit after scaling by large macro factor F
    sm = [slopes_max(T) for T in blocks]
    F = 10**6
    for j, T in enumerate(blocks):
        x0 = min(p[0] for p in T); y0 = min(p[1] for p in T)
        T = [(x - x0, y - y0) for (x, y) in T]
        K = int(sm[j]) + 2          # shear: internal slopes now in [1, 2K]
        T = shear(T, K)
        # steepen: multiply y by big factor G so internal slopes >= G > macro slopes
        G = 10**4
        T = [(x, y*G) for (x, y) in T]
        # macro centre: X = j*F*span, Y = cap curve
        span = max(p[0] for p in T) + 1
        hgt = max(p[1] for p in T) + 1
        out.append((T, span, hgt))
    # macro placement: chord slopes must be < G (internal min slope); use X_j = j*Xs, Y_j = -(j*j)*Ys small
    Xs = max(s for _, s, _ in out) * 10**6
    res = []
    for j, (T, span, hgt) in enumerate(out):
        X = j * Xs; Y = -(j*j) * 10**3 * Xs   # macro chord slopes ~ -(2j+1)*1000, a cap
        res += [(x + X, y + Y) for (x, y) in T]
    return res
