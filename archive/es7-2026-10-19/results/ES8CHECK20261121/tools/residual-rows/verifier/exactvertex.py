"""Exact vertex reconstruction (verify-residual-row, own code): solve the LP with HiGHS simplex, read the basis,
solve the basic system in Fractions, then re-check every row exactly.  A feasible exact point with sum h = B in the
system {rows, capacity rows, endpoint rows, h0 = 0} certifies LP value exactly B (the lower bound B is the sum of the
two capacity rows), i.e. exactly zero LP gain from the endpoint rows."""
import gzip, json, sys
from fractions import Fraction
import numpy as np
import highspy

REPO, EXTRA, B = sys.argv[1], sys.argv[2], int(sys.argv[3])
SLICES = [int(t) for t in sys.argv[4].split(",")]
WITH_EP = sys.argv[5] == "1"
cat = json.load(gzip.open(REPO + "/archive/es7-2026-10-19/results/LO33N20261113/budget34/data/frozen-inputs/source-2650.json.gz"))
states = [tuple(s) for s in cat["states"]]
idx = {s: i for i, s in enumerate(states)}
NS = 154
F = [i for i in range(NS) if states[i][0] >= 5]
Lo = [i for i in range(NS) if states[i][0] <= 4]
FLAT = [idx[(k, k, k, k, 0)] for k in range(1, 7)]
SECOND = [idx[s] for s in [(1, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 1, 1, 0, 0), (1, 1, 1, 1, 0)]]
rows = [(list(r["support"]), r["rhs"]) for r in cat["constraints"]]
if EXTRA.endswith(".json"):
    extra = json.load(open(EXTRA))
else:
    extra = [json.loads(l) for l in open(EXTRA)]
nc = [(list(r["support"]), r["rhs"]) for r in extra if sorted(r["support"]) not in (F, Lo)]


def solve_exact(T):
    # constraint list: (support, lo, hi)
    C = [(s, Fraction(d), None) for s, d in rows + nc] + [(F, Fraction(T), None), (Lo, Fraction(B - T), None)]
    if WITH_EP:
        C += [(FLAT, None, Fraction(5)), (SECOND, None, Fraction(3))]
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    h.setOptionValue("solver", "simplex")
    inf = highspy.kHighsInf
    for i in range(NS):
        h.addVar(0.0, 0.0 if i == 0 else 1.0)
    h.changeColsCost(NS, np.arange(NS, dtype=np.int32), np.ones(NS))
    for s, lo, hi in C:
        h.addRow(float(lo) if lo is not None else -inf, float(hi) if hi is not None else inf,
                 len(s), np.array(s, dtype=np.int32), np.ones(len(s)))
    h.run()
    bas = h.getBasis()
    cs, rs = list(bas.col_status), list(bas.row_status)
    K = highspy.HighsBasisStatus
    fixed = {}
    basic_cols = []
    for i in range(NS):
        if cs[i] == K.kBasic:
            basic_cols.append(i)
        elif cs[i] == K.kUpper:
            fixed[i] = Fraction(0) if i == 0 else Fraction(1)
        else:
            fixed[i] = Fraction(0)
    tight = []
    for j, (s, lo, hi) in enumerate(C):
        if rs[j] == K.kBasic:
            continue
        val = lo if (rs[j] == K.kLower and lo is not None) else (hi if hi is not None else lo)
        tight.append((s, val))
    assert len(tight) == len(basic_cols), (len(tight), len(basic_cols))
    pos = {c: k for k, c in enumerate(basic_cols)}
    m = len(basic_cols)
    A = []
    for s, val in tight:
        row = [Fraction(0)] * (m + 1)
        rhs = val
        for i in s:
            if i in pos:
                row[pos[i]] += 1
            else:
                rhs -= fixed[i]
        row[m] = rhs
        A.append(row)
    # Gauss-Jordan in Fractions
    r = 0
    for c in range(m):
        p = next((k for k in range(r, m) if A[k][c] != 0), None)
        if p is None:
            raise RuntimeError("singular basis")
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for k in range(m):
            if k != r and A[k][c] != 0:
                f = A[k][c]
                A[k] = [a - f * b for a, b in zip(A[k], A[r])]
        r += 1
    x = dict(fixed)
    for k, c in enumerate(basic_cols):
        x[c] = A[k][m]
    xs = [x[i] for i in range(NS)]
    # exact re-check
    bad_bounds = sum(1 for i in range(NS) if not (0 <= xs[i] <= (0 if i == 0 else 1)))
    viol = 0
    for s, lo, hi in C:
        t = sum(xs[i] for i in s)
        if (lo is not None and t < lo) or (hi is not None and t > hi):
            viol += 1
    tot = sum(xs)
    return {"slice": [T, B - T], "with_endpoint_rows": WITH_EP, "highs": h.modelStatusToString(h.getModelStatus()),
            "basis_size": m, "sum_h": str(tot), "bound_violations": bad_bounds, "row_violations": viol,
            "rows_checked": len(C), "h0": str(xs[0]), "flat_sum": str(sum(xs[i] for i in FLAT)),
            "second_sum": str(sum(xs[i] for i in SECOND)), "max_den": max(v.denominator for v in xs),
            "n_fractional": sum(1 for v in xs if v.denominator != 1),
            "hF": str(sum(xs[i] for i in F)), "hLo": str(sum(xs[i] for i in Lo))}


print("base", len(rows), "extra non-capacity", len(nc))
res = [solve_exact(T) for T in SLICES]
for e in res:
    print(json.dumps(e))
json.dump(res, open(sys.argv[6], "w"), indent=1)
