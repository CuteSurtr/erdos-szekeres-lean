#!/bin/bash
# The side search of README.md: one antipodal pair added to SYMMAX/c4_28points.txt, six (trials, box, seed) settings run
# in parallel (one core each). usage: run_addpairs.sh ADDPAIRS_BINARY RESULTS_DIR > addpairs.log
A=$1; R=$2; D=$(mktemp -d)
i=0
for cfg in "4000 300 1" "1500000 60 60" "1500000 150 150" "1500000 300 300" "300000 150 7" "300000 40 8"; do
  set -- $cfg; i=$((i + 1))
  ( echo "== trials $1, box $2, seed $3"; "$A" "$R/SYMMAX/c4_28points.txt" 7 1 "$1" "$2" "$3" 2>&1 > /dev/null ) > "$D/$i.part" &
done
wait
for j in 1 2 3 4 5 6; do cat "$D/$j.part"; done
rm -r "$D"
