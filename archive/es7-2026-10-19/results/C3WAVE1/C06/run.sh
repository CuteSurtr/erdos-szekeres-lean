#!/bin/bash
# Close roots one at a time, in order, until END (epoch s). Arg1: END, arg2: jobs.
# Live files are in $D (outside git); they are copied into RES for commits.
export PATH=/opt/bin:$PATH
RES=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C06
D=/opt/work/live
END=$1; JOBS=${2:-4}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
while read -r R; do
  grep -qx "$R" $D/roots_done.txt 2>/dev/null && continue
  now=$(date +%s); [ $now -ge $END ] && break
  H=$(python3 -c "print(round(($END-$now)/3600,4))")
  echo "=== ROOT $R start $(date -u +%T) H=$H jobs=$JOBS" >> $D/driver.log
  timeout $((END-now)) python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $R --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H > $D/cur.log 2>&1
  rc=$?
  cat $D/cur.log >> $D/driver.log
  echo "=== ROOT $R end $(date -u +%T) rc=$rc" >> $D/driver.log
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $D/cur.log; then echo STOPPED >> $D/driver.log; break; fi
  if grep -q '"open_frontier": 0' $D/cur.log; then echo "$R" >> $D/roots_done.txt; else break; fi
done < $RES/roots.txt
pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check
echo "=== RUNNER EXIT $(date -u +%T)" >> $D/driver.log
