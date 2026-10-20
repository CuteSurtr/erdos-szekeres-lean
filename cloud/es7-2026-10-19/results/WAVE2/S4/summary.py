#!/usr/bin/env python3
"""Per-case summary of S4 results (run from results/WAVE2/S4); writes summary.json, prints a markdown table."""
import json, os, subprocess
ORDER = "U7_L14 U7_L9 U7_L2 U6_L11 U6_L7 U5_L14 U5_L8 U5_L2 U4_L13 U4_L8 U4_L2 U3_L13 U3_L9 U3_L5 U6-15_L U6-10_L U_L5-16 U_L5-14 U_L5-12 U_L5-10 U5-9_L U_L5-7 U5-6_L U_L4-14 U4-13_L U4-11_L U4-9_L U_L4-7 U4-6_L".split()
sk = dict(l.split(None, 1) for l in open("skipped.txt")) if os.path.exists("skipped.txt") else {}
out = []; print("| case | state | method | top cubes | verified leaves | splits | open | unchecked/rejected | SAT | solve s | check s | march s | cover |"); print("|" + "---|" * 13)
for c in ORDER:
    if not os.path.isdir(c):
        st = "skipped (closed by " + sk[c].split()[1].split("/")[2] + ")" if c in sk else "not reached / not started by S4"
        print(f"| {c} | {st} |" + " - |" * 11); out.append({"case": c, "state": st}); continue
    rs = [json.loads(l) for l in open(f"{c}/leaves.jsonl")]
    cu = [r for r in rs if "cube" in r]
    nl = sum(1 for l in open(f"{c}/leaves.icnf") if l.startswith("a "))
    no = sum(1 for l in open(f"{c}/open.icnf") if l.startswith("a "))
    meth = rs[0].get("method", "close_march")
    top = next((r["ncubes"] for r in rs if "ncubes" in r), "-")
    sp = sum(r.get("status") == "SPLIT" for r in cu); bad = sum(r.get("status") == "UNSAT_UNCHECKED" for r in cu)
    sat = sum(r.get("status") == "SAT" for r in cu)
    solve = round(sum(r.get("solve_s", 0) for r in cu), 1); chk = round(sum(r.get("check_s", 0) for r in cu), 1)
    ms = round(sum(r.get("march_s", 0) + r.get("split_s", 0) for r in rs), 1)
    cov = subprocess.run(["python3", "../../Mii-S/scripts/covercheck.py", f"{c}/leaves.icnf"], capture_output=True, text=True).stdout.split()[1]
    state = "CLOSED" if nl > 0 and no == 0 and cov == "COVERED" else "OPEN"
    d = dict(case=c, state=state, method=meth, top=top, leaves=nl, splits=sp, open=no, unchecked=bad, sat=sat, solve_s=solve, check_s=chk, march_s=ms, cover=cov, case_sha256=rs[0]["case_sha256"])
    out.append(d); print(f"| {c} | **{state}** | {meth} | {top} | {nl} | {sp} | {no} | {bad} | {sat} | {solve} | {chk} | {ms} | {cov} |")
json.dump(out, open("summary.json", "w"), indent=1)
