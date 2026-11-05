#!/bin/bash
# check_wrapper.sh CUBE_BASE : verify one UNSAT proof and hash every artifact.  Nothing is deleted.
# VERDICT: VERIFIED only if cake_lpr (the verified CakeML LRAT/LPR checker) prints the line "s VERIFIED UNSAT".
#   cake_lpr exits 0 even when checking fails, so only that line counts.  REJECTED if it prints "Checking failed".
#   Anything else (killed, out of memory, crash) is INTERRUPTED and the supervisor may retry.
# lrat-check (drat-trim 2e3b2dc) is NOT used: its RATs==0 branch accepts a vacuous empty-clause step
#   (tested 5 Nov 2026: "p cnf 1 1 / 1 0" with proof "2 0 0" is reported "c VERIFIED", rc 0).
b=$1
echo "start=$(date +%Y-%m-%dT%H:%M:%S)" > $b.check.meta
sha256sum $b.cnf $b.lrat $b.out > $b.hashes.txt; echo "hash_rc=$?" >> $b.check.meta
t0=$(date +%s)
nice -n 5 cake_lpr --CML_HEAP_SIZE=12000 $b.cnf $b.lrat > $b.cake.log 2>&1; rc=$?
t1=$(date +%s)
if grep -q '^s VERIFIED UNSAT' $b.cake.log; then v=VERIFIED
elif grep -q 'Checking failed' $b.cake.log; then v=REJECTED
else v=INTERRUPTED; fi
echo "rc=$rc verdict=$v seconds=$((t1-t0)) checker=cake_lpr" >> $b.check.meta
sha256sum $b.cake.log >> $b.hashes.txt
echo done >> $b.check.meta
