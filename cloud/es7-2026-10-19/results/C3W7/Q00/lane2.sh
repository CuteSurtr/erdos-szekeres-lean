#!/bin/bash
# C3W7 Q00 lane 2: units at positions = 2 (mod 3) of units.tsv (positions from 0, header excluded)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/opt/work/units.tsv
END=1792940471
LOG=/opt/work/driver2.log
OUT=/opt/work/out2.jsonl
tail -n +2 $UNITS | awk -F'\t' -v k=2 '(NR-1) % 3 == k {print $2}' | while read U; do
  now=$(date +%s)
  if [ $((END - now)) -le 0 ]; then echo "=== STOP: END reached $(date -u +%FT%TZ)" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf $OUT $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.cur 2>&1
  cat /opt/work/ct2.cur >> /opt/work/ct2.full
  if grep -qE "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct2.cur; then grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct2.cur >> $LOG; fi
  tail -1 /opt/work/ct2.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND" /opt/work/ct2.cur; then echo "=== STOP: SAT FOUND" >> $LOG; break; fi
done
echo "=== LANE 2 done $(date -u +%FT%TZ)" >> $LOG
