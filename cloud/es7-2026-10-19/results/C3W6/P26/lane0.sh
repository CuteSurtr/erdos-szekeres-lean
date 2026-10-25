#!/bin/bash
# C3W6 P26 lane 0: units at positions ≡ 0 (mod 3) of units.tsv (positions from 0, header excluded)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921608
LOG=/opt/work/driver0.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' -v k=0 '(NR-1)%3==k {print $2}' | while read U; do
  [ $(( END - $(date -u +%s) )) -gt 0 ] || { echo "=== END reached $(date -u '+%F %T')" >> $LOG; break; }
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct0.cur 2>&1
  cat /opt/work/ct0.cur >> /opt/work/ct0.full
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct0.cur >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  tail -n 1 /opt/work/ct0.cur >> $LOG
  if grep -q "SAT FOUND" /opt/work/ct0.cur; then touch /opt/work/STOP_SAT; fi
  [ -e /opt/work/STOP_SAT ] && break
done
echo "=== LANE 0 done $(date -u '+%F %T')" >> $LOG
