#!/bin/bash
# C3SIG G0 runner: per node, sigma_cubes K=3 cap 300 jobs 3; if cubes stay open, K=6 cap 300 jobs 3; each node within an even share of the time to END.
export PATH=/opt/bin:$PATH
T=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
OUT=/opt/work/out.jsonl; LOG=/opt/work/driver.log
END=$(date -u -d '2026-10-21T06:26:00Z' +%s)
mapfile -t NODES < <(cut -f2 /opt/work/nodes.tsv)
n=${#NODES[@]}
cd $T
run_k() { # node K deadline
  local s=$(date +%s); echo "=== $1 K=$2 start $(date -u +%FT%TZ) deadline $(date -u -d @$3 +%TZ)" >> $LOG
  setsid python3 sigma_cubes.py /opt/work/base.cnf $OUT $1 $2 300 3 >> $LOG 2>&1 &
  local p=$! killed=0
  while kill -0 $p 2>/dev/null; do
    if [ $(date +%s) -ge $3 ]; then kill -KILL -- -$p 2>/dev/null; pkill -KILL -f "cadical.*$1__" ; killed=1; break; fi
    if grep -q '"SATISFIABLE"' $LOG; then echo "SAT FOUND" >> $LOG; fi
    sleep 5
  done
  wait $p 2>/dev/null
  echo "{\"meta\": \"run\", \"node\": \"$1\", \"K\": $2, \"cap\": 300, \"jobs\": 3, \"start\": $s, \"end\": $(date +%s), \"killed_at_share_deadline\": $killed}" >> $OUT
  echo "=== $1 K=$2 end $(date -u +%FT%TZ) killed=$killed" >> $LOG
}
for i in "${!NODES[@]}"; do
  N=${NODES[$i]}; now=$(date +%s); left=$((END-now)); [ $left -le 60 ] && break
  dl=$((now + left/(n-i)))
  run_k $N 3 $dl
  grep -q 'SAT FOUND\|"status": "SATISFIABLE"' $LOG $OUT && { echo STOP_SAT >> $LOG; exit 1; }
  open=$(python3 -c "import json,sys;r=[json.loads(l) for l in open('$OUT')];c=[x for x in r if x.get('node')=='$N' and 'cube' in x and len(x['cube'])==3];print(8-sum(1 for x in c if x.get('certified')))")
  grep -q '"certified": false' $OUT && echo "PROOF NOT ACCEPTED (see out.jsonl)" >> $LOG
  if [ "$open" -gt 0 ] && [ $((dl - $(date +%s))) -gt 300 ]; then run_k $N 6 $dl; fi
  grep -q '"status": "SATISFIABLE"' $OUT && { echo STOP_SAT >> $LOG; exit 1; }
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
