#!/usr/bin/env python3
"""Test the gluing recipes on the positive-control models (conjectured-maximum rung models):
each must glue to a 32-element signotope with no convex 7-gon (the classical size).
Negative test: the 757 recipe applied to a model of the cap/cup-swapped rung (7,7,5)@26
(which has 6-caps) must produce convex 7-gons, so the checker is not vacuous.
usage: glue_controls.py CACHE_DIR OUT.json"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = Path(sys.argv[1]).resolve()
cases = [("757", 26, "k7a5u7N26", True), ("756", 25, "k7a5u6N25", True), ("766", 30, "k7a6u6N30", True),
         ("757", 26, "k7a7u5N26", False)]
rows = []
for rung, N, tag, expect_ok in cases:
    for enc in ("ours", "bb"):
        m = C / "ctl" / f"{tag}_{enc}.model"
        g = C / "glue" / f"{tag}_{enc}_glued.txt"; g.parent.mkdir(exist_ok=True)
        n = int(subprocess.run([sys.executable, str(HERE / "glue.py"), rung, str(N), str(m), str(g)],
                               capture_output=True, text=True, check=True).stdout)
        pc = subprocess.run([str(C / "sigcheckB"), str(n), str(n + 1), str(n + 1), "7", str(g)], capture_output=True, text=True)
        chk = json.loads(pc.stdout)
        passed = chk["ok"] == expect_ok and chk["sig_viol"] == 0
        row = {"rung": rung, "model": f"{tag}_{enc}", "glued_points": n, "expect_no_7gon": expect_ok, "check": chk, "pass": passed}
        print(json.dumps(row), flush=True); rows.append(row)
Path(sys.argv[2]).write_text(json.dumps({"all_pass": all(r["pass"] for r in rows), "rows": rows}, indent=1))
print(json.dumps({"all_pass": all(r["pass"] for r in rows)}))
