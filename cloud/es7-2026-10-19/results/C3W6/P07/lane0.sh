#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921588
K=0
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | awk -v k=$K '(NR-1)%3==k' | cut -f2 | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -qs "SAT FOUND" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 >> $LOG 2>&1
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
