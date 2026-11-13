#!/bin/bash
# cake.sh : cake_lpr (heap 8000 MB) on every cube proof that lrat-check VERIFIED, one at a time.
#   P=<work dir with cubes/, results.txt> S=<dir with resolve/bin/cake_lpr> bash cake.sh
set -u
B=$S/resolve/bin
for n in $(grep 'lrat-check: \[.c VERIFIED' $P/results.txt | awk '{print $2}'); do
  $B/cake_lpr --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000 $P/cubes/$n.cnf $P/cubes/$n.lrat > $P/logs/cake_$n.log 2>&1
  echo "$(date +%H:%M:%S) $n cake: $(grep -m1 -E 's VERIFIED|FAIL|rror' $P/logs/cake_$n.log)" >> $P/cake_results.txt
done
