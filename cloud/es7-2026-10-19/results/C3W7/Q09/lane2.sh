#!/bin/bash
# lane 2 of C3W7 Q09: units at positions = 2 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=$(cat /opt/work/END)
LOG=/opt/work/driver2.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR % 3 == (2 + 1) % 3 {print $2}' | while read U; do
  [ -e /opt/work/STOP ] && break
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  OUT=$(cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1)
  echo "$OUT" > /opt/work/last2.txt
  echo "$OUT" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> $LOG
  echo "$OUT" | tail -1 >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if echo "$OUT" | grep -q "^SAT FOUND"; then touch /opt/work/STOP; break; fi
done
echo "=== LANE 2 done $(date -u '+%F %T')" >> $LOG
