#!/usr/bin/env python3
"""Independent re-check (written from scratch, stdlib only) of the six C4CUT realizability cuts.

Checks
 0. The three-term Grassmann-Pluecker identity [abc][ade] - [abd][ace] + [abe][acd] = 0 on random integer points
    (exact integers), and that it fails if the middle sign is flipped (control).
 1. The variable map c4_n32L.json is consistent with the fourfold rotation rho: 4o+r -> 4o+((r+1) mod 4):
    for every sorted triple t, sorted(rho t) has the same variable and sign = parity * sign(t); and the variable
    classes are exactly the rotation orbits (no extra identification).
 2. For each cut: its variables are exactly the 55 orbit variables of the inner labels 20..31; the forbidden
    assignment (negation of each literal) gives a sign for each of the 220 inner triples.
 3. For each certificate row I recompute myself which GP term is the unique minority term (from the forbidden signs,
    including the -1 coefficient of the middle term), and check the row's 'plus' pair is that term and its 'minus'
    pair is one of the other two terms. Then the weighted exponent of every bracket must cancel exactly.
    Real points in general position with these signs would give sum_w (log|plus| - log|minus|) > 0 but the
    cancellation makes the sum identically 0: contradiction. So the forbidden pattern is not realizable.
 4. Mutation controls: flipping one clause literal (or one weight) must make the check fail.
usage: my_check_c4cuts.py MAP_JSON CUTS_JSONL
"""
import json, random, sys, hashlib
from itertools import combinations

MAP, CUTS = sys.argv[1], sys.argv[2]


def det3(p, q, r):
    # homogeneous (1, x, y)
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


# ---- 0. GP identity -------------------------------------------------------
rng = random.Random(20261101)
for trial in range(3000):
    a, b, c, d, e = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(5)]
    lhs = det3(a, b, c) * det3(a, d, e) - det3(a, b, d) * det3(a, c, e) + det3(a, b, e) * det3(a, c, d)
    assert lhs == 0, "GP identity fails"
bad = 0
for trial in range(200):
    a, b, c, d, e = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(5)]
    lhs = det3(a, b, c) * det3(a, d, e) + det3(a, b, d) * det3(a, c, e) + det3(a, b, e) * det3(a, c, d)
    bad += (lhs != 0)
assert bad > 150, "control: wrong-sign GP should usually fail"
print("0. GP identity holds on 3000 random integer quintuples; wrong-sign control fails on", bad, "/ 200")

# ---- 1. map vs rotation ---------------------------------------------------
mp = json.load(open(MAP, 'rb'))
assert mp['N'] == 32 and mp['m'] == 4 and mp['K'] == 7, (mp['N'], mp['m'], mp['K'])
T = {}
for a, b, c, v, s in mp['triples']:
    assert a < b < c and s in (1, -1)
    T[(a, b, c)] = (v, s)
assert len(T) == 4960 == len(list(combinations(range(32), 3)))


def rho(x):
    o, r = divmod(x, 4)
    return 4 * o + (r + 1) % 4


def sort_parity(seq):
    seq = list(seq)
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if seq[i] > seq[j])
    return tuple(sorted(seq)), (1 if inv % 2 == 0 else -1)


classes = {}
for t, (v, s) in T.items():
    u, par = sort_parity(rho(x) for x in t)
    v2, s2 = T[u]
    assert v2 == v, f"rotation maps {t} to {u} but variables differ"
    assert s2 == par * s, f"sign inconsistency at {t} -> {u}"
    classes.setdefault(v, set()).add(t)
# classes == orbits
for v, cl in classes.items():
    t0 = min(cl)
    orb = set()
    t = t0
    for k in range(4):
        orb.add(t)
        t, _ = sort_parity(rho(x) for x in t)
    assert orb == cl, f"variable {v}: class {sorted(cl)} is not one rotation orbit {sorted(orb)}"
print(f"1. map: {len(T)} triples, {len(classes)} variables; signs consistent with rho; classes = rotation orbits")
print("   map SHA-256:", hashlib.sha256(open(MAP, 'rb').read()).hexdigest())

inner = list(range(20, 32))
inner_triples = list(combinations(inner, 3))
inner_vars = {T[t][0] for t in inner_triples}
assert len(inner_triples) == 220 and len(inner_vars) == 55


