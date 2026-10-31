#!/bin/bash
# C3W7 Q17 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940454
LOG=/opt/work/driver1.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR%3==2' | cut -f2 | while read U; do
  now=$(date +%s); left=$((END-now))
  if [ $left -le 0 ]; then echo "=== END reached before $U $(date -u)" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.cur 2>&1
  tail -n 1 /opt/work/ct1.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.cur; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.cur >> $LOG; fi
done
echo "=== LANE 1 done $(date -u '+%F %T')" >> $LOG
