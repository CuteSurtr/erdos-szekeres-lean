#!/bin/bash
# C3W7 Q04 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
END=1792940460   # start 1792925160 (10:46:00 UTC) + 4.5 h - 15 min = 15:01:00 UTC
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
LOG=/opt/work/driver1.log
tail -n +2 /opt/work/units.tsv | awk -F'\t' 'NR%3==(1+1)%3 {print $2}' > /opt/work/lane1.units
cd $TOOLS
while read U; do
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.out 2>&1
  cat /opt/work/ct1.out >> /opt/work/ct1.all
  tail -1 /opt/work/ct1.out >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.out; then grep "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.out >> $LOG; break; fi
done < /opt/work/lane1.units
echo "=== LANE 1 done $(date -u +%FT%TZ)" >> $LOG
