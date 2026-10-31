#!/bin/bash
# F6 reallocation at 03:17 UTC: the two arm F loops (defaults; jitter variant) are replaced by
# one grow_guided loop (seeds 6000211..) and one arm F loop with --smart-bt (seeds 6000111..).
# usage: run_arms2.sh SCRATCH DEADLINE
S=$1; DL=$2
R=$(cd "$(dirname "$0")/../.." && pwd); F2=$R/F2; O=$S/run; PY=/usr/bin/python3
armf() { sd=$1; shift
  while [ $(( DL - $(date +%s) )) -gt 300 ]; do
    t=$(( DL - $(date +%s) )); [ $t -gt 1800 ] && t=1800
    $PY $F2/s2/scripts/arm_f.py $S/e26.cnf --seed $sd --time $t "$@" -o $O/armF_$sd.jsonl > $O/armF_$sd.log 2>&1
    sd=$((sd+1)); done; }
grow() { sd=$1
  while [ $(( DL - $(date +%s) )) -gt 300 ]; do
    t=$(( DL - $(date +%s) )); [ $t -gt 2700 ] && t=2700
    $PY $F2/scripts/grow_guided.py $O/gg $sd $(echo "$t/3600" | bc -l) --cnf $S/e26.cnf --server $S/prefix_server > $O/gg_$sd.log 2>&1
    sd=$((sd+1)); done; }
armf 6000111 --jitter 0.3 --extra-props 2 --smart-bt & grow 6000211 &
wait
