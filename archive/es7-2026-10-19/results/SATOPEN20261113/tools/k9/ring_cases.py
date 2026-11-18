#!/usr/bin/env python3
"""Exact case list of the ring "two displaced layers" (C.5) and its certification status (15 Nov 2026).

A case is dropped when its fixed order already makes some run forbidden by a proved theorem monotone:
  Theorem 3: psi_3..psi_13 (all 11 layers) weakly monotone;  Theorem 4: 12 consecutive phases weakly monotone.
Linear ex2_J_K: the 13 layers {1..15}-{J,K} increase with index. Cyclic cycx_kK_pP (P = 1..13): the 14 layers
s = {1..15}-{K} in phase order s_{P+1} < ... < s_14 < s_1 < ... < s_P; within each of the two segments phase increases
with the index, and between them it decreases, so a run of >= 3 consecutive layers is monotone exactly when all its
layers avoid the free layers and lie in one segment.  Theorem 5 (no monotone subsequence of length 14) removes no
case here (no segment has 14 layers).  Expected counts (C.5): 95 linear, 175 cyclic.
usage: ring_cases.py [CUBES_DIR]   prints counts, the certified/remaining lists, and asserts the counts.
"""
import os
import sys

RUNS = [range(3, 14)] + [range(a, a + 12) for a in range(1, 5)]   # Theorem 3 run, Theorem 4 runs


def covered_linear(j, k):
    free = {j, k}
    return any(not free & set(r) for r in RUNS)        # all other layers increase together


def covered_cyclic(K, P):
    s = [i for i in range(1, 16) if i != K]
    segA, segB = set(s[P:]), set(s[:P])
    return any(set(r) <= segA or set(r) <= segB for r in RUNS)


linear = [(j, k) for j in range(1, 16) for k in range(j + 1, 16) if not covered_linear(j, k)]
cyclic = [(K, P) for K in range(1, 16) for P in range(1, 14) if not covered_cyclic(K, P)]
assert len(linear) == 95 and len(cyclic) == 175, (len(linear), len(cyclic))

if __name__ == '__main__':
    C = sys.argv[1] if len(sys.argv) > 1 else '/home/jay/research/data/satopen-20261113/k9/cubes'

    def certified(name):
        p = os.path.join(C, name, 'result.txt')
        return os.path.exists(p) and 'VERIFIED_LINES 1' in open(p).read()

    for kind, cases, fmt in (('linear', linear, 'ex2_{}_{}'), ('cyclic', cyclic, 'cycx_k{}_p{}')):
        names = [fmt.format(*c) for c in cases]
        done = [n for n in names if certified(n)]
        print(f'{kind}: {len(names)} cases, {len(done)} certified, {len(names) - len(done)} remaining')
        print('  remaining:', ' '.join(n for n in names if n not in done))
