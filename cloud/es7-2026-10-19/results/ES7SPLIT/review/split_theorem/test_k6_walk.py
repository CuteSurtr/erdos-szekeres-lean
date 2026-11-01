#!/usr/bin/env python3
"""k = 6 analogue at the extremal size 16, with Baek's N(6,4,6) = 11 as the only black box.
Prediction (same proof as Theorem 5): every z-split with |A|,|B| >= 2 of a 16-point set with gon <= 5 has
(|A|,|B|,c,d) in {(5,11,2,3), (11,5,3,2)}.
We build an Erdos-Szekeres-type 16-point set (blocks T_i = cups-caps extremal sets, placed on a steep macro cap),
verify gon <= 5 exactly, then random-walk (move one point, accept iff general position and gon <= 5 remain) and
enumerate all splits exactly at every visited set.
Also k = 7: walks from the classical 32 set (data/classical32.txt) with the Remark's prediction:
(16,16,3,3), (26,6,4,2), (6,26,2,4) or the |A|,|B| <= 6/>= 26 types.
"""
import random
import sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import orient, general_position
from gon_ind import gon
from splits_ind import all_splits, load


def longest(P, kind):
    Q = sorted(P)
    m = len(Q)
    if m <= 2:
        return m
    L = {}
    best = 2
    for k in range(m):
        for j in range(k):
            L.setdefault((j, k), 2)
            for i in range(j):
                o = orient(Q[i], Q[k], Q[j])  # >0: Q_j above chord (cap triple)
                good = o > 0 if kind == 'cap' else o < 0
                if good and L[(i, j)] + 1 > L[(j, k)]:
                    L[(j, k)] = L[(i, j)] + 1
                    best = max(best, L[(j, k)])
    return best


def cupcap(a, b, rng):
    """Set with no a-cup and no b-cap, size C(a+b-4, a-2), integer coordinates."""
    if a <= 2 or b <= 2:
        return [(0, 0)]
    L = cupcap(a - 1, b, rng)
    R = cupcap(a, b - 1, rng)
    allp = L + R
    span = max(abs(p[0]) for p in allp) + max(abs(p[1]) for p in allp) + 1
    smax = 1
    for P in (L, R):
        for p in P:
            for q in P:
                if p[0] != q[0]:
                    smax = max(smax, abs((q[1] - p[1]) // (q[0] - p[0])) + 1)
    W = 2 * span + rng.randint(1, 5)
    H = (smax + 2) * 4 * (W + span) + rng.randint(0, 7)
    return L + [(x + W, y + H) for x, y in R]


def es16(rng):
    k = 6
    blocks = []
    for i in range(k - 1):
        T = cupcap(k - i, i + 2, rng)  # no (6-i)-cup, no (i+2)-cap
        assert longest(T, 'cup') < k - i and longest(T, 'cap') < i + 2 and len(T) in (1, 4, 6)
        blocks.append(T)
    S = []
    x0, y0 = 0, 0
    M = 10 ** 6
    for i, T in enumerate(blocks):
        S += [(x0 + x, y0 + y) for x, y in T]
        x0 += 10 ** 5
        y0 -= M * (i + 1) * 10 ** 5
        M *= 1000
    return S


def walk(rng, S, kmax, steps, predict, label):
    stats = dict(visited=0, with_split=0, splits=0, violations=0)
    types = {}
    R = max(max(abs(p[0]), abs(p[1])) for p in S)
    for st in range(steps):
        sp, _ = all_splits(S)
        stats['visited'] += 1
        if sp:
            stats['with_split'] += 1
        for s in sp:
            stats['splits'] += 1
            key = (s['nA'], s['nB'], s['c'], s['d'])
            types[key] = types.get(key, 0) + 1
            if not predict(key):
                stats['violations'] += 1
                print('VIOLATION', label, key)
        # one accepted move
        for _ in range(200):
            i = rng.randrange(len(S))
            # move scale relative to local coordinates
            sc = rng.choice([1, 3, 10, 100, 1000, 10**4, 10**5, 10**6, 10**8])
            p = (S[i][0] + rng.randint(-sc, sc), S[i][1] + rng.randint(-sc, sc))
            T = S[:i] + [p] + S[i + 1:]
            if len(set(T)) == len(T) and general_position(T) and gon(T) <= kmax:
                S = T
                break
    print(label, dict(**stats, types=types))


def main():
    which = sys.argv[1]
    seed = int(sys.argv[2])
    steps = int(sys.argv[3])
    rng = random.Random(seed)
    if which == 'k6':
        S = es16(rng)
        assert len(S) == 16 and general_position(S)
        g = gon(S)
        print('ES16 built, gon =', g)
        assert g <= 5
        walk(rng, S, 5, steps, lambda t: t in ((5, 11, 2, 3), (11, 5, 3, 2)), 'k6 seed %d' % seed)
    else:
        S = load(sys.argv[4])
        assert gon(S) <= 6

        def pred(t):
            nA, nB, c, d = t
            if (c, d) == (3, 3):
                return nA == 16 and nB == 16
            if (c, d) == (4, 2):
                return nB <= 6 and nA >= 26
            if (c, d) == (2, 4):
                return nA <= 6 and nB >= 26
            return False
        walk(rng, S, 6, steps, pred, 'k7 seed %d' % seed)


if __name__ == '__main__':
    main()
