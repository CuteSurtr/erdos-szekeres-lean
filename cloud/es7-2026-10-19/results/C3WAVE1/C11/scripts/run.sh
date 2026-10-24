#!/bin/bash
# run.sh DEADLINE_EPOCH : roots one at a time; kill the driver's process group on SAT / rejection / deadline
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C11
JOBS=${JOBS:-3}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
for R in $(awk 'NR>1{print $2}' $D/roots.txt); do
 while true; do
  now=$(date +%s); left=$(( $1 - now )); [ $left -le 60 ] && { echo "=== DEADLINE $(date -u +%T)" | tee -a $D/driver.log; echo "=== RUNNER DONE" >> /opt/work/run.out; exit 0; }
  H=$(python3 -c "print(round($left/3600,4))")
  echo "=== ROOT $R start $(date -u +%T) hours $H jobs $JOBS" | tee -a $D/driver.log
  : > /opt/work/cur.log
  setsid python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H > /opt/work/cur.log 2>&1 &
  P=$!; n=0; ev=""
  while kill -0 $P 2>/dev/null; do
    sleep 5
    m=$(wc -l < /opt/work/cur.log); [ $m -gt $n ] && { sed -n "$((n+1)),${m}p" /opt/work/cur.log >> $D/driver.log; n=$m; }
    if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/cur.log; then ev=$(grep -m1 "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/cur.log); break; fi
    [ $(date +%s) -ge $1 ] && { ev=DEADLINE; break; }
  done
  kill -TERM -$P 2>/dev/null; sleep 2; kill -KILL -$P 2>/dev/null; pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check; rm -f /opt/work/ct/*
  m=$(wc -l < /opt/work/cur.log); [ $m -gt $n ] && sed -n "$((n+1)),${m}p" /opt/work/cur.log >> $D/driver.log
  case "$ev" in
   "") break ;;   # driver finished this root
   DEADLINE) echo "=== DEADLINE, driver stopped $(date -u +%T)" | tee -a $D/driver.log; echo "=== RUNNER DONE" >> /opt/work/run.out; exit 0 ;;
   "SAT FOUND"*) echo "=== SAT FOUND, stopped $(date -u +%T)" | tee -a $D/driver.log; echo "=== STOPPED SAT" >> /opt/work/run.out; exit 1 ;;
   "PROOF NOT ACCEPTED"*)
     N=${ev#PROOF NOT ACCEPTED }; oom=$(dmesg | grep -c "Killed process.*cake_lpr\|Killed process.*lrat-check\|Killed process.*cadical")
     echo "=== $ev; OOM kills so far: $oom; rechecking alone $(date -u +%T)" | tee -a $D/driver.log
     r=$(/opt/work/recheck.sh $N); echo "$r" >> $D/rechecks.jsonl; echo "=== recheck: $r" | tee -a $D/driver.log
     if echo "$r" | grep -q '"cake_lpr": "s VERIFIED UNSAT"' && echo "$r" | grep -q '"lrat_check": "c VERIFIED"'; then
       [ $JOBS -gt 2 ] && [ "$oom" -gt "${LASTOOM:-0}" ] && JOBS=$((JOBS-1)) && echo "=== memory: lowering jobs to $JOBS" | tee -a $D/driver.log
       LASTOOM=$oom; continue
     else echo "=== REAL REJECTION $N" | tee -a $D/driver.log; echo "=== STOPPED REJECT" >> /opt/work/run.out; exit 1; fi ;;
  esac
 done
done
echo "=== RUNNER DONE $(date -u +%T)" | tee -a $D/driver.log; echo "=== RUNNER DONE" >> /opt/work/run.out
