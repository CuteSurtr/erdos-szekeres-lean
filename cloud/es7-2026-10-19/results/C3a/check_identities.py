#!/usr/bin/env python3
"""Re-verify identities 1-4 of the C3a task on random 3-fold symmetric sets (exact signs).
usage: check_identities.py NSETS SEED"""
import itertools
import json
import random
import sys

from c3geom import Labelled, ochi, random_c3


def check(L):
    n, m = L.n, L.m
    bad = []
    # 1. R acts on labels as i -> i - m mod 3m
    if L.Rlab != [(i - m) % n for i in range(n)]:
        bad.append("id1")
    eps = [1 if i < m else -1 for i in range(n)]
    for (i, j, k), c in L.chip.items():
        # 2. chi_S = chi' * (-1)^(sigma_i+sigma_j+sigma_k)
        if L.chiS[(i, j, k)] != c * (-1) ** (L.sigma[i] + L.sigma[j] + L.sigma[k]):
            bad.append(("id2", i, j, k))
        # 3. chi'(Ri,Rj,Rk) = chi'(ijk) eps_i eps_j eps_k
        R = L.Rlab
        if ochi(L.chip, (R[i], R[j], R[k])) != c * eps[i] * eps[j] * eps[k]:
            bad.append(("id3", i, j, k))
        # 4. prefix condition on inversions
        pat = (L.inv[(i, j)], L.inv[(i, k)], L.inv[(j, k)])
        ok = {(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)} if c > 0 else {(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)}
        if pat not in ok:
            bad.append(("id4prefix", i, j, k))
    for i in range(n):
        if L.sigma[L.Rlab[i]] != L.sigma[i] ^ (1 if i >= m else 0):
            bad.append(("id3sigma", i))
    for i, j in itertools.combinations(range(n), 2):
        if L.before[(i, j)] != L.inv[(i, j)] ^ L.sigma[i] ^ L.sigma[j]:
            bad.append(("id4order", i, j))
        if L.sigma[i] == 0 and L.sigma[j] == 1 and L.inv[(i, j)] != 1:
            bad.append(("id4forced01", i, j))
        if L.sigma[i] == 1 and L.sigma[j] == 0 and L.inv[(i, j)] != 0:
            bad.append(("id4forced10", i, j))
    # sigma pattern per orbit: (s, not s, s) on labels (r, r+m, r+2m)
    for r in range(m):
        if not (L.sigma[r + m] == 1 - L.sigma[r] and L.sigma[r + 2 * m] == L.sigma[r]):
            bad.append(("sigmapattern", r))
    return bad


def main():
    N, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    nbad = 0
    for t in range(N):
        m = rng.randint(1, 11)
        shape = rng.choice(["disk", "ring", (rng.randint(-900, 900), rng.randint(-900, 900))])
        L = Labelled(random_c3(m, rng, shape=shape), rng)
        b = check(L)
        if b:
            nbad += 1
            print(json.dumps({"set": t, "m": m, "bad": b[:10]}))
    print(json.dumps({"sets": N, "seed": seed, "failures": nbad}))


if __name__ == "__main__":
    main()
