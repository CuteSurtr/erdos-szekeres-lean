#!/bin/bash
# C3SIG G1 runner: per node, K=3 (cap 300, 3 jobs); if cubes stay open, K=6 (cap 300, 3 jobs); each node limited to an even share of the time left before END
export PATH=/opt/bin:$PATH
T=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
END=$(date -u -d '2026-10-21 06:25' +%s)
LOG=/opt/work/driver.log; OUT=/opt/work/out.jsonl
cd $T
mapfile -t NODES < <(cut -f2 /opt/work/nodes.tsv)
n=${#NODES[@]}
run() { # node K deadline
  echo "=== $1 K=$2 start $(date -u +%T) deadline $(date -u -d @$3 +%T)" >> $LOG
  setsid python3 sigma_cubes.py /opt/work/base.cnf $OUT $1 $2 300 3 >> $LOG 2>&1 &
  local p=$!
  while kill -0 $p 2>/dev/null; do
    if [ $(date +%s) -ge $3 ]; then echo "=== $1 K=$2 STOPPED at share deadline $(date -u +%T)" >> $LOG; kill -TERM -- -$p; sleep 3; pkill -9 -g $p; pkill -9 cadical; pkill -9 lrat-check; pkill -9 cake_lpr; break; fi
    sleep 5
  done
  wait $p 2>/dev/null
  rm -f /opt/work/exp/*
  echo "=== $1 K=$2 end $(date -u +%T)" >> $LOG
}
for ((i=0;i<n;i++)); do
  node=${NODES[$i]}; now=$(date +%s); left=$((END-now)); [ $left -le 0 ] && break
  dl=$((now + left/(n-i)))
  run $node 3 $dl
  if grep -q '"status": "SATISFIABLE"' $OUT; then echo "SAT FOUND" >> $LOG; exit 1; fi
  if grep "\"node\": \"$node\"" $OUT | grep '"status": "UNSATISFIABLE"' | grep -q '"certified": false'; then echo "PROOF NOT ACCEPTED $node" >> $LOG; fi
  c=$(grep "\"node\": \"$node\"" $OUT | grep -c '"certified": true')
  if [ "$c" -lt 8 ] && [ $(date +%s) -lt $((dl-120)) ]; then run $node 6 $dl; fi
done
echo "=== RUNNER DONE $(date -u +%T)" >> $LOG
