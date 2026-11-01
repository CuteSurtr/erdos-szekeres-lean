#!/usr/bin/env python3
"""End-to-end test of the Theorem 5 mechanism in the k-analogues where all needed ETV numbers are known.

k = 5: S with gon(S) <= 4 and |S| = 8 (= 2^(k-2), the maximum).  Prediction from Lemma 2/3 + Cor 4 + counting:
   every z-split with |A|,|B| >= 2 has c = cap_z(A) = 2, d = cup_z(B) = 2, |A| = |B| = 4
   (since c + d <= 4 forces (2,2) and N(5,3,5) = 4).
k = 6: S with gon(S) <= 5 and |S| = 16.  Prediction: (c,d) in {(2,3),(3,2)} with sizes (5,11) / (11,5)
   (uses N(6,3,6) = 5 and Baek's N(6,4,6) = C(5,2)+1 = 11).
Sets are found by exact local search (minimise the number of convex k-subsets), then all splits are enumerated
exactly with splits_ind.all_splits.  Any split violating the prediction would refute the mechanism.
"""
import random
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from igeom import orient, general_position, convex_quads, in_convex_position_idx
from splits_ind import all_splits
from gon_ind import gon


def count_convex_k(S, k):
    quads = convex_quads(S)
    return sum(1 for T in combinations(range(len(S)), k) if in_convex_position_idx(T, quads))


def local_search(rng, n, k, R, steps):
    while True:
        S = [(rng.randint(0, R), rng.randint(0, R)) for _ in range(n)]
        if len(set(S)) == n and general_position(S):
            break
    cur = count_convex_k(S, k)
    for _ in range(steps):
        if cur == 0:
            return S
        i = rng.randrange(n)
        scale = rng.choice([R // 50 + 1, R // 10 + 1, R])
        p = (S[i][0] + rng.randint(-scale, scale), S[i][1] + rng.randint(-scale, scale))
        T = S[:i] + [p] + S[i + 1:]
        if len(set(T)) != n or not general_position(T):
            continue
        c = count_convex_k(T, k)
        if c <= cur:
            S, cur = T, c
    return S if cur == 0 else None


def main():
    k = int(sys.argv[1])
    nsets = int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    n = 2 ** (k - 2)
    found = 0
    stats = dict(sets=0, sets_with_split=0, splits=0, violations=0)
    types = {}
    tries = 0
    while found < nsets and tries < 50 * nsets:
        tries += 1
        S = local_search(rng, n, k, 10 ** 4, 4000 if k == 5 else 6000)
        if S is None:
            continue
        assert gon(S) <= k - 1
        found += 1
        stats['sets'] += 1
        sp, st = all_splits(S)
        if sp:
            stats['sets_with_split'] += 1
        for s in sp:
            stats['splits'] += 1
            key = (s['nA'], s['nB'], s['c'], s['d'])
            types[key] = types.get(key, 0) + 1
            if k == 5:
                ok = (s['c'], s['d'], s['nA'], s['nB']) == (2, 2, 4, 4)
            else:
                ok = (s['c'], s['d'], s['nA'], s['nB']) in ((2, 3, 5, 11), (3, 2, 11, 5))
            if not ok:
                stats['violations'] += 1
                print('VIOLATION', S, s)
    print(dict(k=k, n=n, seed=seed, tries=tries, **stats, types=types))


if __name__ == '__main__':
    main()
