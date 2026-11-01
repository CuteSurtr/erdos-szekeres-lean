#!/bin/bash
# C3W7 Q03 lane 0: units at positions = 0 (mod 3) of units.tsv (positions from 0)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940483
LOG=/opt/work/driver0.log
mkdir -p /opt/work/ct
awk -F'\t' 'NR%3==(0+1)%3 {print $2}' /opt/work/units.tsv | while read U; do
  [ $((END - $(date -u +%s))) -gt 0 ] || { echo "=== END reached before $U $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct_out0.txt 2>&1
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct_out0.txt >> $LOG
  tail -1 /opt/work/ct_out0.txt >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND" /opt/work/ct_out0.txt && { echo "=== STOP: SAT FOUND" >> $LOG; break; }
done
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
