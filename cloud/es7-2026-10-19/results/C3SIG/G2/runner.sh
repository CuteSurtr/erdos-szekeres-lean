#!/bin/bash
# C3SIG G2 runner: per node, K=3 (cap 300, 3 jobs); if any cube open, K=6 (cap 300, 3 jobs).
# Each node gets deadline = now + (END - now) / (nodes left); the run is killed at its deadline.
export PATH=/opt/bin:$PATH
END=1792563919
T=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
OUT=/opt/work/out.jsonl; LOG=/opt/work/driver.log
cd $T
mapfile -t NODES < <(cut -f2 /opt/work/nodes.tsv)
n=${#NODES[@]}
for i in "${!NODES[@]}"; do
  N=${NODES[$i]}; now=$(date +%s); left=$((n-i)); DL=$((now + (END-now)/left))
  [ $((END-now)) -le 60 ] && { echo "=== NODE $N not reached $(date -u +%FT%TZ)" >> $LOG; continue; }
  for K in 3 6; do
    now=$(date +%s); [ $((DL-now)) -le 30 ] && { echo "=== NODE $N K=$K skipped (node share used) $(date -u +%FT%TZ)" >> $LOG; break; }
    echo "=== NODE $N K=$K start $(date -u +%FT%TZ) deadline $(date -u -d @$DL +%FT%TZ)" >> $LOG
    setsid python3 sigma_cubes.py /opt/work/base.cnf $OUT $N $K 300 3 >> $LOG 2>&1 &
    P=$!
    while kill -0 $P 2>/dev/null; do
      [ $(date +%s) -ge $DL ] && { echo "=== NODE $N K=$K KILLED at deadline $(date -u +%FT%TZ)" >> $LOG; kill -- -$P; sleep 3; kill -9 -- -$P 2>/dev/null; pkill -9 -f "cadical.*/opt/work/exp"; break; }
      sleep 5
    done
    wait $P 2>/dev/null
    rm -f /opt/work/exp/*.cnf /opt/work/exp/*.lrat
    echo "=== NODE $N K=$K end $(date -u +%FT%TZ)" >> $LOG
    if grep -q '"status": "SATISFIABLE"' $OUT; then echo "SAT FOUND" >> $LOG; exit 1; fi
    if python3 - "$OUT" "$N" <<'PY'
import json,sys
r=[json.loads(l) for l in open(sys.argv[1])]
bad=[x for x in r if x["node"]==sys.argv[2] and x["status"]=="UNSATISFIABLE" and not x.get("certified")]
sys.exit(0 if bad else 1)
PY
    then echo "PROOF NOT ACCEPTED $N" >> $LOG; fi
    [ $K = 3 ] && python3 - "$OUT" "$N" <<'PY' && { echo "=== NODE $N K=3 all 8 certified, no K=6" >> $LOG; break; }
import json,sys
r=[json.loads(l) for l in open(sys.argv[1]) ]
r=[x for x in r if x["node"]==sys.argv[2] and len(x["cube"])==3]
sys.exit(0 if len(r)==8 and all(x.get("certified") for x in r) else 1)
PY
  done
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
