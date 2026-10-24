#!/usr/bin/env python3
"""Per-case summary of W26 leaves.jsonl files (prints a markdown table)."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("| case | top cubes | top.icnf sha256 | splits | verified leaves | other UNSAT | open | SAT | solve s | check s | march s | max proof MB |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for c in ["U14_L", "U7_L", "U_L10", "U13_L"]:
    rs = [json.loads(l) for l in open(f"{R}/{c}/leaves.jsonl")]
    top = next(r for r in rs if r.get("top"))
    cub = [r for r in rs if "cube" in r]
    ver = sum(1 for r in cub if r["status"] == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT")
    oth = sum(1 for r in cub if r["status"] == "UNSAT" and r.get("cake_lpr") != "s VERIFIED UNSAT")
    spl = sum(1 for r in cub if r["status"] == "SPLIT")
    sat = sum(1 for r in rs if r.get("status") == "SAT")
    op = sum(1 for l in open(f"{R}/{c}/open.icnf")) if os.path.exists(f"{R}/{c}/open.icnf") else "-"
    sv = sum(r.get("solve_s", 0) for r in rs); ck = sum(r.get("check_s", 0) for r in rs)
    ms = sum(r.get("split_s", 0) for r in rs) + top["march_s"]
    pb = max([r.get("proof_bytes", 0) for r in rs]) / 1e6
    print(f"| {c} | {top['ncubes']} | `{top['top_sha256'][:16]}…` | {spl} | {ver} | {oth} | {op} | {sat} | {sv:.0f} | {ck:.0f} | {ms:.0f} | {pb:.0f} |")
