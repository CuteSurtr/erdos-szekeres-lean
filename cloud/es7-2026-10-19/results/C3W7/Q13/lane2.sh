#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792940494
K=2
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log /opt/work/full*.log 2>/dev/null; then echo "=== STOP" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%T)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > /opt/work/cur$K.out 2>&1
  cat /opt/work/cur$K.out >> /opt/work/full$K.log
  grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/cur$K.out >> $LOG
  tail -n 1 /opt/work/cur$K.out >> $LOG
  echo "=== UNIT $U end $(date -u +%T)" >> $LOG
done
echo "=== LANE DONE $(date -u +%T)" >> $LOG
