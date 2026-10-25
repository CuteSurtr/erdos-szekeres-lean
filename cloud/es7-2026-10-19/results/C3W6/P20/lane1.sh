#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921577
K=1
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
mkdir -p /opt/work/unitlogs
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if cat /opt/work/driver*.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP $(date -u +%T)" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%T)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/unitlogs/$U.log 2>&1
  grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/unitlogs/$U.log >> $LOG
  tail -n 1 /opt/work/unitlogs/$U.log >> $LOG
  echo "=== UNIT $U end $(date -u +%T)" >> $LOG
done
echo "=== LANE $K DONE $(date -u +%T)" >> $LOG