# ---- 2/3. cuts ------------------------------------------------------------
def check_cut(rec, verbose=True):
    lits = rec['clause']
    vars_ = [abs(x) for x in lits]
    if len(set(vars_)) != len(vars_):
        return "repeated variable"
    if set(vars_) != inner_vars:
        return "clause variables are not exactly the inner orbit variables"
    forb = {abs(x): (x < 0) for x in lits}           # forbidden value of each variable
    chi = {t: (T[t][1] if forb[T[t][0]] else -T[t][1]) for t in inner_triples}

    def br(x, y, z):                                   # signed orientation of the ordered triple
        u, par = sort_parity((x, y, z))
        return par * chi[u]

    expo = {}
    for row in rec['certificate']:
        q = row['anchor_quintuple']
        if len(set(q)) != 5 or not all(x in chi_pts for x in q):
            return "bad anchor"
        a, b, c, d, e = q
        w = row['weight']
        if type(w) is not int or w <= 0:
            return "bad weight"
        terms = [(+1, (a, b, c), (a, d, e)), (-1, (a, b, d), (a, c, e)), (+1, (a, b, e), (a, c, d))]
        tsign = [co * br(*t1) * br(*t2) for co, t1, t2 in terms]
        # exactly one minority sign must exist (three nonzero reals summing to zero)
        npos = tsign.count(1)
        if npos not in (1, 2):
            return "all three GP terms have the same sign: pattern violates GP itself"
        minority = tsign.index(1) if npos == 1 else tsign.index(-1)
        key = lambda t1, t2: frozenset([tuple(sorted(t1)), tuple(sorted(t2))])
        keys = [key(t1, t2) for _, t1, t2 in terms]
        plus = frozenset(tuple(sorted(t)) for t in row['plus'])
        minus = frozenset(tuple(sorted(t)) for t in row['minus'])
        if plus != keys[minority]:
            return "plus pair is not the minority GP term"
        if minus not in keys or minus == plus:
            return "minus pair is not another GP term"
        for t in plus:
            expo[t] = expo.get(t, 0) + w
        for t in minus:
            expo[t] = expo.get(t, 0) - w
    if not rec['certificate']:
        return "empty certificate"
    nz = {t: x for t, x in expo.items() if x}
    if nz:
        return f"exponents do not cancel ({len(nz)} brackets)"
    return None


chi_pts = set(inner)
recs = [json.loads(l) for l in open(CUTS)]
assert len(recs) == 6
patterns = []
for i, rec in enumerate(recs):
    err = check_cut(rec)
    assert err is None, f"cut {i}: {err}"
    patterns.append(frozenset(rec['clause']))
    print(f"2/3. cut {i}: 55 inner variables, {len(rec['certificate'])} rows, weights "
          f"{min(r['weight'] for r in rec['certificate'])}..{max(r['weight'] for r in rec['certificate'])}: certificate valid")
assert len(set(patterns)) == 6, "cuts not distinct"
print("   the six forbidden inner chirotopes are pairwise distinct")

# ---- 4. mutation controls -------------------------------------------------
import copy
rej = tot = 0
unused_total = 0
for i, rec in enumerate(recs):
    used = set()
    for row in rec['certificate']:
        for t in row['plus'] + row['minus']:
            used.add(T[tuple(sorted(t))][0])
    unused_total += len(inner_vars - used)
    # flip each literal whose variable the certificate actually uses
    for j, lit in enumerate(rec['clause']):
        if abs(lit) not in used:
            continue
        m = copy.deepcopy(rec); m['clause'][j] = -m['clause'][j]
        rej += check_cut(m) is not None; tot += 1
    m = copy.deepcopy(rec); m['certificate'][0]['weight'] += 1
    rej += check_cut(m) is not None; tot += 1
    m = copy.deepcopy(rec); m['certificate'].pop()
    rej += check_cut(m) is not None; tot += 1
print(f"4. mutation controls rejected: {rej} / {tot} (literal flips on used variables, weight change, dropped row);"
      f" variables not used by any row, summed over cuts: {unused_total}")
assert rej == tot
print("ALL CHECKS PASSED")
