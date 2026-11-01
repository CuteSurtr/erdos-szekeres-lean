#!/usr/bin/env python3
"""Realizability cut loop for the fourfold 32-point formula (SYM5 symcnf_layers.py 32 7 4, sha c3933d9a...).

Repeat: solve base + cuts with CaDiCaL; on SAT read the chirotope of the model; for a list of point subsets (inner
layers first) look for a biquadratic final polynomial: a nonnegative integer combination of Grassmann-Pluecker
comparisons "|minority term| > |other term|" whose bracket exponents cancel (Bokowski-Richter). Found by an LP
(HiGHS), then made exact with rational arithmetic and re-verified from the signs alone. The certificate shows that
no real point configuration has all the bracket signs it uses, so the clause "not all of these signs" is sound for
every real configuration (no symmetry assumption). Add it and repeat until UNSAT or no certificate is found.
usage: c4cut.py WORKDIR CADICAL MAX_ITERS"""
import itertools, json, os, re, subprocess, sys, time
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

W, CAD, MAXIT = sys.argv[1], sys.argv[2], int(sys.argv[3])
BASE, MAP = os.path.join(W, "c4_n32L.cnf"), os.path.join(W, "c4_n32L.json")
CUTS, LOG = os.path.join(W, "cuts.jsonl"), open(os.path.join(W, "c4cut.log"), "a", buffering=1)
log = lambda m: LOG.write(time.strftime("%H:%M:%SZ ", time.gmtime()) + m + "\n")
tri = {}  # sorted triple -> (var, sign): chi(i,j,k) = sign * value(var)
for i, j, k, v, s in json.load(open(MAP))["triples"]:
    tri[(i, j, k)] = (v, s)
LAYER = lambda o: list(range(4 * o, 4 * o + 4))
SUBSETS = [sum((LAYER(o) for o in range(5, 8)), []),            # inner 12 (layers 5-7)
           sum((LAYER(o) for o in range(4, 8)), []),            # inner 16
           sum((LAYER(o) for o in range(3, 8)), []),            # inner 20
           list(range(32))]


def chi_of(model, a, b, c):
    """orientation sign of the ordered triple (a, b, c) in the model"""
    t = sorted((a, b, c)); v, s = tri[tuple(t)]
    val = s * (1 if model[v] else -1)
    # parity of the permutation sorting (a, b, c)
    perm = [t.index(x) for x in (a, b, c)]
    inv = sum(1 for x in range(3) for y in range(x + 1, 3) if perm[x] > perm[y])
    return val if inv % 2 == 0 else -val


def comparisons(model, pts):
    """rows (plus, minus, signs_used): log|[T1]| + log|[T2]| > log|[T3]| + log|[T4]|"""
    rows = []
    for a in pts:
        rest = [x for x in pts if x != a]
        for b, c, d, e in itertools.combinations(rest, 4):
            terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
            sg = [co * chi_of(model, *t1) * chi_of(model, *t2) for t1, t2, co in terms]
            if len(set(sg)) == 1:
                raise ValueError(f"GP sign violation at {(a, b, c, d, e)}")
            mi = next(x for x in range(3) if sg.count(sg[x]) == 1)
            used = tuple(sorted({tuple(sorted(t)) for t1, t2, _ in terms for t in (t1, t2)}))
            for o in range(3):
                if o != mi:
                    rows.append(((frozenset_key(terms[mi][0]), frozenset_key(terms[mi][1])),
                                 (frozenset_key(terms[o][0]), frozenset_key(terms[o][1])), (a, b, c, d, e), used))
    return rows


frozenset_key = lambda t: tuple(sorted(t))


