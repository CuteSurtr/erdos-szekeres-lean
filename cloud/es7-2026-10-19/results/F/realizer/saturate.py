#!/usr/bin/env python3
"""Exact checks of realized K-gon-free point sets, then exact one-point saturation with trackA/sat.c.

For each integer point file (one "x y" per line, label order of the model):
  * optional: the realized orientations equal the model chirotope (--models/--P/--m, exact);
  * general position and the exact largest convex subset (must be < K);
  * for m = 2: exact central symmetry p_{2o+1} = -p_{2o};
  * |coordinates| < 2^27 (sat.c's exactness bound);
  * sat.c "sat" mode: enumerates every face of the arrangement of the C(N,2) lines and tests a
    point in each; bad_candidates = number of positions where a new point creates NO convex K-gon.
    The face count is cross-checked against Euler's relation (faces_euler == faces_hit).
    bad_candidates = 0 and full face coverage => no point can be added (the set is saturated).
    If bad_candidates > 0, the head of sat.c's list of such candidates is reported (bad_file_head);
    any extension must then be constructed and re-checked exactly before it is claimed.
usage: saturate.py --sat path/to/sat --K 7 [--m 2] [--models FILE --P 32 [--center]] a.pts b.pts ...
Prints one JSON line per file.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chiro import largest_convex_subset, read_models, verify_exact, orient_exact  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sat", required=True)
    ap.add_argument("--K", type=int, default=7)
    ap.add_argument("--m", type=int, default=1)
    ap.add_argument("--models")
    ap.add_argument("--P", type=int)
    ap.add_argument("--center", action="store_true", help="models have the centre as last point")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    models = read_models(a.models, a.P, a.m, a.center) if a.models else None
    for path in a.files:
        pts = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
        out = {"file": os.path.basename(path), "N": len(pts)}
        name = os.path.splitext(os.path.basename(path))[0]
        if models is not None and name.startswith("model"):
            chi = models[int(name[5:]) - 1]
            ok, bad, zero = verify_exact(pts, chi)
            out["matches_model_exactly"] = ok
        gp = all(orient_exact(pts[i], pts[j], pts[k]) != 0
                 for i in range(len(pts)) for j in range(i + 1, len(pts)) for k in range(j + 1, len(pts)))
        out["general_position"] = gp
        out["largest_convex_subset"] = largest_convex_subset(pts)
        if a.m == 2:
            out["centrally_symmetric"] = all(pts[2 * o + 1] == (-pts[2 * o][0], -pts[2 * o][1]) for o in range(len(pts) // 2))
        mx = max(max(abs(x), abs(y)) for x, y in pts)
        out["max_abs_coord"] = mx
        if mx >= 2 ** 27:
            out["sat"] = "skipped: coordinates exceed 2^27"
            print(json.dumps(out), flush=True)
            continue
        with tempfile.TemporaryDirectory() as td:
            badf = os.path.join(td, "bad.txt")
            r = subprocess.run([a.sat, "sat", path, str(a.K), badf], capture_output=True, text=True)
            js = [l for l in r.stdout.splitlines() if l.startswith("{")]
            res = json.loads(js[-1]) if js else {"error": r.stdout[-500:] + r.stderr[-500:]}
            out["sat"] = res
            if js:
                out["faces_covered"] = res["faces_euler"] == res["faces_hit_by_valid_candidates"]
                out["saturated"] = res["bad_candidates"] == 0 and out["faces_covered"]
                if res["bad_candidates"] > 0 and os.path.exists(badf):
                    out["bad_file_head"] = open(badf).read()[:2000]
        print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
