#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921593
K=2
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.last 2>&1; cat /opt/work/ct$K.last >> /opt/work/ctfull$K.log
  tail -n 1 /opt/work/ct$K.last >> $LOG
  grep -h "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$K.last >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
