"""Random subsets of the real 57-point residual set (residual conditions are hereditary):
check last-point / lower-hull / second-point claims with exact Fractions (verify-residual-row)."""
import gzip, json, random, sys
from fractions import Fraction
sys.path.insert(0, sys.argv[1])
from resstate import cup_table, residual_states, residual_conditions, lower_hull_indices

REPO = sys.argv[2]
N = int(sys.argv[3])
cat = json.load(gzip.open(REPO + "/archive/es7-2026-10-19/results/LO33N20261113/budget34/data/frozen-inputs/source-2650.json.gz"))
idx = {tuple(s): i for i, s in enumerate(cat["states"])}
SECOND = {idx[s] for s in [(1, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 1, 1, 0, 0), (1, 1, 1, 1, 0)]}
d = json.load(open(REPO + "/archive/es7-2026-10-19/results/THEORY310N20261113/data/residual57_points.json"))
P0 = [(Fraction(x), Fraction(y)) for x, y in d["R_chart_points"]]
cup0 = cup_table(P0)
rng = random.Random(1121)
fails, tested, sizes, lhsizes = [], 0, {}, {}
flat_last = {}
for t in range(N):
    k = rng.randint(2, 57)
    S = sorted(rng.sample(range(57), k))
    P = [P0[i] for i in S]
    cup = {(a, b, c): cup0[S[a], S[b], S[c]] for a in range(k) for b in range(a + 1, k) for c in range(b + 1, k)}
    st, rk = residual_states(k, cup)
    ok, why = residual_conditions(k, cup, rk)
    if not ok:
        fails.append(("NONRESIDUAL_SUBSET", S, why)); continue
    if len(set(st)) != k or any(s not in idx for s in st):
        fails.append(("SANITY", S)); continue
    last = st[-1]
    if not (last[0] == last[1] == last[2] == last[3] >= 1):
        fails.append(("LAST", S, last))
    if idx[st[1]] not in SECOND:
        fails.append(("SECOND", S, st[1]))
    LH = lower_hull_indices(P)
    lhsizes[len(LH)] = lhsizes.get(len(LH), 0) + 1
    for v in LH[1:]:
        s = st[v]
        if not (s[0] == s[1] == s[2] == s[3] >= 1):
            fails.append(("LH", S, v, s))
    flat_last[last[0]] = flat_last.get(last[0], 0) + 1
    tested += 1
print(json.dumps({"subsets_tested": tested, "fails": len(fails), "first_fails": fails[:3],
                  "lower_hull_size_hist": dict(sorted(lhsizes.items())), "last_k_hist": dict(sorted(flat_last.items()))}))
