#!/usr/bin/env python3
"""A6-6 check: try to reproduce C2FINAL/sample/sample.txt (seed 20261101) and extra_sample.txt (seed 20261102) with
a range of natural draw procedures, since the draw script itself is not in the repository. A match would make the
draw checkable; no match only means none of these procedures is the one used.
usage: try_draw.py RESULTS_DIR"""
import glob, itertools, json, os, random, sys

RES = sys.argv[1]
recs = []
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    for l in open(f):
        if l.strip():
            recs.append((src, json.loads(l)))
target = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "sample.txt")) if l.strip()]
target2 = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "extra_sample.txt")) if l.strip()]
cases = [f"P{i}" for i in range(1, 9)]


def natkey(u):
    c, rest = u.split("_", 1)
    try:
        return (int(c[1:]), [int(x) for x in rest.split("-")], "")
    except ValueError:  # third-layer pieces such as P8_3-11/2-4-5 (LOCAL only)
        return (int(c[1:]), [10 ** 6], rest)


def pops(filt, order, dedup):
    """population per (case, kind) as a list of 'unit@src' strings."""
    P = {}
    for c in cases:
        for k in ("H", "Q"):
            L = [(s, r) for s, r in recs if r.get("case") == c and r.get("kind") == k and filt(s, r)]
            if dedup == "first":
                seen, M = set(), []
                for s, r in L:
                    if r["unit"] not in seen:
                        seen.add(r["unit"]); M.append((s, r))
                L = M
            if order == "scan":
                pass
            elif order == "unit":
                L = sorted(L, key=lambda x: x[1]["unit"])
            elif order == "unitsrc":
                L = sorted(L, key=lambda x: (x[1]["unit"], x[0]))
            elif order == "nat":
                L = sorted(L, key=lambda x: (natkey(x[1]["unit"]), x[0]))
            elif order == "str":
                L = sorted(L, key=lambda x: f"{x[1]['unit']}@{x[0]}")
            P[(c, k)] = [f"{r['unit']}@{s}" for s, r in L]
    return P


filters = {
    "cloud_cert": lambda s, r: "LOCAL" not in s and r.get("certified"),
    "cloud_unsat": lambda s, r: "LOCAL" not in s and r.get("status") == "UNSATISFIABLE",
    "cloud_any": lambda s, r: "LOCAL" not in s,
    "all_cert": lambda s, r: bool(r.get("certified")),
}


def draws(P, rng, scheme, method):
    H, Q = [], []
    pick = (lambda L, k: rng.sample(L, k)) if method == "sample" else \
           (lambda L, k: [rng.choice(L) for _ in range(k)]) if method == "choice" else \
           (lambda L, k: (lambda M: (rng.shuffle(M), M[:k])[1])(list(L)))
    if scheme == "per_case_HQ":
        for c in cases:
            H += pick(P[(c, "H")], 2); Q += pick(P[(c, "Q")], 1)
    elif scheme == "per_case_QH":
        for c in cases:
            Q += pick(P[(c, "Q")], 1); H += pick(P[(c, "H")], 2)
    elif scheme == "allH_allQ":
        for c in cases:
            H += pick(P[(c, "H")], 2)
        for c in cases:
            Q += pick(P[(c, "Q")], 1)
    elif scheme == "allQ_allH":
        for c in cases:
            Q += pick(P[(c, "Q")], 1)
        for c in cases:
            H += pick(P[(c, "H")], 2)
    return H + Q


hits = []
tried = 0
for (fn, f), order, dedup, scheme, method in itertools.product(
        filters.items(), ["scan", "unit", "unitsrc", "nat", "str"], ["none", "first"],
        ["per_case_HQ", "per_case_QH", "allH_allQ", "allQ_allH"], ["sample", "choice", "shuffle"]):
    P = pops(f, order, dedup)
    for seedform in ("int", "str"):
        seed = 20261101 if seedform == "int" else "20261101"
        rng = random.Random(seed)
        got = draws(P, rng, scheme, method)
        tried += 1
        nmatch = sum(a == b for a, b in zip(got, target))
        setmatch = len(set(got) & set(target))
        if setmatch >= 3:
            hits.append((setmatch, nmatch, fn, order, dedup, scheme, method, seedform))
print("python", sys.version.split()[0], "procedures tried:", tried)
hits.sort(reverse=True)
for h in hits[:15]:
    print("  set-overlap", h[0], "positional", h[1], h[2:])
if not hits:
    print("  no procedure reproduced 3 or more of the 24 sampled records")

# numpy variants, if numpy is importable
try:
    import numpy as np
    nh = []
    for (fn, f), order, dedup in itertools.product(filters.items(), ["scan", "unit", "unitsrc", "nat", "str"], ["none", "first"]):
        P = pops(f, order, dedup)
        for scheme in ("per_case_HQ", "allH_allQ"):
            for gen in ("default_rng", "RandomState"):
                g = np.random.default_rng(20261101) if gen == "default_rng" else np.random.RandomState(20261101)
                H, Q = [], []
                if scheme == "per_case_HQ":
                    for c in cases:
                        H += list(np.array(P[(c, "H")])[g.choice(len(P[(c, "H")]), 2, replace=False)])
                        Q += list(np.array(P[(c, "Q")])[g.choice(len(P[(c, "Q")]), 1, replace=False)])
                else:
                    for c in cases:
                        H += list(np.array(P[(c, "H")])[g.choice(len(P[(c, "H")]), 2, replace=False)])
                    for c in cases:
                        Q += list(np.array(P[(c, "Q")])[g.choice(len(P[(c, "Q")]), 1, replace=False)])
                got = H + Q
                so = len(set(got) & set(target))
                if so >= 3:
                    nh.append((so, fn, order, dedup, scheme, gen))
    print("numpy", np.__version__, "hits:", sorted(nh, reverse=True)[:10] or "none with overlap >= 3")
except ImportError:
    print("numpy not available")
