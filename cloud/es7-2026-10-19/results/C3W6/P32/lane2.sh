#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921611
LOG=/opt/work/driver2.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | awk -F'\t' '(NR-1)%3==2 {print $2}' | while read U; do
  [ $(date +%s) -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct2.last 2>&1
  cat /opt/work/ct2.last >> /opt/work/ct2.full
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct2.last >> $LOG
  tail -1 /opt/work/ct2.last >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== LANE DONE $(date -u +%FT%TZ)" >> $LOG
