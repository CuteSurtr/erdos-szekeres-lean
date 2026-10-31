#!/bin/bash
# C3W6 P01 lane 2: units of units.tsv at positions = 2 (mod 3), one close_tree run per unit at cap 900
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
END=1792921609
LOG=/opt/work/driver2.log
UNITS=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W6/P01/units.tsv
mkdir -p /opt/work/ct
tail -n +2 $UNITS | awk -F'\t' -v k=2 '(NR-1) % 3 == k {print $2}' | while read U; do
  [ $(date +%s) -lt $END ] || break
  echo "=== UNIT $U start $(date -u +%FT%TZ)" >> $LOG
  OUTP=$(cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out2.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 2>&1)
  echo "$OUTP" | grep -E "\"status\"|SAT FOUND|PROOF NOT ACCEPTED|unsplittable\": true" >> $LOG
  echo "$OUTP" | tail -1 >> $LOG
  echo "=== UNIT $U end $(date -u +%FT%TZ)" >> $LOG
  if echo "$OUTP" | grep -qE "SAT FOUND|PROOF NOT ACCEPTED"; then echo "=== STOP $(date -u +%FT%TZ)" >> $LOG; break; fi
done
echo "=== LANE 2 done $(date -u +%FT%TZ)" >> $LOG
