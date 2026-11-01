#!/bin/sh
# Reproduce the independent check of the 9-fold 253-point set (all code in this directory, written from scratch).
# Run from cloud/es7-2026-10-19/results.  Writes its tables to check253/out_p9 and check253/bf_work.
V=PRIMEFOLD/check253
PTS=PRIMEFOLD/sets/k10/rule_p9_253pts.pts
PY="python3 -I"
${CC:-cc} -O2 -Wall ${CFLAGS:-} -o $V/dpcheck $V/dpcheck.c
mkdir -p $V/out_p9 $V/bf_work
$PY $V/exact_orient.py $PTS $V/out_p9                       # exact signs of all C(253,3) triples + exact (y,x)/(x,y) ranks
$V/dpcheck $V/out_p9/ranks.txt $V/out_p9/orient_upper.bin    # three DPs: lowest anchor, leftmost anchor, cup+cap
$PY $V/decimal_crosscheck.py $PTS $V/out_p9                  # all signs again with 150-digit decimals
$PY $V/bruteforce_test.py $V/out_p9 $V/bf_work $V/dpcheck    # DP vs brute force (60 subsets + 45 random sets)
