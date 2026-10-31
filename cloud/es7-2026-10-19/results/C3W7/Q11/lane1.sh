#!/bin/bash
# lane 1: units at positions = 1 (mod 3) of units.tsv, one close_tree run per unit
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
UNITS=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W7/Q11/units.tsv
END=$(cat /opt/work/end_epoch)
LOG=/opt/work/driver1.log
cd $TOOLS
tail -n +2 $UNITS | awk -F'\t' 'NR%3==(1+1)%3 {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.out 2>&1
  cat /opt/work/ct1.out >> /opt/work/ct1.all
  grep -h "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.out >> $LOG
  tail -1 /opt/work/ct1.out >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.out && { echo "=== LANE STOP" >> $LOG; break; }
done
echo "=== LANE 1 done $(date -u +%FT%TZ)" >> $LOG
