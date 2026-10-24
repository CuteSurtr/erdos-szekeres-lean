#!/usr/bin/env python3
"""Exact checks of a 32-point integer set and both saturation tests.
  1. general position (Python ints) and exact largest convex subset (chiro.largest_convex_subset);
  2. x-sorted signotope (convert.py's exact shear if x repeats) + brute_kgon (axioms, convex 7-sets);
  3. (a) geometric: tools/trackA/sat.c over every face of the line arrangement (needs |coord| < 2^27);
     (b) abstract: ext_solve one-point extension at all 33 x-positions in the 33-point gen_cnf.py CNF.
usage: check32.py SATC EXT_SOLVE BRUTE_KGON BASE33.cnf WORKDIR a.pts [b.pts ...]   (JSON lines)"""
import itertools, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "A", "scripts"))
from chiro import largest_convex_subset, orient_exact  # noqa
from convert import to_sig  # noqa

satc, ext, brute, cnf, wd = sys.argv[1:6]
os.makedirs(wd, exist_ok=True)
for path in sys.argv[6:]:
    name = os.path.splitext(os.path.basename(path))[0]
    pts = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = len(pts)
    out = {"file": os.path.basename(path), "N": n}
    out["general_position"] = all(orient_exact(pts[i], pts[j], pts[k]) != 0 for i, j, k in itertools.combinations(range(n), 3))
    out["largest_convex_subset"] = largest_convex_subset(pts)
    mx = max(max(abs(x), abs(y)) for x, y in pts); out["max_abs_coord"] = mx
    spts, signs, sheared = to_sig(pts)
    sigf = os.path.join(wd, name + ".sig")
    with open(sigf, "w") as f:
        for v, (i, j, k) in enumerate(itertools.combinations(range(1, n + 1), 3)):
            f.write(f"{i} {j} {k} {1 if signs[v] == '+' else -1}\n")
    r = subprocess.run([brute, str(n), "7", sigf], capture_output=True, text=True)
    out["brute_kgon"] = r.stdout.strip()[-200:]
    if mx < 2 ** 27:
        badf = os.path.join(wd, name + ".bad")
        r = subprocess.run([satc, "sat", path, "7", badf], capture_output=True, text=True)
        js = [l for l in r.stdout.splitlines() if l.startswith("{")]
        res = json.loads(js[-1]) if js else {"error": (r.stdout + r.stderr)[-300:]}
        out["sat_c"] = res
        if js:
            out["faces_covered"] = res["faces_euler"] == res["faces_hit_by_valid_candidates"]
            out["geom_saturated"] = res["bad_candidates"] == 0 and out["faces_covered"]
    else:
        out["sat_c"] = "skipped: |coord| >= 2^27"
    jobs = f"S {name} {n} {signs}\n" + "".join(f"P {p}\n" for p in range(1, n + 2))
    r = subprocess.run([ext, cnf, str(n + 1), "1000000", "lucky=0"], input=jobs, capture_output=True, text=True)
    R = [l.split() for l in r.stdout.splitlines() if l.startswith("R ")]
    out["ext_positions"] = len(R)
    out["ext_sat"] = [int(x[2]) for x in R if x[3] == "SAT"]
    out["ext_unknown"] = [int(x[2]) for x in R if x[3] == "UNKNOWN"]
    out["ext_unsat"] = sum(1 for x in R if x[3] == "UNSAT")
    W = [l for l in r.stdout.splitlines() if l.startswith("W ")]
    if W:
        with open(os.path.join(wd, name + ".ext_models"), "w") as f: f.write("\n".join(W) + "\n")
    out["abstract_saturated"] = len(R) == n + 1 and out["ext_unsat"] == n + 1
    print(json.dumps(out), flush=True)
