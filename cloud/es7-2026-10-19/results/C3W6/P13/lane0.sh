#!/bin/bash
# C3W6 P13 lane 0: units at positions = 0 (mod 3) of units.tsv, cap 900, no further split
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921607
LOG=/opt/work/driver0.log
awk -F'\t' 'NR>1 && (NR-2)%3==0 {print $2}' /opt/work/units.tsv | while read U; do
  [ $(date +%s) -lt $END ] || { echo "=== END reached $(date -u +%FT%TZ)" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  OUT=$(cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1)
  echo "$OUT" | grep -E "SAT FOUND|PROOF NOT ACCEPTED|unsplittable\": true" >> $LOG
  echo "$OUT" | tail -2 | head -1 | sed 's/^/solve: /' >> $LOG
  echo "$OUT" | tail -1 >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if echo "$OUT" | grep -qE "SAT FOUND|PROOF NOT ACCEPTED"; then echo "=== STOP lane" >> $LOG; break; fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
