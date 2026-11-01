import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_splits import one_sided, general_position, lp_witness, verify_split
from backtrack_onesided import enumerate_onesided
from exact_z import z_exists, verify
sys.path.insert(1, sys.argv[1])           # tools/ directory of this result (read-only use)
import splits as primary
def planted(rng, na, nb):
    A = [(rng.randint(-50, 50), rng.randint(0, 40)) for _ in range(na)]
    B = [(rng.randint(-50, 50) + rng.randint(-3, 3), -10**6 + rng.randint(-30, 30)) for _ in range(nb)]
    return A + B
rng = random.Random(2026)
agree = dis = 0; neg = 0; counts = {}
for trial in range(120):
    n = rng.randint(8, 13)
    if trial % 3 == 0:
        P = [(rng.randint(-30, 30), rng.randint(-30, 30)) for _ in range(n)]
    else:
        na = rng.randint(2, n - 2); P = planted(rng, na, n - na)
    if not general_position(P):
        continue
    for A in enumerate_onesided(P)[0]:
        B = frozenset(range(n)) - A
        mine, _ = z_exists(P, A, B)
        sz = primary.find_z(P, A, B)
        theirs = "none" if sz is None else ("numeric" if (isinstance(sz, tuple) and sz and sz[0] == "numeric") else "exact")
        # my own LP-based witness search as a third opinion
        third = any(verify_split(P, A, B, z)[0] for z in lp_witness(P, A, B))
        key = (mine, theirs, third); counts[key] = counts.get(key, 0) + 1
        if False:
            agree += 1
        else:
            pass
        neg += (not mine)
print("counts (exact_z, splits.find_z, my_lp):", counts)
