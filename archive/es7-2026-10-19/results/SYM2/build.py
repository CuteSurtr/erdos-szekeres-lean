"""Centrally symmetric Erdős–Szekeres-type sets: clusters on the odd cubic y = x^3.

g(a, b): a set of C(a+b-4, a-2) points with no a-cup and no b-cap (the cups-caps recursion: g(a-1, b) on the left,
g(a, b-1) far up and to the right, every slope between the two parts larger than every slope inside them).
sym(k): clusters C_0..C_{k-2} centred on the curve y = x^3 at x = 2i-(k-2) (scaled), C_i a flattened copy of
g(i+2, k-i) for the left half and C_{k-2-i} = -C_i (the half-turn about the origin) for the right half."""
from math import comb


def g(a, b):
    if a <= 2 or b <= 2:
        return [(0, 0)]
    L, R = g(a - 1, b), g(a, b - 1)
    def box(P):
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        return min(xs), max(xs), min(ys), max(ys)
    def maxslope(P):
        s = 0
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                dx = abs(P[i][0] - P[j][0]); dy = abs(P[i][1] - P[j][1])
                s = max(s, -(-dy // dx) if dx else 10 ** 9)
        return s
    lx0, lx1, ly0, ly1 = box(L); rx0, rx1, ry0, ry1 = box(R)
    s = max(maxslope(L), maxslope(R), 1)
    dx = (lx1 - rx0) + 1                      # R starts just right of L
    span = (rx1 + dx) - lx0                   # widest x-distance between a point of L and a point of R
    dy = (ly1 - ry0) + (s + 1) * span + 1     # every L-R slope > s
    return sorted(L + [(x + dx, y + dy) for x, y in R])


def flatten(P, K):
    """x -> K x: slopes shrink by K, cups and caps are unchanged."""
    return [(K * x, y) for x, y in P]


def centre(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return [(2 * x - (min(xs) + max(xs)), 2 * y - (min(ys) + max(ys))) for x, y in P]   # integer, centred at 0 (doubled)


def sym(k, X=10 ** 6, Y=10 ** 6, K=None):
    n = k - 2
    assert n % 2 == 1, "k odd only"
    pts = []
    for i in range(n // 2 + 1):
        C = centre(g(i + 2, k - i))
        if K is None:
            pass
        C = flatten(C, K or 1)
        q = 2 * i - n                          # odd, negative on the left half
        cx, cy = X * q, Y * q ** 3
        left = [(cx + x, cy + y) for x, y in C]
        pts += left + [(-x, -y) for x, y in left]
    return sorted(pts)


if __name__ == "__main__":
    import sys
    for a in range(2, 8):
        for b in range(2, 8):
            assert len(g(a, b)) == comb(a + b - 4, a - 2)
    print("g sizes ok")


def gsym(a):
    """Centrally symmetric set with no a-cup and no a-cap, C(2a-4, a-2) points: L = g(a-1, a) and its half-turn,
    placed like the two parts of the cups-caps recursion (every slope between them above every slope inside)."""
    if a <= 2:
        return [(0, 0)]
    L = centre(g(a - 1, a))
    xs, ys = [p[0] for p in L], [p[1] for p in L]
    s = 1
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            dx = abs(L[i][0] - L[j][0]); dy = abs(L[i][1] - L[j][1])
            s = max(s, -(-dy // dx) if dx else 10 ** 9)
    w, hgt = max(xs) - min(xs), max(ys) - min(ys)
    dx = w + 1; dy = (s + 1) * (2 * w + 2 * dx) + 2 * hgt + 1
    left = [(x - dx, y - dy) for x, y in L]
    return sorted(left + [(-x, -y) for x, y in left])


def sym_even(k, X, Y, K):
    """k even: clusters i = 0..k-2 at x = 2i-(k-2) (the middle one at 0 is gsym(k/2+1)), C_{k-2-i} = -C_i."""
    n = k - 2
    pts = []
    for i in range(n // 2):
        C = flatten(centre(g(i + 2, k - i)), K)
        q = 2 * i - n
        left = [(X * q + x, Y * q ** 3 + y) for x, y in C]
        pts += left + [(-x, -y) for x, y in left]
    pts += flatten(gsym(k // 2 + 1), K)
    return sorted(pts)
