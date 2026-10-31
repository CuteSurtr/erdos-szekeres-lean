#!/bin/bash
# C3W7 Q21 lane 0: units at positions = 0 (mod 3) of units.tsv (positions from 0, header excluded)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940492
LOG=/opt/work/driver0.log
cd $TOOLS
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR%3==(0+1)%3 {print $2}' > /opt/work/lane0.units
while read -r U; do
  [ $(( END - $(date -u +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct0.cur 2>&1
  cat /opt/work/ct0.cur >> /opt/work/ct0.full
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct0.cur >> $LOG
  tail -1 /opt/work/ct0.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND" /opt/work/ct0.cur; then echo "STOP: SAT FOUND" >> $LOG; break; fi
done < /opt/work/lane0.units
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
