#!/bin/bash
# per node: K=3 (cap 300, 3 jobs); if any cube open, K=6 until the node's share of time is used.
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
END=$(date -u -d '2026-10-21 06:24' +%s)
LOG=/opt/work/driver.log; OUT=/opt/work/out.jsonl
cd $TOOLS
mapfile -t NODES < <(cut -f2 /opt/work/nodes.tsv)
n=${#NODES[@]}
run() { # node K deadline
  echo "=== $1 K=$2 start $(date -u +%T) deadline $(date -u -d @$3 +%T)" >> $LOG
  setsid python3 sigma_cubes.py /opt/work/base.cnf $OUT $1 $2 300 3 >> $LOG 2>&1 &
  local p=$!
  while kill -0 $p 2>/dev/null; do
    if [ $(date +%s) -ge $3 ]; then echo "=== $1 K=$2 KILLED at deadline $(date -u +%T)" >> $LOG; kill -TERM -- -$p; sleep 2; kill -KILL -- -$p 2>/dev/null; break; fi
    grep -q '"status": "SATISFIABLE"' $OUT 2>/dev/null && { echo "SAT FOUND" >> $LOG; kill -TERM -- -$p; exit 1; }
    sleep 5
  done
  wait $p 2>/dev/null
  rm -f /opt/work/exp/*.cnf /opt/work/exp/*.lrat
  echo "=== $1 K=$2 end $(date -u +%T)" >> $LOG
}
for i in "${!NODES[@]}"; do
  N=${NODES[$i]}; now=$(date +%s); left=$(( (END-now)/(n-i) )); DL=$((now+left))
  run $N 3 $DL
  grep -q '"status": "SATISFIABLE"' $OUT && { echo "SAT FOUND" >> $LOG; exit 1; }
  if python3 -c "
import json,sys
r=[json.loads(l) for l in open('$OUT')]; r=[x for x in r if x['node']=='$N' and len(x['cube'])==3]
sys.exit(0 if len(r)==8 and all(x.get('certified') for x in r) else 1)"; then echo "=== $N K=3 all certified" >> $LOG
  else run $N 6 $DL; fi
done
echo "=== ALL DONE $(date -u +%T)" >> $LOG
