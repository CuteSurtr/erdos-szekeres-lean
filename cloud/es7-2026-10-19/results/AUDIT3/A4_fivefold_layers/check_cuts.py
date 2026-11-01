#!/usr/bin/env python3
"""Independent check of the C4CUT realizability cuts (audit A4; standard library only, no project code).

1. Symbolic proof of the 3-term Grassmann-Pluecker identity for affine plane points (homogeneous coordinate 1):
   [abc][ade] - [abd][ace] + [abe][acd] = 0, by polynomial expansion in the 10 coordinates.
2. For each cut: recover the forbidden assignment from the clause literals; derive the orientation sign of EVERY
   triple of the inner 12 labels 20..31 from the variable map (chi(sorted) = s * value(var)); check:
   - the clause variables are exactly the triple-orbit variables of labels 20..31 (no other variables);
   - every certificate row: anchor quintuple of distinct inner labels, the 'plus' pair is the unique minority
     term of its GP relation, the 'minus' pair is one of the other two terms; positive integer weights;
   - the weighted bracket exponents cancel exactly (so sum_w (log|plus| - log|minus|) = 0, contradicting > 0);
   - additionally: the forbidden pattern is an abstract uniform acyclic chirotope on the 12 points (A4 + GP sign
     conditions on all 4- and 5-subsets) and is invariant under the labelled rotation (so the cuts are not vacuous
     relaxations of something already excluded), and the six patterns are pairwise distinct.
3. Mutation tests: a flipped literal, a changed weight, a dropped row, swapped plus/minus must be rejected.
usage: check_cuts.py MAP_JSON CUTS_JSONL
"""
import hashlib, itertools, json, sys, copy, random


# ---------- 1. symbolic GP identity
def padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(sorted(k1 + k2))
            r[k] = r.get(k, 0) + v1 * v2
            if r[k] == 0:
                del r[k]
    return r


def var(name):
    return {(name,): 1}


ONE = {(): 1}


def det3(P, a, b, c):
    """det [[xa, ya, 1], [xb, yb, 1], [xc, yc, 1]] as a polynomial"""
    xa, ya = P[a]; xb, yb = P[b]; xc, yc = P[c]
    t1 = pmul(xa, padd(yb, yc, -1))
    t2 = pmul(ya, padd(xb, xc, -1))
    t3 = padd(pmul(xb, yc), pmul(yb, xc), -1)
    return padd(padd(t1, t2, -1), t3)


P = {i: (var(f"x{i}"), var(f"y{i}")) for i in "abcde"}
gp = padd(padd(pmul(det3(P, *"abc"), det3(P, *"ade")), pmul(det3(P, *"abd"), det3(P, *"ace")), -1),
          pmul(det3(P, *"abe"), det3(P, *"acd")))
assert gp == {}, "GP identity fails"
# the affine bracket equals the orientation determinant (q - p) x (r - p)
orient_poly = padd(pmul(padd(P["b"][0], P["a"][0], -1), padd(P["c"][1], P["a"][1], -1)),
                   pmul(padd(P["b"][1], P["a"][1], -1), padd(P["c"][0], P["a"][0], -1)), -1)
assert padd(det3(P, *"abc"), orient_poly, -1) == {}
print("1. symbolic: [abc][ade] - [abd][ace] + [abe][acd] == 0 identically; [abc] == orientation determinant")


# ---------- 2. the cuts
def orient(chi, a, b, c):
    s = tuple(sorted((a, b, c)))
    inv = (a > b) + (a > c) + (b > c)
    return chi[s] if inv % 2 == 0 else -chi[s]


