#!/bin/bash
# C3W6 P11 lane 2: units at positions ≡ 2 (mod 3) of units.tsv, END = 2026-10-25 09:46:50 UTC
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921610
LOG=/opt/work/driver2.log
cut -f2 /opt/work/units.tsv | awk 'NR%3==0' | while read U; do
  [ $(( END - $(date -u +%s) )) -gt 0 ] || { echo "=== END reached before $U $(date -u '+%F %T')" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.cur 2>&1
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct2.cur >> $LOG
  tail -1 /opt/work/ct2.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct2.cur && { echo "=== STOP: SAT FOUND" >> $LOG; break; }
done
echo "=== LANE 2 done $(date -u '+%F %T')" >> $LOG
