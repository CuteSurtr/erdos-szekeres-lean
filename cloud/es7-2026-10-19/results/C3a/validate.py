#!/usr/bin/env python3
"""Validation 3a: for random 3-fold symmetric sets, build the true assignment of every
variable of c3cnf (base variables from exact coordinates, chain variables as the least
fixpoint of their definitions) and evaluate every clause.  Required: all non-gon clauses
true; gon clauses all true  <=>  convk (exhaustive) finds no convex k-set.
usage: validate.py M K NSETS SEED   (prints one JSON summary line)"""
import itertools
import json
import random
import subprocess
import sys

import numpy as np

from c3cnf import C3Enc
from c3geom import Labelled, random_c3

CONVK = "/opt/s/convk"


def flat(clauses):
    lens = np.fromiter((len(c) for c in clauses), dtype=np.int64, count=len(clauses))
    lits = np.fromiter(itertools.chain.from_iterable(clauses), dtype=np.int64, count=int(lens.sum()))
    starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
    return lits, starts


def brute(n, k, chiS):
    inp = f"{n} {k}\n" + " ".join(str(chiS[t]) for t in itertools.combinations(range(n), 3)) + "\n"
    out = subprocess.run([CONVK], input=inp, capture_output=True, text=True, check=True).stdout
    return out.split()[0] == "gon"


def true_assignment(e, L):
    n, k = e.n, e.k
    A = np.zeros(e.nv + 1, dtype=bool)
    conflicts = []

    def setlit(lit, val, what):
        v, want = abs(lit), (val if lit > 0 else not val)
        if setd.get(v, want) != want:
            conflicts.append(what)
        setd[v] = want
        A[v] = want

    setd = {}
    for t, lit in e.C.items():
        setlit(lit, L.chip[t] > 0, ("C", t))
    for i in range(n):
        setlit(e.sig(i), bool(L.sigma[i]), ("sigma", i))
    for p, v in e.inv.items():
        setlit(v, bool(L.inv[p]), ("inv", p))
    for p, v in e.Bv.items():
        setlit(v, bool(L.before[p]), ("B", p))
    for t, lit in e.T.items():
        setlit(lit, L.chiS[t] > 0, ("T", t))
    if getattr(e, "gon", "chain") == "conv":
        def O(t):
            st = tuple(sorted(t))
            a, b, c = t
            par = -1 if ((a > b) + (a > c) + (b > c)) & 1 else 1
            return par * L.chiS[st]
        cv = {}
        for S in sorted(e.conv, key=len):
            if len(S) == 4:
                ins = lambda d, a, b, c: O((a, b, d)) == O((b, c, d)) == O((c, a, d))
                cv[S] = not any(ins(d, *[q for q in S if q != d]) for d in S)
            else:
                cv[S] = all(cv[tuple(x for x in S if x != y)] for y in S)
            A[e.conv[S]] = cv[S]
        gonS = any(all(cv[tuple(x for x in S if x != y)] for y in S) for S in itertools.combinations(range(n), k))
        return A, conflicts, gonS
    # oriented ccw table and before table
    ccw = np.zeros((n, n, n), dtype=bool)
    for (i, j, l), s in L.chiS.items():
        for (a, b, c), sg in (((i, j, l), 1), ((j, l, i), 1), ((l, i, j), 1), ((j, i, l), -1), ((i, l, j), -1), ((l, j, i), -1)):
            ccw[a, b, c] = (s * sg) > 0
    bef = np.zeros((n, n), dtype=bool)
    for (i, j), b in L.before.items():
        bef[i, j] = bool(b)
        bef[j, i] = not b
    chain_gon = False
    for x in range(n):
        Y = bef[x][None, :] & ccw[x]  # Y[b, c] = B(x,c) & ccw(x,b,c)
        np.fill_diagonal(Y, False)
        Y[x, :] = False
        Y[:, x] = False
        for (xx, b, c), v in ((key, v) for key, v in e.Y.items() if key[0] == x):
            A[v] = Y[b, c]
        W = bef[x][:, None] & Y  # W2[a, b]
        for r in range(2, k - 1):
            for a, b in itertools.permutations([q for q in range(n) if q != x], 2):
                A[e.W[(r, x, a, b)]] = W[a, b]
            # next[b, c] = OR_a W[a, b] & ccw[a, b, c] & Y[b, c]
            nxt = np.einsum("ab,abc->bc", W.astype(np.int32), ccw.astype(np.int32)) > 0
            nxt &= Y
            W = nxt
        if W.any():
            chain_gon = True
    return A, conflicts, chain_gon


def main():
    M, K, NS, seed = map(int, sys.argv[1:5])
    gon = sys.argv[5] if len(sys.argv) > 5 else "chain"
    rng = random.Random(seed)
    e = C3Enc(M, K, gon=gon)
    e.build()
    lits, starts = flat(e.clauses)
    secs = e.sections
    gon_start = [s for s in secs if s[0] == "gon"][0][1]
    del e.clauses
    res = {"m": M, "k": K, "encoding": gon, "seed": seed, "sets": 0, "gon": 0, "nogon": 0, "fail": []}
    for t in range(NS):
        shape = rng.choice(["disk", "ring", "thin", "thin", (rng.randint(-900, 900), rng.randint(-900, 900))])
        pts = random_c3(M, rng, shape=shape)
        L = Labelled(pts, rng)
        L0 = L
        if L.sigma[0]:  # point reflection, same line l (item 5)
            pts = [((-p[0][0], -p[0][1]), (-p[1][0], -p[1][1])) for p in pts]
            L = Labelled(pts, rng, u=L.u)
            assert L.sigma[0] == 0 and L.orig == L0.orig
        A, conf, chain_gon = true_assignment(e, L)
        val = A[np.abs(lits)] ^ (lits < 0)
        sat = np.logical_or.reduceat(val, starts)
        bad_core = np.nonzero(~sat[:gon_start])[0]
        gon_ok = bool(sat[gon_start:].all())
        has = brute(L.n, K, L.chiS)
        res["sets"] += 1
        res["gon" if has else "nogon"] += 1
        failed = conf or len(bad_core) or (gon_ok == has) or (chain_gon != has)
        if failed:
            names = sorted({next(s[0] for s in secs if s[1] <= c < s[1] + s[2]) for c in bad_core[:50]})
            res["fail"].append({"set": t, "conflicts": conf[:5], "bad_core": int(len(bad_core)),
                                "bad_sections": names, "gon_clauses_ok": gon_ok, "brute_gon": has})
    print(json.dumps(res))


if __name__ == "__main__":
    main()
