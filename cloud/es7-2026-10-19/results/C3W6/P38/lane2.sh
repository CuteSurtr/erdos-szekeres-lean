#!/bin/bash
# C3W6 P38 lane 2: units at positions = 2 (mod 3) of units.tsv, one close_tree.py call per unit
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/opt/work/units.tsv
END=1792921604
LOG=/opt/work/driver2.log
cd $TOOLS
tail -n +2 $UNITS | awk -F'\t' 'NR%3==3%3 {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.last 2>&1
  cat /opt/work/ct2.last >> /opt/work/ct2.full
  tail -1 /opt/work/ct2.last >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct2.last; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct2.last >> $LOG; echo "=== STOP" >> $LOG; break; fi
done
echo "=== LANE DONE $(date -u '+%F %T')" >> $LOG
