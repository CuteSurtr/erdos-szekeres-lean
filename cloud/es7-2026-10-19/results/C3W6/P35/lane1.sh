#!/bin/bash
# C3W6 P35 lane 1: units at positions = 1 (mod 3) of units.tsv
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921614
UNITS=/opt/work/units.tsv
LOG=/opt/work/driver1.log
FULL=/opt/work/full1.log
CUR=/opt/work/cur1.log
cd $TOOLS
tail -n +2 $UNITS | awk -F'\t' '(NR-1) % 3 == 1 {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $FULL
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 < /dev/null > $CUR 2>&1
  cat $CUR >> $FULL
  tail -n 1 $CUR >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $CUR; then grep "SAT FOUND\|PROOF NOT ACCEPTED" $CUR >> $LOG; fi
  if grep -q "SAT FOUND" $CUR; then echo "=== LANE STOP (SAT)" >> $LOG; break; fi
done
echo "=== LANE 1 done $(date -u +%FT%TZ)" >> $LOG
