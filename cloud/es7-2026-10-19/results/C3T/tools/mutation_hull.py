#!/usr/bin/env python3
"""Planted bugs in hullcase.hull_order must be caught by validate_hull.py.
usage: mutation_hull.py M K NSETS SEED"""
import json
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = {
    "swap_sigma_orders": "    if s == 0:\n        return [0, a + m, 2 * m, a, m, a + 2 * m]\n    return [0, a, 2 * m, a + 2 * m, m, a + m]\n",
    "reverse_orientation": "    if s == 0:\n        return [0, a + m, m, a + 2 * m, 2 * m, a][::1]\n    return [0, a + 2 * m, m, a, 2 * m, a + m]\n",
    "wrong_rotation": "    if s == 0:\n        return [0, a, m, a + m, 2 * m, a + 2 * m]\n    return [0, a + m, m, a + 2 * m, 2 * m, a]\n",
}
src = open(os.path.join(HERE, "hullcase.py")).read()
orig = "    if s == 0:\n        return [0, a, 2 * m, a + 2 * m, m, a + m]\n    return [0, a + m, 2 * m, a, m, a + 2 * m]\n"
assert orig in src
M, K, NS, seed = sys.argv[1:5]
mdir = os.path.join("/tmp", "c3s_mut")
os.makedirs(mdir, exist_ok=True)
for name, body in MUT.items():
    d = os.path.join(mdir, name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "hullcase.py"), "w").write(src.replace(orig, body))
    vsrc = open(os.path.join(HERE, "validate_hull.py")).read().replace("sys.path.insert(0, HERE)", f"sys.path.insert(0, {d!r})")
    vsrc = vsrc.replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}')
    open(os.path.join(d, "validate_hull.py"), "w").write(vsrc)
    r = json.loads(subprocess.run([sys.executable, os.path.join(d, "validate_hull.py"), M, K, NS, seed],
                                  capture_output=True, text=True, check=True).stdout)
    h6 = sum(v for c, v in r["case_counts"].items() if c.startswith("H6"))
    print(json.dumps({"mutation": name, "tested": r["tested"], "h6_sets": h6, "failures": len(r["fail"]), "caught": len(r["fail"]) > 0}))
