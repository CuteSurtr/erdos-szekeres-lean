#!/bin/bash
# Auditor A5: syntactic checks of the reduction maps on the full base (one process at a time).
cd "$(dirname "$0")" || exit 1
B=${BASE_CNF:?set BASE_CNF to the central base CNF written by SYMZ/zcnf.py rot 17 7 --m 2 --hull}
for b in 1 2 3 4 5 6 7 8; do a=$((17 - b)); echo "== (A) b=$b a=$a"; ./symcheck $B symmaps/sigma_A$b.bin symmaps/hull_a$a.cnf; echo "exit $?"; done
for a in 1 2 3 4 5 6 7 8; do echo "== (B) a=$a"; ./symcheck $B symmaps/sigma_B$a.bin symmaps/hull_a$a.cnf; echo "exit $?"; done
