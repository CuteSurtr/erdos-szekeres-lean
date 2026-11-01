#!/usr/bin/env python3
"""Exactness audit of the split enumeration (produces logs/split_exactness.txt).

For every linear partition of a set (tools/splits.py; this list contains every nontrivial z-split by Lemma 4' of
proofs/split_theorem.md), count how many pass the exact one-sidedness test, how many of those the LP rejects, how
many receive an exact rational z, and how many end as "numeric-only".  When pass_one_sidedness is 0, "no nontrivial
z-split" is decided by exact integer tests alone; the LP plays no part.

This is the inline code that wrote logs/split_exactness.txt, saved as a script; input paths are resolved from the
location of this file.  Usage: python3 tools/split_exactness.py > split_exactness.txt
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from geom import read_points
import splits


def audit(P):
    parts = splits.linear_partitions(P)
    passed_exact = 0; lp_rejected = 0; found = 0; numeric_only = 0
    for A, B in parts:
        sA = splits.side_vector(P, A, B)
        if sA is None: continue
        sB = splits.side_vector(P, B, A)
        if sB is None: continue
        passed_exact += 1
        z = splits.find_z(P, A, B)
        if z is None: lp_rejected += 1
        elif isinstance(z, tuple) and z and z[0] == "numeric": numeric_only += 1
        else: found += 1
    return dict(partitions=len(parts), pass_one_sidedness=passed_exact, lp_rejected=lp_rejected, found_exact=found,
                numeric_only=numeric_only)


for f in ["classical32", "mirror32", "central32", "c3_31points", "c3_30points", "c6_30points", "c4_28points",
          "c3_27points"]:
    print(f, audit(read_points(os.path.join(ROOT, "data", f"{f}.txt"))))
# walk sample
tot = dict(sets=0, pass_one_sidedness=0, lp_rejected=0, found_exact=0, numeric_only=0)
for fn in ["walk_classical32", "walk_mirror32", "walk_central32", "walk_random"]:
    for line in open(os.path.join(ROOT, "data", "walks", f"{fn}.txt")):
        f = line.split(); c = list(map(int, f[5:])); P = list(zip(c[0::2], c[1::2]))
        a = audit(P); tot["sets"] += 1
        for k in ("pass_one_sidedness", "lp_rejected", "found_exact", "numeric_only"): tot[k] += a[k]
print("walk sample (with duplicates):", tot)
