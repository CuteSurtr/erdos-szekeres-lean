#!/bin/bash
# closes the roots of roots.txt one at a time; DEADLINE = unix time to stop the driver
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C01
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
JOBS=${JOBS:-4}
while read idx root; do
  now=$(date +%s); left=$((DEADLINE-now)); [ $left -le 60 ] && break
  H=$(python3 -c "print(round($left/3600,3))")
  echo "=== root $idx $root start $(date -u +%T) hours $H jobs $JOBS" >> $D/run.log
  setsid python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $root --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H >> $D/run.log 2>&1 &
  pid=$!
  while kill -0 $pid 2>/dev/null; do
    if [ $(date +%s) -ge $DEADLINE ]; then echo "=== deadline: killing driver $(date -u +%T)" >> $D/run.log; kill -TERM -- -$pid; sleep 5; kill -KILL -- -$pid 2>/dev/null; break; fi
    sleep 10
  done
  wait $pid; rc=$?
  echo "=== root $idx end $(date -u +%T) rc $rc" >> $D/run.log
  if tail -3 $D/run.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP for inspection" >> $D/run.log; exit 3; fi
done < $D/roots.txt
echo "=== ALL DONE $(date -u +%T)" >> $D/run.log
