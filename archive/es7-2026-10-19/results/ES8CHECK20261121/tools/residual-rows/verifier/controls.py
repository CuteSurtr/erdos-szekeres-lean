"""Exact controls for candidate row C3 (verify-residual-row). Read-only on the repo snapshot."""
import gzip, json, random, sys, itertools
from fractions import Fraction
sys.path.insert(0, sys.argv[1])  # agent dir
from resstate import cup_table, residual_states, residual_conditions, largest_convex, lower_hull_indices

REPO = sys.argv[2]
cat = json.load(gzip.open(REPO + "/archive/es7-2026-10-19/results/LO33N20261113/budget34/data/frozen-inputs/source-2650.json.gz"))
states = [tuple(s) for s in cat["states"]]
idx = {s: i for i, s in enumerate(states)}
FLAT = [idx[(k, k, k, k, 0)] for k in range(1, 7)]
SECOND = [idx[s] for s in [(1, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 1, 1, 0, 0), (1, 1, 1, 1, 0)]]
print("flat state indices", FLAT, "second-point state indices", SECOND)

report = {"flat_idx": FLAT, "second_idx": SECOND}


def check_config(P, label, require_residual=True, stats=None):
    n = len(P)
    cup = cup_table(P)
    st, ranks = residual_states(n, cup)
    ok, why = residual_conditions(n, cup, ranks)
    if require_residual and not ok:
        return None
    # sanity: catalog membership and injectivity (Lean state_injective)
    for s in st:
        if s not in idx:
            return ("NOT_IN_CATALOG", label, s)
    if len(set(st)) != n:
        return ("NOT_INJECTIVE", label)
    if st[0] != (0, 0, 0, 0, 0):
        return ("FIRST_NOT_ZERO", label)
    fails = []
    if n >= 2:
        last = st[-1]
        if not (last[0] == last[1] == last[2] == last[3] >= 1):
            fails.append(("LAST_NOT_FLAT", last))
        if idx[st[1]] not in SECOND:
            fails.append(("SECOND_BAD", st[1]))
        for v in lower_hull_indices(P):
            if v == 0:
                continue
            s = st[v]
            if not (s[0] == s[1] == s[2] == s[3] >= 1):
                fails.append(("LH_NOT_FLAT", v, s))
    if stats is not None:
        nonflat_inner = sum(1 for v in range(1, n) if not (st[v][0] == st[v][1] == st[v][2] == st[v][3]))
        stats["nonflat_nonhull_points"] += nonflat_inner
        stats["second_state_counts"][str(st[1])] = stats["second_state_counts"].get(str(st[1]), 0) + 1
        stats["last_state_counts"][str(st[-1])] = stats["last_state_counts"].get(str(st[-1]), 0) + 1
    return ("FAIL", label, fails) if fails else ("OK", st)


# 1. the real 57-point residual set
d = json.load(open(REPO + "/archive/es7-2026-10-19/results/THEORY310N20261113/data/residual57_points.json"))
P = [(Fraction(x), Fraction(y)) for x, y in d["R_chart_points"]]
assert all(P[i][0] < P[i + 1][0] for i in range(len(P) - 1))
cup = cup_table(P)
st, ranks = residual_states(len(P), cup)
okres, why = residual_conditions(len(P), cup, ranks)
lc = largest_convex(P, cup)
LH = lower_hull_indices(P)
r57 = {"n": len(P), "residual_conditions": why, "largest_convex": lc,
       "lower_hull": [(v, st[v]) for v in LH], "second_state": st[1], "last_state": st[-1],
       "check": check_config(P, "real57")[0], "distinct_states": len(set(st))}
print("real57", r57)
report["real57"] = r57

# 2. random residual sets (integer coordinates, distinct x, general position)
rng = random.Random(20261121)
stats = {"tested": 0, "rejected_nonresidual": 0, "rejected_octagon": 0, "fail": 0,
         "nonflat_nonhull_points": 0, "second_state_counts": {}, "last_state_counts": {}, "by_n": {}}
target = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
fails = []
attempts = 0
while stats["tested"] < target and attempts < 50 * target:
    attempts += 1
    n = rng.randint(2, 26)
    mode = rng.random()
    xs = rng.sample(range(-10**6, 10**6), n)
    xs.sort()
    if mode < 0.4:
        pts = [(x, rng.randint(-10**6, 10**6)) for x in xs]
    elif mode < 0.7:  # convex-ish perturbation to create long cups/caps
        pts = [(x, (x * x) // (10**6) * rng.choice([1, -1]) + rng.randint(-2 * 10**5, 2 * 10**5)) for x in xs]
    else:  # gaussian clusters
        pts = [(x, int(rng.gauss(0, 3 * 10**5))) for x in xs]
    try:
        cup = cup_table(pts)
    except ValueError:
        continue
    stt, rk = residual_states(n, cup)
    ok, why = residual_conditions(n, cup, rk)
    if not ok:
        stats["rejected_nonresidual"] += 1
        continue
    if largest_convex(pts, cup) >= 8:
        stats["rejected_octagon"] += 1
        continue
    res = check_config(pts, ("rand", attempts), True, stats)
    stats["tested"] += 1
    stats["by_n"][n] = stats["by_n"].get(n, 0) + 1
    if res[0] != "OK":
        stats["fail"] += 1
        fails.append(res)
stats["attempts"] = attempts
stats["fails"] = fails[:5]
print("random", json.dumps({k: v for k, v in stats.items() if k != "by_n"}))
print("by_n", dict(sorted(stats["by_n"].items())))
report["random"] = stats

# 3. abstract colourings (no geometry): last-point and second-point claims hold for every colouring
def abstract_check(n, cup):
    stt, rk = residual_states(n, cup)
    ok, why = residual_conditions(n, cup, rk)
    if not ok:
        return None
    last = stt[-1]
    good = (last[0] == last[1] == last[2] == last[3] >= 1) and idx.get(stt[1]) in SECOND and all(s in idx for s in stt)
    # abstract 'lower hull vertex': v with cup(u,v,w) true for all u<v<w
    for v in range(1, n):
        if all(cup[u, v, w] for u in range(v) for w in range(v + 1, n)):
            s = stt[v]
            good = good and (s[0] == s[1] == s[2] == s[3] >= 1)
    return good

ab = {}
for n in range(2, 7):
    trip = list(itertools.combinations(range(n), 3))
    tot = good = 0
    if len(trip) <= 10:
        it = itertools.product([False, True], repeat=len(trip))
    else:
        it = (tuple(rng.random() < 0.5 for _ in trip) for _ in range(30000))
    for bits in it:
        cup = dict(zip(trip, bits))
        r = abstract_check(n, cup)
        if r is None:
            continue
        tot += 1
        good += bool(r)
    ab[n] = (tot, good)
print("abstract colourings (tested, passing):", ab)
report["abstract"] = ab

# 4. negative control: the checker does reject a non-flat claim on an interior point
neg = None
for res_try in range(2000):
    n = 8
    xs = sorted(rng.sample(range(-1000, 1000), n))
    pts = [(x, rng.randint(-1000, 1000)) for x in xs]
    try:
        cup = cup_table(pts)
    except ValueError:
        continue
    stt, rk = residual_states(n, cup)
    LH = set(lower_hull_indices(pts))
    nonhull_nonflat = [v for v in range(1, n) if v not in LH and not (stt[v][0] == stt[v][1] == stt[v][2] == stt[v][3])]
    if nonhull_nonflat:
        neg = {"points": pts, "nonhull_nonflat": [(v, stt[v]) for v in nonhull_nonflat]}
        break
print("negative control (non-hull points with non-flat states exist):", neg is not None, neg["nonhull_nonflat"][:3] if neg else None)
report["negctrl_found"] = neg is not None
json.dump(report, open(sys.argv[1] + "/controls_out.json", "w"), indent=1, default=str)
