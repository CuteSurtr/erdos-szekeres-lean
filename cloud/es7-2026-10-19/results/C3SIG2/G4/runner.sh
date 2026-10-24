#!/bin/bash
# C3SIG2 G4 runner: per node, sigma_cubes K=3 cap 300 jobs 3; if cubes stay open, refine.py (8 cubes on the
# 6 smallest free residues per open cube, cap 300, jobs 3); each node within an even share of the time to END.
export PATH=/opt/bin:$PATH
T=/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
OUT=/opt/work/out.jsonl; LOG=/opt/work/driver.log
END=$(date -u -d '2026-10-21T07:56:00Z' +%s)
mapfile -t NODES < <(tail -n +2 /opt/work/nodes.tsv | cut -f2)
n=${#NODES[@]}
cd $T
run_k() { # node level deadline cmd...
  local N=$1 L=$2 D=$3; shift 3
  local s=$(date +%s); echo "=== $N L=$L start $(date -u +%FT%TZ) deadline $(date -u -d @$D +%TZ)" >> $LOG
  setsid "$@" >> $LOG 2>&1 &
  local p=$! killed=0
  while kill -0 $p 2>/dev/null; do
    if [ $(date +%s) -ge $D ]; then kill -KILL -- -$p 2>/dev/null; pkill -KILL -f "cadical.*$N__" ; killed=1; break; fi
    if grep -q '"SATISFIABLE"' $LOG; then echo "SAT FOUND" >> $LOG; fi
    sleep 5
  done
  wait $p 2>/dev/null
  echo "{\"meta\": \"run\", \"node\": \"$N\", \"level\": \"$L\", \"cap\": 300, \"jobs\": 3, \"start\": $s, \"end\": $(date +%s), \"killed_at_share_deadline\": $killed}" >> $OUT
  echo "=== $N L=$L end $(date -u +%FT%TZ) killed=$killed" >> $LOG
}
for i in "${!NODES[@]}"; do
  N=${NODES[$i]}; now=$(date +%s); left=$((END-now)); [ $left -le 60 ] && break
  dl=$((now + left/(n-i)))
  run_k $N K3 $dl python3 sigma_cubes.py /opt/work/base.cnf $OUT $N 3 300 3
  grep -q '"status": "SATISFIABLE"' $OUT && { echo STOP_SAT >> $LOG; exit 1; }
  grep -q '"certified": false' $OUT && echo "PROOF NOT ACCEPTED (see out.jsonl)" >> $LOG
  open=$(python3 -c "import json;r=[json.loads(l) for l in open('$OUT')];c=[x for x in r if x.get('node')=='$N' and 'cube' in x and len(x['cube'])==3];print(8-sum(1 for x in c if x.get('certified')))")
  if [ "$open" -gt 0 ] && [ $((dl - $(date +%s))) -gt 300 ]; then run_k $N K6 $dl python3 /opt/work/refine.py /opt/work/base.cnf $OUT $N 300 3; fi
  grep -q '"status": "SATISFIABLE"' $OUT && { echo STOP_SAT >> $LOG; exit 1; }
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
