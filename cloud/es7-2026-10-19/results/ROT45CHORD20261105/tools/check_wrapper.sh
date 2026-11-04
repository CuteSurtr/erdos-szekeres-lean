#!/bin/bash
# check_wrapper.sh CUBE_BASE CUTOFF_EPOCH : lrat-check one UNSAT proof, then SHA-256 of all artifacts.
# Verdict VERIFIED requires lrat-check exit code 0 and the line "c VERIFIED".  Nothing is deleted.
b=$1; cut=$2; left=$(( cut - $(date +%s) )); [ $left -lt 1 ] && left=1
echo "start=$(date +%Y-%m-%dT%H:%M:%S)" > $b.check.meta
t0=$(date +%s)
timeout $left nice -n 5 lrat-check $b.cnf $b.lrat > $b.check.log 2>&1; rc=$?
t1=$(date +%s)
if [ $rc -eq 0 ] && grep -q '^c VERIFIED' $b.check.log; then v=VERIFIED; else v=NOT-VERIFIED; fi
echo "rc=$rc verdict=$v seconds=$((t1-t0))" >> $b.check.meta
sha256sum $b.cnf $b.lrat $b.out $b.check.log > $b.hashes.txt
echo done >> $b.check.meta
