#!/usr/bin/env python3
"""Collect mutation-test outputs (MUTDIR/<cnf>_<mutation>.json) into JSON lines on stdout."""
import glob
import json
import os
import sys

for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    d = json.load(open(p))
    base, mut = os.path.basename(p)[:-5].rsplit("_", 1)
    print(json.dumps({"cnf": base, "mutation": mut, "samples": d["samples"], "mismatches": d["mismatches"],
                      "map_conflicts": d["map_conflicts"], "detected": d["mismatches"] > 0 or d["map_conflicts"] > 0}))
