#!/usr/bin/env python3
"""Part 1 encoding validation for the mirror CNFs (Task C).

usage: validate.py <cnfdir> <bindir> <outdir> [nsets=1000] [seed=1]

A. 1,000 random exactly mirror-symmetric 33-point integer sets in general position with one
   axis point (half with the axis point interior, a quarter on top, a quarter at the bottom).
   For every set:
   A1 x-sorted orientations satisfy every orientation-only clause of gen_etv.py's m33k7.cnf
      (signotope axioms + identification clauses = sign rule), and the direct identity
      X(i,j,k) = X(34-k,34-j,34-i) holds;
   A2 the same for the orbit-substituted m33k7int.sub.cnf (after the WLOG y-reflection that
      makes X(1,2,3) true) when the axis point is interior, and for extreme sets the
      "axis point interior" clause pair is violated (so it is exactly the interior condition);
   A3 for extreme sets (bottom ones y-reflected to the top), the projective hull frame
      (x,y)->(x/d,1/d), d=y0-y: the orientations satisfy every orientation-only clause of
      hm33k7.cnf and hm33k7.sub.cnf, and the map preserves all orientations not involving p;
   A4 the full CNF under the set's orientations as assumptions is UNSAT iff the set has a
      convex 7-gon (cgon count); random sets all have 7-gons, so this checks gon detection.
B. Small-k equivalence: random mirror sets at (N,k) = (7,5), (8,5), (9,5), (11,6), both frames;
   CNF-under-orientations SAT must equal "no convex k-gon" by exhaustive Python check.
"""
import sys, os, json, random, subprocess, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mirlib import *

cnfdir, bindir, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
nsets = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
os.makedirs(outdir, exist_ok=True)
rng = random.Random(seed)
report = {"seed": seed}


def xonly(cnf, nX, out):
    nv, cls = read_cnf(cnf)
    keep = [c for c in cls if all(abs(l) <= nX for l in c)]
    with open(out, "w") as f:
        f.write(f"p cnf {nX} {len(keep)}\n")
        for c in keep:
            f.write(" ".join(map(str, c)) + " 0\n")
    return len(keep)


def asolve(cnf, lines):
    r = subprocess.run([os.path.join(bindir, "asolve"), cnf], input="".join(l + " 0\n" for l in lines),
                       capture_output=True, text=True, check=True)
    res = [ln.split()[1] for ln in r.stdout.split("\n") if ln.strip()]
    assert len(res) == len(lines)
    return res


def lits(X, idx):
    return " ".join(str(idx[t] if v else -idx[t]) for t, v in X.items())


def kgons(P, k):
    r = subprocess.run([os.path.join(bindir, "cgon"), "count", str(k)], input="".join(f"{x} {y}\n" for x, y in P),
                       capture_output=True, text=True, check=True)
    tok = dict(t.split("=") for t in r.stdout.split()[1:])
    return int(tok[f"c{k}"])


t0 = time.time()
N = 33
idx = triple_index(N)
nX = len(idx)
for name in ["m33k7", "hm33k7", "m33k7int.sub", "hm33k7.sub"]:
    report[f"xonly_clauses_{name}"] = xonly(f"{cnfdir}/{name}.cnf", nX, f"{outdir}/{name}.xonly.cnf")
