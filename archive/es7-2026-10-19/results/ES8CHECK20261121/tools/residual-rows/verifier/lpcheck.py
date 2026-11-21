"""Independent LP re-measurement for candidate row C3 (verify-residual-row).
min sum h over h in [0,1]^154, h0 = 0, rows sum_{S} h >= rhs (2,650 Lean rows + extra non-capacity rows),
capacity rows h(F) >= T, h(Lo) >= B - T; with and without the two endpoint rows
sum_{FLAT} h <= 5 and sum_{SECOND} h <= 3.  HiGHS gives a point; it is then rounded to Fractions and every
row is re-checked exactly (the lower bound B is trivial from the two capacity rows)."""
import gzip, json, sys
from fractions import Fraction
import numpy as np
import highspy

REPO, EXTRA, B = sys.argv[1], sys.argv[2], int(sys.argv[3])
SLICES = [int(t) for t in sys.argv[4].split(",")]
cat = json.load(gzip.open(REPO + "/archive/es7-2026-10-19/results/LO33N20261113/budget34/data/frozen-inputs/source-2650.json.gz"))
states = [tuple(s) for s in cat["states"]]
idx = {s: i for i, s in enumerate(states)}
NS = 154
F = [i for i in range(NS) if states[i][0] >= 5]
Lo = [i for i in range(NS) if states[i][0] <= 4]
FLAT = [idx[(k, k, k, k, 0)] for k in range(1, 7)]
SECOND = [idx[s] for s in [(1, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 1, 1, 0, 0), (1, 1, 1, 1, 0)]]
rows = [(r["support"], r["rhs"]) for r in cat["constraints"]]
extra = json.load(open(EXTRA)) if EXTRA.endswith(".json") else [json.loads(l) for l in open(EXTRA)]
# drop the capacity rows of the extra file (first two, supports F / Lo)
nc = []
for r in extra:
    s = sorted(r["support"])
    if s == F or s == Lo:
        continue
    nc.append((r["support"], r["rhs"]))
print("base rows", len(rows), "extra non-capacity rows", len(nc))
allrows = rows + nc


def solve(T, endpoint):
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    inf = highspy.kHighsInf
    for i in range(NS):
        h.addVar(0.0, 0.0 if i == 0 else 1.0)
    h.changeColsCost(NS, np.arange(NS, dtype=np.int32), np.ones(NS))
    R = list(allrows) + [(F, T), (Lo, B - T)]
    for s, d in R:
        h.addRow(float(d), inf, len(s), np.array(s, dtype=np.int32), np.ones(len(s)))
    if endpoint:
        h.addRow(-inf, 5.0, 6, np.array(FLAT, dtype=np.int32), np.ones(6))
        h.addRow(-inf, 3.0, 4, np.array(SECOND, dtype=np.int32), np.ones(4))
    h.run()
    st = h.modelStatusToString(h.getModelStatus())
    x = list(h.getSolution().col_value)
    return st, h.getInfo().objective_function_value, x, R


def exact_check(x, R, endpoint, den=720):
    q = [Fraction(v).limit_denominator(den) for v in x]
    q = [min(max(v, Fraction(0)), Fraction(1)) for v in q]
    q[0] = Fraction(0)
    viol = sum(1 for s, d in R if sum(q[i] for i in s) < d)
    ep = (sum(q[i] for i in FLAT) <= 5, sum(q[i] for i in SECOND) <= 3)
    return sum(q), viol, ep, max(v.denominator for v in q), q


out = {}
for T in SLICES:
    st0, v0, x0, R = solve(T, False)
    st1, v1, x1, R1 = solve(T, True)
    tot, viol, ep, den, q = exact_check(x1, R, True)
    x0q = exact_check(x0, R, False)
    ent = {"slice": (T, B - T), "lp_without": (st0, v0), "lp_with": (st1, v1),
           "exact_point_with": {"sum_h": str(tot), "violated_rows": viol, "endpoint_rows_ok": ep, "max_den": den,
                                 "flat_sum": str(sum(q[i] for i in FLAT)), "second_sum": str(sum(q[i] for i in SECOND)),
                                 "integral": all(v.denominator == 1 for v in q)},
           "without_point_flat_second": (str(sum(x0q[4][i] for i in FLAT)), str(sum(x0q[4][i] for i in SECOND)))}
    # range of the hole sums on the two sets over {rows, capacity rows, sum h <= B}
    rng = {}
    for name, S in (("FLAT", FLAT), ("SECOND", SECOND)):
        for sense in (1, -1):
            hh = highspy.Highs(); hh.setOptionValue("output_flag", False); hh.setOptionValue("threads", 1)
            for i in range(NS):
                hh.addVar(0.0, 0.0 if i == 0 else 1.0)
            c = np.zeros(NS); c[S] = sense
            hh.changeColsCost(NS, np.arange(NS, dtype=np.int32), c)
            for s, d in R:
                hh.addRow(float(d), highspy.kHighsInf, len(s), np.array(s, dtype=np.int32), np.ones(len(s)))
            hh.addRow(-highspy.kHighsInf, float(B), NS, np.arange(NS, dtype=np.int32), np.ones(NS))
            hh.run()
            rng[(name, "min" if sense == 1 else "max")] = (hh.modelStatusToString(hh.getModelStatus()),
                                                           sense * hh.getInfo().objective_function_value)
    ent["range_over_rows_sumh_le_B"] = {f"{k[0]}_{k[1]}": v for k, v in rng.items()}
    out[T] = ent
    print(json.dumps(ent))
json.dump(out, open(sys.argv[5], "w"), indent=1, default=str)
