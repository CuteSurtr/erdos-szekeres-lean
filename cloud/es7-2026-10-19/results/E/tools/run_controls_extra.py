#!/usr/bin/env python3
"""D3 controls and extra 3-fold controls (JSON lines).  usage: run_controls_extra.py CNF_DIR CADICAL OUT_DIR"""
import json
import os
import subprocess
import sys
import time

cnfdir, cad, outdir = sys.argv[1:4]
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(outdir, exist_ok=True)
rows = [
    ("n9k5d3", "UNSATISFIABLE", "ES(5)=9"),
    ("n9k6d3", "UNSATISFIABLE", "a D3 6-orbit is cocircular, hence a convex hexagon"),
    ("n21k6d3", "UNSATISFIABLE", "ES(6)=17"),
    ("n15k6d3", "UNSATISFIABLE", "implied by the 3-fold n15k6m3 answer (D3 is a sub-case of C3)"),
    ("n21k7d3", "SATISFIABLE", "random exact D3 21-point sets without convex 7-gon exist (symval2)"),
    ("n9k6m3", "SATISFIABLE", "small 3-fold hexagon-free sets exist"),
    ("n12k6m3", "SATISFIABLE", "realizable 3-fold 12-point hexagon-free sets found (symval2, anneal_sym)"),
]
for tag, exp, why in rows:
    t0 = time.time()
    outp = os.path.join(outdir, tag + ".out")
    with open(outp, "w") as f:
        subprocess.run([cad, "-q", "-t", "1800", os.path.join(cnfdir, tag + ".cnf")], stdout=f)
    st = next((l.split()[1] for l in open(outp) if l.startswith("s ")), None)
    rec = {"cnf": tag, "expected": exp, "got": st, "seconds": round(time.time() - t0, 1),
           "verdict": "OK" if st == exp else "FAIL", "reason": why}
    if st == "SATISFIABLE":
        r = subprocess.run([sys.executable, os.path.join(here, "modelcheck.py"), os.path.join(cnfdir, tag + ".json"), outp],
                           capture_output=True, text=True)
        rec["model_check"] = json.loads(r.stdout.strip().splitlines()[-1])
    print(json.dumps(rec), flush=True)
