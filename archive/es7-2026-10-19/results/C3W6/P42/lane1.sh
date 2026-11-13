#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921586
K=1
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
awk -v k=$K '(NR-1)%3==k' /opt/work/units.txt | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/driver*.log; then echo "=== STOP SAT" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/full$K.log
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
  tail -n 1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
done
echo "=== LANE $K DONE $(date -u +%FT%TZ)" >> $LOG
