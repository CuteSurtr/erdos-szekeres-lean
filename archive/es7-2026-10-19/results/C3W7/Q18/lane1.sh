#!/bin/bash
# C3W7 Q18 lane 1: units at positions = 1 (mod 3) of units.tsv, one solve each at cap 900
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792940490
LOG=/opt/work/driver1.log
cd $TOOLS
awk 'NR % 3 == (1 + 1) % 3' /opt/work/units.txt | while read -r U; do
  [ $(( END - $(date -u +%s) )) -gt 0 ] || break
  echo "=== UNIT $U start $(date -u '+%F %T')" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl "$U" --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.out 2>&1
  echo "rc=$? $(tail -n 1 /opt/work/ct1.out)" >> $LOG
  echo "=== UNIT $U end $(date -u '+%F %T')" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct1.out; then cat /opt/work/ct1.out >> $LOG; cp /opt/work/ct1.out /opt/work/flag1.out; break; fi
done
echo "=== LANE 1 done $(date -u '+%F %T')" >> $LOG
