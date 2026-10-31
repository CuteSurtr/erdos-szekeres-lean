#!/bin/bash
# C3W7 Q16 lane 1: units at positions = 1 (mod 3) of units.tsv (positions from 0, header excluded)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940459
LOG=/opt/work/driver1.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR%3==(1+1)%3 {print $2}' | while read U; do
  [ $(( END - $(date +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  OUTL=$(cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1 | tee -a /opt/work/full1.log)
  echo "$OUTL" | grep -E "SAT FOUND|PROOF NOT ACCEPTED" >> $LOG
  echo "$OUTL" | tail -1 >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if echo "$OUTL" | grep -q "SAT FOUND"; then echo STOP_SAT >> $LOG; break; fi
done
echo "=== LANE 1 done $(date -u '+%F %T')" >> $LOG