def certificate(model, pts):
    rows = comparisons(model, pts)
    cols = sorted({t for p, m, _, _ in rows for t in p + m}); ci = {t: n for n, t in enumerate(cols)}
    data, ri, cj = [], [], []
    for n, (p, m, _, _) in enumerate(rows):
        for t in p: ri.append(n); cj.append(ci[t]); data.append(1.0)
        for t in m: ri.append(n); cj.append(ci[t]); data.append(-1.0)
    A = csr_matrix((data, (ri, cj)), shape=(len(rows), len(cols)))
    # dual: lambda >= 0, A^T lambda = 0, sum lambda = 1  (feasible iff the strict system is infeasible)
    Aeq = csr_matrix(np.vstack([A.T.toarray(), np.ones((1, len(rows)))]))
    beq = np.zeros(len(cols) + 1); beq[-1] = 1.0
    res = linprog(np.ones(len(rows)), A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
    if res.status != 0:
        return None, len(rows)
    sup = [n for n in range(len(rows)) if res.x[n] > 1e-9]
    lam = exact_null(rows, sup, ci)
    if lam is None:
        return "inexact", len(rows)
    return [(rows[n], lam[k]) for k, n in enumerate(sup) if lam[k] != 0], len(rows)


def exact_null(rows, sup, ci):
    """exact positive integer vector lambda on sup with sum lambda_n * row_n = 0, or None"""
    M = []  # columns = support rows, matrix rows = triples
    trip = sorted({t for n in sup for t in rows[n][0] + rows[n][1]})
    ti = {t: r for r, t in enumerate(trip)}
    M = [[Fraction(0)] * len(sup) for _ in trip]
    for k, n in enumerate(sup):
        for t in rows[n][0]: M[ti[t]][k] += 1
        for t in rows[n][1]: M[ti[t]][k] -= 1
    # reduced row echelon form
    piv, r = [], 0
    for c in range(len(sup)):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; f = M[r][c]; M[r] = [x / f for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                g = M[i][c]; M[i] = [x - g * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(len(sup)) if c not in piv]
    if len(free) != 1:
        return None
    lam = [Fraction(0)] * len(sup); lam[free[0]] = Fraction(1)
    for i, c in enumerate(piv): lam[c] = -M[i][free[0]]
    if any(x < 0 for x in lam):
        lam = [-x for x in lam]
    if any(x < 0 for x in lam):
        return None
    from math import lcm
    L = lcm(*[x.denominator for x in lam]); return [int(x * L) for x in lam]


def verify(model, cert):
    """exact re-check from signs: each comparison's minority, and cancellation of bracket exponents"""
    expo = {}
    for (p, m, (a, b, c, d, e), _), w in cert:
        terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
        sg = [co * chi_of(model, *t1) * chi_of(model, *t2) for t1, t2, co in terms]
        keys = [(frozenset_key(t1), frozenset_key(t2)) for t1, t2, _ in terms]
        mi = keys.index(p)
        assert sg.count(sg[mi]) == 1 and m in keys and keys.index(m) != mi
        for t in p: expo[t] = expo.get(t, 0) + w
        for t in m: expo[t] = expo.get(t, 0) - w
    assert all(v == 0 for v in expo.values()) and cert


def clause(model, cert):
    signs = sorted({t for _, _, _, used in (r for r, _ in cert) for t in used})
    lits = []
    for t in signs:
        v, s = tri[t]; val = 1 if model[v] else -1
        lits.append(-v if val == 1 else v)  # negate the model's value of var v
    return sorted(set(lits), key=abs), signs


def used_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (g("Pages active") + g("Pages wired down") + g("Pages occupied by compressor")) * 16384 / 1e9


def solve(cuts):
    while (u := used_gb()) > 42.0:
        log(f"guard: {u:.1f} GB in use, waiting"); time.sleep(30)
    F = os.path.join(W, "cur.cnf")
    with open(BASE, "rb") as f, open(F, "wb") as g:
        while not (hdr := f.readline()).startswith(b"p cnf"):
            g.write(hdr)
        _, _, nv, nc = hdr.split()
        g.write(f"p cnf {int(nv)} {int(nc) + len(cuts)}\n".encode())
        while (b := f.read(1 << 24)): g.write(b)
        g.write("".join(" ".join(map(str, c)) + " 0\n" for c in cuts).encode())
    out = subprocess.run([CAD, "-q", "-t", "1800", F], capture_output=True, text=True).stdout
    st = next((l[2:] for l in out.splitlines() if l.startswith("s ")), "UNKNOWN")
    model = {}
    if st == "SATISFIABLE":
        for l in out.splitlines():
            if l.startswith("v "):
                for x in map(int, l[2:].split()):
                    if x: model[abs(x)] = x > 0
    os.remove(F)
    return st, model


cuts = [json.loads(l)["clause"] for l in open(CUTS)] if os.path.exists(CUTS) else []
for it in range(MAXIT):
    t0 = time.time(); st, model = solve(cuts)
    log(f"iter {it}: {len(cuts)} cuts -> {st} ({time.time() - t0:.0f} s)")
    if st != "SATISFIABLE":
        break
    for pts in SUBSETS:
        cert, nrows = certificate(model, pts)
        log(f"  subset of {len(pts)} points: {nrows} comparisons, certificate: "
            f"{'none' if cert is None else cert if isinstance(cert, str) else f'{len(cert)} rows'}")
        if cert and not isinstance(cert, str):
            verify(model, cert)
            lits, signs = clause(model, cert)
            rec = {"iter": it, "subset": pts, "clause": lits, "signs": [list(t) for t in signs],
                   "certificate": [{"anchor_quintuple": list(q), "plus": [list(t) for t in p],
                                    "minus": [list(t) for t in m], "weight": w} for (p, m, q, _), w in cert]}
            with open(CUTS, "a") as f: f.write(json.dumps(rec) + "\n")
            cuts.append(lits); log(f"  cut {len(cuts)}: {len(lits)} literals, {len(cert)} comparisons, "
                                   f"weights sum {sum(w for _, w in cert)}")
            break
    else:
        log("  no certificate on any subset; stopping"); break
log("stop")
