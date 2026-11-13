#!/usr/bin/env python3
"""Independent check of claim C2 (accounting identity 252+154+2 = 408, 311 = 408-97).

Standard library only, exact integers.  Reads (read-only) the repository catalogs.
Usage: python3 -I check_identity.py <balanced-v2-source.json> <residual-source.json> <source-2650.json.gz>
"""
import gzip
import json
import sys
from itertools import product
from math import comb

ok = True


def check(label, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + label)
    ok = ok and bool(cond)


# ---------------------------------------------------------------- 1. arithmetic
check("C(10,5) == 252", comb(10, 5) == 252)
check("C(10,4) - C(8,3) == 154", comb(10, 4) - comb(8, 3) == 154)
check("C(11,6) - C(8,5) + 2 == 408  (MV formula C(2n-5,n-2)-C(2n-8,n-3)+2 at n=8)",
      comb(2 * 8 - 5, 8 - 2) - comb(2 * 8 - 8, 8 - 3) + 2 == 408)
check("252 + 154 + 2 == 408", 252 + 154 + 2 == 408)
check("64 + 33 == 97", 64 + 33 == 97)
check("408 - 97 == 311", 408 - 97 == 311)
check("(252-64) + (154-33) + 1 + 1 == 311", (252 - 64) + (154 - 33) + 1 + 1 == 311)
# Lean constants: balanced_bound_of_hole_budget gives 251 - budget, residual 153 - budget,
# forces_of_population_bounds gives B + R + 2.
B = 251 - 63
R = 153 - 32
check("Lean: B = 251-63 = 188 = 252-64", B == 188 == 252 - 64)
check("Lean: R = 153-32 = 121 = 154-33", R == 121 == 154 - 33)
check("Lean: B + R + 2 == 311", B + R + 2 == 311)
# earlier records for consistency of the composition constant
check("313 record: 190 + 121 + 2 == 313", 190 + 121 + 2 == 313)
check("312 record: 189 + 121 + 2 == 312", 189 + 121 + 2 == 312)
check("314 record: 190 + 122 + 2 == 314", 190 + 122 + 2 == 314)

# general-n form of the identity: C(2n-6,n-3) + [C(2n-6,n-4) - C(2n-8,n-5)] + 2 == MV(n)
gen = all(
    comb(2 * n - 6, n - 3) + comb(2 * n - 6, n - 4) - comb(2 * n - 8, n - 5) + 2
    == comb(2 * n - 5, n - 2) - comb(2 * n - 8, n - 3) + 2
    for n in range(6, 60)
)
check("general n in [6,60): balanced count + residual baseline + 2 == MV(n)", gen)
check("MV(7) == 113 (survey value)", comb(9, 5) - comb(6, 4) + 2 == 113)

# ---------------------------------------------------------------- 2. brute-force state counts


def downsets(width, height):
    """All down-sets of the poset [width] x [height] (cells (i,j), 1-based), by
    cell-by-cell DFS: a cell may be added only if (i-1,j) and (i,j-1) are present.
    Independent of the column-height characterization."""
    cells = [(i, j) for i in range(1, width + 1) for j in range(1, height + 1)]
    out = []

    def rec(k, cur):
        if k == len(cells):
            out.append(frozenset(cur))
            return
        i, j = cells[k]
        rec(k + 1, cur)  # exclude
        if (i == 1 or (i - 1, j) in cur) and (j == 1 or (i, j - 1) in cur):
            cur.add((i, j))
            rec(k + 1, cur)
            cur.discard((i, j))

    rec(0, set())
    return out


# The DFS above can add a cell whose lower neighbours are added *later* in cell order?
# No: cells are processed in lexicographic order (i, j), and (i-1, j), (i, j-1) both precede
# (i, j) lexicographically, so the test sees their final status.  Each down-set arises once.
bal = downsets(5, 5)
check("down-sets of [5]x[5] by DFS == 252", len(bal) == 252)
heights_bal = sorted(
    tuple(max([j for (i, j) in D if i == c] + [0]) for c in range(1, 6)) for D in bal
)
seq_bal = sorted(
    f for f in product(range(6), repeat=5) if all(f[k] >= f[k + 1] for k in range(4))
)
check("nonincreasing height profiles 5>=f1>=..>=f5>=0 == 252 and match DFS", heights_bal == seq_bal and len(seq_bal) == 252)

res_all = downsets(4, 6)  # first coordinate in 1..4 indexes columns, heights up to 6
check("down-sets of [4]x[6] == 210", len(res_all) == 210)
# (2.1): f1 < 6 or f2 = 6, i.e. exclude down-sets in which (1,6) is a maximal cell
excluded = [D for D in res_all if (1, 6) in D and (2, 6) not in D]
check("down-sets with (1,6) maximal == 56 == C(8,3)", len(excluded) == 56 == comb(8, 3))
res = [D for D in res_all if not ((1, 6) in D and (2, 6) not in D)]
check("residual catalog count == 154", len(res) == 154)
heights_res = sorted(
    tuple(max([j for (i, j) in D if i == c] + [0]) for c in range(1, 5)) for D in res
)

# ---------------------------------------------------------------- 3. repository catalogs
if len(sys.argv) >= 3:
    bsrc = json.load(open(sys.argv[1]))
    rsrc = json.load(open(sys.argv[2]))
    bst = [tuple(s) for s in bsrc["states"]]
    rst = [tuple(s) for s in rsrc["states"]]
    check("balanced catalog: 252 distinct states", len(bst) == 252 == len(set(bst)))
    check("balanced catalog == enumerated profiles", sorted(bst) == seq_bal)
    check("balanced catalog: 3131 rows", len(bsrc["constraints"]) == 3131)
    check("residual catalog: 154 distinct states", len(rst) == 154 == len(set(rst)))
    check("residual catalog: fifth coordinate always 0", all(len(s) == 5 and s[4] == 0 for s in rst))
    check("residual catalog == enumerated (2.1)-profiles", sorted(s[:4] for s in rst) == heights_res)
    check("balanced index 0 is empty state", bst[0] == (0, 0, 0, 0, 0))
    check("residual index 0 is empty state", rst[0] == (0, 0, 0, 0, 0))
if len(sys.argv) >= 4:
    with gzip.open(sys.argv[3], "rt") as fh:
        r2650 = json.load(fh)
    keys = list(r2650.keys()) if isinstance(r2650, dict) else None
    print("source-2650 keys:", keys)
    if isinstance(r2650, dict):
        st = r2650.get("states")
        rows = r2650.get("constraints") or r2650.get("rows")
        if st is not None:
            check("2650 catalog: 154 states, same as residual-source", [tuple(s) for s in st] == rst)
        if rows is not None:
            check("2650 catalog: 2650 rows", len(rows) == 2650)
            mx = max(max(r["support"]) for r in rows)
            check("2650 catalog: supports within 0..153", mx <= 153)

print("ALL CHECKS PASSED" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