c = 17
interior_cup = [idx[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1)]
sets = []
nonhull_lines, sub_lines, hull_lines, sub_kind = [], [], [], []
direct_bad = 0
proj_bad = 0
interior_ok = 0
for s in range(nsets):
    where = "interior" if s % 2 == 0 else ("top" if s % 4 == 1 else "bottom")
    P = mirror_set(16, 1, rng, R=10**6, where=where)
    sets.append((where, P))
    Q = xsorted(P)
    assert Q[16][0] == 0
    X = orientations(Q)
    direct_bad += sum(1 for (i, j, k), v in X.items() if X[(N + 1 - k, N + 1 - j, N + 1 - i)] != v)
    nonhull_lines.append(lits(X, idx))
    # the interior clause pair, evaluated directly
    has_cup = any(X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1))
    has_cap = any(not X[(i, c, k)] for i in range(1, c) for k in range(c + 1, N + 1))
    interior_ok += ((has_cup and has_cap) == (where == "interior"))
    if where == "interior":
        X2 = X if X[(1, 2, 3)] else {t: (not v) for t, v in X.items()}
        sub_lines.append(lits(X2, idx))
    else:
        P2 = P if where == "top" else [(x, -y) for x, y in P]
        T, XH = hull_frame(P2)
        # orientation preservation of the projective map on triples avoiding p
        p = [q for q in P2 if q[0] == 0][0]
        rest = [q for q in P2 if q != p]
        for a, b, d in rng.sample(list(itertools.combinations(range(32), 3)), 200):
            u = lambda q: (F(q[0], p[1] - q[1]), F(1, p[1] - q[1]))
            if (orient(rest[a], rest[b], rest[d]) > 0) != (orient(u(rest[a]), u(rest[b]), u(rest[d])) > 0):
                proj_bad += 1
        hull_lines.append(lits(XH, idx))
report["A_sets"] = nsets
report["A1_direct_mirror_identity_violations"] = direct_bad
report["A2_interior_clause_matches_geometry"] = f"{interior_ok}/{nsets}"
report["A3_projective_orientation_mismatches_in_sampled_triples"] = proj_bad
res = {}
res["m33k7.xonly"] = asolve(f"{outdir}/m33k7.xonly.cnf", nonhull_lines)
res["m33k7int.sub.xonly"] = asolve(f"{outdir}/m33k7int.sub.xonly.cnf", sub_lines)
res["hm33k7.xonly"] = asolve(f"{outdir}/hm33k7.xonly.cnf", hull_lines)
res["hm33k7.sub.xonly"] = asolve(f"{outdir}/hm33k7.sub.xonly.cnf", hull_lines)
for k, v in res.items():
    report[f"A_{k}_SAT"] = f"{v.count('SAT')}/{len(v)}"
# A4: full CNFs, gon detection (subset of 100 sets per frame keeps it quick; cgon is exact)
sub = list(range(0, nsets, max(1, nsets // 200)))
full_nh = asolve(f"{cnfdir}/m33k7.cnf", [nonhull_lines[i] for i in sub])
k7 = [kgons(sets[i][1], 7) for i in sub]
report["A4_m33k7_full_unsat_iff_7gon"] = f"{sum((r == 'UNSAT') == (g > 0) for r, g in zip(full_nh, k7))}/{len(sub)}"
report["A4_min_7gons_in_random_sets"] = min(k7)
full_h = asolve(f"{cnfdir}/hm33k7.cnf", hull_lines[:100])
report["A4_hm33k7_full_UNSAT"] = f"{full_h.count('UNSAT')}/{len(full_h)}"
report["A_time_s"] = round(time.time() - t0, 1)
print(json.dumps(report), flush=True)

# B: small-k equivalence
t1 = time.time()
for (Nn, k, npairs, axis) in [(7, 5, 3, 1), (8, 5, 4, 0), (9, 5, 4, 1), (11, 6, 5, 1)]:
    idn = triple_index(Nn)
    for frame in (["nonhull", "hull"] if axis == 1 else ["nonhull"]):
        lines, truth = [], []
        for s in range(2000):
            if frame == "hull":
                P = mirror_set(npairs, 1, rng, R=1000, where="top")
                _, X = hull_frame(P)
            else:
                P = mirror_set(npairs, axis, rng, R=1000, where=None)
                X = orientations(xsorted(P))
            lines.append(lits(X, idn))
            truth.append(not has_kgon(P, k))
        cnf = f"{cnfdir}/{'h' if frame == 'hull' else ''}m{Nn}k{k}.cnf"
        r = asolve(cnf, lines)
        agree = sum((x == "SAT") == t for x, t in zip(r, truth))
        report[f"B_{frame}_N{Nn}_k{k}"] = {"agree": f"{agree}/{len(r)}", "kgon_free_sets": sum(truth)}
report["B_time_s"] = round(time.time() - t1, 1)
print(json.dumps(report, indent=1))
json.dump(report, open(f"{outdir}/validate_report.json", "w"), indent=1)
