#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921570
LOG=/opt/work/driver1.log
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR%3==(1+1)%3 {print $2}' | while read U; do
  [ $(date +%s) -ge $END ] && break
  if grep -q "SAT FOUND" /opt/work/driver*.log; then echo "=== STOP"; break; fi
  echo "=== UNIT $U start $(date -u +%T)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.last 2>&1
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct1.last
  tail -1 /opt/work/ct1.last
  echo "=== UNIT $U end $(date -u +%T)"
done >> $LOG 2>&1
echo "=== LANE DONE $(date -u +%T)" >> $LOG
