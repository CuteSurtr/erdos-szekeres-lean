#!/bin/bash
# lane 0: units at positions = 0 (mod 3) of units.tsv (positions from 0, header excluded)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(cat /opt/work/END)
LOG=/opt/work/driver0.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR % 3 == (0 + 1) % 3 {print $2}' | while read U; do
  [ -e /opt/work/STOP ] && break
  [ $(( END - $(date +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  OUT=$(cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1)
  echo "$OUT" > /opt/work/last0.txt
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  echo "$OUT" | tail -1 >> $LOG
  if echo "$OUT" | grep -qE 'SAT FOUND|PROOF NOT ACCEPTED'; then echo "$OUT" | grep -E 'SAT FOUND|PROOF NOT ACCEPTED' >> $LOG; touch /opt/work/STOP; break; fi
done
echo "=== LANE 0 done $(date -u +%FT%TZ)" >> $LOG
