#!/bin/bash
# Close roots one at a time, in order, until END (epoch s). Arg1: END, arg2: jobs.
export PATH=/opt/bin:$PATH
RES=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C06
END=$1; JOBS=${2:-4}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
while read -r R; do
  grep -qx "$R" $RES/roots_done.txt 2>/dev/null && continue
  now=$(date +%s); [ $now -ge $END ] && break
  H=$(python3 -c "print(round(($END-$now)/3600,4))")
  echo "=== ROOT $R start $(date -u +%T) H=$H jobs=$JOBS" >> $RES/driver.log
  timeout $((END-now)) python3 close_tree.py /opt/work/base.cnf $RES/out.jsonl $R --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H > /opt/work/live/cur.log 2>&1
  rc=$?
  cat /opt/work/live/cur.log >> $RES/driver.log
  echo "=== ROOT $R end $(date -u +%T) rc=$rc" >> $RES/driver.log
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/live/cur.log; then echo STOPPED >> $RES/driver.log; break; fi
  if grep -q '"open_frontier": 0' /opt/work/live/cur.log; then echo "$R" >> $RES/roots_done.txt; else break; fi
done < $RES/roots.txt
pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check
echo "=== RUNNER EXIT $(date -u +%T)" >> $RES/driver.log
