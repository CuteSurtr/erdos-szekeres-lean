#!/usr/bin/env python3
"""Independent check of the realizability cuts in cuts.jsonl (written by c4cut.py); standard library only.

For each cut: the clause forbids one sign pattern. Recover that pattern from the clause literals alone (literal -v
forbids v = true, literal v forbids v = false) and the variable map (triple -> var, sign). Then check every
certificate row against those signs only:
- the anchored quintuple (a,b,c,d,e) gives the Grassmann-Pluecker relation
  [abc][ade] - [abd][ace] + [abe][acd] = 0, all six brackets are among the pattern's signs;
- the row's 'plus' pair is the unique term of minority sign and its 'minus' pair is another term, so in any real
  configuration with these signs (general position) log|plus| > log|minus|;
- the weights are positive integers and the weighted bracket exponents cancel exactly, so summing gives 0 > 0.
Hence no real configuration has all the signs, and the clause removes no real configuration.
usage: verify_cuts.py MAP_JSON CUTS_JSONL"""
import hashlib, json, sys

MAP, CUTS = sys.argv[1:3]
tri = {tuple(t[:3]): (t[3], t[4]) for t in json.load(open(MAP))["triples"]}


def orient(chi, a, b, c):
    """sign of the ordered triple from the sign of its sorted version"""
    s = sorted((a, b, c))
    v = chi[tuple(s)]
    # count inversions of (a, b, c) relative to sorted order
    seq = [a, b, c]
    inv = (seq[0] > seq[1]) + (seq[0] > seq[2]) + (seq[1] > seq[2])
    return v if inv % 2 == 0 else -v


ok = 0
for n, line in enumerate(open(CUTS)):
    rec = json.loads(line)
    lits = rec["clause"]
    assert len(lits) == len(set(abs(x) for x in lits)), "repeated variable in clause"
    forbidden = {abs(x): x < 0 for x in lits}  # value of v in the forbidden pattern
    chi = {}
    for t in map(tuple, rec["signs"]):
        v, s = tri[t]
        assert v in forbidden, f"cut {n}: sign of {t} has no clause literal"
        chi[t] = s * (1 if forbidden[v] else -1)
    assert {tri[t][0] for t in chi} == set(forbidden), f"cut {n}: clause has literals outside the pattern"
    expo = {}
    for row in rec["certificate"]:
        a, b, c, d, e = row["anchor_quintuple"]
        assert len({a, b, c, d, e}) == 5, f"cut {n}: anchor quintuple has repeated points"
        w = row["weight"]
        assert type(w) is int and w > 0, f"cut {n}: weight must be a positive integer"
        terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
        sg = [co * orient(chi, *t1) * orient(chi, *t2) for t1, t2, co in terms]
        keys = [tuple(sorted([tuple(sorted(t1)), tuple(sorted(t2))])) for t1, t2, _ in terms]
        plus = tuple(sorted(tuple(t) for t in row["plus"]))
        minus = tuple(sorted(tuple(t) for t in row["minus"]))
        assert plus in keys and minus in keys and plus != minus, f"cut {n}: row pairs are not GP terms"
        assert sg.count(sg[keys.index(plus)]) == 1, f"cut {n}: plus term is not the unique minority"
        for t in plus: expo[t] = expo.get(t, 0) + w
        for t in minus: expo[t] = expo.get(t, 0) - w
    assert rec["certificate"] and all(x == 0 for x in expo.values()), f"cut {n}: exponents do not cancel"
    ok += 1
print(f"{ok} cuts verified: each clause forbids a sign pattern with no real realization")
print("map SHA-256:", hashlib.sha256(open(MAP, "rb").read()).hexdigest())
