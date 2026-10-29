#!/usr/bin/env python3
"""Collect the exploratory runs of the compact encoding (no proofs) into one TSV: experiment, formula, cube, solver,
cap, result, seconds.  usage: exploratory.py SGNDIR OUT.tsv"""
import glob, json, os, re, sys
D, out = sys.argv[1:3]
rows = []
def cad(path):
    s = open(path, errors="replace").read()
    st = "UNSAT" if "s UNSATISFIABLE" in s else ("SAT" if "s SATISFIABLE" in s else "no answer")
    t = re.findall(r"total process time since initialization:\s+([\d.]+)", s)
    return st, (t[-1] if t else "")
code = {10: "SAT", 20: "UNSAT", 0: "no answer"}
for f, exp, formula in [("cs/res.jsonl", "lookahead cubes, depth 10 (lacube)", "s34pc (no --rs)"),
                        ("cs/l2res.jsonl", "second layer, before the unit-propagation filter", "s34pcr"),
                        ("cs/l2res2.jsonl", "second layer, after the filter", "s34pcr"),
                        ("cs/l3res.jsonl", "third layer under Q3.11", "s34pcr"),
                        ("cs4/res.jsonl", "fourth layer under Q3.11/H4.10.29", "s34pcr"),
                        ("cs30/res.jsonl", "nested parallelograms, n = 30", "p30 (n=30, --par --centre --rs)"),
                        ("cs32/res.jsonl", "nested parallelograms, n = 32", "p32 (n=32, --par --centre --rs)")]:
    p = os.path.join(D, f)
    if not os.path.exists(p): continue
    cap = {"cs/res.jsonl": 900, "cs/l2res.jsonl": 900, "cs/l2res2.jsonl": 1200, "cs/l3res.jsonl": 600}.get(f, 600)
    for l in open(p):
        r = json.loads(l)
        if r.get("exit") == 1: continue          # launcher error before the solver ran (output path), rerun later
        rows.append([exp, formula, str(r["cube"]), "CaDiCaL 3.0.1", str(cap), code.get(r["exit"], str(r["exit"])), str(r["wall_s"])])
for name, exp in [("h34k17c", "hexagonal hull, k = 17 (calibration)"), ("h34k10c", "hexagonal hull, k = 10 (calibration)"),
                  ("s34pcr_l2cover", "cover of the second-layer split (all 3,850 cubes)")]:
    p = os.path.join(D, name + ".out")
    if os.path.exists(p):
        st, t = cad(p); rows.append([exp, name, "-", "CaDiCaL 3.0.1", "1800" if name.startswith("h34") else "3600", st, t])
for nm, cadt in [("H3.23.26", "455.47"), ("H3.13.24", "922.13")]:
    p = os.path.join(D, "cs", f"k_{nm}.out")
    if os.path.exists(p):
        s = open(p).read(); st = "UNSAT" if "s UNSATISFIABLE" in s else "no answer"
        w = int(os.path.getmtime(p) - os.path.getmtime(os.path.join(D, "cs", f"k_{nm}.cnf")))
        rows.append([f"solver comparison (CaDiCaL: {cadt} s)", "s34pcr", nm, "Kissat 4.0.4", "1200", st, f"~{w} (wall)"])
with open(out, "w") as g:
    g.write("experiment\tformula\tcube\tsolver\tcap_s\tresult\tseconds\n")
    for r in rows: g.write("\t".join(r) + "\n")
print(len(rows), "rows")
