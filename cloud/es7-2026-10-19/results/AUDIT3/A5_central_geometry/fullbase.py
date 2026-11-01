#!/usr/bin/env python3
"""Auditor A5: evaluate EVERY clause of the real base CNF (all 16,653,336, including the convex-7-gon encoding with its
auxiliary variables) on real centrally symmetric 34-point sets labelled in the angular normal form (every hull vertex
as first point, original and reflected). Expected: the only falsified clauses are the 7-set clauses of 7-sets in
convex position, one per half-turn orbit (canonical 7-set) -- checked as an exact set equality, with each such 7-set
re-checked for convex position directly from the coordinates.
Optionally (--cube) the labelling's own hull cube and second-layer cube are appended as unit clauses, i.e. the unit CNF
that the lanes solved is evaluated (cubes read from the lanes' files; for a >= 9 the case is first moved to 17 - a by
reduction (A) -- labelling from p_a -- so only file cubes are used).
usage: fullbase.py BASE_CNF BASE_JSON RESULTS_DIR MODE [args]
  MODE heptagon FILE           : the 34-point two-heptagon set, all hull-vertex labellings, original and reflected
  MODE perturb FILE K SEED     : K random symmetric perturbations of that set (kept only if in general position)
  MODE random K SEED           : K random sets (parallelogram hull), all hull-vertex labellings"""
import os, subprocess, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5lib import *

BASE, MAPF, RES, MODE = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
mp = Map(MAPF)
convnum, last = conv_numbering(mp.nX)
assert last == mp.nv
hull, _ = load_cubes(os.path.join(RES, "C2C34", "cubes.txt"))
L2 = {a: load_cubes(os.path.join(RES, "C2P", "cubes", f"P{a}_cubes.txt"))[0] for a in range(1, 9)}
pt = lambda o, r: 2 * o + r


def full_assignment(X):
    val, conv = assignment(mp, X, convnum)
    U7 = convex_7sets_canonical(conv)
    exp = set()
    for U in U7:
        pts = [X[i] for i in U]
        assert len(hull_ccw(pts)) == 7, "7-set from the table not in convex position"
        exp.add(frozenset(-convnum[canon(U[:i] + U[i + 1:])] for i in range(7)))
    return np.array([1 if x > 0 else 0 for x in val], dtype=np.uint8), exp, U7