def check_cut(rec, tri, inner, strict_extra=True):
    lits = rec["clause"]
    if len(lits) != len({abs(x) for x in lits}):
        return "repeated variable"
    forb = {abs(x): (x < 0) for x in lits}     # literal -v forbids v = True; literal v forbids v = False
    inner_vars = {tri[t][0] for t in itertools.combinations(inner, 3)}
    if set(forb) != inner_vars:
        return f"clause variables != inner triple-orbit variables ({len(set(forb))} vs {len(inner_vars)})"
    chi = {t: tri[t][1] * (1 if forb[tri[t][0]] else -1) for t in itertools.combinations(inner, 3)}
    expo = {}
    if not rec["certificate"]:
        return "empty certificate"
    for row in rec["certificate"]:
        q = row["anchor_quintuple"]
        if len(set(q)) != 5 or not set(q) <= set(inner):
            return "bad anchor"
        a, b, c, d, e = q
        w = row["weight"]
        if type(w) is not int or w <= 0:
            return "bad weight"
        terms = [((a, b, c), (a, d, e), +1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), +1)]
        sg = [co * orient(chi, *t1) * orient(chi, *t2) for t1, t2, co in terms]
        if len(set(sg)) == 1:
            return "GP sign condition violated by the pattern itself"
        mino = [i for i in range(3) if sg.count(sg[i]) == 1]
        assert len(mino) == 1
        key = lambda T: tuple(sorted((tuple(sorted(T[0])), tuple(sorted(T[1])))))
        keys = [key(T) for T in terms]
        plus = tuple(sorted(tuple(sorted(x)) for x in row["plus"]))
        minus = tuple(sorted(tuple(sorted(x)) for x in row["minus"]))
        if plus != keys[mino[0]]:
            return "plus is not the minority term"
        if minus not in keys or minus == plus:
            return "minus is not another term"
        for tt in plus:
            expo[tt] = expo.get(tt, 0) + w
        for tt in minus:
            expo[tt] = expo.get(tt, 0) - w
    if any(v != 0 for v in expo.values()):
        return "exponents do not cancel"
    if strict_extra:
        # abstract chirotope axioms on the pattern (informative)
        for S in itertools.combinations(inner, 4):
            for tpt in S:
                p_, q_, r_ = [x for x in S if x != tpt]
                v = [orient(chi, tpt, q_, r_), orient(chi, p_, tpt, r_), orient(chi, p_, q_, tpt)]
                if v[0] == v[1] == v[2] and orient(chi, p_, q_, r_) != v[0]:
                    return "pattern violates interiority (A4)"
        for S in itertools.combinations(inner, 5):
            for x in S:
                y1, y2, y3, y4 = [y for y in S if y != x]
                t = [orient(chi, x, y1, y2) * orient(chi, x, y3, y4), -orient(chi, x, y1, y3) * orient(chi, x, y2, y4),
                     orient(chi, x, y1, y4) * orient(chi, x, y2, y3)]
                if len(set(t)) == 1:
                    return "pattern violates GP signs"
        # rotation invariance: label 4o + r -> 4o + (r + 1) % 4
        rot = lambda i: 4 * (i // 4) + (i % 4 + 1) % 4
        for t in chi:
            if orient(chi, *map(rot, t)) != chi[t]:
                return "pattern not rotation invariant"
    return None, chi


def main():
    MAP, CUTS = sys.argv[1:3]
    print("map sha256:", hashlib.sha256(open(MAP, "rb").read()).hexdigest())
    print("cuts sha256:", hashlib.sha256(open(CUTS, "rb").read()).hexdigest())
    info = json.load(open(MAP))
    tri = {tuple(t[:3]): (t[3], t[4]) for t in info["triples"]}
    inner = list(range(20, 32))
    recs = [json.loads(l) for l in open(CUTS)]
    pats = []
    for n, rec in enumerate(recs):
        r = check_cut(rec, tri, inner)
        if not isinstance(r, tuple):
            print(f"cut {n}: FAIL: {r}")
            sys.exit(1)
        pats.append(tuple(sorted(r[1].items())))
        ws = [row["weight"] for row in rec["certificate"]]
        print(f"cut {n}: OK  ({len(rec['clause'])} literals, {len(rec['certificate'])} rows, weight sum {sum(ws)}, "
              f"max weight {max(ws)})")
    assert len(set(pats)) == len(pats), "repeated pattern"
    print(f"2. all {len(recs)} cuts verified; patterns pairwise distinct; each is an abstract rotation-invariant "
          f"uniform acyclic chirotope on labels 20..31")
    # relation between patterns: are they equivalent under relabelling by the symmetry group of the normal form?
    # (informative only) count, for each pair, the number of differing triple signs
    diffs = [[sum(1 for (k1, v1), (k2, v2) in zip(p, q) if v1 != v2) for q in pats] for p in pats]
    print("   pairwise numbers of differing triple signs:", diffs)
    # ---------- 3. mutations
    rnd = random.Random(5)
    caught = total = 0
    for n, rec in enumerate(recs):
        muts = []
        r1 = copy.deepcopy(rec); i = rnd.randrange(len(r1["clause"])); r1["clause"][i] = -r1["clause"][i]; muts.append(r1)
        r2 = copy.deepcopy(rec); r2["certificate"][0]["weight"] += 1; muts.append(r2)
        r3 = copy.deepcopy(rec); del r3["certificate"][rnd.randrange(len(r3["certificate"]))]; muts.append(r3)
        r4 = copy.deepcopy(rec); row = r4["certificate"][0]; row["plus"], row["minus"] = row["minus"], row["plus"]; muts.append(r4)
        r5 = copy.deepcopy(rec); r5["certificate"][1]["weight"] = 0; muts.append(r5)
        r6 = copy.deepcopy(rec); del r6["clause"][0]; muts.append(r6)
        for mrec in muts:
            total += 1
            try:
                res = check_cut(mrec, tri, inner, strict_extra=False)
            except KeyError:
                res = "missing sign"
            caught += not isinstance(res, tuple)
    print(f"3. mutations rejected: {caught}/{total}")


if __name__ == "__main__":
    main()
