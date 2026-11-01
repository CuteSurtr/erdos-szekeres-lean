#!/bin/bash
# C3W7 Q33 lane 0: units at positions = 0 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940500
LOG=/opt/work/driver0.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=0 '(NR-1)%3==k {print $2}' | while read U; do
  [ $(( END - $(date +%s) )) -gt 0 ] || { echo "=== END reached before $U $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct0.cur 2>&1
  cat /opt/work/ct0.cur >> /opt/work/ct0.all
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct0.cur >> $LOG
  tail -1 /opt/work/ct0.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct0.cur && { echo "=== STOP: SAT FOUND" >> $LOG; break; }
done
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
