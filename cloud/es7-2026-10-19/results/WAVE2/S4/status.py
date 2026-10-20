#!/usr/bin/env python3
"""Task S4 step (a): status of a case in every other machine's directory.
Prints CLOSED <dir> | STARTED <dir> | FREE."""
import glob, os, sys
case = sys.argv[1]; st = "FREE"; who = ""
for d in sorted(glob.glob(f"results/WAVE1/*/{case}") + glob.glob(f"results/WAVE2/*/{case}")):
    if d.startswith("results/WAVE2/S4/"): continue
    lv = os.path.join(d, "leaves.icnf"); op = os.path.join(d, "open.icnf")
    nl = sum(1 for l in open(lv) if l.strip()) if os.path.exists(lv) else 0
    oa = sum(1 for l in open(op) if l.startswith("a")) if os.path.exists(op) else None
    if nl > 0 and oa == 0: print("CLOSED", d); sys.exit()
    if nl > 0 or os.path.exists(os.path.join(d, "top.icnf")): st, who = "STARTED", d
print(st, who)
