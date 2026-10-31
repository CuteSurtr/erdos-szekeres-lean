#!/usr/bin/env python3
"""Clause-level soundness test of sgn.py on real configurations.

For each labelled real configuration (my own --par normal form, rs edge choice, exact integers):
  * every clause is evaluated with o-vars = real orientations and aux vars = intended meaning;
  * if the set has no convex K-gon (my independent angular DP), ANY falsified clause is a soundness bug;
  * if it has one, falsified clauses must all be final kgon clauses [-EU_k(a,b), -EU_t(n+1-b,n+1-a)] or [-EU_K(.)]
    and each must correspond to a real k-cup + t-cap from a to b (a real K-gon); anything else is a bug.
  * optionally CaDiCaL on CNF + o-units (existence of aux values): must be SAT when K-gon-free.
usage: t2_cnf.py MODE SEED TRIALS"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build, cadical_with_units

PTS32 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "es7c", "cloud", "es7-2026-10-19", "results",
                     "SYM2", "sym7_32points.txt")


def load32():
    return [tuple(int(x) for x in l.split()) for l in open(PTS32) if l.strip()]


def classify_bad(F, S, bad, val):
    """returns list of problems (clauses that are not legitimate K-gon witnesses)."""
    n, K = F.n, F.K
    probs = []
    o = orient_table(S)
    cup = exact_cups(o, n, K)
    for c in bad:
        mns = [F.mean.get(abs(l)) for l in c]
        if all(l < 0 for l in c) and all(mn is not None and mn[0] == 'EU' for mn in mns):
            # final clause: -EU_k(a,b) [, -EU_t(n+1-b, n+1-a)]
            if len(c) == 1:
                _, k, a, b = mns[0]
                # k == K: K-cup/K-cap unit; or k == t == (K+2)/2 with (a,b) self-mirror: deduped [-EU_k(a,b), -EU_k(a,b)]
                ok = k == K or (2 * k == K + 2 and a + b == n + 1)
            elif len(c) == 2:
                (_, k1, a1, b1), (_, k2, a2, b2) = mns
                ok = (k1 + k2 == K + 2 and ((a2, b2) == (n + 1 - b1, n + 1 - a1)))
            else:
                ok = False
            if ok:
                continue
        probs.append(c)
    return probs


def check(F, S, use_sat=False, label=""):
    n = len(S)
    bad, val = F.evaluate(S)
    mc = max_convex(S)
    res = {"n": n, "K": F.K, "maxconv": mc, "falsified": len(bad)}
    if mc < F.K:
        if bad:
            res["BUG"] = [[F.describe(l) for l in c] for c in bad[:5]]
    else:
        probs = classify_bad(F, S, bad, val)
        if probs:
            res["BUG"] = [[F.describe(l) for l in c] for c in probs[:5]]
        if not bad:
            res["note"] = "K-gon present but no clause falsified (incomplete encoding?)"
    if use_sat:
        units = [v if val[v] else -v for v in range(1, F.no + 1)]
        sat = cadical_with_units(F, units)
        res["sat_with_o_units"] = sat
        if mc < F.K and not sat:
            res["BUG_SAT"] = True
        if mc >= F.K and sat:
            res["note2"] = "SAT despite K-gon"
    return res


def summarize(results, title):
    bugs = [r for r in results if "BUG" in r or "BUG_SAT" in r]
    free = sum(1 for r in results if r["maxconv"] < r["K"])
    print(json.dumps({"test": title, "configs": len(results), "K_gon_free": free, "with_K_gon": len(results) - free,
                      "bugs": len(bugs),
                      "notes": sum(1 for r in results if "note" in r or "note2" in r)}))
    for b in bugs[:5]:
        print("  BUG", json.dumps(b))
    return bugs


def par_subsets_of_32(rng, T, sizes):
    """antipodal subsets of the 32-point set that keep its parallelogram hull (always contain the 4 hull vertices),
    plus a few whose hull is a different parallelogram"""
    P = load32(); H = hull_ccw(P); hs = set(H)
    inner_pairs = sorted({max(p, neg(p)) for p in P if p not in hs})
    hull_pairs = sorted({max(p, neg(p)) for p in H})
    out = []
    for _ in range(T):
        mm = rng.choice(sizes)
        sub = rng.sample(inner_pairs, mm)
        Q = [x for p in hull_pairs + sub for x in (p, neg(p))]
        out.append(Q)
    return out


if __name__ == "__main__":
    mode = sys.argv[1]; seed = int(sys.argv[2]); T = int(sys.argv[3])
    rng = random.Random(seed)
    t0 = time.time()
    if mode == "real32":
        # the real set itself (n=32) for every admissible rs edge choice, with and without --centre
        P = load32(); results = []
        for centre in (False, True):
            F = build(32, 7, par=True, centre=centre, rs=True)
            for ch in range(4):
                S, info = par_normal_form(P, rs=True, choice=ch)
                results.append(check(F, S, use_sat=True))
            F2 = build(32, 7, par=True, centre=centre, rs=False)
            for ch in range(4):
                S, info = par_normal_form(P, rs=False, choice=ch)
                r = check(F2, S, use_sat=True); results.append(r)
        summarize(results, "real 32-point set, n=32 K=7, all edge choices")
    elif mode == "sub32":
        # antipodal subsets (parallelogram hull kept), K=7, with --sym --par --centre --rs
        results = []
        for Q in par_subsets_of_32(rng, T, list(range(2, 14))):
            n = len(Q)
            F = build(n, 7, par=True, centre=True, rs=True)
            for ch in range(2):
                S, info = par_normal_form(Q, rs=True, choice=ch)
                results.append(check(F, S, use_sat=(rng.random() < 0.3)))
        summarize(results, "antipodal subsets of the 32-point set (K=7, --sym --par --centre --rs)")
    print("time", round(time.time() - t0, 1))
