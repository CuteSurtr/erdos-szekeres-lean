#!/usr/bin/env python3
"""For given hull cases, the uniform measure (conditioned on the case cube) covered by the
closed cubes of C2 and Mii (baseline.py's lists).  Usage: case_overlap.py RESULTS NSAMP SPEC..."""
import sys, os
import numpy as np
R, NS = sys.argv[1], int(sys.argv[2])
sys.path.insert(0, os.path.join(R, "Mii-S/scripts")); sys.argv = sys.argv[:1] + [R, "1", "1"]
import importlib.util
spec = importlib.util.spec_from_file_location("bl", os.path.join(R, "Mii-S/scripts/baseline.py"))
src = open(os.path.join(R, "Mii-S/scripts/baseline.py")).read().split("rng = np.random")[0]
ns = {}; exec(src, ns)
import hullsplit as H
closed = ns["c2"]() + [c for v in ns["mii"]()[0].values() for c in v]
rng = np.random.default_rng(5)
for sp in os.environ["SPECS"].split():
    U, L = sp.split("/"); U = tuple(int(x) for x in U.split(",") if x); L = tuple(int(x) for x in L.split(",") if x)
    cube = H.cube(U, L); fixed = {abs(l): l > 0 for l in cube}
    cs = [c for c in set(closed) if not any(abs(l) in fixed and fixed[abs(l)] != (l > 0) for l in c)]
    vs = sorted({abs(l) for c in cs for l in c}); pos = {v: i for i, v in enumerate(vs)}
    A = rng.random((NS, len(vs))) < 0.5
    for v, b in fixed.items():
        if v in pos: A[:, pos[v]] = b
    hit = np.zeros(NS, bool)
    for c in cs:
        idx = [pos[abs(l)] for l in c]; sg = np.array([l > 0 for l in c]); hit |= (A[:, idx] == sg).all(axis=1)
    print(sp, "consistent closed cubes", len(cs), "covered fraction", round(float(hit.mean()), 4))
