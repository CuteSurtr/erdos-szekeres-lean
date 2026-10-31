#!/bin/bash
# usage: dualcheck.sh CNF PROOF   (env: LRAT_FIXED, CAKE_LPR = checker binaries)
# Runs two LRAT checkers: lrat-check with lrat-check-E2.patch applied (the unpatched
# drat-trim 2e3b2dc lrat-check accepts a hintless empty clause, see
# logs/lrat_check_soundness.md), and the CakeML-verified cake_lpr.  Prints "c VERIFIED"
# and exits 0 only if both accept.
a=$("$LRAT_FIXED" "$1" "$2" 2>&1 | grep -E '^c (NOT )?VERIFIED' | head -1)
b=$("$CAKE_LPR" "$1" "$2" 2>&1 | head -1)
echo "c lrat-check-E2patch: $a"
echo "c cake_lpr: $b"
if [ "$a" = "c VERIFIED" ] && [ "$b" = "s VERIFIED UNSAT" ]; then echo "c VERIFIED"; exit 0; fi
echo "c NOT VERIFIED"; exit 1
