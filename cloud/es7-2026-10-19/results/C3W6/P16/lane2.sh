#!/bin/bash
# lane 2 of C3W6/P16
export PATH=/opt/bin:$PATH
K=2; END=$(cat /opt/work/end_epoch); TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver$K.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=$K '(NR-1)%3==k{print $2}' | while read U; do
  [ $(( END - $(date +%s) )) -gt 0 ] || { echo "=== END reached $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  (cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02) > /opt/work/ct$K.cur 2>&1
  cat /opt/work/ct$K.cur >> /opt/work/ct$K.full
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct$K.cur >> $LOG
  tail -n 1 /opt/work/ct$K.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$K.cur && break
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
