"""Validate the complete enumerators against definitional brute force over all 2^n partitions (small n)."""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_splits import enumerate_models, one_sided, general_position, orient
from backtrack_onesided import enumerate_onesided
from exact_z import z_exists, verify

def brute(P):
    n = len(P); out = set()
    for mask in range(1 << n):
        A = frozenset(i for i in range(n) if mask >> i & 1); B = frozenset(range(n)) - A
        if len(A) >= 2 and len(B) >= 2 and one_sided(P, A, B):
            out.add(A)
    return out

def planted(rng, na, nb):
    # A: points near the upper part of a large circle-ish arc (random), B: far below, flattened
    A = [(rng.randint(-50, 50), rng.randint(0, 40)) for _ in range(na)]
    B = [(rng.randint(-50, 50) + rng.randint(-3, 3), -10**6 + rng.randint(-30, 30)) for _ in range(nb)]
    return A + B

rng = random.Random(2026)
wd = os.path.dirname(os.path.abspath(__file__))
tot = {"sets": 0, "positive_sets": 0, "partitions": 0, "with_z": 0}
for trial in range(120):
    n = rng.randint(8, 13)
    if trial % 3 == 0:
        P = [(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)]
    else:
        na = rng.randint(2, n - 2); P = planted(rng, na, n - na)
    if not general_position(P):
        continue
    tot["sets"] += 1
    bf = brute(P)
    bt = set(enumerate_onesided(P)[0])
    sat = set(A for A, B in enumerate_models(P, wd, "val")[0])
    assert bf == bt == sat, (P, len(bf), len(bt), len(sat))
    if bf: tot["positive_sets"] += 1
    tot["partitions"] += len(bf)
    for A in bf:
        B = frozenset(range(n)) - A
        ok, w = z_exists(P, A, B)
        if ok:
            assert verify(P, A, B, w); tot["with_z"] += 1
print("agreement brute force == backtracking == SAT on all sets:", tot)
