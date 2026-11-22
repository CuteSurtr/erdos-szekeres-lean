#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): the HEURISTIC launch numbers from the gate's calibration (logs/calib_gate.out).
Prints one JSON object: CPU-h, wall days at 3/6/12 compiles, export hours, disk in GB."""
import json
from pathlib import Path

G = Path("/home/jay/research/data/formalize-20261122/s3520-gate")
LEAVES = 119054033
rows = [json.loads(l) for l in (G / "logs/calib_gate.out").read_text().splitlines() if l.strip()]
units = [r for r in rows if "unit" in r and r["modules"]]
allr = next(r for r in rows if "all" in r)
rates = [r["cpu_s_per_leaf"] for r in units] + [allr["cpu_s_per_leaf"]]
mod_lo = min(r["per_module_cpu_s_per_leaf_range"][0] for r in units)
mod_hi = max(r["per_module_cpu_s_per_leaf_range"][1] for r in units)
lo, hi = min(rates), max(rates)
src = [r["src_B_per_leaf"] for r in units]
ol = [r["olean_B_per_leaf"] for r in units]
out = {
    "cpu_s_per_leaf_units": {r["unit"]: r["cpu_s_per_leaf"] for r in units}, "cpu_s_per_leaf_all": allr["cpu_s_per_leaf"],
    "per_module_range": [mod_lo, mod_hi],
    "cpu_h_units_range": [round(LEAVES * lo / 3600), round(LEAVES * hi / 3600)],
    "cpu_h_module_range": [round(LEAVES * mod_lo / 3600), round(LEAVES * mod_hi / 3600)],
    "wall_days": {n: [round(LEAVES * lo / n / 86400, 1), round(LEAVES * hi / n / 86400, 1)] for n in (3, 6, 12)},
    "export_h": [round(LEAVES * 0.000315 / 3600, 1), round(LEAVES * 0.00035 / 3600, 1)],
    "compile_leaves_per_s": {n: round(n / allr["cpu_s_per_leaf"]) for n in (3, 6, 12)},
    "src_GB": [round(LEAVES * min(src) / 1e9), round(LEAVES * max(src) / 1e9)],
    "olean_GB": [round(LEAVES * min(ol) / 1e9), round(LEAVES * max(ol) / 1e9)],
    "kept_GB": [round(LEAVES * (min(src) + min(ol)) / 1e9), round(LEAVES * (max(src) + max(ol)) / 1e9)],
    "max_anon_mb": allr["anon"], "max_rss_mb": allr["rss"],
}
print(json.dumps(out, indent=1))
