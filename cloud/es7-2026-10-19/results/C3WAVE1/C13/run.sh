#!/bin/bash
# runs roots one at a time; STOP at epoch $1, JOBS $2
STOP=$1; J=$2; D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C13
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S
( echo 0s0-1s0_6; tail -n +2 $D/roots.tsv | cut -f2 ) | while read R; do
  now=$(date +%s); [ $now -ge $STOP ] && break
  H=$(python3 -c "print(round(($STOP-$now)/3600,4))")
  echo "=== ROOT $R start $(date -u +%T) H=$H jobs=$J" >> $D/driver.log
  python3 tools/close_tree.py /opt/work/base.cnf $D/out.jsonl $R --jobs $J --caps 300,300,600 --cadopts=--sat --split-singles --hours $H > /opt/work/cur.log 2>&1
  rc=$?; cat /opt/work/cur.log >> $D/driver.log
  echo "=== ROOT $R end $(date -u +%T) rc=$rc" >> $D/driver.log
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/cur.log; then echo "=== HALT" >> $D/driver.log; touch /opt/work/HALT; break; fi
done
echo "=== ALL DONE $(date -u +%T)" >> $D/driver.log
