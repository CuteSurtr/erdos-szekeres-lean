#!/bin/bash
# W27 driver: whole-case 60 s attempts, then close_march.py per still-open case in listed order.
# Resumable: a case with a verified whole-case record or a finished close run is skipped.
H=$(cd "$(dirname "$0")/.." && pwd); W=/opt/es7tools/work; DL=${DEADLINE:?}
CASES="U5_L U_L9 U_L12"
for c in $CASES; do
  grep -q '"whole_case": true' $H/$c/leaves.jsonl 2>/dev/null || python3 $H/scripts/direct.py $W/$c.cnf $H/$c $W/d_$c 60 &
done; wait
for c in $CASES; do
  grep -q '"whole_case": true.*VERIFIED' $H/$c/leaves.jsonl && { echo "$c closed whole"; continue; }
  python3 $H/scripts/close_march.py $W/$c.cnf $H/$c --depth 7 --timeout 300 --split-depth 6 --jobs 4 \
     --deadline $DL --work $W/cm_$c
done
echo ALLDONE
