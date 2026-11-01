#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921608
K=0
LOG=/opt/work/driver$K.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1)%3==k {print $2}' | while read U; do
  [ $(date +%s) -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/driver*.log /opt/work/ct*.log 2>/dev/null; then echo "=== STOP SAT" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ct$K.log
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
  tail -n 1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
done
echo "=== LANE $K DONE $(date -u +%FT%TZ)" >> $LOG
