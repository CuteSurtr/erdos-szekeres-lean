#!/usr/bin/env python3
"""Print a one-line status per cnc2 run directory (from state.json).  usage: status.py RUNDIR..."""
import json
import sys
from collections import Counter
from fractions import Fraction

for rd in sys.argv[1:]:
    try:
        st = json.load(open(rd + "/state.json"))
    except Exception as e:
        print(rd, "no state", e)
        continue
    cbd = {int(k): v for k, v in st["closed_by_depth"].items()}
    opens = [len(c) for c, _ in st["open"]]
    D = max([0] + list(cbd) + opens)
    cw = Fraction(sum(v << (D - d) for d, v in cbd.items()), 1 << D)
    oh = Counter(opens)
    print(rd.rstrip("/").split("/")[-1], "jobs", st["jobs"], "splits", st["splits"], "closed", st["closed"],
          "open", len(opens), "open_depths", dict(sorted(oh.items())), "closed_weight", f"{cw} ~ {float(cw):.6g}",
          "solve_h", round(st["solve_ms_total"] / 3.6e6, 3), "elapsed_h", round(st.get("elapsed_this_run", 0) / 3600, 3),
          "sat", bool(st["sat"]))
