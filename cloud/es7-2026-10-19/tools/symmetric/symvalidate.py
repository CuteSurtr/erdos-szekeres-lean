#!/usr/bin/env python3
"""Soundness test of a symcnf.py CNF against random *realizable* rotationally symmetric point
sets (the direction that matters: every realizable symmetric configuration with the normal-form
labelling must be a model iff it has no convex K-gon).

For each sample: random orbit representatives, rotated copies, (centre at the origin), the
labelling normal form of symcnf.py applied geometrically, chi from exact integer coordinates
(rounded from floats, resampled if any triple is nearly degenerate), then
  (1) fix the triple-orbit variables of the CNF to chi; the remaining (auxiliary) part is decided
      exactly by unit propagation (it is Horn: upward definitional clauses + negative K-set clauses)
  (2) brute-force: largest convex subset of the set points with the exact DP of
      scripts/es_lower_bound_witness.py (geometric, independent of chi).
Required: CNF satisfiable  <=>  largest convex subset < K.  Reports counts and mismatches.
Also checks that every realizable sample is symmetric in chi (sanity of the labelling).

usage: symvalidate.py cnf map.json samples [seed] [dump_first_free_sample.pts]
"""
import itertools
import json
import math
import random
import os
import sys

sys.path.insert(0, os.path.join(os.environ.get("ES_REPO", "."), "scripts"))  # ES_REPO = repository root
from es_lower_bound_witness import largest_convex_subset, orient  # noqa: E402


def load_cnf(path):
    clauses = []
    nv = 0
    with open(path) as f:
        for line in f:
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                nv = int(line.split()[2])
                continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0
            clauses.append(lits[:-1])
    return nv, clauses


def sat_given_X(nv, clauses, occ, xassign):
    val = [None] * (nv + 1)
    for v, b in xassign.items():
        val[v] = b
    queue = list(range(len(clauses)))
    inq = [True] * len(clauses)
    while queue:
        ci = queue.pop()
        inq[ci] = False
        c = clauses[ci]
        unassigned = None
        nun = 0
        satisfied = False
        for l in c:
            v = val[abs(l)]
            if v is None:
                nun += 1
                unassigned = l
                if nun > 1:
                    break
            elif v == (l > 0):
                satisfied = True
                break
        if satisfied or nun > 1:
            continue
        if nun == 0:
            return False
        var = abs(unassigned)
        val[var] = unassigned > 0
        for cj in occ[var]:
            if not inq[cj]:
                inq[cj] = True
                queue.append(cj)
    for c in clauses:
        if not any((val[abs(l)] if val[abs(l)] is not None else False) == (l > 0) for l in c):
            raise RuntimeError("completion with False failed: aux part not Horn?")
    return True


def parity(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv & 1 else 1


def sample_points(info, rng, scale=10 ** 9):
    """returns integer points indexed as in the CNF (orbit points, then centre), or None"""
    m, t = info["m"], info["t"]
    has_center = info["center"] != "none"
    # random representatives in polar form
    rad = [rng.uniform(0.15, 1.0) for _ in range(t)]
    ang = [rng.uniform(0, 2 * math.pi) for _ in range(t)]
    # labelling normal form: orbit 0 = the first; rotate frame so that (0,0) is at angle 0
    theta0 = ang[0]
    ang = [a - theta0 for a in ang]
    reps = []
    for o in range(t):
        if o == 0:
            reps.append(0.0)
            continue
        # representative: the orbit point with angle in (0, 2pi/m)
        a = ang[o] % (2 * math.pi / m)
        if a < 1e-9 or 2 * math.pi / m - a < 1e-9:
            return None
        reps.append(a)
    # order of orbits 1..t-1
    others = list(range(1, t))
    if m % 2 == 1:
        others.sort(key=lambda o: reps[o])          # angle at the centre
    else:
        px, py = rad[0], 0.0
        others.sort(key=lambda o: math.atan2(rad[o] * math.sin(reps[o]) - py, rad[o] * math.cos(reps[o]) - px))
    order = [0] + others
    pts = []
    for o in order:
        for r in range(m):
            a = reps[o] + 2 * math.pi * r / m
            pts.append((rad[o] * math.cos(a), rad[o] * math.sin(a)))
    if has_center:
        pts.append((0.0, 0.0))
    ipts = [(round(x * scale), round(y * scale)) for x, y in pts]
    # degeneracy guard: every triple clearly non-collinear relative to rounding error
    for a, b, c in itertools.combinations(range(len(ipts)), 3):
        if abs(orient(ipts[a], ipts[b], ipts[c])) < 64 * scale:
            return None
    return ipts


def chi_from_points(info, ipts):
    xassign = {}
    for a, b, c, v, s in info["triples"]:
        d = orient(ipts[a], ipts[b], ipts[c])
        val = 1 if d > 0 else -1
        want = s * val   # chi(a,b,c) = s * var  =>  var = s * chi
        if v in xassign and xassign[v] != (want > 0):
            return None   # symmetry broken by rounding (should not happen with the guard)
        xassign[v] = want > 0
    return xassign


def main():
    cnf, mp, samples = sys.argv[1], sys.argv[2], int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    dump = sys.argv[5] if len(sys.argv) > 5 else None   # write the first K-gon-free realizable sample here
    info = json.load(open(mp))
    K = info["K"]
    nv, clauses = load_cnf(cnf)
    occ = [[] for _ in range(nv + 1)]
    for ci, c in enumerate(clauses):
        for l in c:
            occ[abs(l)].append(ci)
    rng = random.Random(seed)
    n_ok = n_free = n_sat = mism = degenerate = symbroken = 0
    while n_ok < samples:
        ipts = sample_points(info, rng)
        if ipts is None:
            degenerate += 1
            continue
        xa = chi_from_points(info, ipts)
        if xa is None:
            symbroken += 1
            continue
        n_ok += 1
        setpts = [ipts[i] for i in info["setpts"]]
        big = largest_convex_subset(setpts)
        free = big < K
        sat = sat_given_X(nv, clauses, occ, xa)
        n_free += free
        n_sat += sat
        if free and dump:
            with open(dump, "w") as f:
                for x, y in ipts:
                    f.write(f"{x} {y}\n")
            dump = None
        if sat != free:
            mism += 1
            if mism <= 3:
                print("MISMATCH sat=", sat, "largest convex=", big, ipts)
    print(json.dumps({"cnf": cnf, "N": info["N"], "K": K, "m": info["m"], "center": info["center"],
                      "samples": n_ok, "kgon_free": n_free, "cnf_sat": n_sat, "mismatches": mism,
                      "resampled_degenerate": degenerate, "symmetry_broken_by_rounding": symbroken}))
    sys.exit(1 if mism else 0)


if __name__ == "__main__":
    main()
