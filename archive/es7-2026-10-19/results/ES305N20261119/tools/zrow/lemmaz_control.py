#!/usr/bin/env python3
"""Exact positive control for Lemma Z (ES306N20261119 §9), own code from the Lean definitions:
  capLabel(u,v) = (points of the longest cap ending with edge (u,v)) - 1, cupLabel likewise (ActualRanks.labels);
  f_v(i) = max over u < v of cupLabel(u,v) restricted to capLabel(u,v) >= i+1, else 0   (BalancedStates.column).
On random integer point sets in general position with distinct x and no 7-cap and no 7-cup, check
  (1) the states f_v are pairwise distinct (balancedState_injective),
  (2) Lemma Z: the owners of states with f(0) <= 4 and f(4) = 0 contain no 6-cap and no 6-cup,
  (3) negative control: the owners of states with f(0) <= 5 contain a 6-cup in some sets (so (2) is not vacuous).
Exact integers only. usage: lemmaz_control.py SETS SEED
"""
import itertools, random, sys


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def chains(P):
    """cap[u][v], cup[u][v]: points in the longest cap / cup ending with edge (u, v) (P sorted by x)."""
    n = len(P); cap = [[0] * n for _ in range(n)]; cup = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            cap[u][v] = cup[u][v] = 2
            for t in range(u):
                o = orient(P[t], P[u], P[v])
                if o < 0: cap[u][v] = max(cap[u][v], cap[t][u] + 1)   # right turn: t,u,v is a cap
                elif o > 0: cup[u][v] = max(cup[u][v], cup[t][u] + 1)
    return cap, cup


def longest(S, P, kind):
    """longest cap (kind=-1) or cup (+1) inside the subset S (indices sorted by x)"""
    best = {}; m = 1 if S else 0
    for j, v in enumerate(S):
        for i in range(j):
            u = S[i]; best[(u, v)] = 2
            for t in S[:i]:
                if (t, u) in best and orient(P[t], P[u], P[v]) * kind > 0:
                    best[(u, v)] = max(best[(u, v)], best[(t, u)] + 1)
            m = max(m, best[(u, v)])
    return m


def main():
    sets, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
    tested = zsizes = neg_hits = 0
    while tested < sets:
        n = rng.randint(12, 40)
        P = sorted({(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(n)})
        if len({p[0] for p in P}) != len(P): continue
        if any(orient(a, b, c) == 0 for a, b, c in itertools.combinations(P, 3)): continue
        cap, cup = chains(P)
        if max(max(r) for r in cap) >= 7 or max(max(r) for r in cup) >= 7: continue   # need no 7-cap, no 7-cup
        n = len(P)
        F = []
        for v in range(n):
            f = []
            for i in range(5):
                vals = [cup[u][v] - 1 for u in range(v) if cap[u][v] - 1 >= i + 1]
                f.append(max(vals) if vals else 0)
            assert all(f[i] >= f[i + 1] for i in range(4)) and all(0 <= x <= 5 for x in f)
            F.append(tuple(f))
        assert len(set(F)) == n, 'states not injective'
        Zown = [v for v in range(n) if F[v][0] <= 4 and F[v][4] == 0]
        assert longest(Zown, P, -1) <= 5 and longest(Zown, P, +1) <= 5, 'Lemma Z fails'
        Wide = [v for v in range(n) if F[v][0] <= 5]
        if longest(Wide, P, +1) >= 6: neg_hits += 1
        tested += 1; zsizes += len(Zown)
    print(f'sets {tested}: injective and Lemma Z hold on all; mean Z-owners {zsizes / tested:.1f}; '
          f'negative control (f(0) <= 5 allows a 6-cup) hit in {neg_hits} sets')


if __name__ == '__main__':
    main()
