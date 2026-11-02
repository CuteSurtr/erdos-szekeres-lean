#!/usr/bin/env python3
"""Cross-check of the chain family against brute force on small cases.

For random nested configurations (m, t small) compare
  (a) 'chain family satisfied by the least-fixpoint extension of the real assignment'
  (b) 'no K points in convex position' (brute force over all K-subsets, convex hull by monotone chain).
Soundness of the encoding requires (b) => (a); the encoding is exact if also (a) => (b).
Also checks that the non-chain families are satisfied.
usage: test_bruteforce.py CNF N seed
"""
import sys, json, random, itertools, math
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen
from validate import layers_to_points, random_layers
from validate2 import real_assign, stream_check


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull_size(P):
    P = sorted(P)
    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2


def has_convex_k(pts, K):
    for S in itertools.combinations(pts, K):
        if hull_size(list(S)) == K:
            return True
    return False


if __name__ == '__main__':
    cnf = sys.argv[1]
    meta = json.load(open(cnf + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    E = gen.Enc(m, K, t)
    base = E.nv
    N = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    stats = {'free_both': 0, 'kgon_both': 0, 'MISMATCH_sound': 0, 'mismatch_exact': 0, 'nonchain_viol': 0}
    for s in range(N):
        mode = ['free', 'needle'][s % 2]
        layers = random_layers(m, t, rng, mode)
        assign, mind = real_assign(E, m, layers)
        if mind < 1e-9:
            continue
        bad = stream_check(cnf, meta, dict(assign), base)
        pts, lay = layers_to_points(m, layers)
        kg = has_convex_k(pts, K)
        chain_ok = (bad['chain'] == 0)
        if any(bad[f] for f in ('order', 'angle', 'nest')):
            stats['nonchain_viol'] += 1
        if not kg and chain_ok:
            stats['free_both'] += 1
        elif kg and not chain_ok:
            stats['kgon_both'] += 1
        elif not kg and not chain_ok:
            stats['MISMATCH_sound'] += 1
            print('UNSOUND?', layers)
        else:
            stats['mismatch_exact'] += 1
    print(cnf, 'N =', N, stats)