def case_of(X):
    Hc, _ = hull_classes(X)
    if len(Hc) != 2:
        return ("H" if len(Hc) == 3 else "?", Hc, None)
    a = Hc[1]
    inner_idx = [q for q in range(N) if q // 2 not in (0, a)]
    V2, V2idx = hull_classes(X, inner_idx)
    return ("P", a, V2 if len(V2idx) in (4, 6) else None)


def run_batch(jobs, tag, extra_lines=None):
    """jobs: list of (description, X). Returns per-job results. extra_lines: list of clause strings appended."""
    L = len(jobs)
    assert 1 <= L <= 64
    vals, exps = [], []
    for desc, X in jobs:
        v, e, U7 = full_assignment(X)
        vals.append(v)
        exps.append(e)
    M = np.zeros(mp.nv + 1, dtype=np.uint64)
    for j, v in enumerate(vals):
        M |= (v.astype(np.uint64) << np.uint64(j))
    mpath = os.path.join(HERE, f"_masks_{tag}.bin")
    M.astype("<u8").tofile(mpath)
    opath = os.path.join(HERE, f"_fals_{tag}.txt")
    cmd = [os.path.join(HERE, "evalcnf"), BASE, mpath, str(L), opath]
    if extra_lines is not None:
        epath = os.path.join(HERE, f"_extra_{tag}.cnf")
        open(epath, "w").write("".join(l + "\n" for l in extra_lines))
        cmd.append(epath)
    r = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout.decode()
    total = int(r.split()[1])
    got = [set() for _ in range(L)]
    got_idx = [[] for _ in range(L)]
    for line in open(opath):
        f = line.split()
        idx, m, lits = int(f[0]), int(f[1], 16), frozenset(int(x) for x in f[2:])
        for j in range(L):
            if m >> j & 1:
                got[j].add(lits)
                got_idx[j].append(idx)
    os.remove(mpath)
    os.remove(opath)
    out = []
    for j, (desc, X) in enumerate(jobs):
        ok = got[j] == exps[j] and len(got_idx[j]) == len(exps[j])
        out.append((desc, ok, len(exps[j]), len(got_idx[j]), total, got_idx[j][:3]))
    return out


def labellings(P, with_reflection=True):
    jobs = []
    for f in hull_ccw(P):
        jobs.append((f"first={f}", label(P, f)))
    if with_reflection:
        Q = reflect(P, 0)
        for f in hull_ccw(Q):
            jobs.append((f"reflected first={f}", label(Q, f)))
    return jobs


def read_set(path):
    pts = [tuple(int(x) for x in l.split()) for l in open(path) if l.strip() and not l.startswith("#")]
    assert len(pts) == N
    return pts


t0 = time.time()
allok = True
if MODE == "heptagon":
    P = read_set(sys.argv[5])
    assert general_position(P) and all(neg(p) in P for p in P)
    jobs = labellings(P)
    for desc, X in jobs:
        print(desc, "case", case_of(X))
    res = run_batch(jobs, "hept")
    for r in res:
        print("base only:", r)
        allok &= r[1]
    # unit CNFs as solved: base + the labelling's own second-layer cube (case moved to a <= 8 by (A) if needed)
    for desc, X in jobs:
        kind, a, V = case_of(X)
        if kind != "P":
            continue
        if a >= 9:
            X = label([p for p in X[:N]], X[pt(a, 0)])
            kind, a, V = case_of(X)
            desc += f" -> (A) relabelled from p_a"
        name = f"P{a}_" + "-".join(map(str, V))
        cube = L2[a][name]
        res = run_batch([(desc + " + cube " + name, X)], "heptc", [f"{l} 0" for l in cube])
        print("unit CNF:", res[0])
        allok &= res[0][1]
elif MODE == "perturb":
    P0 = read_set(sys.argv[5])
    K, seed = int(sys.argv[6]), int(sys.argv[7])
    rng = random.Random(seed)
    reps = [p for i, p in enumerate(P0) if i < 17]
    assert sym(reps) == [q for p in reps for q in (p, neg(p))]
    jobs = []
    nsets = 0
    while nsets < K:
        d = rng.choice([1000, 10000, 50000, 200000])
        Q = sym([(x + rng.randint(-d, d), y + rng.randint(-d, d)) for x, y in reps])
        if not general_position(Q):
            continue
        nsets += 1
        for desc, X in labellings(Q, with_reflection=(nsets % 2 == 0)):
            jobs.append((f"perturb#{nsets} d={d} {desc} case={case_of(X)}", X))
    for b in range(0, len(jobs), 64):
        for r in run_batch(jobs[b:b + 64], f"pert{b}"):
            print(r, flush=True)
            allok &= r[1]
elif MODE == "random":
    K, seed = int(sys.argv[5]), int(sys.argv[6])
    rng = random.Random(seed)
    jobs = []
    for k in range(K):
        while True:
            P = [lambda: gen_parallelogram(rng, inner_kind=2), lambda: gen_parallelogram(rng, inner_kind=3),
                 lambda: gen_hexagon(rng)][k % 3]()
            if general_position(P):
                break
        for desc, X in labellings(P, with_reflection=(k % 2 == 0)):
            jobs.append((f"random#{k} {desc} case={case_of(X)}", X))
    for b in range(0, len(jobs), 16):
        for r in run_batch(jobs[b:b + 16], f"rand{b}"):
            print(r, flush=True)
            allok &= r[1]
print("ALL OK" if allok else "FAILURE", f"{time.time() - t0:.0f}s")
