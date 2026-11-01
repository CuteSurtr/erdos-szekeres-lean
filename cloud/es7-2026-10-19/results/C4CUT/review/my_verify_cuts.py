"""Reviewer's own check of the C4CUT certificates (does not reuse verify_cuts.py / c4cut.py code).
usage: my_verify_cuts.py MAP CUTS"""
import json, sys, random, itertools
from collections import Counter

MAP, CUTS = sys.argv[1:3]
info = json.load(open(MAP))
var_of = {}       # sorted triple -> (var, s) with chi(sorted) = s * value(var)
trip_of_var = {}
for i, j, k, v, s in info["triples"]:
    var_of[(i, j, k)] = (v, s)
    trip_of_var.setdefault(v, []).append((i, j, k))


def perm_sign(seq):
    """sign of the permutation taking sorted(seq) to seq (distinct entries), by explicit cycle decomposition"""
    srt = sorted(seq)
    pos = [srt.index(x) for x in seq]
    sign, seen = 1, [False] * len(pos)
    for i in range(len(pos)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True; j = pos[j]; L += 1
            if L % 2 == 0:
                sign = -sign
    return sign


# 1. the three-term GP identity with explicit term signs, checked exactly on random integer points
def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


rnd = random.Random(7)
for _ in range(5000):
    a, b, c, d, e = [(rnd.randint(-999, 999), rnd.randint(-999, 999)) for _ in range(5)]
    assert det(a, b, c) * det(a, d, e) - det(a, b, d) * det(a, c, e) + det(a, b, e) * det(a, c, d) == 0
# and that it is not an identity with a different sign pattern (sanity: the check above is discriminating)
bad = 0
for _ in range(100):
    a, b, c, d, e = [(rnd.randint(-999, 999), rnd.randint(-999, 999)) for _ in range(5)]
    bad += det(a, b, c) * det(a, d, e) + det(a, b, d) * det(a, c, e) + det(a, b, e) * det(a, c, d) != 0
assert bad > 90
print("GP identity [abc][ade] - [abd][ace] + [abe][acd] = 0 verified exactly on 5000 random quintuples")

inner = set(range(20, 32))
inner_vars = {var_of[t][0] for t in itertools.combinations(sorted(inner), 3)}
patterns = []
for n, line in enumerate(open(CUTS)):
    rec = json.loads(line)
    lits = rec["clause"]
    vals = {}
    for x in lits:
        v = abs(x)
        assert v not in vals
        vals[v] = (x < 0)   # the clause is falsified iff every literal is false: x>0 -> v false, x<0 -> v true
    assert set(vals) == inner_vars, f"cut {n}: clause vars differ from the 55 inner-12 triple-orbit vars"

    def chi(a, b, c):
        t = tuple(sorted((a, b, c)))
        v, s = var_of[t]
        if v not in vals:
            raise KeyError(("bracket sign not fixed by the clause", t))
        return perm_sign((a, b, c)) * s * (1 if vals[v] else -1)

    # sanity: the forbidden pattern is a valid acyclic CC system on 4/5 points? (not needed for soundness)
    expo = Counter()
    nrows = 0
    for row in rec["certificate"]:
        a, b, c, d, e = row["anchor_quintuple"]
        assert len({a, b, c, d, e}) == 5
        w = row["weight"]
        assert type(w) is int and w > 0
        terms = [(+1, (a, b, c), (a, d, e)), (-1, (a, b, d), (a, c, e)), (+1, (a, b, e), (a, c, d))]
        signs = [co * chi(*t1) * chi(*t2) for co, t1, t2 in terms]
        cnt = Counter(signs)
        assert len(cnt) == 2, "GP sign condition violated by the forbidden pattern itself"
        mi = [i for i in range(3) if cnt[signs[i]] == 1][0]
        pair = lambda i: frozenset([frozenset(terms[i][1]), frozenset(terms[i][2])])
        P = frozenset(frozenset(t) for t in row["plus"])
        M = frozenset(frozenset(t) for t in row["minus"])
        assert P == pair(mi), f"cut {n}: 'plus' is not the minority term"
        assert M in [pair(i) for i in range(3) if i != mi], f"cut {n}: 'minus' is not another term"
        for t in P: expo[t] += w
        for t in M: expo[t] -= w
        nrows += 1
    assert nrows > 0 and all(x == 0 for x in expo.values()), f"cut {n}: exponents do not cancel"
    used = set(expo)
    patterns.append({var: vals[var] for var in vals})
    print(f"cut {n}: OK  rows={nrows}  distinct brackets used={len(used)}  weight sum={sum(r['weight'] for r in rec['certificate'])}"
          f"  max weight={max(r['weight'] for r in rec['certificate'])}")

# distinctness of the six forbidden patterns, also up to the residual symmetries (mirror = global sign flip)
for i, j in itertools.combinations(range(len(patterns)), 2):
    same = all(patterns[i][v] == patterns[j][v] for v in patterns[i])
    flip = all(patterns[i][v] != patterns[j][v] for v in patterns[i])
    print(f"patterns {i},{j}: identical={same} global-flip={flip}  hamming={sum(patterns[i][v] != patterns[j][v] for v in patterns[i])}")
