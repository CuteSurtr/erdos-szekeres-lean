#!/usr/bin/env python3
"""Compare pycheck TSV lines with tcheck per-context TSV. usage: compare_py.py TCHECK.contexts.tsv PY.tsv"""
import sys
c = {}
for l in open(sys.argv[1]).readlines()[1:]:
    f = l.rstrip("\n").split("\t"); c[f[0]] = (f[1], f[2], f[5], f[7], f[8])
bad = n = leaves = 0
for l in open(sys.argv[2]):
    f = l.rstrip("\n").split("\t")
    if f[0] == "master":
        print("py master: nodes %s leaves %s min_margin %s max_row %s errors %s" % tuple(f[1:])); continue
    n += 1; leaves += int(f[2])
    exp = (f[1], f[2], f[3] if f[3] != "None" else "NA", f[4], f[5])
    if c[f[0]] != exp:
        bad += 1
        if bad < 5: print("DIFF", f, c[f[0]])
print(f"compared {n} contexts, {leaves} leaves; differences {bad}")
