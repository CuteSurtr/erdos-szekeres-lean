#!/bin/bash
# lane 0 of C3W7 Q20: units at positions = 0 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver0.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR % 3 == (0 + 1) % 3 {print $2}' > /opt/work/lane0.units
while read -r U; do
  END=$(cat /opt/work/END); [ $(( END - $(date +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > /opt/work/full0.cur 2>&1
  cat /opt/work/full0.cur >> /opt/work/full0.log
  tail -n 1 /opt/work/full0.cur >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/full0.cur; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/full0.cur >> $LOG; break; fi
done < /opt/work/lane0.units
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
