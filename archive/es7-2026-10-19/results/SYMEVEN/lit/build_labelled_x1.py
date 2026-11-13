#!/usr/bin/env python3
"""Builder: a half-turn-symmetric (X,Y)-blow-up (Baek-Balko SoCG 2025, Def. 13 / Lemma 14) of a
centrally symmetric base S, for x = 1 (k = m + 2), with an ARBITRARY half-turn-symmetric left/right labelling
(not necessarily a threshold).  Left-labelled point p_i: (x_i, y_i) = (1, k-2-s_i) with s_i = largest left-gon at
p_i (cluster: a cap of k-1-s_i points rotated clockwise by pi/2, i.e. a right-bulging almost vertical arc; the
leftmost point gets a cap of k-1 points).  Right-labelled clusters are the half-turn images of the left ones.
Lemma 14 conditions are checked explicitly; the output set is then checked exactly by check_set.py (separately).
Usage: python3 -I build_labelled_x1.py BASE m a b LEFTPOS OUT
  (a, b): sweep direction; LEFTPOS: comma-separated 1-based sweep positions labelled left.
"""
import sys
import math
from itertools import combinations


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
    N = len(base); k = m + 2
    R = sorted((a * x + b * y, -b * x + a * y) for (x, y) in base)
    assert len(set(p[0] for p in R)) == N
    assert all((-R[i][0], -R[i][1]) == R[N - 1 - i] for i in range(N)), 'sweep order not antipodal'
    L = [p - 1 for p in leftpos]
    Rt = sorted(N - 1 - i for i in L)
    assert sorted(L + Rt) == list(range(N)), 'labelling not a half-turn-symmetric partition'
    # exact s-values
    def best_gon(idx, side):
        # largest convex subset with R[idx] as rightmost (side='L') or leftmost (side='R')
        pool = list(range(idx)) if side == 'L' else list(range(idx + 1, N))
        for r in range(len(pool), 0, -1):
            for T in combinations(pool, r):
                if in_convex_position([R[j] for j in T] + [R[idx]]):
                    return r + 1
        return 1
    s = {}
    for i in range(N):
        s[i] = best_gon(i, 'L') if i in L else best_gon(i, 'R')
    sij = {}
    for i, j in combinations(range(N), 2):
        best = 2
        mid = list(range(i + 1, j))
        for r in range(len(mid), 0, -1):
            if any(in_convex_position([R[i], R[j]] + [R[t] for t in T]) for T in combinations(mid, r)):
                best = r + 2
                break
        sij[(i, j)] = best
    x = 1
    X = {}; Y = {}
    for i in range(N):
        if i in L:
            X[i] = x; Y[i] = (k - 1 - x - s[i]) if i > 0 else 0
        else:
            Y[i] = x; X[i] = (k - 1 - x - s[i]) if i < N - 1 else 0
    for i in range(N):
        assert X[i] >= 0 and Y[i] >= 0 and X[i] + Y[i] <= k - 1, ('(a) fails', i)
    viol = [(i, j) for i, j in combinations(range(N), 2) if X[i] + Y[j] > k - 1 - sij[(i, j)]]
    print('s-values by sweep position:', [s[i] for i in range(N)], ' labels:', ''.join('L' if i in L else 'R' for i in range(N)))
    print('(x_i, y_i):', [(X[i], Y[i]) for i in range(N)])
    print('Lemma 14 condition (b) violations:', viol)
    size = sum(math.comb(k - 2, l) for l in range(X[0] + 1)) + sum(math.comb(X[i] + Y[i], X[i]) for i in range(1, N - 1)) \
        + sum(math.comb(k - 2, l) for l in range(Y[N - 1] + 1))
    print('Lemma 14 size:', size, ' 2^(k-2) =', 2 ** (k - 2))
    # geometry (x = 1: every left cluster is a cap rotated clockwise by pi/2 = right-bulging arc)
    D = max(max(abs(c) for c in p) for p in R)
    rho = min(abs(orient(R[i], R[j], R[l])) / (6 * D) for i, j, l in combinations(range(N), 3))
    gX = min(abs(R[i][0] - R[j][0]) for i, j in combinations(range(N), 2))
    H = 2 * D; cmax = k - 1
    beta = rho / (10 * cmax); alpha = beta / (10 * 2 * cmax * H / gX)
    K = max(1, math.ceil(1 / alpha)) * 10
    Kb, Ka = int(beta * K), max(1, int(alpha * K))
    pts = []
    for i in L:
        c = (k - 1) if i == 0 else (k - 1 - s[i])
        assert c == math.comb(X[i] + Y[i], X[i]) or i == 0
        X0, Y0 = R[i][0] * K, R[i][1] * K
        pts += [(X0 - Ka * t * t, Y0 + Kb * t) for t in range(1, c + 1)]
    pts += [(-u, -v) for (u, v) in pts]
    print('built points:', len(pts))
    with open(out, 'w') as f:
        f.write(f'# half-turn-symmetric Lemma-14 blow-up (x=1, k={k}) of {sys.argv[1]}, direction ({a},{b}), '
                f'left-labelled sweep positions {leftpos}\n')
        for (u, v) in pts:
            f.write(f'{u} {v}\n')


main()
