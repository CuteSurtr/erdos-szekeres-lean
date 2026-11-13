#!/usr/bin/env python3
"""Builder for x = 2 (k = m + 4): half-turn-symmetric Lemma-14 blow-up of a centrally symmetric base with an
arbitrary half-turn-symmetric left/right labelling (the x = 2 variant of build_labelled_x1.py).  Cluster pre-images
are produced by the routines of cor15_build_x2.py (P_au = classical cups/caps set, valtr_endpoint = P'(k, x+2, k));
the placement and the labelling are done here, and the output is checked separately by check_set.py.
Usage (from this directory): python3 build_labelled_x2.py BASE m a b LEFTPOS OUT
"""
import sys
import math
from fractions import Fraction
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from cor15_build_x2 import P_au, valtr_endpoint, check_cluster  # noqa: E402


def load(fn):
    pts = []
    for line in open(fn):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        u, v = line.replace(',', ' ').split()[:2]
        pts.append((int(u), int(v)))
    return pts


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def in_convex_position(T):
    for p in T:
        others = [q for q in T if q != p]
        for a, b, c in combinations(others, 3):
            s = orient(a, b, c) > 0
            if (orient(a, b, p) > 0) == s and (orient(b, c, p) > 0) == s and (orient(c, a, p) > 0) == s:
                return False
    return True


def main():
    base = load(sys.argv[1]); m = int(sys.argv[2]); a = int(sys.argv[3]); b = int(sys.argv[4])
    leftpos = sorted(int(t) for t in sys.argv[5].split(',')); out = sys.argv[6]
    x = 2; k = m + 2 * x; N = len(base)
    RB = sorted((a * px + b * py, -b * px + a * py) for (px, py) in base)
    assert all((-RB[i][0], -RB[i][1]) == RB[N - 1 - i] for i in range(N))
    L = [p - 1 for p in leftpos]
    assert sorted(L + [N - 1 - i for i in L]) == list(range(N))

    def left_gon(idx):
        pool = list(range(idx))
        for r in range(len(pool), 0, -1):
            for T in combinations(pool, r):
                if in_convex_position([RB[j] for j in T] + [RB[idx]]):
                    return r + 1
        return 1
    s = {i: left_gon(i) for i in L}
    print('left-labelled positions and s-values:', [(i + 1, s[i]) for i in L])
    pre = {}
    for i in L:
        if i == 0:
            E = valtr_endpoint(k, x)
            ok, info = check_cluster(E, k, x + 2, kgon=k)
            assert ok and len(E) == sum(math.comb(k - 2, l) for l in range(x + 1)), info
            pre[i] = E
        else:
            aa = k + 1 - x - s[i]
            Q = P_au(aa, x + 2)
            ok, info = check_cluster(Q, aa, x + 2)
            assert ok and len(Q) == math.comb(k - 1 - s[i], x), (i, s[i], len(Q), info)
            pre[i] = Q
    rotc = {}
    for i, Q in pre.items():
        R = [(py, -px) for px, py in Q]  # clockwise quarter-turn
        cx = (min(p[0] for p in R) + max(p[0] for p in R)) // 2
        cy = (min(p[1] for p in R) + max(p[1] for p in R)) // 2
        rotc[i] = [(px - cx, py - cy) for px, py in R]
    D = max(max(abs(c) for c in p) for p in RB)
    rho = min(Fraction(abs(orient(RB[i], RB[j], RB[l])), 6 * D) for i, j, l in combinations(range(N), 3))
    gX = min(abs(RB[i][0] - RB[j][0]) for i, j in combinations(range(N), 2))
    H = 2 * D
    worst = Fraction(10 ** 30)
    for R in rotc.values():
        for p, q in combinations(R, 2):
            dX = abs(q[0] - p[0]); dY = abs(q[1] - p[1])
            if dX:
                worst = min(worst, Fraction(dY, dX))
    wX = max(max(abs(p[0]) for p in R) for R in rotc.values()) + 1
    wY = max(max(abs(p[1]) for p in R) for R in rotc.values()) + 1
    be = rho / (10 * wY)
    al = be / (Fraction(20) * H / (gX * worst))
    al = min(al, rho / (10 * wX))
    K = math.ceil(1 / min(al, be)) * 10
    alK = max(1, math.floor(al * K)); beK = max(1, math.floor(be * K))
    pts = []
    for i in L:
        X0, Y0 = RB[i][0] * K, RB[i][1] * K
        pts += [(X0 + alK * px, Y0 + beK * py) for px, py in rotc[i]]
    pts += [(-px, -py) for (px, py) in pts]
    print('built points:', len(pts), ' 2^(k-2) =', 2 ** (k - 2))
    with open(out, 'w') as f:
        f.write(f'# half-turn-symmetric Lemma-14 blow-up (x=2, k={k}) of {sys.argv[1]}, direction ({a},{b}), '
                f'left-labelled sweep positions {leftpos}\n')
        for (px, py) in pts:
            f.write(f'{px} {py}\n')


main()
