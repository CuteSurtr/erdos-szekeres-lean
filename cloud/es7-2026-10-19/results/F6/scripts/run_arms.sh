#!/bin/bash
# F6 production run: 4 workers until DEADLINE (epoch s). Seeds in [6000000,7000000).
# usage: run_arms.sh SCRATCH DEADLINE
S=$1; DL=$2
R=$(cd "$(dirname "$0")/../.." && pwd)        # results/
F2=$R/F2; O=$S/run; mkdir -p $O
PY=/usr/bin/python3
armf() { # worker, seed base, extra opts
  w=$1; sd=$2; shift 2
  while [ $(( DL - $(date +%s) )) -gt 300 ]; do
    t=$(( DL - $(date +%s) )); [ $t -gt 1800 ] && t=1800
    $PY $F2/s2/scripts/arm_f.py $S/e26.cnf --seed $sd --time $t "$@" -o $O/armF_$sd.jsonl > $O/armF_$sd.log 2>&1
    sd=$((sd+1))
  done
}
grow() {
  sd=$1
  while [ $(( DL - $(date +%s) )) -gt 300 ]; do
    t=$(( DL - $(date +%s) )); [ $t -gt 2700 ] && t=2700
    $PY $F2/scripts/grow_guided.py $O/gg $sd $(echo "$t/3600" | bc -l) --cnf $S/e26.cnf --server $S/prefix_server > $O/gg_$sd.log 2>&1
    sd=$((sd+1))
  done
}
kph() {
  $PY $F2/s2/scripts/gen_models.py $S/e26.cnf --seed 6000301 --count 3000 --time 1200 -o $O/models_6000301.txt 2> $O/gen_6000301.log
  t=$(( DL - $(date +%s) - 120 ))
  timeout $t $PY $R/F6/scripts/realize_models.py $O/models_6000301.txt --time 4 --jobs 1 --seedbase 6500000 -o $O/real_6000301.jsonl > $O/real_6000301.log 2>&1
}
armf 1 6000001 & armf 2 6000101 --jitter 0.3 --extra-props 2 --bt-depth 4 & grow 6000201 & kph &
wait
